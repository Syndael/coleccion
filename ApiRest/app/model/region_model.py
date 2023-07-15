from marshmallow import Schema
from app.utils.datos import db


class Region(db.Model):
    __tablename__ = 'REGION'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))
    corto = db.Column(db.String(50))

    def __init__(self, descripcion, corto):
        self.descripcion = descripcion
        self.corto = corto


class RegionSchema(Schema):
    class Meta:
        fields = ('id', 'descripcion', 'corto')