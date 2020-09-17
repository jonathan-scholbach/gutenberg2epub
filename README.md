_gutenberg2epub_ is a tool for creating free e-books from __Projekt Gutenberg__, a collection of public domain literature (https://www.projekt-gutenberg.org/).

# Prerequisites

1. This tool needs `pandoc` to be installed on your system. For a guide how to install pandoc, see https://pandoc.org/installing.html.

2. This tool runs on `Python3`. Get it at https://www.python.org/downloads/. Make sure Python is in your PATH. This is a description how to add Python to your PATH on Windows: https://projects.raspberrypi.org/en/projects/using-pip-on-windows/4.

3. You should run the tool in a virtual environment. After having Python3 installed, run `pip3 install virtualenv` in a terminal. 

# Download and Installation

Either download the repository from GitHub by clicking the green button _Clone or download_ and then _Download ZIP_, save the zip file and unzip it.

Or clone the repository by typing the following in your terminal: (This requires `git` to be installed on your machine)

```
git clone git@github.com:jonathan-scholbach/epubFromGutenberg.git
```

Then, in a terminal, navigate to the directory `epubFromGutenberg`. In there, create and activate the virtual environment, and install the requirements:

```
virtualenv env --python=python3
source env/bin/activate
pip install -r requirements.txt
```

# Use

To generate an e book, navigate to `epubFromGutenberg` in a terminal. In there, you have to activate the virtual environment. 

On Windows, run:

```
\env\Scripts\activate.bat
```

On Linux or Mac run:
```
source env/bin/activate
```

Then you can invoke the script `epub.py` and pass the url of the title page of the book as an argument:
```
python epub.py <URL-OF-TITLEPAGE>
```

This will create a directory `books` and within this a directory for the author of the book. In there, three files will be created: an html file with the content of the book, a txt file containing the metadata of the book in yaml format and an epub file containing the e-book.


# Bug Reporting

This tool is just a prototype. It has not been tested thoroughly against different special cases of books that might occur on Projekt Gutenberg. There might be books formatted in a different way, which the tool does not process correctly. If you find a bug, feel free to file an issue in the issues section of the GitHub repository. When doing so, please add the link to the book you wanted to fetch in the issue's description.
