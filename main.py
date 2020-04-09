import re
from absl import app, flags

from utils.collection_processing import *
# from utils.boolean import *
from utils.inverted_index import *
from utils.vectorial import *


def find_recipes(arg):
    
    if FLAGS.model == 'boolean':
        recipes_df = load_data('./input/recipes.csv')
        inverted_index = load_inverted_index_pickle('./indexes/index.txt')
        result = processing_boolean_query_with_inverted_index(
            BooleanOperator, FLAGS.query, inverted_index)
        print(recipes_df[recipes_df['id'].isin(result)])

    elif FLAGS.model == 'vectorial':
        recipes_df = load_data('./input/recipes.csv')
        inverted_index = load_inverted_index_pickle('./indexes/index_numbered.txt')
        result = vectorial_search(inverted_index,FLAGS.query,recipes_df.shape[0])
        print(result)


if __name__ == "__main__":

    FLAGS = flags.FLAGS
    flags.DEFINE_string('query', '', 'Ingredients you want to look for')
    flags.DEFINE_string('model', 'boolean', 'Model used for the search')

    app.run(find_recipes)
