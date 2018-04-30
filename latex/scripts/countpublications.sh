#!/usr/bin/env sh

withID=`grep "article{LHCb-PAPER-20" LHCb-PAPER.bib | wc -l`
arxiv=`grep "arXiv" LHCb-PAPER.bib | wc -l`
pub=`grep "journal" LHCb-PAPER.bib | wc -l`
note=`grep "note" LHCb-PAPER.bib | wc -l`

echo "There are $withID papers with a number, $arxiv on arxiv and $pub published ($note not yet)"


