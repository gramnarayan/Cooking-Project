Cooking-Project
===============
Input: Text file where each line contains URL to recipe on recipe.com, number of repetitions (can be non-integer number) comma-separated.
Output: Ingredients in all collective recipes in input file, with number of ingredients.

Basic outline:
First, we want to parse our input file and get all the URL's and the repetitions associated with them. We then submit an HTTP GET request to the URL to get it's webdata in XML format. Then we process the XML to get the ingredients (this might be easiest by convertin into a python dictionary, but not sure. TODO: Look into python's handling of XML files). We then put ingredients in a dictionary with the number of repetitions, and output the dictionary in a text file.

What would be nice going into the future:
- Integrate parsing for multiple websites, which gives a functionality not on any specific website
- Have a search for key terms rather than specifying the URL, with maybe number of servings desired rather than number of repetitions of the recipe (will require parsing to figure out number of servings in the recipe as written as well).