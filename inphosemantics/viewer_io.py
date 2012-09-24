# Functions to view and analyze data gathered by vector space models
# trained on InPhO-related corpora

from vsm import model
from vsm import viewer
from vsm.viewer import tfviewer
from vsm.viewer import tfidfviewer
from vsm.viewer import lsaviewer
from vsm.viewer import beagleenvironmentviewer as envv
from vsm.viewer import beaglecontextviewer as ctxv
from vsm.viewer import beagleorderviewer as ordv
from vsm.viewer import beaglecompositeviewer as comv

import bookkeeping as bk
import model_io
import corpus_io



__all__ = ['viewer']



def viewer(matrix_name):

    matrices = bk._get_matrices()

    corpus_name = matrices.get(matrix_name, 'vsm_corpus')

    corpus = corpus_io.load_corpus(corpus_name)

    matrix = model_io.load_matrix(matrix_name)

    model_type = matrices.get(matrix_name, 'model_type')



    if model_type == 'tf':

        return tfviewer.TfViewer(corpus=corpus, matrix=matrix)

    elif model_type == 'tfidf':

        return tfidfviewer.TfIdfViewer(corpus=corpus, matrix=matrix)

    elif model_type == 'lsa':

        return lsaviewer.LsaViewer(corpus=corpus, svd_matrices=matrix)

    elif model_type == 'beagle-environment':

        return envv.BeagleEnvironmentViewer(corpus=corpus, matrix=matrix)

    elif model_type == 'beagle-context':

        return ctxv.BeagleContextViewer(corpus=corpus, matrix=matrix)

    elif model_type == 'beagle-order':

        return ordv.BeagleOrderViewer(corpus=corpus, matrix=matrix)

    elif model_type == 'beagle-composite':

        return comv.BeagleCompositeViewer(corpus=corpus, matrix=matrix)
