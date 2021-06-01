
#include <stdio.h>
#include <sys/sysinfo.h>
#include <stdarg.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>
#include <unistd.h>
#include <sys/types.h>
#include <errno.h>
#include <fcntl.h>

#include <execinfo.h>

// PROT_READ/WRITE
#include <sys/mman.h>

#define MAP_SIZE 4096UL
#define MAP_MASK (MAP_SIZE - 1)

// cat /proc/meminfo
// head /dev/mem | hexdump -C

//# define PATH_MAX 255   
// from pmap.c
void print_maps(pid_t pid)
{
    char fname[PATH_MAX];
    unsigned long writable = 0, total = 0, shared = 0;
    FILE *f;

    sprintf(fname, "/proc/%ld/maps", (long)pid);
    f = fopen(fname, "r");

    if(!f) {
        printf("Not able to open maps file\n");
        return;
    }

    while(!feof(f)) {

        char buf[PATH_MAX+100], perm[5], dev[6], mapname[PATH_MAX];
        unsigned long begin, end, size, inode, foo;
        int n;

        if(fgets(buf, sizeof(buf), f) == 0)
            break;

        mapname[0] = '\0';
        sscanf(buf, "%lx-%lx %4s %lx %5s %ld %s", &begin, &end, perm,
            &foo, dev, &inode, mapname);
        size = end - begin;
        total += size;
        /* the permission string looks like "rwxp", where each character can
        * be either the letter, or a hyphen.  The final character is either
        * p for private or s for shared.  We want to add up private writable
        * mappings, to get a feel for how much private memory this process
        * is taking.
        *
        * Also, we add up the shared mappings, to see how much this process
        * is sharing with others.
        */
        if(perm[3] == 'p') {
            if(perm[1] == 'w')
            writable += size;
        } else if(perm[3] == 's') {
            shared += size;
        } else {
            printf("unable to parse permission string: '%s'\n", perm);
            return;
        }
            
        n = printf("%08lx (%ld KB)", begin, (end - begin)/1024);
        n += printf("%*s %s (%s %ld) ", 22-n, "", perm, dev, inode);
        printf("%*s %s\n", 44-n, "", mapname);
    }
    printf("mapped:   %ld KB writable/private: %ld KB shared: %ld KB\n",
	    total/1024, writable/1024, shared/1024);
    fclose(f);
}

void print_name_pid(pid_t pid)
{
    char name[PATH_MAX];
    int c, i = 0;
    FILE *f;

    sprintf(name, "/proc/%ld/cmdline", (long) pid);
    f = fopen(name, "r");

    if(!f) {
        printf("Not able to open cmdline file\n");
        return;
    }

    while((c = getc(f)) != EOF && c != 0)
	    name[i++] = c;

    name[i] = '\0';
    printf("%s(%ld)\n", name, (long)pid);
    fclose(f);
}

/**
 * total_ram : in bytes
 * walk_size : always 2^n
 * */
void read_ram(unsigned long total_ram, unsigned int walk_size) {

    unsigned char buffer[walk_size];
    int dump_size = 0;

    off_t cur_addr = 0x0;
    void *map_base, *virt_addr; 
    unsigned long read_result;

    unsigned long iter = total_ram / walk_size;
    unsigned int mask = walk_size - 1;

    int fd;
    FILE *dumpfd;
    int b = 0;
    int i = 0;
    int cn = 0;

    if (__builtin_popcount(walk_size) != 1) {
        printf("Invalid walk_size %u\n", walk_size);
        return;
    }

    if((fd = open("/dev/mem", O_RDWR | O_SYNC)) == -1) {
        printf("Can't open /dev/mem\n");
        return;
    };
    printf("/dev/mem opened\n");

    dumpfd = fopen("dump.bin", "wb");
    if (dumpfd == NULL) {
        printf("Can't create dump file\n");
        goto error;
    }



    for (i = 0; i < iter; i++) {
        map_base = mmap(0, walk_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, cur_addr & ~mask);
        if (map_base == (void *)-1) {
            printf("Mapping failed for addr 0x%lX\n", cur_addr);
            cur_addr = cur_addr + walk_size;
            continue;
        }
        virt_addr = map_base + (cur_addr & mask);
        read_result = *((unsigned short *) virt_addr);
        if (read_result) {
            //printf("Value at address 0x%lX (%p): 0x%lX\n", cur_addr, virt_addr, read_result);
        }

        bzero(buffer, walk_size);
        memcpy(buffer, virt_addr, walk_size);

        /*
        for (b = 0; b < walk_size; b++) {
            buffer[b] = *((unsigned char *) (virt_addr+b));
        }
        */
        cn = fwrite(buffer, walk_size, 1, dumpfd);
        if (cn < 1) {
            printf("Error writing file\n");
            goto done;
        }
        dump_size += cn*walk_size;
        //fflush(dumpfd);
        printf("Cur dump size %d bytes\n", dump_size);
        if(munmap(map_base, walk_size) == -1) {
            printf("UnMapping failed for addr 0x%lX\n", cur_addr);
            goto error;
        }

        if (dump_size >= walk_size*10000) {
            goto done;
        }
        cur_addr = cur_addr + walk_size;
    }

done:
    fclose(dumpfd);
error:
    close(fd);
}

void print_backtrace(void) {
    void *bt[1024];
    int bt_size;
    char **bt_syms;
    int i;

    bt_size = backtrace(bt, 1024);
    bt_syms = backtrace_symbols(bt, bt_size);
    printf("%s\n", "BACKTRACE -----------");
    for (i = 1; i < bt_size; i++) {
        size_t len = strlen(bt_syms[i]);
        printf("%s\n", bt_syms[i]);
    }
    printf("%s\n", "END------------------");
    free(bt_syms);
}

int main() {
    struct sysinfo info;
    if (sysinfo(&info) == -1) {
        printf("sysinfo returned error\n");
        return 1;
    }
    printf("Total RAM %lu bytes \n", info.totalram);
    printf("Mem unit %d bytes\n", info.mem_unit);

    pid_t pid = getpid();
    printf("%d\n", pid);
    print_name_pid(pid);
    print_maps(pid);
    read_ram(info.totalram, 1 << 12);
    printf("%p\n", __builtin_return_address(0));


    print_backtrace();

}