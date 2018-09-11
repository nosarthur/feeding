all: analyze.py data.csv
	python3 analyze.py && cp image.png ~/Downloads/
