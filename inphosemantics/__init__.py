import os

from vsm import corpus



__all__ = ['data_root',
           '_get_plain_corpora',
           '_get_vsm_corpora',
           '_get_masking_fns']



data_root = '/var/inphosemantics/data/fresh'



def _get_plain_corpora():

    plain_corpora = dict()
    
    plain_corpora['test'] = os.path.join(data_root, 'test', 'plain')

    return plain_corpora



def _get_vsm_corpora():

    vsm_corpora = dict()

    vsm_corpora['test'] = os.path.join(data_root, 'test', 'vsmcorp', 'test.npz')

    return vsm_corpora



def _get_masking_fns():
    
    nltk_stop = []

    jones_stop = []

    masking_fns = dict()

    masking_fns['freq1'] = corpus.mask_f1
    
    masking_fns['nltk'] = lambda c: corpus.mask_from_stoplist(c, nltk_stop)
    
    masking_fns['jones'] = lambda c: corpus.mask_from_stoplist(c, jones_stop)

    return masking_fns
