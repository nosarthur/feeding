all: analyze.py feed.csv stool.csv
	python3 analyze.py && cp image.png ~/Downloads/
