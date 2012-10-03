def np2word2word(matrix, labels, filename=None, comment=None):

    out = ''

    if comment:
        out += comment

    out += '\n' # First line of CSV represents title
    
    labels = ['"' + label + '"' for label in labels]

    out += ' , ' + ', '.join(labels) + '\n'

    for i in xrange(matrix.shape[0]):
        
        values = [str(value) for value in matrix[i,:]]
        
        out += labels[i] + ', ' + ', '.join(values) + '\n'


    if filename:
        with open(filename, 'w') as f:
            f.write(out)

    return out
