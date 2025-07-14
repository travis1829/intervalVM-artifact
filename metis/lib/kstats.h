#pragma once

#include <stdint.h>

#include "amd64.h"

// XXX(Austin) With decent per-CPU static variables, we could just use
// a per-CPU variable for each of these stats, plus some static
// constructor magic to build a list of them, and we could avoid this
// nonsense.  OTOH, this struct is easy to get into user space.

#define KSTATS_TLB(X)                                                  \
  /* # of TLB shootdown operations.  One shootdown may target multiple \
   * cores. */                                                         \
  X(uint64_t, tlb_shootdown_count)                                     \
  /* Total number of targets of TLB shootdowns.  This divided by       \
   * tlb_shootdowns is the average number of targets per shootdown     \
   * operation. */                                                     \
  X(uint64_t, tlb_shootdown_targets)                                   \
  /* Total number of cycles spent in TLB shootdown operations. */      \
  X(uint64_t, tlb_shootdown_cycles)                                    \

#define KSTATS_VM(X)                            \
  X(uint64_t, page_fault_count)                 \
  X(uint64_t, page_fault_cycles)                \
  X(uint64_t, page_fault_alloc_count)                 \
  X(uint64_t, page_fault_alloc_cycles)                \
  X(uint64_t, page_fault_fill_count)                  \
  X(uint64_t, page_fault_fill_cycles)                 \
                                                \
  X(uint64_t, mmap_count)                       \
  X(uint64_t, mmap_cycles)                      \
  /* Total number of cycles wasted during mmap() because we needed to  \
   * restart the whole operation. */                                   \
  X(uint64_t, mmap_retry_cycles)                \
                                                \
  X(uint64_t, munmap_count)                     \
  X(uint64_t, munmap_cycles)                    \

#define KSTATS_KALLOC(X)                        \
  X(uint64_t, kalloc_page_alloc_count)          \
  X(uint64_t, kalloc_page_free_count)           \
  X(uint64_t, kalloc_hot_list_refill_count)     \
  X(uint64_t, kalloc_hot_list_flush_count)      \
  X(uint64_t, kalloc_hot_list_steal_count)      \
  X(uint64_t, kalloc_hot_list_remote_free_count)        \

#define KSTATS_REFCACHE(X)                      \
  X(uint64_t, refcache_review_count)            \
  X(uint64_t, refcache_review_cycles)           \
  X(uint64_t, refcache_flush_count)             \
  X(uint64_t, refcache_flush_cycles)            \
  X(uint64_t, refcache_reap_count)              \
  X(uint64_t, refcache_reap_cycles)             \
  X(uint64_t, refcache_item_flushed_count)      \
  X(uint64_t, refcache_item_reviewed_count)     \
  X(uint64_t, refcache_item_freed_count)        \
  X(uint64_t, refcache_item_requeued_count)     \
  X(uint64_t, refcache_item_disowned_count)     \
  X(uint64_t, refcache_dirtied_count)           \
  X(uint64_t, refcache_conflict_count)          \
  X(uint64_t, refcache_weakref_break_failed)    \

#define KSTATS_SOCKET(X)\
  X(uint64_t, socket_load_balance) \
  X(uint64_t, socket_local_read)   \
  X(uint64_t, socket_local_sendto_cycles)   \
  X(uint64_t, socket_local_client_sendto_cycles)   \
  X(uint64_t, socket_local_sendto_cnt)   \
  X(uint64_t, socket_local_client_sendto_cnt)   \
  X(uint64_t, socket_local_recvfrom_cycles)   \
  X(uint64_t, socket_local_recvfrom_cnt)   \

#define KSTATS_FILE(X)                          \
  X(uint64_t, write_cycles)                     \
  X(uint64_t, write_count)                      \
  X(uint64_t, mnode_alloc)                      \
  X(uint64_t, mnode_free)                       \

#define KSTATS_SCHED(X)                         \
  X(uint64_t, sched_tick_count)                 \
  X(uint64_t, sched_blocked_tick_count)         \
  X(uint64_t, sched_delayed_tick_count)         \

#define KSTATS_ALL(X)                           \
  KSTATS_TLB(X)                                 \
  KSTATS_VM(X)                                  \
  KSTATS_KALLOC(X)                              \
  KSTATS_REFCACHE(X)                            \
  KSTATS_SOCKET(X)                              \
  KSTATS_SCHED(X)                               \
  KSTATS_FILE(X)                                \

struct kstats;

struct kstats
{
#define X(type, name) type name;
  KSTATS_ALL(X)
#undef X
};
