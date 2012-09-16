# Functions to tokenize InPhO-related plain text corpora and write the
# results



from inphosemantics import *

from vsm import corpus
from vsm.corpus import util



_plain_corpora = _get_plain_corpora()

_vsm_corpora = _get_vsm_corpora()

_masking_fns = _get_masking_fns()



def inphocorpus(plain, vsm_corpus, masking_fns=[]):

    plain_file = _plain_corpora[plain]

    vsm_corpus_file = _vsm_corpora[vsm_corpus]

    tok = util.MultipleArticleTokenizer(plain_file)

    c = corpus.MaskedCorpus(corpus=tok.words,
                            tok_names=tok.tok_names,
                            tok_data=tok.tok_data)

    for fn in masking_fns:

        _masking_fns[fn](c)

    c.save(vsm_corpus_file)



def load_inphocorpus(vsm_corpus):

    vsm_corpus_file = _vsm_corpora[vsm_corpus]

    return corpus.MaskedCorpus.load(vsm_corpus_file)
