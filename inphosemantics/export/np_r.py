from rpy2.robjects import r
from rpy2.robjects import numpy2ri as npr



__all__ = ['save_matrix_R',
           'save_simmat_R']



def save_matrix_R(filename, matrix, row_labels=None, col_labels=None):

    rmatrix = npr.numpy2ri(matrix)

    r.assign('data', rmatrix)
    
    if row_labels:
        
        r("rownames(%s) <- c%s" % ('data', tuple(row_labels)))

    if col_labels:

        r("colnames(%s) <- c%s" % ('data', tuple(col_labels)))

    r.save('data', file=filename)    



def save_simmat_R(filename, simmat):

    rmatrix = npr.numpy2ri(simmat.matrix)

    r.assign('data', rmatrix)
    
    r("rownames(%s) <- c%s" % ('data', tuple(simmat.labels)))

    r("colnames(%s) <- c%s" % ('data', tuple(simmat.labels)))

    r.save('data', file=filename)    



