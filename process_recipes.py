'''
Where we're at currently: ingredients from recipe.com are output to a file. However, what is difficult is actually multiplying the quantities by the number of repetitions we want. Suggestion: Find the "quantity" field for each ingredient, find any number in it and double it or whatever. 

Combining ingredients shared between recipes is another hard task -- this could perhaps be completed with a "common ingredients" input file and more regex searching.

Another thing to look into is providing a search functionality on major websites. We can search for an inquiry, provide the top 10 results numbered to the user, ask them to type one of the numbers or "0" for skip.
'''
import os
import re
import httplib2
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser

class RecipeComParser(HTMLParser):
    ingredients = []
    found_ingredient = False
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr == ('class','floatleft itemUnit W420'):
                print "Found ingredient"
                self.found_ingredient = True

    def handle_data(self, data):
        if self.found_ingredient:
            # Assuming this data is the ingredients
            print "Ingredient: ", data
            self.ingredients.append(data)
            self.found_ingredient = False


def read_input_file(input_fp):
    input_file = open(input_fp, 'r')
    input_data = input_file.read()
    input_file.close()
    return input_data

def get_recipe_page(recipe_url):
    h = httplib2.Http()
    (response, content) = h.request(recipe_url, "GET")
    if response['status'] != '200':
        print "HTTP Response Status: %s" % response['status']
        print "Recipe: " + recipe + " does not exist."
        raise httplib2.ServerNotFoundError("Could not find requested recipe")
    return content

def write_ingredients_to_file(recipe_ingredients_dict, output_fp):
    output_file = open(output_fp, 'w')
    for recipe in recipe_ingredients_dict.keys():
        output_file.write(recipe + ' x %s' % recipe_repetitions[recipe] + '\n')
        for ingredient in recipe_ingredients_dict[recipe]:
            output_file.write(ingredient + '\n')
    output_file.close()


recipes_and_ingredients = {}
recipe_repetitions = {} # key: recipe URL value: repetitions
input_recipes = os.path.join(os.curdir, 'recipes.txt')
output_ingredients = os.path.join(os.curdir, 'ingredients.txt')


# now we need to process the input_file to get the fields we want.
recipes_and_reps = re.split("\n", read_input_file(input_recipes))
for recipe_and_rep in recipes_and_reps:
    if recipe_and_rep == '': continue

    recipe_url = re.split(",", recipe_and_rep)[0]
    recipe_reps = re.split(",",recipe_and_rep)[1]
    
    recipe_repetitions[recipe_url] = recipe_reps

    try:
        content = get_recipe_page(recipe_url)
    except httplib2.ServerNotFoundError as e:
        print "Recipe URL: %s was not valid." % recipe_url
        print e.args
        continue

    recipe_parser = RecipeComParser()
    recipe_parser.feed(content)
    recipes_and_ingredients[recipe_url] = recipe_parser.ingredients

write_ingredients_to_file(recipes_and_ingredients, output_ingredients)

