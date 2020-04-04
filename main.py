import pandas as pd
import re
from absl import app,flags

from utils.search_engine import *


def find_recipes(arg):

    recipes_df = pd.read_csv('./input/recipes.csv', header=None, usecols=[0,1,2,5],names=['id','name','ingredients','category_id'])

    def replace(x):
        res = x.copy()
        if x.isna()['ingredients']:
            res['ingredients']=x['name']
        return res

    recipes_df = recipes_df.apply(replace, axis=1)

    corpus = {}
    for i,recipe in enumerate(recipes_df.itertuples()):
        corpus[recipe.id] = []
        ingredients = recipe.ingredients.split(',')
        for ingredient in ingredients:
            numbers_list = re.findall(r'[0-9]+',ingredient)
            numbers_list += ['-','/',',','(',')',"'"]
            for nbr in numbers_list:
                ingredient = ingredient.replace(nbr,' ')
            ingredient = ingredient.strip()
            corpus[recipe.id] += ingredient.split(' ')
    stop_words = count_frequency(corpus, 35)
    corpus = remove_stop_words(corpus, stop_words)
    inv_index = build_inverted_index(corpus,1)
    
    result = query_processing(inv_index, FLAGS.query, corpus)
    docs = search_docs(result)
    print(recipes_df[recipes_df['id'].isin(docs)])

if __name__ == "__main__":

    FLAGS = flags.FLAGS
    flags.DEFINE_string('query','','Ingredients you want to look for')

    app.run(find_recipes)