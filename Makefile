all: plot.py
	mkdir plots
	python3 plot.py

upload:
	rsync -e ssh -r --delete plots/ ram:/var/www/~issa/pageview_plots/

clean:
	rm -fr plots
