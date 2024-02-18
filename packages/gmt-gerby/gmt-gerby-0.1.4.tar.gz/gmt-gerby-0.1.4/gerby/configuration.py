import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

DATABASE_PATH = os.environ.get("DATABASE_PATH", BASE_PATH)

# configuration for the website
COMMENTS = os.path.join(DATABASE_PATH, "comments.sqlite")
DATABASE = os.path.join(DATABASE_PATH, "db.sqlite")
UNIT = "section"
DEPTH = 0

# branding
PROJECT_TITLE = os.environ.get("PROJECT_TITLE", "A Gerby Project")
PROJECT_DESCRIPTION = os.environ.get("PROJECT_DESCRIPTION", "This should be replaced with a short description of the project")

# configuration for the import
PATH = "book"
PAUX = "book.paux"
TAGS = "tags"
PDF = "book.pdf"

print("configuration.py loaded. DATABASE_PATH: {}".format(DATABASE_PATH))

if not os.path.exists(DATABASE):
    raise Exception("database {} does not exist".format(DATABASE))

if not os.path.exists(COMMENTS):
    print("comments database {} does not exist".format(COMMENTS))

