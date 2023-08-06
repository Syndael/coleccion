from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.estado_model import EstadoSchema
from app.model.idioma_model import IdiomaSchema
from app.model.base_model import BaseSchema
from app.model.plataforma_model import PlataformaSchema
from app.model.region_model import RegionSchema
from app.model.tienda_model import TiendaSchema


class Coleccion(db.Model):
    __tablename__ = 'COLECCION'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('BASE.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    idioma_id = db.Column(db.Integer, db.ForeignKey('IDIOMA.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('REGION.id'))
    estado_general_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    estado_caja_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    fecha_compra = db.Column(db.Date)
    fecha_recibo = db.Column(db.Date)
    unidades = db.Column(db.Integer)
    coste = db.Column(db.Float)
    tienda_id = db.Column(db.Integer, db.ForeignKey('TIENDA.id'))
    notas = db.Column(db.String(500))
    activado = db.Column(db.Boolean)
    codigo = db.Column(db.String(250))

    base = db.relationship('Base', primaryjoin='Coleccion.base_id == Base.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Coleccion.plataforma_id == Plataforma.id')
    idioma = db.relationship('Idioma', primaryjoin='Coleccion.idioma_id == Idioma.id')
    region = db.relationship('Region', primaryjoin='Coleccion.region_id == Region.id')
    estado_general = db.relationship('Estado', primaryjoin='Coleccion.estado_general_id == Estado.id')
    estado_caja = db.relationship('Estado', primaryjoin='Coleccion.estado_caja_id == Estado.id')
    tienda = db.relationship('Tienda', primaryjoin='Coleccion.tienda_id == Tienda.id')

    def __init__(self, base, plataforma, idioma=None, region=None, estado_general=None, estado_caja=None, fecha_compra=None, fecha_recibo=None, unidades=None, coste=None, tienda=None, notas=None, activado=None, codigo=None):
        self.base = base
        self.plataforma = plataforma
        self.idioma = idioma
        self.region = region
        self.estado_general = estado_general
        self.estado_caja = estado_caja
        self.fecha_compra = fecha_compra
        self.fecha_recibo = fecha_recibo
        self.unidades = unidades
        self.coste = coste
        self.tienda = tienda
        self.notas = notas
        self.activado = activado
        self.codigo = codigo


class ColeccionSchema(Schema):
    base = fields.Nested(BaseSchema)
    plataforma = fields.Nested(PlataformaSchema)
    idioma = fields.Nested(IdiomaSchema)
    region = fields.Nested(RegionSchema)
    estado_general = fields.Nested(EstadoSchema)
    estado_caja = fields.Nested(EstadoSchema)
    tienda = fields.Nested(TiendaSchema)

    class Meta:
        fields = ('id', 'base', 'plataforma', 'idioma', 'region', 'estado_general', 'estado_caja', 'fecha_compra', 'fecha_recibo', 'unidades', 'coste', 'tienda', 'notas', 'activado', 'codigo')
        include_relationships = True