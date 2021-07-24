import flask
from flask_bcrypt import check_password_hash
from wtforms import Form, validators, PasswordField, StringField

from schema import User


class LoginForm(Form):
    login = StringField(validators=[validators.required()], label='Логин')
    password = PasswordField(validators=[validators.required()], label='Пароль')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Неверный пользователь')

        if not check_password_hash(user.password, self.password.data.encode('utf-8')):
            raise validators.ValidationError('Неверный пароль')

    def get_user(self):
        db = flask.current_app.db
        return db.session.query(User).filter_by(username=self.login.data).first()
