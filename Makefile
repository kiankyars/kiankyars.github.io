# Uses pdflatex (TinyTeX / TeX Live). Install missing packages with: make deps
.PHONY: all clean deps

all: CV.pdf
	$(MAKE) clean

CV.pdf: CV.tex
	pdflatex CV.tex
	pdflatex CV.tex

clean:
	rm -f CV.aux CV.log CV.out CV.fls CV.fdb_latexmk CV.synctex.gz

# Install TinyTeX packages required by CV.tex (run once if you get "File not found" errors)
# Note: calc/tabularx come from tools, lmodern from lm
deps:
	tlmgr install titlesec tools geometry xcolor enumitem fontawesome5 amsmath hyperref eso-pic bookmark lastpage changepage paracol needspace datetime2 lm
