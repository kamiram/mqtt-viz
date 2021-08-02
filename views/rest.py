import json
from flask import request, current_app
from flask.views import View

from schema import Sensor, SensorProduct, SensorModel, SensorPressform


class JsonDataView(View):
    methods = ['POST', 'GET']

    def dispatch_request(self):
        text = request.form.get('text')
        app = current_app
        session = app.db.session
        query = session.query(Sensor)
        return app.response_class(
            response=json.dumps([sensor.as_dict() for sensor in query], indent=4),
            status=200,
            mimetype='application/json'
        )
