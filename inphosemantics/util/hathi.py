import os
import shutil
import re
import logging
import ConfigParser as cfg

from nltk.corpus import wordnet as wn
import enchant

from inphosemantics import bookkeeping as bk
import cfgtemplates as tmpl



hathi_root = '/var/inphosemantics/data/fresh/hathi'



def initialize_hathi_files(confirm=False):

    if confirm:

        for book in os.listdir(hathi_root):

            book_root = os.path.join(hathi_root, book)
            
            print 'Structuring', book_root
            
            raw_root = os.path.join(book_root, 'raw')
            
            plain_root = os.path.join(book_root, 'plain')
            
            raw_files = os.listdir(book_root)
            
            os.mkdir(raw_root)
            
            os.mkdir(plain_root)
            
            for f in raw_files:
                
                src = os.path.join(book_root, f)
                
                if f.endswith('txt'):

                    dst = os.path.join(plain_root, f)

                    shutil.copy(src, dst)

                dst = os.path.join(raw_root, f)

                shutil.move(src, dst)

            os.mkdir(os.path.join(book_root, 'vsm-corpora'))

            os.mkdir(os.path.join(book_root, 'vsm-matrices'))

    else:

        print 'Use the argument confirm=True '\
              'if you really want to do this.'


            
def rm_hathi_plain(confirm=False):

    if confirm:

        for book in os.listdir(hathi_root):

            book_root = os.path.join(hathi_root, book)

            plain_root = os.path.join(book_root, 'plain')

            shutil.rmtree(plain_root)

    else:

        print 'Use the argument confirm=True '\
              'if you really want to do this.'



def rm_hathi_logs(confirm=False):

    if confirm:

        for book in os.listdir(hathi_root):

            book_root = os.path.join(hathi_root, book)

            for f in os.listdir(book_root):

                if f.endswith('log'):

                    log_file = os.path.join(book_root, f)

                    os.remove(log_file)

    else:

        print 'Use the argument confirm=True '\
              'if you really want to do this.'




def cp_hathi_rawtoplain(confirm=False):

    if confirm:

        for book in os.listdir(hathi_root):

            # For debugging
            # if book == 'uc2.ark+=13960=t1zc80k1p':
            # if book == 'uc2.ark+=13960=t8tb11c8g':
                
            book_root = os.path.join(hathi_root, book)
            
            raw_root = os.path.join(book_root, 'raw')
            
            plain_root = os.path.join(book_root, 'plain')
            
            raw_files = os.listdir(raw_root)
            
            os.mkdir(plain_root)
            
            print 'Copying from', raw_root
            
            for f in raw_files:
                
                if f.endswith('txt'):

                    src = os.path.join(raw_root, f)
            
                    dst = os.path.join(plain_root, f)

                    shutil.copy(src, dst)

    else:

        print 'Use the argument confirm=True '\
              'if you really want to do this.'



def write_hathi_plain_cfg():

    cfg_file = os.path.join(bk._plain_corpora_dir, 'hathi-plain-corpora.cfg')

    defaults = { 'root': '/var/inphosemantics/data/fresh' }

    plain_cfg = cfg.SafeConfigParser(defaults)

    for book in os.listdir(hathi_root):

        book_root = os.path.join(hathi_root, book)

        metadata_file = os.path.join(book_root, 'raw',
                                     book + '_metadata.json')

        tmpl.add_inpho_plain(plain_cfg, book, book_root, metadata_file)

    with open(cfg_file, 'w') as f:

        plain_cfg.write(f)


        
def write_hathi_vsm_corp_cfg():

    cfg_file = os.path.join(bk._vsm_corpora_dir, 'hathi-vsm-corpora.cfg')

    defaults = { 'root': '/var/inphosemantics/data/fresh' }

    vsm_corp_cfg = cfg.SafeConfigParser(defaults)

    for book in os.listdir(hathi_root):

        book_root = os.path.join(hathi_root, book)

        tmpl.add_inpho_vsm_corp(vsm_corp_cfg, book, book_root)

    with open(cfg_file, 'w') as f:

        vsm_corp_cfg.write(f)


    
def write_hathi_matrices_cfg():

    cfg_file = os.path.join(bk._matrices_dir, 'hathi-vsm-matrices.cfg')

    defaults = { 'root': '/var/inphosemantics/data/fresh' }

    matrices_cfg = cfg.SafeConfigParser(defaults)

    for book in os.listdir(hathi_root):

        book_root = os.path.join(hathi_root, book)

        tmpl.add_inpho_matrices(matrices_cfg, book, book_root)

    with open(cfg_file, 'w') as f:

        matrices_cfg.write(f)



def proc_hathi_coll():
    """
    """
    for book in os.listdir(hathi_root):

        # For debugging
        # if book == 'uc2.ark+=13960=t1zc80k1p':
        # if book == 'uc2.ark+=13960=t8tb11c8g':

        proc_hathi_book(book)
            


def proc_hathi_book(book):

    book_root = os.path.join(hathi_root, book)

    logger = logging.getLogger(book)

    logger.setLevel(logging.INFO)

    log_file = os.path.join(book_root, book + '-raw-proc.log')

    handler = logging.FileHandler(log_file, mode='w')

    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(message)s')

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    print 'Processing', book_root

    plain_root = os.path.join(book_root, 'plain')

    try:
        
        rm_pg_headers(plain_root, logger)

        rm_lb_hyphens(plain_root, logger)

    finally:
        
        handler.close()



def rm_lb_hyphens(plain_root, logger):
    """
    Looks for a hyphen followed by whitespace or a line break.

    Reconstructs word and checks to see if the result exists in either
    WordNet or the OS's default spellchecker dictionary. If so,
    replaces fragments with reconstructed word.
    """

    d = enchant.Dict('en_US')

    def recon(match_obj):

        rc_word = match_obj.group(1) + match_obj.group(2)
        
        if wn.synsets(rc_word) or d.check(rc_word):

            logger.info('\nbook: %s\nreconstructed word:\n%s\n',
                         plain_root, rc_word)
            
            return rc_word
        
        logger.info('\nbook: %s\nignored expression:\nleft: %s\nright: %s\n',
                     plain_root, match_obj.group(1), match_obj.group(2))

        return match_obj.group(0)



    def inner(s):

        lb_hyphenated = re.compile(r'(\w+)-\s+(\w+)')

        return lb_hyphenated.sub(recon, s)

    

    page_files = os.listdir(plain_root)

    page_files = [n for n in page_files if n.endswith('txt')]

    for i, page_file in enumerate(page_files):

        filename = os.path.join(plain_root, page_file)

        with open(filename, 'r+w') as f:

            page = f.read()

            page = inner(page)

            f.seek(0)

            f.write(page)



def rm_pg_headers(plain_root, logger, bound=1):
    """
    Tries to detect repeated page headers (e.g., chapter titles). If
    found, removes them.

    The routine takes the first non-empty lines of text, strips them
    of numbers and punctuation and computes frequencies. If frequency
    for the reduced string exceeds `bound`, the corresponding first
    lines are considered headers.
    """

    page_files = os.listdir(plain_root)

    page_files = [n for n in page_files if n.endswith('txt')]

    # Get first non-empty lines

    first_lines = []

    fl = re.compile(r'^\s*([^\n]*\S)*\s\n')
    
    for page_file in page_files:

        page_file = os.path.join(plain_root, page_file)

        with open(page_file, 'r') as f:

            page = f.read()

        first_line = fl.match(page)
            
        if first_line == None:

            first_lines.append('')

        else:

            first_lines.append(first_line.group(0))

    # Remove capitalization, roman numerals for numbers under 50,
    # punctuation, arabic numerals from first lines

    for i in xrange(len(first_lines)):

        line = first_lines[i]

        line = line.lower()

        # An overzealous arabic numeral detector (OCR errors include
        # `i` for `1` for example)

        line = re.sub(r'\b\S*\d+\S*\b', '', line)

        # Roman numerals i to xxxix

        line = re.sub(r'\b(x{0,3})(ix|iv|v?i{0,3})\b', '', line)

        # Collapse line to letters only

        line = re.sub(r'[^a-z]', '', line)

        first_lines[i] = (first_lines[i], line)



    freqs = dict()

    for line, reduced in first_lines:

        if reduced in freqs:

            freqs[reduced] += 1

        else:

            freqs[reduced] = 1


    
    for i, page_file in enumerate(page_files):

        filename = os.path.join(plain_root, page_file)

        line, reduced = first_lines[i]

        if freqs[reduced] > bound:

            with open(filename, 'r') as f:

                page = f.read()

            if page:

                logger.info('\nbook: %s\nfile: %s\nremoved header:\n%s\n',
                             plain_root, page_file, line)

            page = fl.sub('', page)

            with open(filename, 'w') as f:

                f.write(page)


    
