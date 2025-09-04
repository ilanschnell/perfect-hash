CC = gcc -Wall


a.out: main.c
	$(CC) $<


main.c: keys.dat main-tmpl.c
	python ../../perfect_hash.py --pow2 --trials=250 -v -o main.c $^


keys.dat:
	python ./mk_rnd_keys.py 50 >keys.dat


clean:
	rm -f keys.dat main.c a.out


test: a.out
	./a.out
