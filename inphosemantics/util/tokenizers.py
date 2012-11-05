# TODO: Merge vsm.corpus.util and this file
from vsm.corpus.util import *



# Supercedes vsm.corpus.util.textfile_tokenize
def textfile_tokenize(path, sort=False):
    """
    Takes a string and returns a list of strings and a dictionary.
    Intended use: the input string is a directory name containing
    plain text files. The output list is a list of strings, each of
    which is the contents of one of these files. The dictionary is a
    map from indices of this list to the names of the source files.
    """

    out = [],{}
    
    filenames = os.listdir(path)

    if sort:

        filenames.sort()

    for filename in filenames:
        
        filename = os.path.join(path, filename)

        with open(filename, mode='r') as f:

            out[0].append(f.read())

            out[1][len(out[0]) - 1] = filename

    return out



class BookTokenizer(object):
    """
    """
    def __init__(self, path):

        self.path = path

        self.words = []

        self.tok_names = ['pages', 'sentences']

        self.tok_data = None

        self._compute_tokens()
    


    def _compute_tokens(self):

        pages, pages_metadata = textfile_tokenize(self.path, sort=True)

        page_tokens = []

        sentence_spans = []

        print 'Computing page tokens'

        for i, page in enumerate(pages):

            print 'Processing page in', pages_metadata[i]

            sentences = sentence_tokenize(page)

            for sentence in sentences:
                    
                words = word_tokenize(sentence)

                self.words.extend(words)
                    
                sentence_spans.append(len(words))

            page_tokens.append(sum(sentence_spans))

        print 'Computing sentence tokens'

        sentence_tokens = np.cumsum(sentence_spans)

        page_tokens = zip(page_tokens, pages_metadata)

        self.tok_data = [page_tokens, sentence_tokens]



class MultipleBooksTokenizer(object):
    """
    """
    def __init__(self, path):

        self.path = path

        self.words = []

        self.tok_names = ['books', 'pages', 'sentences']

        self.tok_data = None

        self._compute_tokens()
    


    def _compute_tokens(self):

        books_metadata = os.listdir(self.path)

        books = books_metadata

        book_tokens = []

        page_tokens = []

        sentence_spans = []

        print 'Computing book and page tokens'

        for i,book in enumerate(books):

            print 'Processing book in', books_metadata[i]

            pages_path = os.path.join(self.path, book, 'plain')

            pages, pages_metadata = textfile_tokenize(pages_path)

            for (page, page_metadata) in zip(pages, pages_metadata):
                
                sentences = sentence_tokenize(page)

                for sentence in sentences:
                    
                    words = word_tokenize(sentence)

                    self.words.extend(words)
                    
                    sentence_spans.append(len(words))

                page_tokens.append((sum(sentence_spans), page_metadata))
                    
            book_tokens.append(sum(sentence_spans))

        print 'Computing sentence tokens'

        sentence_tokens = np.cumsum(sentence_spans)

        book_tokens = zip(book_tokens, books_metadata)

        self.tok_data = [book_tokens, page_tokens, sentence_tokens]
