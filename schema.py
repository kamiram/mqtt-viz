import enum

from sqlalchemy import MetaData, Column, Boolean, Integer, String, DateTime, ForeignKey, JSON, func, Enum, Float
from sqlalchemy.orm import declarative_base, relationship

from flask_bcrypt import generate_password_hash

metadata = MetaData()
base = declarative_base(metadata=metadata)


class FieldsInit:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super().__init__(*args, **kwargs)


class User(base, FieldsInit):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    username = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False, default='')

    @property
    def is_authenticated(self):
        return self.id is not None

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password).decode()

    def __str__(self):
        return f'{self.id}: {self.username}'


class SensorStatus:
    unknown = 0
    work = 1
    adjustment = 2
    smed = 3
    stop = 4
    fault = 5


class Sensor(base, FieldsInit):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False, default='')
    model = Column(String(50), nullable=False, default='')
    number = Column(Integer, nullable=False, default=0)
    product = Column(String(50), nullable=False, default='')
    pressform = Column(String(50), nullable=False, default='')
    cnt_sockets = Column(String(50), nullable=False, default='')
    active_sockets = Column(String(50), nullable=False, default='')
    cycle_time = Column(Float, nullable=False, default='0')
    cycle_active_time = Column(Float, nullable=False, default='0')
    last_time = Column(Float, nullable=False, default='0')
    status = Column(Integer, nullable=False, default=SensorStatus.unknown)
    mqtt_label = Column(Integer, nullable=False, default=0)

    @property
    def status_blink(self):
        if self.status == SensorStatus.work and self.cycle_active_time >= self.cycle_time * 2:
            return True
        return False

    @property
    def status_color(self):
        if self.status == SensorStatus.work:
            if self.cycle_active_time <= self.cycle_time * 1.2:
                return 'lightgreen'
            if self.cycle_active_time <= self.cycle_time * 2:
                return 'yellow'
            return 'yellow'
        if self.status == SensorStatus.adjustment:
            return 'orange'
        if self.status == SensorStatus.smed:
            return 'lightblue'
        if self.status == SensorStatus.stop:
            return 'silver'
        if self.status == SensorStatus.fault:
            return 'red'
        return 'plum'

    @property
    def cnt_sockets_extra(self):
        return f'{self.cnt_sockets}/{self.active_sockets}'

    @property
    def cycle_time_extra(self):
        return f'{self.cycle_time}/{self.cycle_active_time}'

    def __str__(self):
        return f'{self.id}: {self.model} - {self.product}'

