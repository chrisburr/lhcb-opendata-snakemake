# Name of the main LaTeX file (do not include .tex)
# Ideally, change this and the correspond file to something meaningful,
# e.g. BsToPhiPhi-paper
NAME = CP-in-B-example

## Generally, there's no need to edit beyond this line ##

# Name of the directory that contains figures
FIGDIR = figures

# Name of the directory that contains the bibliography
BIBDIR = bibliography

# Name of the directory that contains feynman diagram sources
DIADIR = diagrams

# Name of the directory where all build artefacts will be placed
BUILDDIR = build

# Name of the directory where generated figures will be placed
GENDIR = generated

# Default LaTeX distribution on lxplus is quite old, so fetch
# a newer one if we're on an lxplus node
HOST = $(shell hostname)
ifneq (,$(findstring lxplus, $(HOST)))
	export PATH := /afs/cern.ch/sw/XML/texlive/latest/bin/x86_64-linux::$(PATH)
endif

# list of all source files
TEXSOURCES = $(wildcard *.tex)
BIBSOURCES = $(wildcard $(BIBDIR)/*.bib)
FIGSOURCES = $(wildcard $(FIGDIR)/*)
DIASOURCES = $(wildcard $(DIADIR)/*.tex)
# construct list of GENDIR/name.pdf from DIADIR/name.tex
DIAFIGURES = $(addsuffix .pdf,$(addprefix $(GENDIR)/,$(basename $(notdir $(DIASOURCES)))))
SOURCES = $(TEXSOURCES) $(FIGSOURCES) $(BIBSOURCES) $(DIAFIGURES) Makefile

LATEX=pdflatex
LATEXOPT=

LATEXMK=latexmk
LATEXMKOPT=-pdf -output-directory=$(BUILDDIR)

.PHONY: all
all: $(NAME).pdf

$(NAME).pdf: $(SOURCES)
	@$(LATEXMK) $(LATEXMKOPT) -pdflatex="$(LATEX) $(LATEXOPT)" $(NAME)

# Make a helper file
$(BUILDDIR)/%.tex: $(DIADIR)/%.tex
	@mkdir -p $(BUILDDIR)
	@printf '\\edef\\feynmanname{\\detokenize{%s}}\n\\input{feynman}\n' $(notdir $(basename $@)) > $@
	@cat $@

# Make a .pdf in BUILDDIR using our helper and a source in DIADIR
$(GENDIR)/%.pdf: $(DIADIR)/%.tex $(BUILDDIR)/%.tex $(TEXSOURCES) Makefile
	@mkdir -p $(GENDIR)
	@$(LATEXMK) $(LATEXMKOPT) -pdflatex="$(LATEX) $(LATEXOPT)" $(BUILDDIR)/$(notdir $(basename $@)).tex
	@pdfcrop $(BUILDDIR)/$(notdir $(basename $@)).pdf $@
	@rm $(BUILDDIR)/$(notdir $(basename $@)).pdf

.PHONY: clean figures
clean:
	@rm -rf $(BUILDDIR) $(GENDIR)

# Just produce the generated figures
figures: $(DIAFIGURES)
