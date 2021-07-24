import flask
import flask_admin
import flask_login

from views.admin.auth import LoginForm


class AdminIndexView(flask_admin.AdminIndexView):

    @flask_admin.expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return flask.redirect(flask.url_for('.login_view'))
        return super().index()

    @flask_admin.expose('/login/', methods=('GET', 'POST'))
    def login_view(self):

        form = LoginForm(flask.request.form)
        if flask_admin.helpers.validate_form_on_submit(form):
            user = form.get_user()
            flask_login.login_user(user)

        if flask_login.current_user.is_authenticated:
            return flask.redirect(flask.url_for('.index'))

        self._template_args['form'] = form
        return super().index()

    @flask_admin.expose('/logout/')
    def logout_view(self):
        flask_login.logout_user()
        return flask.redirect(flask.url_for('.index'))