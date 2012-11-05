import os
import shutil
import re
import codecs
import ConfigParser as cfg

import inphosemantics as sem
from inphosemantics import bookkeeping as bk
import htmltoplain as hp
import cfgtemplates as tmpl


sep_root = '/var/inphosemantics/data/fresh/sep-test'

rand_file = '/var/inphosemantics/data/fresh/random-vector-pool.pickle' 

def initialize_files(confirm=False):

    if confirm:

        for article in os.listdir(sep_root):

            article_root = os.path.join(sep_root, article)
            
            print 'Structuring', article_root
            
            raw_root = os.path.join(article_root, 'raw')
            
            plain_root = os.path.join(article_root, 'plain')
            
            raw_files = os.listdir(article_root)
            
            os.mkdir(raw_root)
            
            os.mkdir(plain_root)
            
            for f in raw_files:
                
                src = os.path.join(article_root, f)
                
                dst = os.path.join(raw_root, f)

                shutil.move(src, dst)

            os.mkdir(os.path.join(article_root, 'vsm-corpora'))

            os.mkdir(os.path.join(article_root, 'vsm-matrices'))

    else:

        print 'Use the argument confirm=True '\
              'if you really want to do this.'



class HtmlToPlain(hp.HtmlToPlain):
    """
    """
    def write_metadata(self, metadata_file):

        try:

            with codecs.open(metadata_file, encoding='utf-8', mode='w') as f:
            
                f.write(self.title)

                print metadata_file, 'generated.'

        except AttributeError:

            print metadata_file, 'was not generated. No metadata available.'


            
    def clean(self, tree):
        """
        Takes an ElementTree object and returns the textual content of
        the article as a list of strings.
        """

        root = tree.getroot()

        article = self.get_body(root)

        if article:

            self.title = self.get_title(root)

            article = hp.clr_toc(article)
            
            article = self.clr_pubinfo(article)
            
            article = self.clr_bib(article)
            
            article = hp.clr_sectnum(article)
            
            article = self.get_body(root)
            
            article = hp.proc_imgs(article)
        
            article = hp.clr_inline(article)
            
            article = hp.fill_par(article)

            return hp.flatten(article)

        return ''



    @staticmethod
    def get_title(elem):

        title_list = hp.filter_by_tag(elem.getiterator(), 'title')

        if title_list:

            return title_list[0].text

        return ''


    
    @staticmethod
    def get_body(tree):
        """
        Takes an Element object and returns a subtree containing
        only the body of an SEP article.
        """
        for el in hp.filter_by_tag(tree.getiterator(), 'div'):

            if el.attrib['id'] == 'aueditable':

                return el
            
        print '** Article body not found **'

        return None



    @staticmethod
    def clr_pubinfo(elem):
        """
        Takes an Element object and removes any node with the id
        attribute 'pubinfo'. (For SEP)
        """
        cp = hp.cp_map(elem)

        for el in hp.filter_by_tag(elem.getiterator(), 'div'):

            if (el.attrib.has_key('id') and
                el.attrib['id'] == 'pubinfo'):

                cp[el].remove(el)

                return elem
        
        print '** Pub info not found **'

        return elem



    @staticmethod
    def clr_bib(elem):
        """
        Takes an Element object and removes nodes which are likely
        candidates for the bibliography in the SEP.
        """
        cp = hp.cp_map(elem)
        
        hs = (hp.filter_by_tag(elem.getiterator(), 'h2') +
              hp.filter_by_tag(elem.getiterator(), 'h3'))
    
        for h in hs:
            
            for el in h.getiterator() + [h]:

                if ((el.text and
                     re.search(r'Bibliography', el.text)) or
                    (el.tail and
                     re.search(r'Bibliography', el.tail))):
                        
                    p = cp[h]

                    i = list(p).index(h)
                        
                    for node in p[i:]:

                        p.remove(node)
                        
                    return elem

        print '** Bibliography not found. **'

        return elem



def art_to_plain(article_root):

    raw_file = os.path.join(article_root, 'raw', 'index.html')

    plain_prefix = 'sep-art-' + os.path.basename(article_root)

    plain_file = plain_prefix + '.txt'

    plain_file = os.path.join(article_root, 'plain', plain_file)

    metadata_file = os.path.join(article_root, 'raw',
                                 plain_prefix + '-metadata.txt')

    h2p = HtmlToPlain(raw_file, plain_file)

    h2p.html_to_plain()

    h2p.write_metadata(metadata_file)


def sep_to_plain():

    for article in os.listdir(sep_root):

        article_root = os.path.join(sep_root, article)

        art_to_plain(article_root)

    return


def write_plain_cfg():

    cfg_file = os.path.join(bk._plain_corpora_dir, 'sep-art-plain-corpora.cfg')

    defaults = { 'root': '/var/inphosemantics/data/fresh' }

    plain_cfg = cfg.SafeConfigParser(defaults)

    for article in os.listdir(sep_root):

        article_root = os.path.join(sep_root, article)

        article_prefix = 'sep-art-' + article

        metadata_file = os.path.join(article_root, 'raw',
                                     article_prefix + '-metadata.txt')

        tmpl.add_inpho_plain(plain_cfg, article_prefix,
                             article_root, metadata_file)

    with open(cfg_file, 'w') as f:

        plain_cfg.write(f)



def write_vsm_corp_cfg():

    cfg_file = os.path.join(bk._vsm_corpora_dir, 'sep-art-vsm-corpora.cfg')

    defaults = { 'root': '/var/inphosemantics/data/fresh' }

    vsm_corp_cfg = cfg.SafeConfigParser(defaults)

    for article in os.listdir(sep_root):

        article_root = os.path.join(sep_root, article)

        article_prefix = 'sep-art-' + article
        
        tmpl.add_inpho_vsm_corp(vsm_corp_cfg, article_prefix,
                                article_root, tokenizer='article')

    with open(cfg_file, 'w') as f:

        vsm_corp_cfg.write(f)



def write_matrices_cfg():

    cfg_file = os.path.join(bk._matrices_dir, 'sep-art-vsm-matrices.cfg')

    defaults = { 'root': '/var/inphosemantics/data/fresh' }

    matrices_cfg = cfg.SafeConfigParser(defaults)

    for article in os.listdir(sep_root):

        article_root = os.path.join(sep_root, article)

        article_prefix = 'sep-art-' + article

        tmpl.add_inpho_matrices(matrices_cfg, article_prefix, article_root, rand_file)

    with open(cfg_file, 'w') as f:

        matrices_cfg.write(f)



def mat_names(model_type):

    names = sem.matrix_names()

    # filters names by model_type
    names = [m for m in names
             if re.search('-' + model_type + '(-|$)', m)]
    
    # filters names by occurrence of 'sep-art'
    names = [m for m in names
             if re.search(r'sep-art', m)]

    return names



def write_batch(matrix_names, filename):

    with open(filename, 'w') as f:

        for m in matrix_names:

            command = 'python -c \"import inphosemantics as sem; '

            command += 'sem.train_model(\'%s\')\"\n'%m 

            f.write(command)
