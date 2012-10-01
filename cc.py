#TODO: Docstring
#TODO: Find way to end program between searching and importing phase. 

def corpus_client(search_term, disp_metadata=False):
    '''
    '''
    #x = plain_corpus_names()
    x = ['dogs', 'cats', 'birds', 'dogs-herding', 'cats-hypoallergenic', 'dogs-no_fur', 'dogs-American', 'cats-American', 'birds-tropical', 'birds-talking', 'cats-bengal']
    import re, os

    x.sort()
    corpora_index = {}
    num = range(len(x))
    for i in num:
	    corpora_index[num[i]+1]=x[i]
   
    corpus_name = ''
    while corpus_name == '':	    
	    try:
	    	    search_term = int(search_term)
	    except ValueError:
		    pass
	    
	    if type(search_term) == int:
		    os.system('clear')
		    print 'Inphosemantics Corpus-Client'
		    print '============================'
		    print '\nSEARCH RESULTS'
		    print '==============='
		    print 'Search Term:', search_term
		    try:
			    corpus_name = corpora_index[search_term]
		    except KeyError:
			    print 'Call number out of range!'
		    else:
			    print search_term, corpus_name
			    if disp_metadata:
				    print 'Metadata', corpus_metadata(corpus_name)
			    else:
				    pass
			    break
	    elif type(search_term) == str:
		    hit = 0
		    os.system('clear')
		    print 'Inphosemantics Corpus-Client'
		    print '============================'
		    print '\nSEARCH RESULTS'
		    print '==============='
		    print 'Search Term:', search_term
		    for key, value in corpora_index.iteritems():
			    if re.search(search_term, value) != None:
				    print key, value
				    if disp_metadata:
					    print 'Metadata', corpus_metadata(value)
				    else:
					    pass
			    else:
				    hit = hit + 1
		    if hit == len(corpora_index.keys()):
			    print 'Term not found!' 
	    else:
		    print 'Invalid input: Argument must be integer or string!'
	    
	    print '\n---------------'
	    print 'Enter call number or search search_term.'
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
		    except KeyError:
		    	    pass
