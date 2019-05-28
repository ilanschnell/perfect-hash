PYTHON_PREFIX=/Users/ilan/a/envs/py37


stations.so: stations.c stations.dat.h stations-code.h
	gcc -arch x86_64 -I${PYTHON_PREFIX}/include/python3.7m \
            -Wall -O3 -Wstrict-prototypes -c stations.c -o stations.o
	gcc -bundle -undefined dynamic_lookup -L${PYTHON_PREFIX}/lib \
            -arch x86_64 stations.o -o stations.so


stations.dat.h: stations.dat
	sed <$< >$@ -e 's:\([^,]*\),\([^,]*\):    {"\1", "\2"},:'


stations-code.h: stations.dat stations-tmpl.h
	python ../../perfect_hash.py --hft=1 $^


clean:
	rm -f stations-code.h stations.dat.h stations.so *.o


test: stations.so
	python -c "import stations; print(stations.locator('DL5BAC'))"
