import os
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'flaskr.db'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_precious'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# database config
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False

IDEAS_PER_REQUEST = 5