
PROGS = mbench mfmbench f_mbench f_mfmbench

all: $(PROGS)

%: %.c
	gcc -O3 -o $@ $<

clean:
	rm -f $(PROGS)