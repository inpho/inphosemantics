# Functions to train various vector space models on InPhO-related
# corpora

from vsm import model
from vsm.model import tf
from vsm.model import tfidf
from vsm.model import lsa
from vsm.model import beagleenvironment
from vsm.model import beaglecontext
from vsm.model import beagleorder
from vsm.model import beaglecomposite

import bookkeeping as bk
import corpus_io



__all__ = ['train_model',
           'matrix_names',
           'load_matrix',
           'model_types']



def train_model(matrix_name):

    matrices = bk._get_matrices()

    corpus_name = matrices.get(matrix_name, 'vsm_corpus')

    corpus = corpus_io.load_vsm_corpus(corpus_name)

    filename = matrices.get(matrix_name, 'filename')

    model_type = matrices.get(matrix_name, 'model_type')



    if model_type == 'tf':

        m = tf.TfModel()

        tok_name = matrices.get(matrix_name, 'tok_name')

        m.train(corpus, tok_name)



    elif model_type == 'tfidf':

        m = tfidf.TfIdfModel()

        tf_file = matrices.get(matrix_name, 'tf_matrix')

        tf_matrix = model.Model.load_matrix(tf_file)

        m.train(tf_matrix=tf_matrix)



    elif model_type == 'lsa':

        m = lsa.LsaModel()

        td_file = matrices.get(matrix_name, 'td_matrix')

        td_matrix = model.Model.load_matrix(td_file)

        k_factors = matrices.getint(matrix_name, 'factors')

        m.train(td_matrix=td_matrix, k_factors=k_factors)

        

    elif model_type == 'beagle-environment':

        m = beagleenvironment.BeagleEnvironment()

        n_columns = matrices.getint(matrix_name, 'n_columns')

        m.train(corpus, n_columns=n_columns)



    elif model_type == 'beagle-context':

        m = beaglecontext.BeagleContext()

        env_file = matrices.get(matrix_name, 'env_matrix')

        env_matrix = model.Model.load_matrix(env_file)

        m.train(corpus, env_matrix=env_matrix)

        

    elif model_type == 'beagle-order':

        m = beagleorder.BeagleOrder()

        env_file = matrices.get(matrix_name, 'env_matrix')

        env_matrix = model.Model.load_matrix(env_file)

        lmda = matrices.getint(matrix_name, 'lambda')

        m.train(corpus, env_matrix=env_matrix, lmda=lmda)



    elif model_type == 'beagle-composite':

        m = beaglecomposite.BeagleComposite()

        ctx_file = matrices.get(matrix_name, 'ctx_matrix')

        ctx_matrix = model.Model.load_matrix(ctx_file)

        ord_file = matrices.get(matrix_name, 'ord_matrix')

        ord_matrix = model.Model.load_matrix(ord_file)

        m.train(corpus, ctx_matrix=ctx_matrix, ord_matrix=ord_matrix)



    m.save_matrix(filename)



def matrix_names():
    """
    matrix_names()

    Returns a list of available pre-trained corpora as specified by the 
    configuration file.

    Examples
    --------
    In [1]: matrix_names()
    Out[1]: 
    ['test-beagle-context',
     'test-beagle-order',
     'test-tfidf-paragraphs',
     'test-beagle-environment',
     'test-tf-paragraphs',
     'test-lsa-paragraphs',
     'test-beagle-composite']
    """		   
    matrices = bk._get_matrices()

    return matrices.sections()



def load_matrix(matrix_name):
    '''
    load_matrix(matrix_name)

    Loads data from a specified pre-trained corpus matrix file.
    
    Parameters
    ----------
    matrix_name : string
    	Named of pre-trained corpus, as specified by the
	configuration file.

    Returns
    -------
    matrix : list of arrays of tokenized data. 

    Examples
    --------
    In [1]: c = load_matrix('test-lsa-paragraphs')
    Loading LSA matrices from /var/inphosemantics/data/fresh/test/vsm-matrices/test-freq1-nltk-lsa-paragraphs-300.npz
    '''

    matrices = bk._get_matrices()

    filename = matrices.get(matrix_name, 'filename')

    model_type = matrices.get(matrix_name, 'model_type')

    if model_type == 'lsa':

        return lsa.LsaModel.load_matrix(filename)

    return model.Model.load_matrix(filename)



def model_types():
    """
    model_types()

    Returns a list of available models as specified by the 
    configuration file.

    Examples
    --------
    In [1]: model_types()
    Out[1]: 
    ['beagle-environment',
    'lsa',
    'tfidf',
    'beagle-context',
    'beagle-composite',
    'tf',
    'beagle-order']
   
    """
    model_types = set()

    matrices = bk._get_matrices()

    for m in matrices.sections():

        model_types.add(matrices.get(m, 'model_type'))
        
    return list(model_types)



