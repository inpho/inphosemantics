"""
TODO: Help the user!

"""

#TODO: Install and import vsm (and tell the user to do it as well)

#Just a test comment. nothing to see here
print 'Welcome to InPhO Semantics!'

import inphosemantics


def available_corpora():
    """
    """
    corpora = request_corpora()

    print corpora




def cheatsheet():
    """
    """
    return



######################################################################
#                              Backend
######################################################################


def request_corpora():

    corpora = ['sep', 'iep', 'philpapers']

    return corpora
