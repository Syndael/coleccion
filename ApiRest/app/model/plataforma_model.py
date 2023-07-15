from marshmallow import Schema
from app.utils.datos import db


class Plataforma(db.Model):
    __tablename__ = 'PLATAFORMA'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    corto = db.Column(db.String(50))

    def __init__(self, nombre, corto):
        self.nombre = nombre
        self.corto = corto


class PlataformaSchema(Schema):
    class Meta:
        fields = ('id', 'nombre', 'corto')