from flask_admin.contrib.sqla import ModelView

from schema import SensorProduct
from . import AdminViewMixin


class SensorsProductAdminView(AdminViewMixin, ModelView):
    column_list = [
        'id', 'name',
    ]

    column_default_sort = 'name'
    column_editable_list = ['name']

    column_labels = {
        'id': 'Номер',
        'name': 'Название'
    }

    def __init__(self, session, *args, **kwargs):
        super().__init__(SensorProduct, session, name='Продукты', *args, **kwargs)
