animals.ps: animals.dot
	neato -Tps $< -Gstart=100 -o $@


animals.dot: animals.py
	python py2dot.py -l $< -o $@


animals.py: ../animals.txt
	python ../perfect_hash.py $< >$@


clean:
	rm animals.py animals.dot animals.ps
