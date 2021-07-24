import flask
from flask import current_app
from flask.views import View


class IndexView(View):
    def dispatch_request(self):
        return flask.render_template('index.html', )

    @current_app.mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        current_app.socketio.emit('mqtt_message', data=data)
