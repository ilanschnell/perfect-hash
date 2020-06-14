install:
	python setup.py install


test:
	cd ${PWD}/examples && bash run-all.sh
	python test.py


clean:
	rm -rf build dist __pycache__ *.egg-info
	rm -f *.pyc
