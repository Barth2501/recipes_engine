from utils.collection_processing import *
from utils.inverted_index import *


# Boolean model
collection = get_pre_processed_collection('./input/recipes.csv')
inverted_index = build_inverted_index_vextorial(collection, 4)
save_inverted_index_pickle(inverted_index, './indexes/index.txt')

# Vectorial model
recipes_df = load_data('./input/recipes.csv')
collection = get_pre_processed_collection('./input/recipes.csv')
inverted_index = build_inverted_index_vextorial(collection, recipes_df)
save_inverted_index_pickle(inverted_index, './indexes/index_numbered.txt')