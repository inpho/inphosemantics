# Functions to tokenize InPhO-related plain text corpora and write the
# results


from vsm import corpus
from vsm.corpus import util

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
    tokenize_corpus(corpus_name)

    Tokenize a given corpus; that is, deconstruct a series of
    strings by word, sentence, and paragraph. 

    Parameters
    ----------
    corpus_name : string
        The plain name of the corpus of interest, as specified 
	in the configuration file. 
    
    Returns
    -------
    matrix : #NEEDS UPDATES

    Notes
    -----

    Word tokenization employs NLTK's Penn Treeback Word Tokenizer.

    Sentence tokenization employs NLTK's Punkt tokenzier. 
    (See Kiss & Strunk (2006)).
    
    Paragraph tokenization is accomplished through the recognition of 
    paragraphs as indicated by two consecutive line breaks.
    
    Examples
    --------
    In [1]: tokenize_corpus('sep')
     #NEEDS UPDATES
    '''
    corpora = bk._get_corpora()
     
    vsm_corpora = bk._get_vsm_corpora()

    vsm_corpus_file = vsm_corpora.get(vsm_corpus_name, 'filename')
    
    plain_name = vsm_corpora.get(vsm_corpus_name, 'plain_name')

    plain_corpora = bk._get_plain_corpora()
    
    plain_dir = plain_corpora.get(plain_name, 'dir')



    tok = util.MultipleArticleTokenizer(plain_dir)

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
    Loads data from a specified corpus into a MaskedCorpus object that has 
    been stored using `save`. Returns a MaskedCorpus object storing the data 
    found in the speciied corpus file.
    """
    corpora = bk._get_vsm_corpora()

    filename = corpora.get(vsm_corpus_name, 'filename')

    if _is_compressed(vsm_corpus_name):

        return corpus.Corpus.load(filename)

    return corpus.MaskedCorpus.load(filename)



def vsm_corpus_names():
    """
    Returns a list of available corpora as specified by the inphosemantics
    configuration file.

    For detailed instructions on adding new corpora, see...
    """

    vsm_corpora = bk._get_vsm_corpora()

    return vsm_corpora.sections()


    
def plain_corpus_names():
    """
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

    plain_corpora = bk._get_plain_corpora()

    metadata_file = plain_corpora.get(plain_name, 'metadata')

    with open(metadata_file, 'r') as f:

        return f.read()

    
