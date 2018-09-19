all: analyze.py feed.csv weight_stool.csv utils.py
	python3 analyze.py && cp image.png ~/Downloads/
clean:
	rm -fr __pycache__
