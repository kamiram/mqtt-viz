import click
from flask import current_app
from flask.cli import AppGroup
from sqlalchemy import select

from schema import User


def register_commands(app):
    user_cli = AppGroup('user', help='Create, change password and set admin state.')

    @user_cli.command('create', help='Create user.', with_appcontext=True)
    def user_create():
        username = click.prompt('Username')
        password1 = click.prompt('Password')
        password2 = click.prompt('Password again')
        if len(password1) < 4:
            print('Password too short.')
            return
        if password1 != password2:
            print('Password2 is not equal password1.')
            return
        is_admin = click.confirm('Is administrator?')

        db = current_app.db
        user = User(username=username, is_admin=is_admin)
        user.set_password(password1)
        db.session.add(user)
        db.session.commit()

    @user_cli.command('password', help='Change user password.', with_appcontext=True)
    @click.argument('username')
    def user_password(username):
        db = current_app.db

        user = db.session.execute(select(User).filter_by(username=username)).scalar_one()
        if user is None:
            print(f'User "{username} does not exists.')
            return

        password1 = click.prompt('Password')
        password2 = click.prompt('Password again')
        if len(password1) < 4:
            print('Password too short.')
            return
        if password1 != password2:
            print('Password2 is not equal password1.')
            return

        user.set_password(password1)
        db.session.commit()

    @user_cli.command('admin', help='Change admin state.', with_appcontext=True)
    @click.argument('username')
    def user_admin(username):
        db = current_app.db
        user = db.session.execute(select(User).filter_by(username=username)).scalar_one()
        if user is None:
            print(f'User "{username} does not exists.')
            return
        is_admin = click.confirm('Is administrator?')

        user.is_admin = is_admin
        db.session.commit()

    app.cli.add_command(user_cli)
