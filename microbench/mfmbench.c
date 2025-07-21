/* Evaluate the performance of mmap() + fault + munmap() */

#include <pthread.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
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

  pthread_barrier_wait(&bar);

  unsigned long count = 0;
  while (!stop) {
    /* mmap() */
    char *p = (char*) mmap(NULL, mmapsize, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) {
      printf("%d: map failed", tid);
      break;
    }

    /* fault */
    for (unsigned long j = 0; j < mmapsize; j += PGSIZE)
      if (p[j] != 0)
        printf("%d: wrong data", tid);
    
    /* munmap() */
    if (munmap(p, mmapsize)) {
      printf("%d: munmap failed", tid);
      break;
    }

    count++;
  }

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
