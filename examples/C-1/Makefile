CC = gcc -Wall


lookup: main.o states-code.o
	$(CC) -o $@ $^


main.o: main.c states-code.h states.dat.h
	$(CC) -c $<


states-code.o: states-code.c states-code.h
	$(CC) -c $<


states-code.c: states.dat states-tmpl.c
	python ../../perfect_hash.py --splitby '|' --keycol 2 $^


states.dat.h: states.dat
	python ./mk_header.py >$@


clean:
	rm -f lookup *.o states.dat.h states-code.c


test: lookup
	./lookup 'NY'
	./lookup 'QW'
