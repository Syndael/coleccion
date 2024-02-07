from marshmallow import Schema
from app.utils.datos import db


class Tienda(db.Model):
    __tablename__ = 'TIENDA'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    url = db.Column(db.String(255))

    def __init__(self, nombre, url=None):
        self.nombre = nombre
        self.url = url


class TiendaSchema(Schema):
    class Meta:
        fields = ('id', 'nombre', 'url')
