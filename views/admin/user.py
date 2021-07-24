from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField

from schema import User
from . import AdminViewMixin


class UserAdminView(AdminViewMixin, ModelView):
    column_list = ['is_active', 'is_admin', 'username', ]
    form_columns = ['is_active', 'is_admin', 'username', 'newpassword']

    column_default_sort = 'username'
    column_editable_list = ['is_active', ]
    column_searchable_list = ['username', ]
    column_filters_list = ['is_active', 'is_admin', ]

    column_labels = {
        'is_active': 'Акт.',
        'is_admin': 'Админ',
        'username': 'Имя пользователя',
        }

    form_excluded_columns = ['password', ]
    form_extra_fields = {
        'newpassword': PasswordField('Новый пароль'),
    }
    form_widget_args = {
        'password': {
            'required': False,
        },
    }

    def on_model_change(self, form, model, is_created):
        if form.newpassword.data is not None:
            model.set_password(form.newpassword.data)
        else:
            del form.password

    def __init__(self, session, *args, **kwargs):
        super().__init__(User, session, name='Пользователи', *args, **kwargs)
