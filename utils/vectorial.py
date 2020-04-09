
def vectorial_search(inverted_index, query, nb_doc):
    query = query.upper()
    query = query.split(' ')
    result = {}
    norm_factor_q = 0
    for term in query:
        weigth_q = 1
        norm_factor_q += 1
        if term in inverted_index.keys():
            for document,weigth_doc,norm_factor in inverted_index[term]:
                if document in result.keys():
                    result[document] += weigth_doc*weigth_q/(norm_factor)**(0.5)
                else:
                    result[document] = weigth_doc*weigth_q/(norm_factor)**(0.5)
    
    ordered_list = [[key,result[key]] for key in result.keys()]
    return sorted(ordered_list, key=lambda x: x[1], reverse=True)
    