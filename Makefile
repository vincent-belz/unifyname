init:
	pip install -r requirements.txt

test:
	cd tests/
	pytest
