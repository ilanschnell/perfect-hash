stations.so: stations.c stations.dat.h stations-code.h
	rm -f stations.so
	python setup.py build_ext --inplace
	mv stations.*so stations.so


stations.dat.h: stations.dat
	sed <$< >$@ -e 's:\([^,]*\),\([^,]*\):    {"\1", "\2"},:'


stations-code.h: stations.dat stations-tmpl.h
	python ../../perfect_hash.py --hft=4 $^


clean:
	rm -f stations-code.h stations.dat.h *.so *.o
	rm -rf build


test: stations.so
	python test.py
