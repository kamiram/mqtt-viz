import flask_login
from flask_admin import Admin


class AdminViewMixin:
    create_modal = False
    edit_modal = False

    list_template = 'admin/list.html'
    edit_template = 'admin/edit.html'

    def is_accessible(self):
        return flask_login.current_user and getattr(flask_login.current_user, 'is_admin', False)


def register_admin(app):
    from .index import AdminIndexView
    from .user import UserAdminView
    from .sensors import SensorsAdminView

    admin = Admin(
        app,
        name='MQTT Viz', template_mode='bootstrap4',
        index_view=AdminIndexView(), base_template='admin/master.html'
    )

    admin.add_view(UserAdminView(app.db.session))
    admin.add_view(SensorsAdminView(app.db.session))
