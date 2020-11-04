import os

from cluedo import AppConfig

basedir = os.path.abspath(os.path.dirname(__file__))

# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
FLASK_ADMIN_SWATCH = 'superhero'

# Create dummy secrey key so we can use sessions
# TODO add in config file
SECRET_KEY = '123456790'

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = AppConfig.sql_alchemy_conn

# Flask-WTF flag for CSRF
CSRF_ENABLED = True