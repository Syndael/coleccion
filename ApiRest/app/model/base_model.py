from marshmallow import Schema
from app.utils.datos import db


class Base(db.Model):
    __tablename__ = 'BASE'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    saga = db.Column(db.String(255))
    fecha_salida = db.Column(db.Date)

    def __init__(self, nombre, saga=None, fecha_salida=None):
        self.nombre = nombre
        self.saga = saga
        self.fecha_salida = fecha_salida


class BaseSchema(Schema):
    class Meta:
        fields = ('id', 'nombre', 'saga', 'fecha_salida')
        include_relationships = True