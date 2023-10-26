from marshmallow import Schema

from app.utils.datos import db


class Gasto(db.Model):
    __tablename__ = 'GASTO'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(250))
    plataforma_nombre = db.Column(db.String(250))
    plataforma_corto = db.Column(db.String(250))
    descripcion = db.Column(db.String(250))
    cantidad = db.Column(db.Integer)
    fisico = db.Column(db.Integer)
    digital = db.Column(db.Integer)
    coste = db.Column(db.Integer)
    orden_desc = db.Column(db.String(250))
    orden_asc = db.Column(db.String(250))

    def __init__(self, id, tipo, plataforma_nombre, plataforma_corto, descripcion, cantidad, fisico, digital, coste, orden_desc,
                 orden_asc):
        self.id = id
        self.tipo = tipo
        self.plataforma_nombre = plataforma_nombre
        self.plataforma_corto = plataforma_corto
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.fisico = fisico
        self.digital = digital
        self.coste = coste
        self.orden_desc = orden_desc
        self.orden_asc = orden_asc


class GastoSchema(Schema):
    class Meta:
        fields = (
        'id', 'tipo', 'plataforma_nombre', 'plataforma_corto', 'descripcion', 'cantidad', 'fisico', 'digital', 'coste',
        'orden_desc', 'orden_asc')
