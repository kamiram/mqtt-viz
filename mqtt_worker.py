from flask import current_app
from flask_mqtt import Mqtt
mqtt = Mqtt()



@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # current_app.socketio.emit('mqtt_message', data=data)
