
from sqlalchemy import MetaData, Column, Boolean, Integer, String, ForeignKey, Float
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
    names = {
        0: 'Неизвестно',
        1: 'Работает',
        2: 'Наладка',
        3: 'smed',
        4: 'Остановлено',
        5: 'Сбой',
    }
    unknown = 0
    work = 1
    adjustment = 2
    smed = 3
    stop = 4
    fault = 5


class SensorModel(base, FieldsInit):
    __tablename__ = 'sensor_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class SensorProduct(base, FieldsInit):
    __tablename__ = 'sensor_product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class SensorPressform(base, FieldsInit):
    __tablename__ = 'sensor_pressform'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class Sensor(base, FieldsInit):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False, default='')
    model_id = Column(Integer, ForeignKey('sensor_model.id'), index=True, nullable=True)
    model = relationship(SensorModel)
    product_id = Column(Integer, ForeignKey('sensor_product.id'), index=True, nullable=True)
    product = relationship('SensorProduct')
    pressform_id = Column(Integer, ForeignKey('sensor_pressform.id'), index=True, nullable=True)
    pressform = relationship(SensorPressform)
    number = Column(Integer, nullable=False, default=0)
    cnt_sockets = Column(String(50), nullable=False, default='')
    active_sockets = Column(String(50), nullable=False, default='')
    cycle_time = Column(Float, nullable=False, default='0')
    status = Column(Integer, nullable=False, default=SensorStatus.unknown)
    mqtt_label = Column(Integer, nullable=False, default=0)

    @property
    def status_name(self):
        return SensorStatus.names.get(self.status, '')

    @property
    def status_color(self):
        if self.status == SensorStatus.work:
            return 'gray'
        if self.status == SensorStatus.adjustment:
            return 'orange'
        if self.status == SensorStatus.smed:
            return 'blue'
        if self.status == SensorStatus.stop:
            return 'gray'
        if self.status == SensorStatus.fault:
            return 'red'
        return 'unknown'

    @property
    def cnt_sockets_extra(self):
        return f'{self.cnt_sockets}/{self.active_sockets}'

    @property
    def cycle_time_extra(self):
        return f'{self.cycle_time}/{self.cycle_active_time}'

    def __str__(self):
        return f'{self.id}: {self.model} - {self.product}'

    dict_fields = [
        'id', 'type', 'model', 'product', 'pressform', 'number',
        'cnt_sockets', 'active_sockets', 'status_color', 'cycle_time',
    ]

    def as_dict(self):
        def value(v):
            if type(v) is float:
                return str(round(v, 2))
            return str(v)
        return {field: value(getattr(self, field, '')) for field in self.dict_fields}
