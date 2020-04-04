from utils.collection_processing import *
from utils.inverted_index import *

collection = get_pre_processed_collection('./input/recipes.csv')
inverted_index = build_inverted_index(collection, 1)
save_inverted_index_pickle(inverted_index, './indexes/index.txt')
