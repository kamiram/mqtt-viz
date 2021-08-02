from flask import jsonify, current_app
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

from schema import Sensor, SensorStatus
from . import AdminViewMixin


class SensorsAdminView(AdminViewMixin, ModelView):
    column_list = [
        # 'type', 'model', 'number', 'product', 'pressform', 'cnt_sockets_extra', 'status', 'mqtt_label',
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
        'pressform': 'Пресс-форма',
        'cnt_sockets': 'Кол-во гнёзд',
        'active_sockets': 'Акт. кол-во гнёзд',
        'cycle_time': 'Время цикла',
        'cycle_active_time': 'Акт.время цикла',
        'cycle_time_extra': 'Время цикла',
        'cnt_sockets_extra': 'Разъемы',
        'status': 'Статус',
        'mqtt_label': 'Имя топика MQTT',
    }

    form_choices = {
        # 'status': [(k, v) for k, v in SensorStatus.names.items()]
    }

    def __init__(self, session, *args, **kwargs):
        super().__init__(Sensor, session, name='Оборудование', *args, **kwargs)

    def after_model_change(self, form, model, is_created):
        data = {field: getattr(model, field) for field in self.column_labels.keys()}
        data['id'] = model.id
        print(data)
        current_app.socketio.emit('message', data=data)
