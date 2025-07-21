/* Evaluate the performance of mmap() + fault + munmap() */

#include <pthread.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>

#define PGSIZE 4096UL

static pthread_barrier_t bar;
unsigned long npages = 512UL;
int stop = 0;

void*
thr(void *arg)
{
  unsigned long mmapsize = npages * PGSIZE;
  int tid = (uintptr_t)arg;

  char file_name[10] = { 0 };
  if (tid >= 1000) {
    printf("too much threads\n");
    return 0;
  }
  file_name[0] = (tid / 100) + '0';
  file_name[1] = ((tid % 100) / 10) + '0';
  file_name[2] = (tid % 10) + '0';

  int fd = open(file_name, O_RDWR | O_CREAT, 0666);
  if (fd == -1) {
    printf("%d: open error\n", tid);
    return 0;
  }

  char buf[PGSIZE];
  memset(buf, 'a', PGSIZE);
  for (unsigned long j = 0; j < mmapsize; j+= PGSIZE) {
    if (write(fd, buf, PGSIZE) != PGSIZE) {
      printf("%d: partial write\n", tid);
      unlink(file_name);
      return 0;
    }
  }
  fsync(fd);

  pthread_barrier_wait(&bar);

  unsigned long count = 0;
  while (!stop) {
    /* mmap() */
    char *p = (char*) mmap(NULL, mmapsize, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FILE, fd, 0);
    if (p == MAP_FAILED) {
      printf("%d: map failed", tid);
      break;
    }

    /* fault */
    for (unsigned long j = 0; j < mmapsize; j += PGSIZE)
      if (p[j] != 'a')
        printf("%d: wrong data", tid);
    
    /* munmap() */
    if (munmap(p, mmapsize)) {
      printf("%d: munmap failed", tid);
      break;
    }

    count++;
  }

  unlink(file_name);
  return (void *)count;
}

int
main(int ac, char **av)
{
  if (ac < 2) {
    printf("usage: %s nthreads npages", av[0]);
    return 0;
  }

  int nthread = atoi(av[1]);
  if (ac >= 3)
    npages = atoi(av[2]);
  printf("nthreads: %d npages: %lu\n", nthread, npages);

  pthread_t* tid = (pthread_t*) malloc(sizeof(*tid)*nthread);

  pthread_barrier_init(&bar, 0, nthread + 1);

  for(uint64_t i = 0; i < nthread; i++)
    pthread_create(&tid[i], 0, thr, (void*) i);

  pthread_barrier_wait(&bar);
  sleep(1);
  stop = 1;
  unsigned long sm = 0;
  for(int i = 0; i < nthread; i++) {
    void *res;
    pthread_join(tid[i], &res);
    sm += (unsigned long)res;
  }
  printf("throughput: %ld ops per second\n", sm);
    
  return 0;
}
