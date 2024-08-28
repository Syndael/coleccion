from marshmallow import Schema, fields
from sqlalchemy import Numeric
from app.utils.datos import db
from app.model.base_dlc_model import BaseDlcSchema
from app.model.progreso_model import ProgresoSchema


class ProgresoSesion(db.Model):
    __tablename__ = 'PROGRESO_SESION'

    id = db.Column(db.Integer, primary_key=True)
    progreso_id = db.Column(db.Integer, db.ForeignKey('PROGRESO.id'))
    base_dlc_id = db.Column(db.Integer, db.ForeignKey('BASE_DLC.id'))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    horas = db.Column(Numeric(precision=20, scale=6))
    fecha_h_inicio = db.Column(db.Date)
    fecha_h_fin = db.Column(db.Date)
    horas_h = db.Column(Numeric(precision=20, scale=6))
    notas = db.Column(db.String(255))
    nombre = db.Column(db.String(255))

    progreso = db.relationship('Progreso', primaryjoin='ProgresoSesion.progreso_id == Progreso.id')
    base_dlc = db.relationship('BaseDlc', primaryjoin='ProgresoSesion.base_dlc_id == BaseDlc.id')

    def __init__(self, progreso, base_dlc=None, fecha_inicio=None, fecha_fin=None, horas=None, notas=None, nombre=None, fecha_h_inicio=None, fecha_h_fin=None, horas_h=None):
        self.progreso = progreso
        self.base_dlc = base_dlc
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.horas = horas
        self.fecha_h_inicio = fecha_h_inicio
        self.fecha_h_fin = fecha_h_fin
        self.horas_h = horas_h
        self.notas = notas
        self.nombre = nombre


class ProgresoSesionSchema(Schema):
    progreso = fields.Nested(ProgresoSchema)
    base_dlc = fields.Nested(BaseDlcSchema)

    class Meta:
        fields = ('id', 'progreso', 'base_dlc', 'fecha_inicio', 'fecha_fin', 'horas', 'notas', 'nombre', 'fecha_h_inicio', 'fecha_h_fin', 'horas_h')
        include_relationships = True
