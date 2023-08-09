from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.base_model import BaseSchema
from app.model.plataforma_model import PlataformaSchema


class BasePlataforma(db.Model):
    __tablename__ = 'BASE_X_PLATAFORMA'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('BASE.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    fecha = db.Column(db.Date)

    base = db.relationship('Base', primaryjoin='BasePlataforma.base_id == Base.id')
    plataforma = db.relationship('Plataforma', primaryjoin='BasePlataforma.plataforma_id == Plataforma.id')

    def __init__(self, base, plataforma, fecha=None):
        self.base = base
        self.plataforma = plataforma
        self.fecha = fecha


class BasePlataformaSchema(Schema):
    base = fields.Nested(BaseSchema)
    plataforma = fields.Nested(PlataformaSchema)

    class Meta:
        fields = ('id', 'base', 'plataforma', 'fecha')
        include_relationships = True
