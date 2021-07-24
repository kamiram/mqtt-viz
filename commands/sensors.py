import json
from time import sleep

import click
import flask
from flask import current_app
from flask.cli import AppGroup
import csv

from schema import Sensor


def register_commands(app):
    sensors_cli = AppGroup('sensors', help='Work with sensors.')

    @sensors_cli.command('import', help='Import from CSV file.', with_appcontext=True)
    @click.argument('filename')
    def sensors_import(filename):
        db = current_app.db
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile,  )
            for row in reader:
                sensor = Sensor()
                sensor.model, sensor.number, sensor.product, sensor.pressform, \
                sensor.cnt_sockets, sensor.active_sockets, \
                status, sensor.mqtt_label, = row
                db.session.add(sensor)
        db.session.commit()
    app.cli.add_command(sensors_cli)

    @sensors_cli.command('scan', help='Test sensors scan.', with_appcontext=True)
    def sensors_import():
        mqtt = flask.current_app.mqtt

        @mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            print(message.topic)
            print(json.dumps(json.loads(message.payload.decode()), indent=4))

        print('Precc Ctrl-C for exit')
        while True:
            sleep(0.1)

    app.cli.add_command(sensors_cli)
