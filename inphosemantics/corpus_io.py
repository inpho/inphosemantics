# Functions to tokenize InPhO-related plain text corpora and write the
# results


from vsm import corpus
from inphosemantics.util import tokenizers as tkz

import bookkeeping as bk



__all__ = ['tokenize_corpus',
           'load_vsm_corpus',
           'vsm_corpus_names',
           'plain_corpus_names',
           'corpus_metadata',
           'load_stoplist']



def _is_compressed(vsm_corpus_name):

    corpora = bk._get_vsm_corpora()

    try:

        return corpora.getboolean(vsm_corpus_name, 'compressed')

    except bk.cfg.NoOptionError:

        return False



def _tokenizer_type(vsm_corpus_name):

    corpora = bk._get_vsm_corpora()

    try:

        tkz_type = corpora.get(vsm_corpus_name, 'tokenizer')

    except bk.cfg.NoOptionError:

        tkz_type = 'articles'



    if tkz_type == 'book':

        return tkz.BookTokenizer

    if tkz_type == 'articles':

        return tkz.MultipleArticlesTokenizer



def _get_masking_fns(vsm_corpus_name):

    corpora = bk._get_vsm_corpora()

    masking_fns = []



    try:

        if corpora.getboolean(vsm_corpus_name, 'freq1'):

            masking_fns.append(corpus.mask_f1)

    except bk.cfg.NoOptionError:

        pass



    stoplists = bk._get_stoplists()

    for name in stoplists.sections():
        
        try:

            if corpora.getboolean(vsm_corpus_name, name):

                stop = load_stoplist(name)

                masking_fns.append(lambda c: corpus.mask_from_stoplist(c, stop))

        except bk.cfg.NoOptionError:

            pass
        


    return masking_fns



def tokenize_corpus(vsm_corpus_name, write_file=True):
    '''
    tokenize_corpus(vsm_corpus_name, write_file=True)

    Tokenize a given corpus; that is, deconstruct a series of
    strings by word, sentence, and paragraph. 

    Parameters
    ----------
    tokenize_corpus_name : string
        The plain name of the corpus of interest, as specified 
	in the configuration file. 
    
    write_file : string, optional
    	If 'True', the tokenized corpus is written to a file.
	Otherwise, tokenized corpus is not written. 

    Returns
    -------
    MaskedCorpus : The array of token data,
    	"vsm.corpus.MaskedCorpus".

    Notes
    -----
    Word tokenization employs NLTK's Penn Treeback Word Tokenizer.

    Sentence tokenization employs NLTK's Punkt tokenzier. 
    (See Kiss & Strunk (2006)).
    
    Paragraph tokenization is accomplished through the recognition of 
    paragraphs as indicated by two consecutive line breaks.
    
    Examples
    --------
    In [1]: c = tokenize_corpus('sep')
    
    In [2]: c = tokenize_corpus('sep', False)
    '''
    corpora = bk._get_corpora()
     
    vsm_corpora = bk._get_vsm_corpora()

    vsm_corpus_file = vsm_corpora.get(vsm_corpus_name, 'filename')
    
    plain_name = vsm_corpora.get(vsm_corpus_name, 'plain_name')

    plain_corpora = bk._get_plain_corpora()
    
    plain_dir = plain_corpora.get(plain_name, 'dir')



    TkzClass = _tokenizer_type(vsm_corpus_name)

    tok = TkzClass(plain_dir)

    c = corpus.MaskedCorpus(corpus=tok.words,
                            tok_names=tok.tok_names,
                            tok_data=tok.tok_data)



    masking_fns = _get_masking_fns(vsm_corpus_name)

    for fn in masking_fns:

        fn(c)



    if _is_compressed(vsm_corpus_name):

        c = c.to_corpus(compress=True)


    if write_file:

        c.save(vsm_corpus_file)
        

    return c




def load_vsm_corpus(vsm_corpus_name):
    """
    load_vsm_corpus(vsm_corpus_name)

    Loads stored data from a specified corpus as found in the 
    configuration file. 

    Parameters
    ----------
    vsm_corpus_name : string
    	The name of the tokenized corpus of interest, as 
	found in the configuration file.

    Returns
    -------
    MaskedCorpus : The array of token data,
    	"vsm.corpus.MaskedCorpus".
    
    Examples
    --------
    In [1]: c = load_vsm_corpus('sep')
    Loading corpus from /var/inphosemantics/data/fresh/sep/vsm-corpora/sep.npz 
    """
    corpora = bk._get_vsm_corpora()

    filename = corpora.get(vsm_corpus_name, 'filename')

    if _is_compressed(vsm_corpus_name):

        return corpus.Corpus.load(filename)

    return corpus.MaskedCorpus.load(filename)



def vsm_corpus_names():
    """
    vsm_corpus_names()

    Returns a list of available corpora as specified in the 
    configuration file.

    Examples
    --------
    In [9]: plain_corpus_names()
    Out[9]: ['philpapers', 'iep', 'test', 'sep']
    """

    vsm_corpora = bk._get_vsm_corpora()

    return vsm_corpora.sections()


    
def plain_corpus_names():
    """
    plain_corpus_names()

    Returns a directory of the parent classes of available 
    corpora as specified in the configuration file.

    Examples
    --------
    In [8]: vsm_corpus_names()
    Out[8]: 
    ['test-freq1-nltk-compressed',
     'test-freq1-nltk',
     'test-freq1-nltk-jones',
     'test']
    """
    plain_corpora = bk._get_plain_corpora()

    return plain_corpora.sections()



def load_stoplist(stoplist_name):
    """
    Load an available stoplist. 
    """
    stoplists = bk._get_stoplists()

    filename = stoplists.get(stoplist_name, 'filename')

    with open(filename, 'r') as f:

        return f.read().split('\n')



def corpus_metadata(plain_name):
    """
    corpus_metadata(plain_name)

    Returns the metadata of a specified corpus family 
    as specified in the configuration file.

    Parameters
    ----------
    plain_name : string
    	The plain name of a corpus.
    
    Returns
    -------
    metadata : string
    	The metadata of a specified corpus.

    Example
    -------
    In [12]: corpus_metadata('sep')
    Out[12]: 'http://plato.stanford.edu/\n'

    """
    plain_corpora = bk._get_plain_corpora()

    metadata_file = plain_corpora.get(plain_name, 'metadata')

    with open(metadata_file, 'r') as f:

        return f.read()

    
