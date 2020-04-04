import collections

def count_frequency(collection,n):
    # A completer
    words = []
    for key in collection.keys():
        counter = collections.Counter(collection[key])
        words += collection[key]
    counter = collections.Counter(words)
    important_list = []
    for element in sorted(list(counter.items()), key=lambda x:x[1], reverse=True):
        if len(important_list) > n:
            break
        else:
            important_list.append(element[0])
    return important_list

def remove_stop_words(collection ,stop_word_file):
    # TO COMPLETE
    new_collection = {}
    for key in collection.keys():
        new_collection[key] = []
        for word in collection[key]:
            if word not in stop_word_file:
                new_collection[key].append(word)
    return new_collection

def build_inverted_index(collection,type_index):
    # On considère ici que la collection est pré-traitée
    inverted_index={}
    if type_index == 1:
        for document in collection:
            for term in collection[document]:
                if term in inverted_index.keys():
                    if document not in inverted_index[term]:
                        inverted_index[term].append(document)
                else:
                    inverted_index[term]=[document]
    elif type_index ==2:
        for document in collection:
            for term in collection[document]:
                if term in inverted_index.keys():
                    if document in inverted_index[term].keys():
                        inverted_index[term][document] = inverted_index[term][document] + 1
                    else:
                        inverted_index[term][document]= 1
                else:
                    inverted_index[term]={}
                    inverted_index[term][document]=1
    elif type_index==3:
        for document in collection:
            n=0
            for term in collection[document]:
                n = n+1
                if term in inverted_index.keys():
                    if document in inverted_index[term].keys():
                        inverted_index[term][document][0] = inverted_index[term][document][0] + 1
                        inverted_index[term][document][1].append(n)
                    else:
                        inverted_index[term][document]= [1,[n]]
                else:
                    inverted_index[term] = {}
                    inverted_index[term][document]=[1,[n]]
                    
    return inverted_index

BooleanOperator = ['AND', 'OR', 'NOT']

def term_incidence_vector(term,matrix,nb_doc):
    # a completer
    vector = [0 for i in range(nb_doc)]
    for doc_nb in matrix[term]:
        vector[doc_nb]=1
    return vector

def query_reformat(query):
    processed_query=[]
    # a completer
    processed_query = query.split(' ')
    return processed_query

def boolean_operator_processing(BoolOperator,term1,term2):
    result=[]
    if BoolOperator == "AND":
        for a , b in zip(term1,term2) :
            if a==1 and b==1 :
                result.append(1)
            else :
                result.append(0)
    elif BoolOperator=="OR" :
        for a,b in zip(term1,term2)  :
            if a==0 and b==0 :
                result.append(0)
            else :
                result.append(1)
    elif BoolOperator == "NOT":
        for b in term1 :
            if b == 1 :
                result.append(0)
            else :
                result.append(1)
    return result

def query_processing(term_incidence_matrix, query, corpus):
    # A completer.
    query = query_reformat(query)
    for i,word in enumerate(query):
        if word not in BooleanOperator:
            vector = term_incidence_vector(word,term_incidence_matrix,len(corpus))
            query[i]=vector
    result = query.pop(0)
    while query != []:
        next_term = query.pop(0)
        if next_term in BooleanOperator:
            v2 = query.pop(0)
            if v2 != 'NOT':
                result = boolean_operator_processing(next_term,result,v2)
            else:
                v3 = query.pop(0)
                inter_result = boolean_operator_processing(v2,v3,[])
                result = boolean_operator_processing(next_term,result,inter_result)
    return result

def search_docs(result):
    doc_list = []
    for i,doc in enumerate(result):
        if doc == 1:
            doc_list.append(i)
    return doc_list
