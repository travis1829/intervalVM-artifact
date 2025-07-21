
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
int stop = 0;

void*
thr(void *arg)
{
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
  if (write(fd, buf, PGSIZE) != PGSIZE) {
    printf("%d: partial write\n", tid);
    unlink(file_name);
    return 0;
  }
  fsync(fd);

  pthread_barrier_wait(&bar);

  unsigned long count = 0;
  while (!stop) {
    char *p = (char*) mmap(NULL, PGSIZE, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FILE, fd, 0);
    if (p == MAP_FAILED) {
      printf("%d: map failed", tid);
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
  if (ac != 2) {
    printf("usage: %s nthreads", av[0]);
    return 0;
  }

  int nthread = atoi(av[1]);

  pthread_t* tid = (pthread_t*) malloc(sizeof(*tid)*nthread);

  pthread_barrier_init(&bar, 0, nthread + 1);

  for(uint64_t i = 0; i < nthread; i++)
    pthread_create(&tid[i], 0, thr, (void*) i);

  pthread_barrier_wait(&bar);
  usleep(100000); // 0.1s
  stop = 1;
  unsigned long sm = 0;
  for(int i = 0; i < nthread; i++) {
    void *res;
    pthread_join(tid[i], &res);
    sm += (unsigned long)res;
  }
  printf("throughput: %ld ops per second\n", sm * 10);
    
  return 0;
}
