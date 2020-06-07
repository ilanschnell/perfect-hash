install:
	python setup.py install


test:
	python test.py


clean:
	rm -rf build dist __pycache__ *.egg-info
	rm -f *.pyc
