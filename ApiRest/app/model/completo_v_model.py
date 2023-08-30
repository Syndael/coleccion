from marshmallow import Schema

from app.utils.datos import db


class Completo(db.Model):
    __tablename__ = 'COMPLETO'

    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(250))
    cantidad = db.Column(db.String(250))
    juegos = db.Column(db.String(2500))
    orden_desc = db.Column(db.String(250))

    def __init__(self, id, mes, cantidad, juegos, orden_desc):
        self.id = id
        self.mes = mes
        self.cantidad = cantidad
        self.juegos = juegos
        self.orden_desc = orden_desc


class CompletoSchema(Schema):
    class Meta:
        fields = ('id', 'mes', 'cantidad', 'juegos', 'orden_desc')
