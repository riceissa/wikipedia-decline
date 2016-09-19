all: plot.py
	mkdir plots
	python3 plot.py

clean:
	rm -fr plots
