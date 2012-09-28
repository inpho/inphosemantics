# Functions to tokenize InPhO-related plain text corpora and write the
# results


from vsm import corpus
from vsm.corpus import util

import bookkeeping as bk



__all__ = ['write_corpus',
           'load_corpus',
           'corpus_names',
           'load_stoplist']



def _is_compressed(corpus_name):

    corpora = bk._get_corpora()

    try:

        return corpora.getboolean(corpus_name, 'compressed')

    except bk.cfg.NoOptionError:

        return False



def _get_masking_fns(corpus_name):

    corpora = bk._get_corpora()

    masking_fns = []

    try:

        if corpora.getboolean(corpus_name, 'freq1'):

            masking_fns.append(corpus.mask_f1)

    except bk.cfg.NoOptionError:

        pass

    try:

        if corpora.getboolean(corpus_name, 'nltk'):

            stop = load_stoplist('nltk')

            masking_fns.append(lambda c: corpus.mask_from_stoplist(c, stop))

    except bk.cfg.NoOptionError:

        pass

    try:

        if corpora.getboolean(corpus_name, 'jones'):

            stop = load_stoplist('jones')

            masking_fns.append(lambda c: corpus.mask_from_stoplist(c, stop))

    except bk.cfg.NoOptionError:

        pass

    return masking_fns



def tokenize_corpus(corpus_name):
    '''
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
     
    '''
    corpora = bk._get_corpora()

    plain_file = corpora.get(corpus_name, 'plain_dir')

    vsm_corpus_file = corpora.get(corpus_name, 'filename')



    tok = util.MultipleArticleTokenizer(plain_file)

    c = corpus.MaskedCorpus(corpus=tok.words,
                            tok_names=tok.tok_names,
                            tok_data=tok.tok_data)



    masking_fns = _get_masking_fns(corpus_name)

    for fn in masking_fns:

        fn(c)



    if _is_compressed(corpus_name):

        c = c.to_corpus(compress=True)


    c.save(vsm_corpus_file)



def load_corpus(corpus_name):
    '''
    Loads data from a specified corpus into a MaskedCorpus object that has 
    been stored using `save`. Returns a MaskedCorpus object storing the data 
    found in the speciied corpus file.
    '''
    corpora = bk._get_corpora()

    filename = corpora.get(corpus_name, 'filename')

    if _is_compressed(corpus_name):

        return corpus.Corpus.load(filename)

    return corpus.MaskedCorpus.load(filename)



def corpus_names():
    '''
    Returns a list of available corpora as specified by the inphosemantics
    configuration file.

    For detailed instructions on adding new corpora, see...
    '''

    corpora = bk._get_corpora()

    return corpora.sections()



def load_stoplist(stoplist_name):
    '''
    Load an available stoplist. 
    '''
    stoplists = bk._get_stoplists()

    filename = stoplists.get(stoplist_name, 'filename')

    with open(filename, 'r') as f:

        return f.read().split('\n')

    
