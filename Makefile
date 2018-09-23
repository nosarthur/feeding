all: src/analyze.py data/feed.csv data/weight_stool.csv src/utils.py
	python3 src/analyze.py && cp image.png ~/Downloads/
clean:
	rm -fr src/__pycache__
