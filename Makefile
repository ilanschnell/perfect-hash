install:
	python setup.py install


test:
	cd ${PWD}/examples && bash run-all.sh
	python test_perfect_hash.py


clean:
	rm -rf build dist __pycache__ *.egg-info
	rm -f *.pyc
