import os
import sys

sys.path.append(os.getcwd())

from Learning_Flask_Framework.Learning_Flask_Framework.app.main import db

if __name__ == '__main__':
    db.create_all()
