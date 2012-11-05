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
    """
    Takes as its input a specified corpus and tokenizes it; that is, it 
    deconstructs a series of strings by word, sentence, and paragraph and 
    returns a list of each respective category. 
    
    Word tokenization employs NLTK's Penn Treeback Word Tokenizer; as such,
    words are tokenized according to the conventions used by the Penn 
    Treebank.

    Sentence tokenization employs NLTK's Punkt tokenzier. The algorithm for 
    this tokenizer is described in Kiss & Strunk (2006).
    
    Paragraph tokenization is accomplished through the recognition of 
    paragraphs as indicated by two consecutive line breaks.
    
    Example:
       In [1]: tokenize_corpus('sep')
     
    """
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

    
