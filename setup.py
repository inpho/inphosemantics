from distutils.core import setup

import setuptools

setup(
    name = "inphosemantics",
    version = "0.1",
    description = ('Software for managing vector space model data '\
                   'for the Indiana Philosophy Ontology Project'),
    author = "The Indiana Philosophy Ontology (InPhO) Project",
    author_email = "inpho@indiana.edu",
    url = "http://inpho.cogs.indiana.edu/",
    download_url = "http://www.github.com/inpho/inphosemantics",
    keywords = [],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        # "License :: OSI Approved :: MIT License", TBD
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
        "Topic :: Text Processing :: Linguistic",
        ],
    install_requires=[
        "numpy>=1.6.1",
        "scipy>=0.10.1",
        "nltk>=2.0.0",
        "vsm>=0.1"
    ],
    packages=['inphosemantics'],

    # package_data=['inphosemantics':
    #               ['config/corpora/*',
    #                'config/matrices/*',
    #                'config/stoplists/*']]

    data_files=[('inphosemantics/config/corpora',
                 ['inphosemantics/config/corpora/sep-corpora.cfg',
                  'inphosemantics/config/corpora/iep-corpora.cfg',
                  'inphosemantics/config/corpora/philpapers-corpora.cfg',
                  'inphosemantics/config/corpora/test-corpora.cfg']),
                ('inphosemantics/config/matrices',
                 ['inphosemantics/config/matrices/sep-matrices.cfg',
                  'inphosemantics/config/matrices/iep-matrices.cfg',
                  'inphosemantics/config/matrices/philpapers-matrices.cfg',
                  'inphosemantics/config/matrices/test-matrices.cfg']),
                ('inphosemantics/config/stoplists',
                 ['inphosemantics/config/stoplists/stoplists.cfg'])]

    )
