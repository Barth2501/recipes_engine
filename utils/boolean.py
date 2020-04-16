import tt
from tt import BooleanExpression
import re
from nltk.tokenize import RegexpTokenizer

BooleanOperator = ['AND', 'OR', 'NOT']


def transformation_query_to_boolean(query):
    boolean_query = []
    for token in query.split():
        boolean_query.append(token)
        boolean_query.append('AND')
    boolean_query.pop()
    return boolean_query


def transformation_query_to_postfixe(query):
    b = BooleanExpression(query)
    return b.postfix_tokens


def remove_non_supported_tokens(query):
    filtered_query = []
    for token in query:
        if not (re.match(r"[0-9]+", token)) or re.match(r".*\..*"):
            filtered_query.append(token)
    return filtered_query


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


def boolean_transformation_query(query, inverted_index):
    tokenized_query = tokenize_query(query)
    filtered_query = remove_non_index_term(tokenized_query, inverted_index)
    filtered_query = remove_non_supported_tokens(filtered_query)
    boolean_query = ""
    for token in filtered_query:
        boolean_query += token
        boolean_query += " "
        boolean_query += "AND "
    boolean_query = boolean_query[:len(boolean_query) - 5]
    return transformation_query_to_postfixe(boolean_query)


def merge_and_postings_list(posting_term1, posting_term2):
    result = []
    i = 0
    j = 0
    n = len(posting_term1)
    m = len(posting_term2)
    while i < n and j < m:
        if posting_term1[i] == posting_term2[j]:
            result.append(posting_term1[i])
            i += 1
            j += 1
        elif posting_term1[i] < posting_term2[j]:
            i += 1
        else:
            j += 1
    return result


def merge_or_postings_list(posting_term1, posting_term2):
    result = []
    n = len(posting_term1)
    m = len(posting_term2)
    i = 0
    j = 0
    while i < n and j < m:
        if posting_term1[i] == posting_term2[j]:
            result.append(posting_term1[i])
            i = i+1
            j = j+1
        else:
            if posting_term1[i] < posting_term2[j]:
                result.append(posting_term1[i])
                i = i+1
            else:
                result.append(posting_term2[j])
                j = j+1
    if i < n - 1:
        for k in range(i, n):
            result.append(posting_term1[k])
    if j < m - 1:
        for k in range(j, m):
            result.append(posting_term2[k])
    return result


def merge_and_not_postings_list(posting_term1, posting_term2):
    result = []
    n = len(posting_term1)
    m = len(posting_term2)
    i = 0
    j = 0
    while i < n and j < m:
        if posting_term1[i] == posting_term2[j]:
            i = i+1
            j = j+1
        else:
            if posting_term1[i] < posting_term2[j]:
                result.append(posting_term1[i])
                i = i+1
            else:
                j += 1
    if i < n - 1:
        for k in range(i, n):
            result.append(posting_term1[k])
    return result


def boolean_operator_processing_with_inverted_index(BoolOperator, posting_term1, posting_term2):
    result = []
    if BoolOperator == "AND":
        result.append(merge_and_postings_list(posting_term1, posting_term2))
    elif BoolOperator == "OR":
        result.append(merge_or_postings_list(posting_term1, posting_term2))
    elif BoolOperator == "NOT":
        result.append(merge_and_not_postings_list(
            posting_term1, posting_term2))
    return result


# Traitement d'une requête booleenne

def processing_boolean_query_with_inverted_index(booleanOperator, query, inverted_index):
    try:
        query = boolean_transformation_query(query, inverted_index)
    except tt.errors.grammar.EmptyExpressionError:
        return []
    print(query)
    evaluation_stack = []
    for term in query:
        if term not in booleanOperator:
            evaluation_stack.append(inverted_index[term])
            print(term)
            print(inverted_index[term])
        else:
            if term.upper() == "NOT":
                operande = evaluation_stack.pop()
                eval_prop = boolean_operator_processing_with_inverted_index(
                    term, evaluation_stack.pop(), operande)
                evaluation_stack.append(eval_prop[0])
                evaluation_stack.append(eval_prop[0])
            else:
                operator = term
                eval_prop = boolean_operator_processing_with_inverted_index(
                    operator, evaluation_stack.pop(), evaluation_stack.pop())
                print(eval_prop)
                evaluation_stack.append(eval_prop[0])
    return evaluation_stack.pop()
