import os
import re
import httplib2
import xml.etree.ElementTree as ET

# The input and output files should be in the current directory.
input_fp = os.path.join(os.curdir, 'recipes.txt')
input_file = open(input_fp, 'r')
print input_file
