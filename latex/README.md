# LHCb LaTeX template

A starting point for typesetting documentation in the LHCb style.

## Usage

To use this template, first [fork the repository][fork] to create your own 
copy.  Then, clone your new repository and rename the `main.tex` file to 
something more meaningful:

```shell
$ git clone ssh://git@gitlab.cern.ch:7999/<username>/LHCb-latex-template.git your-project
$ cd your-project
$ git mv main.tex your-project.tex
```

You then just need to edit the `Makefile` to change the value of `NAME` from 
`main` to whatever name you chose; this would be `your-project` using the 
example above.

```make
NAME = your-project
```

Then commit the changes.

```shell
$ git add your-project.tex Makefile
$ git commit -m "Give main.tex a meaningful name."
$ git push
```

### Building

To create the output PDF, run `make`. All build artefacts, including the PDF, 
are placed in the auto-generated `build` directory. To remove the contents of 
this directory, run `make clean`.

By default, the documentation guidelines will be generated. To begin writing 
_your_ document, comment out the guidelines `input` command in `main.tex` and 
uncomment the one for your text:

```tex
% \input{guidelines/guidelines}

\input{sections/sections}
```

Edit [`sections/sections.tex`][sectionsindex] to add more sections to your 
document.

### GitLab CI

The repository contains [a file](.gitlab-ci.yml) that will cause GitLab to 
build the document automatically whenever your push. You can check the status 
of the build, and download the resulting PDF, from the [pipelines 
page][pipelines].

## Contributing

Contributions to this template are welcome.

If you're unsure whether the changes you'd like to suggest are suitable, or if 
you have a problem you're not sure how to fix, please [open an 
issue][openissue] in the [issue tracker][issues].

Contributions are accepted in the form of [merge requests][mrs].

## Status

This is not the 'official' LHCb template repository (yet!). The official 
template is still currently [hosted on SVN][oldtemplateinstructions] in the 
[LHCbDocs][lhcbdocs] repository.

It has never been mandatory to use the official template, but it is generally 
expected that internal documents follow a very similar style, and it is 
mandated that public documents follow the same style. Naturally, the simplest 
way to adhere to this is to use a template maintained by the collaboration.

This repository aims to update the template with some more modern LaTeX 
practices, such as use of the [booktabs][booktabs], [cleveref][cleveref], and 
[siunitx][siunitx] packages, which aim to simplify the lives of authors who 
wish to be consistent.

## Keeping the bibliography up to date

The 'official' `lhcbdocs` SVN repository contains `.bib` files for LHCb papers, which are lovingly maintained by the EB
chair. This repository contains a script to merge changes to those files in the SVN repository into this repository.
It can be run as follows:
```
python scripts/update_bib_files.py
```
You should see some output like this:
```
Last update was 117445 -> 118011
No update needed, skipping bibliography/LHCb-PAPER.bib
```
if there were no changes, or some more verbose merge output if changes were merged.
The updates will be automatically commited (but not pushed) if they merge cleanly, or you may be asked to resolve
conflicts:
```
Merge of bibliography/main.bib failed, resolve it yourself and then run: git commit --file=/tmp/... bibliography/main.bib
```

## License

Most software repositories maintained by the LHCb collaboration, including 
those for documentation, do not specify a license, and this repository follows 
that convention.

[fork]: https://gitlab.cern.ch/apearce/LHCb-latex-template/forks/new
[pipelines]: https://gitlab.cern.ch/apearce/LHCb-latex-template/pipelines
[sectionsindex]: sections/sections.tex
[openissue]: https://gitlab.cern.ch/apearce/LHCb-latex-template/issues/new
[issues]: https://gitlab.cern.ch/apearce/LHCb-latex-template/issues
[mrs]: https://help.github.com/articles/about-pull-requests/
[oldtemplateinstructions]: https://twiki.cern.ch/twiki/bin/view/LHCb/LHCbDocs#How_to_extract_LHCb_LaTeX_docume
[lhcbdocs]: https://svnweb.cern.ch/cern/wsvn/lhcbdocs/Templates/LHCb-latex-template/latest
[booktabs]: https://www.ctan.org/pkg/booktabs?lang=en
[cleveref]: https://www.ctan.org/pkg/cleveref?lang=en
[siunitx]: https://www.ctan.org/pkg/siunitx?lang=en
