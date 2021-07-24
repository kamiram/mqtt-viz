from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

from schema import Sensor
from . import AdminViewMixin


class SensorsAdminView(AdminViewMixin, ModelView):
    column_list = [
        'type', 'model', 'number', 'product', 'pressform', 'cnt_sockets_extra',
        'cyrcle_time_extra', 'status', 'mqtt_label',
    ]
    # form_columns = ['is_active', 'is_admin', 'username', 'newpassword']

    column_default_sort = 'number'
    column_editable_list = [ ]
    column_searchable_list = ['model', 'product', ]

    column_labels = {
        'type': 'Тип',
        'model': 'Модель',
        'number': 'Номер',
        'product': 'Продукт',
        'pressform': 'Пресс-форма',
        'cnt_sockets': 'Кол-во гнёзд',
        'active_sockets': 'Акт. кол-во гнёзд',
        'cyrcle_time': 'Время цикла',
        'cyrcle_active_time': 'Акт.время цикла',
        'cyrcle_time_extra': 'Время цикла',
        'cnt_sockets_extra': 'Разъемы',
        'status': 'Статус',
        'mqtt_label': 'Имя топика MQTT',
    }

    def __init__(self, session, *args, **kwargs):
        super().__init__(Sensor, session, name='Датчики', *args, **kwargs)
