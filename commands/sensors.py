from pathlib import Path

import click
from flask import current_app
from flask.cli import AppGroup
import csv

from schema import Sensor, SensorModel, SensorProduct, SensorPressform


def register_commands(app):
    sensors_cli = AppGroup('sensors', help='Work with sensors.')

    @sensors_cli.command('import', help='Import from CSV file.', with_appcontext=True)
    @click.argument('filename')
    def sensors_import(filename):
        session = current_app.db.session

        with open(Path.cwd() / 'data' / 'model.txt', newline='') as f:
            items = f.readlines()
        for item in items:
            model = SensorModel(name=item.strip(' \n\r\t'))
            session.add(model)

        with open(Path.cwd() / 'data' / 'product.txt', newline='') as f:
            items = f.readlines()
        for item in items:
            record = SensorProduct(name=item.strip(' \n\r\t'))
            session.add(record)

        with open(Path.cwd() / 'data' / 'pressform.txt', newline='') as f:
            items = f.readlines()
        for item in items:
            record = SensorPressform(name=item.strip(' \n\r\t'))
            session.add(record)
        session.commit()

        models = {item.id: item.name for item in session.query(SensorModel)}
        products = {item.id: item.name for item in session.query(SensorProduct)}
        pressforms = {item.id: item.name for item in session.query(SensorPressform)}

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile,  )
            for row in reader:
                sensor = Sensor()
                model, sensor.number, product, pressform, \
                sensor.cnt_sockets, sensor.active_sockets, \
                status, sensor.mqtt_label, = row
                f_flag = 0
                for k, v in models.items():
                    if v == model.strip(' \n\r\t'):
                        sensor.model_id = k
                        f_flag += 1
                        break
                for k, v in products.items():
                    if v == product.strip(' \n\r\t'):
                        sensor.product_id = k
                        f_flag += 1
                        break
                for k, v in pressforms.items():
                    if v == pressform.strip(' \n\r\t'):
                        sensor.pressform_id = k
                        f_flag += 1
                        break
                if True or f_flag == 3:
                    session.add(sensor)
        session.commit()
    app.cli.add_command(sensors_cli)
