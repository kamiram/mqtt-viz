import json

import flask
from flask_admin.contrib.sqla import ModelView
import requests

from schema import Sensor, SensorStatus
from . import AdminViewMixin


def emit_sensor_update(data):
    @flask.after_this_request
    def emit_data(response):
        response.headers['X-SocketIO-Emit-SensorUpdate'] = json.dumps(data)
        return response


class SensorsAdminView(AdminViewMixin, ModelView):
    column_list = [
        'type', 'model', 'number', 'product', 'pressform', 'cnt_sockets_extra', 'cycle_time', 'status_name', 'mqtt_label',
    ]
    # form_columns = ['is_active', 'is_admin', 'username', 'newpassword']

    column_default_sort = 'number'
    column_editable_list = [ ]
    # column_searchable_list = ['model', 'product', ]

    column_labels = {
        'type': 'Тип',
        'model': 'Модель',
        'number': 'Номер',
        'product': 'Продукт',
        'pressform': 'Прессформа',
        'cnt_sockets': 'Кол-во гнёзд',
        'active_sockets': 'Акт. кол-во гнёзд',
        'cycle_time': 'Время цикла',
        'cnt_sockets_extra': 'Разъемы',
        'status': 'Статус',
        'status_name': 'Статус',
        'mqtt_label': 'MQTT',
    }

    form_choices = {
        'status': [(k, v) for k, v in SensorStatus.names.items()]
    }

    def __init__(self, session, *args, **kwargs):
        super().__init__(Sensor, session, name='Оборудование', *args, **kwargs)

    def after_model_change(self, form, model, is_created):
        emit_sensor_update(model.as_dict())
        # requests.post(flask.current_app.config['SOCKET_SERVER_URL'] + 'update_sensor', data=model.as_dict())

