import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# configuration for the website
COMMENTS = os.path.join(BASE_PATH, "comments.sqlite")
DATABASE = os.path.join(BASE_PATH, "stacks.sqlite")
UNIT = "section"
DEPTH = 0

# configuration for the import
PATH = "book"
PAUX = "book.paux"
TAGS = "tags"
PDF = "book.pdf"

print("configuration.py loaded. BASE_PATH = {}".format(BASE_PATH))