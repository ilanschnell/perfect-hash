CC = gcc -Wall


a.out: main.c
	$(CC) $<


main.c: keys.dat main-tmpl.c
	python ../../perfect_hash.py -v -o main.c $^


clean:
	rm -f main.c a.out


test: a.out
	./a.out
