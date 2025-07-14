OBJDIRS :=
Q	:= @
CC     := gcc
PERL   := perl
TOP	:= $(shell echo $${PWD-'pwd'})
ARCH 	:= $(shell uname -m | sed -e s/x86_64/amd64/ -e s/i.86/i386/)
MAXCPUS := $(shell grep -c processor /proc/cpuinfo)
O       := obj

OPTFLAG := -O3 -g
#OPTFLAG := -g
INCLUDES := -I$(TOP) -I$(TOP)/lib

CFLAGS	:= -std=c99 -fms-extensions -D_GNU_SOURCE -Wall $(OPTFLAG) \
	   -D_X86_64_ $(INCLUDES) -DJTLS=__thread -DJSHARED_ATTR=  \
	   -DJOS_CLINE=64 -DCACHE_LINE_SIZE=64 -MD                 \
	   -DJOS_NCPU=$(MAXCPUS)

COMMON_LIB := -lc -lm -lpthread -lrt -ldl
LIB	   := -L$(O)/lib -lmetis $(COMMON_LIB)

LDEPS := $(O)/lib/libmetis.a

# Which MapReduce applications to build?
PROGS := app/kmeans 			    \
	 app/matrix_mult 		    \
	 app/pca 			    \
	 app/wc 			    \
	 app/wr				    \
	 app/linear_regression		    \
	 app/hist			    \
	 app/string_match		    \
	 app/wrmem			    \
         app/matrix_mult2

PROGS := $(addprefix $(O)/,$(PROGS))

all: $(PROGS)

.PRECIOUS: $(O)/%.o

include lib/Makefrag

$(O)/%.o: %.c
	$(Q)mkdir -p $(@D)
	@echo "CC	$<"
	$(Q)$(CC) $(CFLAGS) -o $@ -c $<

$(O)/%: $(O)/%.o $(LDEPS)
	@echo "MAKE	$@"
	$(Q)$(CXX) $(CFLAGS) -o $@ $< $(LIB)

clean:
	@rm -rf $(PROGS) *.o *.a *~ *.tmp *.bak *.log *.orig $(O)

# This magic automatically generates makefile dependencies
# for header files included from C source files we compile,
# and keeps those dependencies up-to-date every time we recompile.
# See 'mergedep.pl' for more information.
$(O)/.deps: $(foreach dir, $(OBJDIRS), $(wildcard $(O)/$(dir)/*.d))
	@mkdir -p $(@D)
	$(Q)$(PERL) mergedep.pl $@ $^

-include $(O)/.deps

.PHONY: default clean
