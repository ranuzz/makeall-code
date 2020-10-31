#include <stdio.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <errno.h>

// compile : gcc -O0 -Og  -g -o mem mem.c -D_GNU_SOURCE -lpthread

/**
 * Get CPU info from cat /proc/cpuinfo
 * cpu MHz         : 2591.997
 * cache size      : 4096 KB
 * */

#define CPU_CYCLE_PER_SEC 2591997000
#define CACHE_SIZE 4096*1024
#define ITERS 10000
#define TEST_PORT 9689

static __inline__ u_int64_t rdtsc(void) {
    // Applicable to __x86_64__ or __amd64__
    //u_int64_t low, high;
    //__asm__ volatile("rdtsc" : "=a"(low), "=d"(high));
    //return (high << 32) | low;
    u_int64_t msr;

    asm volatile ( "rdtsc\n\t"    // Returns the time in EDX:EAX.
            "shl $32, %%rdx\n\t"  // Shift the upper bits left.
            "or %%rdx, %0"        // 'Or' in the lower bits.
            : "=a" (msr)
            : 
            : "rdx");

    return msr;
}

int rdtsc_cycles(void) {
    double x = 0;
    int i;

    for (i = 0; i < ITERS; i++) {
        u_int64_t a = rdtsc();
        u_int64_t b = rdtsc();
        x += (double) (b-a);
    }
    return (int) (x/ITERS);
}

int cache_read_cycles(void) {
    double x = 0;
    int i;
    int arr_zero;
    for (i = 0; i < ITERS; i++) {
        int *arr = (int *)malloc(CACHE_SIZE * sizeof(char));
        __builtin_prefetch(arr + CACHE_SIZE);
        u_int64_t a = rdtsc();
        asm volatile ("mov %1, %0"
            : "=r" (arr_zero) 
            : "r" (arr[0]));
        u_int64_t b = rdtsc();
        x += (double) (b-a);
        free(arr);
    }
    return (int) (x/ITERS);
}

int mem_read_cycles(void) {
    double x = 0;
    int i;

    for (int i = 0; i < ITERS/100; i++) {
        int *arr1 = (int *)malloc(CACHE_SIZE * sizeof(char));

        int *arr2 = (int *)malloc(CACHE_SIZE * sizeof(char));
        int arr2_zero = arr2[0];
        __builtin_prefetch(arr2 + CACHE_SIZE);

        u_int64_t a = rdtsc();
        int arr1_zero ;//= arr1[0];
        __asm__ volatile ("mov %1, %0"
            : "=r" (arr1_zero)
            : "r" (arr1[0]));
        u_int64_t b = rdtsc();
        x += (double) (b-a);
        free(arr1);
        free(arr2);
    }
    return (int) (x/(ITERS/100));
}

int predicate_guess(int predicate) {
    if (predicate) {
        return 0;
    } else {
        return 1;
    }
}

int branch_pred_diff(void) {
    int i;
    int predicate = 1;
    double x1 = 0;
    for (i = 0; i < ITERS; i++) {
        predicate = predicate_guess(predicate);
        u_int64_t a = rdtsc();
        if (__builtin_expect(predicate, 1)) {
            int *arr = (int *) malloc(CACHE_SIZE * sizeof(int));
            int arr_zero = arr[0];
            free(arr);
        } else {
            int *arr = (int *) malloc(CACHE_SIZE * sizeof(int));
            int arr_zero = arr[0];
            free(arr);            
        }
        u_int64_t b = rdtsc();
        x1 += b - a;
    }

    double x2 = 0;
    predicate = 1;
    for (i = 0; i < ITERS; i++) {
        u_int64_t a = rdtsc();
        if (__builtin_expect(predicate, 1)) {
            int *arr = (int *) malloc(CACHE_SIZE * sizeof(int));
            int arr_zero = arr[0];
            free(arr);
        } else {
            int *arr = (int *) malloc(CACHE_SIZE * sizeof(int));
            int arr_zero = arr[0];
            free(arr);
        }
        u_int64_t b = rdtsc();
        x2 += b - a;
    }

    return (int)(x1/ITERS) - (int)(x2/ITERS);
}

int mem_seq_read_cycles(void) {
    double x = 0;
    int i;
    int arr1_zero;
    char *dest = (char *)malloc(CACHE_SIZE * sizeof(int));
    for (i = 0 ; i < ITERS/100; i++) {
        char *arr1 = (char *)malloc(CACHE_SIZE * sizeof(int));

        int *arr2 = (int *)malloc(CACHE_SIZE * sizeof(char));
        __builtin_prefetch(arr2 + CACHE_SIZE);
        
        /*
        int c;
        for (c = 0; c < CACHE_SIZE; c++) {
            u_int64_t a = rdtsc();
            __asm__ volatile ("mov %1, %0"
                : "=r" (arr1_zero)
                : "r" (arr1[c]));
            u_int64_t b = rdtsc();
            x += (double) (b-a);
        }
        */
        u_int64_t a = rdtsc();
        memcpy(dest, arr1, (CACHE_SIZE * sizeof(int)));
        u_int64_t b = rdtsc();
        x += (double) (b-a);     
        free(arr1);
        free(arr2);               
    }
    return (int) (x/(ITERS/100));
}

int disk_read_cycles(void) {
    double x = 0;
    char *path = "tmp";
    int i;
    char *buf = (char *) malloc(CACHE_SIZE * sizeof(int));

    for (i = 0; i < ITERS/100; i++) {
        int fd = open(path, O_CREAT|O_RDWR, S_IRWXU);
        int bytes = write(fd, buf, CACHE_SIZE * sizeof(int));
        assert(bytes == (CACHE_SIZE*sizeof(int)));
        close(fd);
        fd = open(path, O_RDONLY, S_IRUSR);
        u_int64_t a = rdtsc();
        bytes = read(fd, buf, CACHE_SIZE*sizeof(int));
        u_int64_t b = rdtsc();
        close(fd);
        unlink(path);
        x += (double) (b-a);
    }
    return (int) (x/(ITERS/100));
}

typedef struct netdata {
    int port;
    double cycles;
} netdata_t;

void * client(void *data) {

    netdata_t *nd = (netdata_t *)data;
    double *x = &nd->cycles;
    *x = 0;

    int sockfd, portno, n;

    struct sockaddr_in serv_addr;
    struct hostent *server;

    int bufsize = CACHE_SIZE*2;
    char *buffer = (char *)malloc(sizeof(char) * bufsize);

    portno = nd->port;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        printf("Error opening socket\n");
        goto error;
    }
    server = gethostbyname("localhost");
    if (server == NULL) {
        printf("ERROR, no such host\n");
        goto error;
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);

    serv_addr.sin_port = htons(portno);
    
    printf("[client] trying to connect\n");
    if (connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0)  {
        printf("ERROR connecting\n");
        goto error;
    }
    printf("[client] connection established\n");
    
    int i = 0;
    for (i = 0; i < bufsize; i++) {
        buffer[i] = 'a';
    }

    printf("[client] writing data to server\n");
    u_int64_t a = rdtsc();
    n = write(sockfd,buffer,bufsize);
    if (n < 0) {
        printf("ERROR writing to socket\n");
        goto error;
    }

    //printf("[client] wrote %d bytes, reading data from server\n", n);
    n = read(sockfd,buffer,bufsize);
    while (n < bufsize) {
        int n1 = 0;
        n1 = read(sockfd,buffer,bufsize-n);
        if (n1 == 0) break;
        n += n1;
    }
    if (n < 0) {
        printf("ERROR reading from socket\n");
        goto error;
    }
    u_int64_t b = rdtsc();

    *x = b-a;
    printf("[client] done : cycles : %f\n", *x);
error:
    free(buffer);
    return NULL;
}

void * server(void *data) {

    netdata_t *nd = (netdata_t *)data;
    double *x = &nd->cycles;
    *x = 0;
    
    int sockfd, newsockfd, portno, clilen;
    int bufsize = CACHE_SIZE*2;
    char *buffer = (char *)malloc(sizeof(char) * bufsize);

    struct sockaddr_in serv_addr, cli_addr;
    int n;
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        printf("ERROR opening socket\n");
        goto error;
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    
    portno = nd->port;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
            sizeof(serv_addr)) < 0) {
            printf("ERROR on binding\n");
            goto error;
    }

    listen(sockfd,5);
    clilen = sizeof(cli_addr);
    
    // blocking call

    printf("[server] waiting for client\n");
    newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
    if (newsockfd < 0) { 
        printf("ERROR on accept\n");
        goto error;
    }
    printf("[server] client connection established\n");

    bzero(buffer, bufsize);

    printf("[server] reading data from client\n");
    u_int64_t a = rdtsc();

    n = 0;
    n = read(newsockfd,buffer, bufsize);
    while (n < bufsize) {
        int n1 = 0;
        n1 = read(newsockfd,buffer, bufsize-n);
        if (n1 == 0) break;
        n += n1;
    }
    if (n < bufsize) {
        printf("ERROR reading from socket\n");
        goto error;
    }

    //printf("[server] read %d bytes,  writing data to client\n", n);
    n = write(newsockfd,buffer,bufsize);
    if (n < 0) {
        printf("ERROR writing to socket\n");
        goto error;
    }

    u_int64_t b = rdtsc();
    *x = b-a;

    printf("[server] done : cycles : %f", *x);

error:
    free(buffer);
    return NULL;
}

int loopback_read_cycles(int port) {
    double x = 0;
    pthread_t thread1, thread2;
    netdata_t *client_data = (netdata_t *) malloc(sizeof(struct netdata));
    netdata_t *server_data = (netdata_t *) malloc(sizeof(struct netdata));

    client_data->port = server_data->port = port;

    int  iret1, iret2;

    /* Create independent threads each of which will execute function */

    iret2 = pthread_create( &thread2, NULL, server, (void *) server_data);

    sleep(1);

    iret1 = pthread_create( &thread1, NULL, client, (void *) client_data);

    /* Wait till threads are complete before main continues. Unless we  */
    /* wait we run the risk of executing an exit which will terminate   */
    /* the process and all threads before the threads have completed.   */

    pthread_join( thread1, NULL);
    pthread_join( thread2, NULL); 

    printf("Client returns: %d\n",iret1);
    printf("Server returns: %d\n",iret2);

    x = client_data->cycles + server_data->cycles;

    free(client_data);
    free(server_data);

    return (int) (x);
}

int main()
{
    pid_t pid = getpid();
    printf("Process id : %d\n", pid);

    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0, &set);
    if (sched_setaffinity(0, sizeof(set), &set) == -1) {
        printf("Encountered error (sched_setaffinity)");
        return -1;        
    }

    struct sched_param p;
    if (sched_getparam(pid, &p) == -1) {
        printf("Encountered error (sched_getparam)");
        return -1;
    }
    printf("Process priority : %d\n", p.sched_priority);

    struct timespec tp;
    if (sched_rr_get_interval(pid, &tp) == -1) {
        printf("Encountered error (sched_rr_get_interval)");
        return -1;    
    }
    printf("RR interval : %ld %ld\n", tp.tv_sec, tp.tv_nsec);

    printf("Latency number every programmer should know\n");
    
    int off_cycles = rdtsc_cycles();
    //printf("Cycles spent in calculation : %d\n", c_cycles);
    int c_cycles;

    
    c_cycles = cache_read_cycles();
    printf("Cycles spent in cache read : %d\n", c_cycles-off_cycles);

    c_cycles = branch_pred_diff();
    printf("Cycles spent in branch mis-pred 50%% : %d\n", c_cycles);

    c_cycles = mem_read_cycles();
    printf("Cycles spent in mem read : %d\n", c_cycles-off_cycles);
    
    c_cycles = mem_seq_read_cycles();
    printf("Cycles seq mem %ld bytes - memcpy : %d\n", (CACHE_SIZE * sizeof(int)), c_cycles-off_cycles);

    c_cycles = disk_read_cycles();
    printf("Cycles disk %ld bytes - read : %d\n", (CACHE_SIZE* sizeof(int)), c_cycles-off_cycles);
    
    /*

    int i;
    for (i = 0; i < 10; i++) {
        c_cycles = loopback_read_cycles(TEST_PORT+i);
    }
    c_cycles = c_cycles / 10;
    printf("Cycles loopback read %d bytes - cycles : %d\n", (CACHE_SIZE*4), c_cycles-off_cycles);
    */
}