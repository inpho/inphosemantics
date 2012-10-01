#TODO: Docstring
#TODO: Find way to end program between searching and importing phase. 

def corpus_client(search_term, disp_metadata=False):
    '''
    '''
    import re, os
    
    plain_corpora = ['dogs', 'cats', 'birds']
    #plain_corpora = plain_corpus_names()
    plain_corpora.sort()
    plain_corpora_index = {}
    num1 = range(len(plain_corpora))
    for i in num1:
	    plain_corpora_index[num1[i]+1]=plain_corpora[i]
   

    vsm_corpora = ['dogs', 'cats', 'birds', 'dogs-herding', 'cats-hypoallergenic', 'dogs-no_fur', 'dogs-American', 'cats-American', 'birds-tropical', 'birds-talking', 'cats-bengal']
    #vsm_corpora = vsm_corpus_names()
    vsm_corpora.sort()
    
    plain_corpus_name = ''
    while plain_corpus_name == '':	    
	    try:
	    	    search_term = int(search_term)
	    except ValueError:
		    pass
	    
	    if type(search_term) == int:
		    os.system('clear')
		    print 'Inphosemantics Corpus-Client'
		    print '============================'
		    print '\nSEARCH RESULTS'
		    print '=============='
		    print 'Index Number:', search_term
		    try:
			    plain_corpus_name = plain_corpora_index[search_term]
		    except KeyError:
			    print 'Call number out of range!'
		    else:
			    print search_term, plain_corpus_name
			    if disp_metadata:
				    print 'Metadata:', 'Testing...'
				    #print 'Metadata', corpus_metadata(plain_corpus_name)
			    else:
				    pass
			    break
	    elif type(search_term) == str:
		    hit = 0
		    os.system('clear')
		    print 'Inphosemantics Corpus-Client'
		    print '============================'
		    print '\nSEARCH RESULTS'
		    print '=============='
		    print 'Search Term:', search_term
		    for key, value in plain_corpora_index.iteritems():
			    if re.search(search_term, value) != None:
				    print key, value
				    if disp_metadata:
					    print 'Metadata:', 'Testing...'
					    #print 'Metadata:', corpus_metadata(value)
				    else:
					    pass
			    else:
				    hit = hit + 1
		    if hit == len(plain_corpora_index.keys()):
			    print 'Term not found!' 
	    else:
		    print 'Invalid input: Argument must be integer or string!'
	    
	    print '\n---------------'
	    print 'Enter call number or search term.'
	    print '[To end client, press "ctrl+d"]'
	    try:
		    new_search = raw_input()
	    except EOFError:
		    break
	    else:
		    new_search = re.sub(r'\s', '', new_search).split(',')
		    search_term = new_search[0]
		    try:
		    	    disp_metadata = new_search[1]
		    except IndexError:
		    	    disp_metadata = False


    if plain_corpus_name == '':
	    pass
    else:
	    num2 = 1
	    print '\nAVAILABLE MATRICES'
	    print '=================='
	    for i in vsm_corpora:
		    if re.search(plain_corpus_name, i) != None:
			    print num2, i
			    num2 = num2 + 1

