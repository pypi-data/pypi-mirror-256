# Project Op Cit
This is a plugin for the Crossref Labs API that allows for the automatic digital preservation deposit of incoming XML.

![license](https://img.shields.io/gitlab/license/crossref/labs/opcit) ![activity](https://img.shields.io/gitlab/last-commit/crossref/labs/opcit) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

![FastAPI](https://img.shields.io/badge/fastapi-%23092E20.svg?style=for-the-badge&logo=fastapi&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

The application examines incoming XML deposits, checks for openly licensed material, and deposits it in an extensible range of digital preservation archives.

## Installation
The easiest install is via pip:
    
    pip install opcit

The entry point is the main deposit function, which takes a StarletteRequest object and a [longsight Instrumentation logging object](https://gitlab.com/crossref/labs/longsight).

## Usage


# Credits
* [FastAPI](https://fastapi.tiangolo.com/) for the Crossref Labs API.
* [Git](https://git-scm.com/) from Linus Torvalds _et al_.
* [.gitignore](https://github.com/github/gitignore) from Github.
* [Rich](https://github.com/Textualize/rich) from Textualize.

&copy; Crossref 2023