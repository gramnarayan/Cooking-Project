import os
import re
import httplib2
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    found_ingredient = False
    def handle_starttag(self, tag, attrs):
        for element in attrs:
            if element == ('class','floatleft itemUnit W420'):
                print "Found ingredient"
                self.found_ingredient = True

    def handle_data(self, data):
        if self.found_ingredient:
            # Assuming this data is the ingredients
            print "Ingredient: ", data
            self.found_ingredient = False

ingredients_dict = {}
recipe_repetitions = {} # key: recipe URL value: repetitions
h = httplib2.Http()

# The input and output files should be in the current directory.
input_recipes = os.path.join(os.curdir, 'recipes.txt')
input_fp = open(input_recipes, 'r')
input_file = input_fp.read()
# now we need to process the input_file to get the fields we want.
input_fp.close()
recipes_and_reps = re.split("\n", input_file)
for recipe_and_rep in recipes_and_reps:
    if recipe_and_rep == '': continue

    splitup_r_and_r = re.split(",", recipe_and_rep)
    recipe = splitup_r_and_r[0]
    reps = splitup_r_and_r[1]

    (response, content) = h.request(recipe, "GET")
    if response['status'] != '200':
        print "HTTP Response Status: %s" % response['status']
        print "Recipe: " + recipe + " does not exist."
        continue
    print content[:500] + "\n\n\n"

    parser = MyHTMLParser()
    parser.feed(content)

