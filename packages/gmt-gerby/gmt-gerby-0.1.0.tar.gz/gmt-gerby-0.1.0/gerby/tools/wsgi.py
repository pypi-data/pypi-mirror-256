import sys
import os

#PATH = os.getcwd() + '/..'
#sys.path.append(PATH)
#sys.path.append(".")

from gerby.application import app

#os.chdir(PATH)

if __name__ == "__main__":
    app.run()
