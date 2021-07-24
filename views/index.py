import flask
from flask import current_app
from flask.views import View

from schema import Sensor


class IndexView(View):

    def dispatch_request(self):
        session = current_app.db.session
        sensors = session.query(Sensor)

        return flask.render_template('index.html', sensors=sensors, config=current_app.config)
