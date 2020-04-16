# Recipes search engine

This search engine allows you to find recipes based on the ingredients in your query.

# How to use it

In order to perform a search, you have to run the main file with the command
`python main.py`

To enter a query, use the arg -query and sepratae your ingredients with commas. For instance, the following command will perform a search for recipes containings the ingredients tomates and courgettes.

`python main.py -query=tomates,courgettes`

There are two models available to perform the search that can be chosen with the flag -model. The default model is boolean. By using this model, you will get as result of your query the recipes containing all of the ingredients in your query. You can also use the **vectorial** model with `-model=vectorial`. You will get an ordered list of recipes, the first ones being the ones that match the better your query. For instance, the following command will perform a search for recipes with ingredients tomates and courgettes using the vectorial model :
`python main.py -query=tomates,courgettes -model=vectorial`
