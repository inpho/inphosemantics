"""
Inphosemantics
===============

Features
 1. Easy-to-use interface for generating, tokenizing, and analyzing corpora.
 2. Provides access to diverse array of philosophical corpora.
 3. Compatible with user-specific corpora.
 3. Compatible with the Natural Language Toolkit (NLTK). 

Dependencies:
 1. ipython [ipython.org]
 2. numpy [numpy.scipy.org]
 3. matplotlib [matplotlib.org]
 4. NLTK [nltk.org]

Inphosemantics Documentation
-----------------------------
Documentation is available in two forms: docstrings stored with the code
and online at the InPhO organization's website <github.com/inpho>.


New to python? No problem! The following is a brief overview python's command-
line and Inphosemantics' operational framework:

1. The command line is where commands are entered:

   Example:
      In [1]: print 'Hello world!'
      Hello world!

2. Use python's built-in help function to view a function's docstring, or
   the instructions for a given function:

   Example:
      In [2]: help(available_corpora)

3. Type '%cheatsheet' for a list of useful Inphosemantics commands:

   Example:
   In [3]: cheatsheet()


For more information on python, please visit <python.org>
For more information on InPhO, please visit <inpho.cogs.indiana.edu>

Press 'q' to exit docstring.

"""
from corpus_io import *
from model_io import *
from viewer_io import *
