import os

from flask import Flask
from flask import render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.base import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from cluedo import AppConfig

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(AppConfig.flask_config_path, silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/ping')
    def ping():
        return 'alive!'

    
    from cluedo.www import data
    app.register_blueprint(data.bp)

    with app.app_context():
        admin = Admin(app, name='Cluedo | Sample', template_mode='bootstrap3')

        from cluedo import models

        # Models managed by this app Cluedo package flask app
        admin.add_sub_category(name="Cluedo", parent_name="Cluedo")
        admin.add_view(ModelView(models.Article, db.session, category="Cluedo"))
        admin.add_view(ModelView(models.Filetrack, db.session, category="Cluedo"))

        # Additional links
        admin.add_sub_category(name="Links", parent_name="Other")
        admin.add_link(MenuLink(name='Back Home', url='/', category='Links'))

    return app