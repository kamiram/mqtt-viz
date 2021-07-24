from . import user, sensors


def register_commands(app):
    user.register_commands(app)
    sensors.register_commands(app)