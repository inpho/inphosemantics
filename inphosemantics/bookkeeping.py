import ConfigParser as cfg



_corpora = cfg.SafeConfigParser()

_corpora.read('inphosemantics/vsm-corpora.cfg')

_matrices = cfg.SafeConfigParser()

_matrices.read('inphosemantics/vsm-matrices.cfg')

_stoplists = cfg.SafeConfigParser()

_stoplists.read('inphosemantics/vsm-stoplists.cfg')



def _get_corpora():

    return _corpora



def _get_matrices():

    return _matrices



def _get_stoplists():

    return _stoplists
