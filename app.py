import json

import eventlet
from flask import Flask
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_cors import CORS

from schema import metadata, User, Sensor
from views.admin import register_admin

from views.index import IndexView
import mqtt_worker
from commands import register_commands

eventlet.monkey_patch()

def create_app():
    app = Flask(__name__)
    app.app_context().push()
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config_local.py')
    with open('config.json') as file:
        app.config['MQTT'] = json.loads(file.read())
    app.url_map.host_matching = False

    app.config['MQTT_BROKER_URL'] = app.config['MQTT']['mqtt']['host']
    app.config['MQTT_BROKER_PORT'] = app.config['MQTT']['mqtt']['port']
    app.config['MQTT_USERNAME'] = app.config['MQTT']['mqtt']['username']
    app.config['MQTT_PASSWORD'] = app.config['MQTT']['mqtt']['password']
    app.config['MQTT_KEEPALIVE'] = 5
    app.config['MQTT_TLS_ENABLED'] = False

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

    socketio = SocketIO(app, cors_allowed_origins="*",  async_handlers=True, pingTimeout=500, )
    app.socketio = socketio

    @app.before_first_request
    def init_mqtt():
        mqtt_worker.init_worker(socketio, db)

    bootstrap = Bootstrap(app)

    mqtt_worker.mqtt.init_app(app)
    app.mqtt = mqtt_worker.mqtt

    topic = app.config['MQTT']['mqtt']['topic']
    for sensor in db.session.query(Sensor):
        print(f'subscribe to "{topic}/{sensor.mqtt_label}"')
        mqtt_worker.mqtt.subscribe(f'{topic}/{sensor.mqtt_label}')

    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/index.html', view_func=IndexView.as_view('index.html'))

    register_admin(app)
    register_commands(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.socketio.run(app, use_reloader=False, debug=True)

