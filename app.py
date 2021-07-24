import json

from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from schema import metadata, User
from views.admin import register_admin

from views.admin.index import AdminIndexView
from views.index import IndexView

from commands import register_commands


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config_local.py')
    with open('config.json') as file:
        app.config['MQTT'] = json.loads(file.read())
    app.url_map.host_matching = False

    db = SQLAlchemy(app, metadata=metadata)

    app.db = db

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'ru'

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    bootstrap = Bootstrap(app)

    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/index.html', view_func=IndexView.as_view('index.html'))

    register_admin(app)
    register_commands(app)
    return app
