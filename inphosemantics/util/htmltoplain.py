import os.path
import pickle
import tempfile
import codecs
import re
from unidecode import unidecode
from xml.etree.ElementTree import ElementTree



class HtmlToPlain(object):

    def __init__(self, raw_file, plain_file):

        self.raw_file = raw_file

        self.plain_file = plain_file


        
    def import_html(self):
        """
        'name' here denotes the name of the directory directly
        containing the article
        """
        
        print 'Loading HTML file for the article', self.raw_file
        
        #TODO Error-handling
        
        tmp = tempfile.NamedTemporaryFile()

        tidy = ' '.join(['tidy', '-qn', '-asxml', '--clean yes',
                         '--ascii-chars yes', '--char-encoding utf8'])

        command = '%s %s>%s 2>/dev/null' % (tidy, self.raw_file, tmp.name)

        os.system(command)

        tree = ElementTree()

        tree.parse(tmp.name)

        tmp.close()

        return tree



    def write_plain(self, text):

        print 'Writing plain text file for the article', self.plain_file

        with codecs.open(self.plain_file, encoding='utf-8', mode='w') as f:
            
            f.write(text)

        return



    def html_to_plain(self):

        tree = self.import_html()

        text = self.clean(tree)

        text = '\n\n'.join(text)
            
        text = unidecode(text)

        unknown = re.compile('\\[\\?\\]')

        text = unknown.sub(' ', text)

        self.write_plain(text)
                        
        return



    def clean(self, tree):
        """
        Takes an ElementTree object and returns the textual content of
        the article as a list of strings.
        """

        root = tree.getroot()

        article = self.get_body(root)

        article = proc_imgs(article)
        
        article = clr_inline(article)

        article = fill_par(article)

        return flatten(article)




        
# class IepHtmlToPlain(HtmlToPlain):
    
#     def __init__(self, corpus_param):

#         HtmlToPlain.__init__(self, 'iep', corpus_param)

#     def clean(self, tree, name):
#         """
#         Takes an ElementTree object and a string (name of the
#         article) and returns the textual content of the article as a
#         list of strings.
#         """

#         root = tree.getroot()
#         article = self.get_body(root)

#         if article:
#             clr_toc(article)
#             self.clr_pubinfo(article)
#             self.clr_bib(article)
#             clr_sectnum(article)

#             proc_imgs(article)
#             clr_inline(article)
#             fill_par(article)
#             return flatten(article)
#         else:
#             return ''


#     def get_body(self, root):
#         """
#         Takes an Element object and returns a subtree containing only
#         the body of an IEP article.
#         """
#         for el in filter_by_tag(root.getiterator(), 'div'):
#             if el.get('class') == 'entry':
#                 return el
    
#         print '** Article body not found **'
#         return


#     #TODO: Rewrite in a functional style
#     def clr_pubinfo(self, elem):
#         """
#         Takes an Element object and removes nodes which are likely
#         candidates for the author info sections in the IEP.
#         """
#         cp = cp_map(elem)

#         hs = (filter_by_tag(elem.getiterator(), 'h1') +
#               filter_by_tag(elem.getiterator(), 'h2') +
#               filter_by_tag(elem.getiterator(), 'h3') +
#               filter_by_tag(elem.getiterator(), 'h4') +
#               filter_by_tag(elem.getiterator(), 'h5') +
#               filter_by_tag(elem.getiterator(), 'h6'))
    
#         for h in hs:
#             for el in h.getiterator() + [h]:
#                 if ((el.text and re.search(r'Author', el.text)) 
#                     or 
#                     (el.tail and re.search(r'Author', el.tail))):

#                     p = cp[h]
#                     i = list(p).index(h)

#                     for node in p[i:]:
#                         p.remove(node)
                    
#                     return

#         print '** Author Information not found. **'
#         return


#     #TODO: Rewrite in a functional style        
#     def clr_bib(self, elem):
#         """
#         Takes an Element object and removes nodes which are likely
#         candidates for the bibliographies in the IEP.
#         """
#         cp = cp_map(elem)

#         hs = (filter_by_tag(elem.getiterator(), 'h1') +
#               filter_by_tag(elem.getiterator(), 'h2') +
#               filter_by_tag(elem.getiterator(), 'h3') +
#               filter_by_tag(elem.getiterator(), 'h4') +
#               filter_by_tag(elem.getiterator(), 'h5') +
#               filter_by_tag(elem.getiterator(), 'h6'))
    
#         for h in hs:
#             for el in h.getiterator() + [h]:
#                 if ((el.text and 
#                      (re.search(r'Reference', el.text) 
#                       or re.search(r'Bibliograph', el.text))) 
#                     or (el.tail and 
#                         (re.search(r'Reference', el.tail) 
#                          or re.search(r'Bibliograph', el.tail)))):

#                     p = cp[h]
#                     i = list(p).index(h)
#                     for node in p[i:]:
#                         p.remove(node)
                        
#                     return
                
#         print '** Bibliography not found. **'
#         return



######################################################################
#                        ElementTree utilities
######################################################################


def pre_iter(t, tag=None):
    """
    Takes an Element, and optionally a tag name, and performs a
    preorder traversal and returns a list of nodes visited ordered
    accordingly.
    """
    return t.getiterator(tag)


def post_iter(t, tag=None):
    """
    Takes an Element object, and optionally a tag name, and
    performs a postorder traversal and returns a list of nodes
    visited ordered accordingly.
    """
    nodes = []

    for node in t._children:

        nodes.extend(post_iter(node, tag))

    if tag == "*":

        tag = None
        
    if tag is None or t.tag == tag:

        nodes.append(t)

    return nodes


def flatten(t):
    """
    Takes an Element and returns a list of strings, extracted
    from the text and tail attributes of the nodes in the
    tree, in a sensible order. 
    """
    pre = pre_iter(t)

    post = post_iter(t)

    out = [tag.text for tag in pre]

    i = 0

    for k,n in enumerate(post):

        j = pre.index(n) + k

        i = j if j > i else i + 1

        out.insert(i+1, n.tail)
            
    return [text for text in out if text]


def cp_map(tree):
    """
    Takes an Element object and returns a child:parent dictionary.
    """
    return dict((c, p) for p in tree.getiterator() for c in p)


def match_qname(local, qname):
    """
    Expects a tag name given as the local portion of a QName (e.g.,
    'h1') and matches it against a full QName.
    """
    return re.search('^\{.*\}' + local, qname)


def filter_by_tag(elems, tag):
    """
    Takes a list of Element objects and filters it by a local tag
    name (e.g., 'h1').
    """
    return [el for el in elems if match_qname(tag, el.tag)]


def get_prefix(t):
    """
    Takes an Element object and returns the prefix portion of the
    QName (its tag). For example, if t is XHTML, the QName may be
    'http://www.w3.org/1999/xhtml'. (A typical tag in t would be
    '{http://www.w3.org/1999/xhtml}div').
    """
    p = re.compile('^\{.*\}')

    m = re.search(p, t.tag)

    if m is None:

        return ''

    else:

        return m.group(0)


######################################################################
#   Generic HTML to plain text processing of an Elementree Object
######################################################################


def get_body(self, root):
    """
    Takes an Element object and returns a subtree containing only
    the body of an html document.
    """
    body = filter_by_tag(root.getiterator(), 'body')

    if len(body) != 1:

        raise Exception('Article body not found.')

    else:

        return body[0]



def clr_toc(elem):
    """
    Takes an Element object and removes any subtrees which are
    unordered or ordered lists of anchors. Such things are usually
    tables of contents.
    """
    cp = cp_map(elem)

    uls = filter_by_tag(elem.getiterator(), 'ul')

    ols = filter_by_tag(elem.getiterator(), 'ol')

    for l in ols[:] + uls[:]:

        if reduce(lambda v1, v2: v1 and v2,
                  [filter_by_tag(li.getiterator(), 'a') is not []
                   for li in filter_by_tag(l.getiterator(), 'li')]):

            cp[l].remove(l)

            return elem

    print '** TOC not found **'

    return elem



def clr_sectnum(elem):
    """
    Takes an Element object and removes text identifying section
    numbers.
    """
    hs = (filter_by_tag(elem.getiterator(), 'h1') +
          filter_by_tag(elem.getiterator(), 'h2') +
          filter_by_tag(elem.getiterator(), 'h3') +
          filter_by_tag(elem.getiterator(), 'h4') +
          filter_by_tag(elem.getiterator(), 'h5') +
          filter_by_tag(elem.getiterator(), 'h6'))
    
    n = re.compile('^[a-zA-Z ]*[0-9 \.]+ *')
    
    for h in hs:

        for el in h.getiterator() + [h]:

            if el.text:

                el.text = re.sub(n, '', el.text)

            elif el.tail:

                el.tail = re.sub(n, '', el.tail)
                
    return elem



def proc_imgs(elem):
    """
    Takes an Element object and removes img nodes or replaces them
    with div nodes containing the alt text.
    """
    imgs = filter_by_tag(elem.getiterator(), 'img')
    
    for img in imgs:

        alt = img.attrib['alt']

        if alt:

            img.tag = get_prefix(img) + 'div'

            img.text = alt

    return elem



def clr_inline(elem):
    """
    Takes an Element object, looks for nodes whose tags are xhmtl
    inline tags, and removes these nodes while appending the contents
    of their text and tail attributes in the appropriate places.
    """

    inline = ['b', 'em', 'i', 'tt', 'big', 'small', 'bdo',
              'strong', 'dfn', 'code', 'samp', 'kbd', 'var',
              'cite', 'span', 'font', 'sub', 'sup', 's',
              'strike', 'center', 'a', 'abbr', 'acronym',
              'u', 'br', 'del', 'ins', 'q']
    
    # Recall that text in xhtml documents will show up in two places
    # in an ElementTree Element Object: either in the text or in the
    # tail attribute. Suppose you have this chunk of html
    # '<p>real<em>foo</em>bar</p>'. The text attribute for the node
    # corresponding to the p tag has value 'real'. The text attribute
    # for the node corresponding to the em tag has value 'foo'. Where
    # should 'bar' go? In fact, the *tail* attribute of em stores
    # 'bar'.

    def clr(el, cp):

        for node in el[:]:

            clr(node, cp_map(cp[el]))

        if [inl for inl in inline if match_qname(inl, el.tag)]:

            i = list(cp[el]).index(el)

            if i == 0:

                # no left sibling

                if cp[el].text is None:

                    cp[el].text = ''

                if el.text:

                    cp[el].text = cp[el].text + el.text

                if el.tail:

                    cp[el].text = cp[el].text + el.tail

                cp[el].remove(el)

            else:

                # left sibling

                if cp[el][i-1].tail is None:

                    cp[el][i-1].tail = ''

                if el.text:

                    cp[el][i-1].tail = cp[el][i-1].tail + el.text

                if el.tail:

                    cp[el][i-1].tail = cp[el][i-1].tail + el.tail

                cp[el].remove(el)

        return
    
    for el in elem[:]:

        clr(el, cp_map(elem))

    return elem



def fill_par(elem):
    """
    Takes an Element object and removes extraneous spaces and line
    breaks from text and tail attributes.
    """
    els = elem.getiterator()
    
    sp = re.compile(' +')

    nl = re.compile('\n+')
    
    le = re.compile('^ +')

    tr = re.compile(' +$')
    
    for el in els[:]:

        if el.text:

            el.text = re.sub(nl, ' ', el.text)

            el.text = re.sub(sp, ' ', el.text)

            el.text = re.sub(le, '', el.text)

        if el.tail:

            el.tail = re.sub(nl, ' ', el.tail)

            el.tail = re.sub(sp, ' ', el.tail)

            el.tail = re.sub(tr, '', el.tail)
            
    return elem
