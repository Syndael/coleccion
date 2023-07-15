from marshmallow import Schema
from app.utils.datos import db


class Estado(db.Model):
    __tablename__ = 'ESTADO'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255))
    tipo = db.Column(db.Integer)

    def __init__(self, descripcion, tipo):
        self.descripcion = descripcion
        self.tipo = tipo


class EstadoSchema(Schema):
    class Meta:
        fields = ('id', 'descripcion', 'tipo')