import os
import ConfigParser as cfg

_inphosemantics_dir, inphosemantics_file = os.path.split(__file__)

_config_dir = os.path.join(_inphosemantics_dir, 'config')

_corpora_dir = os.path.join(_config_dir, 'corpora')

_matrices_dir = os.path.join(_config_dir, 'matrices')

_stoplists_dir = os.path.join(_config_dir, 'stoplists')

_corpora = cfg.SafeConfigParser()

_corpora_cfg = [os.path.join(p, n)
                for p, s, f in os.walk(_corpora_dir)
                for n in f]

_corpora.read(_corpora_cfg)

_matrices = cfg.SafeConfigParser()

_matrices_cfg = [os.path.join(p, n)
                for p, s, f in os.walk(_matrices_dir)
                for n in f]

_matrices.read(_matrices_cfg)

_stoplists = cfg.SafeConfigParser()

_stoplists_cfg = [os.path.join(p, n)
                for p, s, f in os.walk(_stoplists_dir)
                for n in f]

_stoplists.read(_stoplists_cfg)



def _get_corpora():

    return _corpora



def _get_matrices():

    return _matrices



def _get_stoplists():

    return _stoplists
