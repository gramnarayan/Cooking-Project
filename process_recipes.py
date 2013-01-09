import os
import re
import httplib2
import xml.etree.ElementTree as ET

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

    page_info = ET.parse(content)
    page_root = page_info.getroot()
    print "Root tag: %s" % page_root.tag
#    for child in page_root:
#        print "Tag: %s Attrib: %s" % (child.tag, child.attrib)
