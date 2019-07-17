import os
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

IDEAS_PER_REQUEST = 5