import re
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict


def remove_non_index_term(query, inverted_index):
    query_filt = []
    for token in query:
        if token in inverted_index:
            query_filt.append(token)
    return query_filt


def tokenize_query(query):
    tokenized_query = []
    tokenizer = RegexpTokenizer(r'(\w+)')
    tokens = tokenizer.tokenize(query)
    for token in tokens:
        if not re.match(r'.*\d+.*', token):
            tokenized_query.append(token.upper())
    return tokenized_query


def query_transformation(query, inverted_index):
    tokenized_query = tokenize_query(query)
    filtered_query = remove_non_index_term(tokenized_query, inverted_index)
    return filtered_query


def vectorial_search(inverted_index, query, nb_doc):
    query = query_transformation(query, inverted_index)
    relevant_recipes = {}
    for term in query:
        weigth_q = 1
        if term in inverted_index:
            for document, weigth_doc, norm_factor in inverted_index[term]:
                if document in relevant_recipes:
                    relevant_recipes[document] += weigth_doc * \
                        weigth_q/(norm_factor)**(0.5)
                else:
                    relevant_recipes[document] = weigth_doc * \
                        weigth_q/(norm_factor)**(0.5)
    ordered_relevant_recipees = OrderedDict(
        sorted(relevant_recipes.items(), key=lambda t: t[1], reverse=True))
    return ordered_relevant_recipees
