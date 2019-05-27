test:
	python perfect_hash.py --test


clean:
	rm -rf build dist __pycache__ *.egg-info
	rm -f *.pyc
