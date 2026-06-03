# Uses pdflatex (TinyTeX / TeX Live). Install missing packages with: make deps
.PHONY: all clean deps

all: CV.pdf
	$(MAKE) clean

# Build the PDF, then publish it to the repo root (served at /CV.pdf).
# The root copy is the single source of truth; no PDF is kept in misc/.
CV.pdf: CV.tex
	pdflatex CV.tex
	pdflatex CV.tex
	mv -f CV.pdf ../CV.pdf

clean:
	rm -f CV.aux CV.log CV.out CV.fls CV.fdb_latexmk CV.synctex.gz

# Install TinyTeX packages required by CV.tex (run once if you get "File not found" errors)
# Note: calc/tabularx come from tools, lmodern from lm
deps:
	tlmgr install titlesec tools geometry xcolor enumitem fontawesome5 amsmath hyperref eso-pic bookmark lastpage changepage paracol needspace datetime2 lm
