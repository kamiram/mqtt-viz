import json

from flask import Flask
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

from schema import metadata, User, Sensor
from views.admin import register_admin

from views.index import IndexView
from views.rest import JsonDataView
from commands import register_commands


def create_app():
    app = Flask(__name__)
    app.app_context().push()
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config_local.py')
    app.url_map.host_matching = False

    db = SQLAlchemy(app, metadata=metadata)
    app.db = db

    babel = Babel(app)

    cors = CORS(app)

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
    app.add_url_rule('/data.json', view_func=JsonDataView.as_view('data.json'))

    register_admin(app)
    register_commands(app)
    return app

