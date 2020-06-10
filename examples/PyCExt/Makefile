stations.so: stations.c stations.dat.h stations-code.h
	python setup.py build_ext --inplace


stations.dat.h: stations.dat
	sed <$< >$@ -e 's:\([^,]*\),\([^,]*\):    {"\1", "\2"},:'


stations-code.h: stations.dat stations-tmpl.h
	python ../../perfect_hash.py --hft=4 $^


clean:
	rm -f stations-code.h stations.dat.h *.so *.o
	rm -rf build


test: stations.so
	python -c "import stations; print(stations.locator('DL5BAC'))"
