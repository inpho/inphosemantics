import os

import ConfigParser as cfg



_corpora = cfg.SafeConfigParser()

_corpora_cfg = [os.path.join(p, n)
                for p, s, f in os.walk('inphosemantics/config/corpora')
                for n in f]

_corpora.read(_corpora_cfg)

_matrices = cfg.SafeConfigParser()

_matrices_cfg = [os.path.join(p, n)
                for p, s, f in os.walk('inphosemantics/config/matrices')
                for n in f]

_matrices.read(_matrices_cfg)

_stoplists = cfg.SafeConfigParser()

_stoplists_cfg = [os.path.join(p, n)
                for p, s, f in os.walk('inphosemantics/config/stoplists')
                for n in f]

_stoplists.read(_stoplists_cfg)



def _get_corpora():

    return _corpora



def _get_matrices():

    return _matrices



def _get_stoplists():

    return _stoplists
