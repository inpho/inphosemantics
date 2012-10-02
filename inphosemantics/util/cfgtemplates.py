import os

import ConfigParser as cfg



def add_inpho_plain(plain_cfg, plain_name, corpus_root, metadata_file):

    plain_cfg.add_section(plain_name)

    plain_dir = os.path.join(corpus_root, 'plain')
    
    plain_cfg.set(plain_name, 'dir', plain_dir)

    raw_dir = os.path.join(corpus_root, 'raw')

    plain_cfg.set(plain_name, 'raw_dir', raw_dir)

    metadata_file = os.path.join(raw_dir, metadata_file)

    plain_cfg.set(plain_name, 'metadata', metadata_file)

    return plain_cfg



def add_inpho_vsm_corp(vsm_corp_cfg, plain_name, corpus_root):

    vsm_corp_root = os.path.join(corpus_root, 'vsm-corpora')

    section = plain_name + '-freq1-nltk'

    vsm_corp_cfg.add_section(section)

    filename = os.path.join(vsm_corp_root, section + '.npz')

    vsm_corp_cfg.set(section, 'filename', filename)

    vsm_corp_cfg.set(section, 'plain_name', plain_name)

    vsm_corp_cfg.set(section, 'freq1', 'True')

    vsm_corp_cfg.set(section, 'nltk', 'True')

    section = plain_name + '-freq1-nltk-jones'

    vsm_corp_cfg.add_section(section)

    filename = os.path.join(vsm_corp_root, section + '.npz')

    vsm_corp_cfg.set(section, 'filename', filename)

    vsm_corp_cfg.set(section, 'plain_name', plain_name)

    vsm_corp_cfg.set(section, 'freq1', 'True')

    vsm_corp_cfg.set(section, 'nltk', 'True')

    vsm_corp_cfg.set(section, 'jones', 'True')

    return vsm_corp_cfg




def add_inpho_matrices(matrices_cfg, plain_name, corpus_root):

    matrices_root = os.path.join(corpus_root, 'vsm-matrices')

    section = plain_name + '-tf-pages'

    matrices_cfg.add_section(section)

    filename = os.path.join(matrices_root, '%(vsm_corpus)s-%(model_type)s-%(tok_name)s.npy')

    matrices_cfg.set(section, 'filename', filename)
 
    matrices_cfg.set(section, 'vsm_corpus', plain_name + '-freq1-nltk')

    matrices_cfg.set(section, 'model_type', 'tf')

    matrices_cfg.set(section, 'tok_name', 'pages')

    section = plain_name + '-tfidf-pages'

    matrices_cfg.add_section(section)

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-%(model_type)s-%(tok_name)s.npy')

    matrices_cfg.set(section, 'filename', filename)

    matrices_cfg.set(section, 'vsm_corpus', plain_name + '-freq1-nltk')

    filename = os.path.join(matrices_root, '%(vsm_corpus)s-tf-%(tok_name)s.npy')

    matrices_cfg.set(section, 'tf_matrix', filename)

    matrices_cfg.set(section, 'model_type', 'tfidf')

    matrices_cfg.set(section, 'tok_name', 'pages')
        
    section = plain_name + '-lsa-pages'

    matrices_cfg.add_section(section)

    filename = os.path.join(matrices_root,
                            ('%(vsm_corpus)s-%(model_type)s-%(tok_name)s'
                             + '-%(factors)s.npy'))

    matrices_cfg.set(section, 'filename', filename)

    filename = os.path.join(matrices_root, '%(vsm_corpus)s-tfidf-%(tok_name)s.npy')

    matrices_cfg.set(section, 'td_matrix', filename)

    matrices_cfg.set(section, 'vsm_corpus', plain_name + '-freq1-nltk')
        
    matrices_cfg.set(section, 'model_type', 'lsa')

    matrices_cfg.set(section, 'tok_name', 'pages')

    matrices_cfg.set(section, 'factors', '300')
        
    section = plain_name + '-beagle-environment'

    matrices_cfg.add_section(section)

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-%(model_type)s-%(n_columns)s.npy')

    matrices_cfg.set(section, 'filename', filename)

    matrices_cfg.set(section, 'vsm_corpus', plain_name + '-freq1-nltk-jones')    

    matrices_cfg.set(section, 'model_type', 'beagle-environment')

    matrices_cfg.set(section, 'n_columns', '2048')
        
    section = plain_name + '-beagle-context'

    matrices_cfg.add_section(section)

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-%(model_type)s-%(n_columns)s.npy')

    matrices_cfg.set(section, 'filename', filename)

    matrices_cfg.set(section, 'vsm_corpus', plain_name + '-freq1-nltk-jones')    

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-beagle-environment-%(n_columns)s.npy')
    
    matrices_cfg.set(section, 'env_matrix', filename)

    matrices_cfg.set(section, 'model_type', 'beagle-context')

    matrices_cfg.set(section, 'n_columns', '2048')
    
    section = plain_name + '-beagle-order'
        
    matrices_cfg.add_section(section)

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-%(model_type)s-%(n_columns)s-%(lambda)s.npy')

    matrices_cfg.set(section, 'filename', filename)

    matrices_cfg.set(section, 'vsm_corpus', plain_name + '-freq1-nltk-jones')    

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-beagle-environment-%(n_columns)s.npy')
    
    matrices_cfg.set(section, 'env_matrix', filename)

    matrices_cfg.set(section, 'model_type', 'beagle-order')

    matrices_cfg.set(section, 'n_columns', '2048')
    
    matrices_cfg.set(section, 'lambda', '7')

    section = plain_name + '-beagle-composite'

    matrices_cfg.add_section(section)

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-%(model_type)s-%(n_columns)s-%(lambda)s.npy')

    matrices_cfg.set(section, 'filename', filename)

    matrices_cfg.set(section, 'vsm_corpus', plain_name + '-freq1-nltk-jones')    

    matrices_cfg.set(section, 'model_type', 'beagle-composite')

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-beagle-context-%(n_columns)s.npy')
    
    matrices_cfg.set(section, 'ctx_matrix', filename)

    filename = os.path.join(matrices_root,
                            '%(vsm_corpus)s-beagle-order-%(n_columns)s-%(lambda)s.npy')
    
    matrices_cfg.set(section, 'ord_matrix', filename)

    matrices_cfg.set(section, 'n_columns', '2048')

    matrices_cfg.set(section, 'lambda', '7')
