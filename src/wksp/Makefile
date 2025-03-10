objects := foo.o bar.o all.o
%.o: %.c
	gcc -c $< -o $@


all: $(objects)
	gcc 
foo.o: foo.c
bar.o: bar.c
all.o: all.c
all.c:
	@echo "int main() {return 0;}" > all.c

%.c:
	@touch $@

clean:
	rm $(wildcard *.o) $(wildcard *.c)
