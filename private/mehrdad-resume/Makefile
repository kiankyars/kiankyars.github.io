# Uses pdflatex (TinyTeX / TeX Live). Install missing packages with: make deps
.PHONY: all clean deps

all: Resume.pdf
	$(MAKE) clean

Resume.pdf: Resume.tex
	pdflatex Resume.tex
	pdflatex Resume.tex

clean:
	rm -f Resume.aux Resume.log Resume.out Resume.fls Resume.fdb_latexmk Resume.synctex.gz

deps:
	tlmgr install titlesec tools geometry xcolor enumitem fontawesome5 amsmath hyperref eso-pic bookmark lastpage changepage paracol needspace datetime2 lm
