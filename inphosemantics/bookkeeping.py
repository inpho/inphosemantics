import os
import ConfigParser as cfg



# TODO: abstract module from a specific configuration directory;
# establish user and system locations for config files. Version
# inphodata's config files separately



_inphosemantics_dir, inphosemantics_file = os.path.split(__file__)

_config_dir = os.path.join(_inphosemantics_dir, 'config')

_plain_corpora_dir = os.path.join(_config_dir, 'plain-corpora')

_vsm_corpora_dir = os.path.join(_config_dir, 'vsm-corpora')

_matrices_dir = os.path.join(_config_dir, 'matrices')

_stoplists_dir = os.path.join(_config_dir, 'stoplists')



_plain_corpora = cfg.SafeConfigParser()

_plain_corpora_cfg = [os.path.join(p, n)
                      for p, s, f in os.walk(_plain_corpora_dir)
                      for n in f]

_plain_corpora.read(_plain_corpora_cfg)

_vsm_corpora = cfg.SafeConfigParser()

_vsm_corpora_cfg = [os.path.join(p, n)
                    for p, s, f in os.walk(_vsm_corpora_dir)
                    for n in f]

_vsm_corpora.read(_vsm_corpora_cfg)

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



def _get_plain_corpora():

    return _plain_corpora



def _get_vsm_corpora():

    return _vsm_corpora



def _get_matrices():

    return _matrices



def _get_stoplists():

    return _stoplists
