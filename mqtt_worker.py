import json
from datetime import datetime

from flask_mqtt import Mqtt
from schema import Sensor

mqtt = Mqtt()


def init_worker(socketio, db):
    session = db.session

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        payload = json.loads(message.payload.decode())
        sensor = session.query(Sensor).filter_by(mqtt_label=payload['port']).first()
        if payload['value'] == 'OFF':
            timestamp = datetime.now().timestamp()
            sensor.cycle_active_time = timestamp - sensor.last_time
            sensor.last_time = timestamp
            session.commit()
            data = {
                'id': sensor.id,
                'cycle_active_time': sensor.cycle_active_time,
                'status_color': sensor.status_color,
                'status_blink': sensor.status_blink,
            }
            socketio.emit('message', data=data)

