from marshmallow import Schema
from app.utils.datos import db


class Empresa(db.Model):
    __tablename__ = 'EMPRESA'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    tipo = db.Column(db.Integer)
    url = db.Column(db.String(255))

    def __init__(self, nombre, tipo, url=None):
        self.nombre = nombre
        self.tipo = tipo
        self.url = url


class EmpresaSchema(Schema):
    class Meta:
        fields = ('id', 'nombre', 'tipo', 'url')
