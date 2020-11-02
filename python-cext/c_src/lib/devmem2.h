#ifndef DEV_MEM_H
#define DEV_MEM_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include <ctype.h>
#include <termios.h>
#include <sys/types.h>
#include <sys/mman.h>

void process(off_t target, int access_type, unsigned long writeval);
unsigned long read_addr(off_t target);
unsigned long write_addr(off_t target, unsigned long writeval);
void usage(void);

#endif