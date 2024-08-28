from marshmallow import Schema, fields

from app.model.base_model import BaseSchema
from app.model.edicion_model import EdicionSchema
from app.model.empresa_model import EmpresaSchema
from app.model.estado_model import EstadoSchema
from app.model.idioma_model import IdiomaSchema
from app.model.plataforma_model import PlataformaSchema
from app.model.region_model import RegionSchema
from app.model.tienda_model import TiendaSchema
from app.utils.datos import db


class Coleccion(db.Model):
    __tablename__ = 'COLECCION'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('BASE.id'))
    edicion_id = db.Column(db.Integer, db.ForeignKey('EDICION.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    idioma_id = db.Column(db.Integer, db.ForeignKey('IDIOMA.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('REGION.id'))
    estado_general_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    estado_caja_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    reparto_id = db.Column(db.Integer, db.ForeignKey('EMPRESA.id'))
    fecha_reserva = db.Column(db.Date)
    fecha_compra = db.Column(db.Date)
    fecha_recibo = db.Column(db.Date)
    unidades = db.Column(db.Integer)
    precio = db.Column(db.Float)
    coste = db.Column(db.Float)
    reparto_seguimiento = db.Column(db.String(100))
    envio = db.Column(db.Float)
    tienda_id = db.Column(db.Integer, db.ForeignKey('TIENDA.id'))
    url = db.Column(db.String(255))
    ig = db.Column(db.String(255))
    notas = db.Column(db.String(500))
    activado = db.Column(db.Boolean)
    codigo = db.Column(db.String(250))
    mascara_aux = db.Column(db.String(50))

    base = db.relationship('Base', primaryjoin='Coleccion.base_id == Base.id')
    edicion = db.relationship('Edicion', primaryjoin='Coleccion.edicion_id == Edicion.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Coleccion.plataforma_id == Plataforma.id')
    idioma = db.relationship('Idioma', primaryjoin='Coleccion.idioma_id == Idioma.id')
    region = db.relationship('Region', primaryjoin='Coleccion.region_id == Region.id')
    estado_general = db.relationship('Estado', primaryjoin='Coleccion.estado_general_id == Estado.id')
    estado_caja = db.relationship('Estado', primaryjoin='Coleccion.estado_caja_id == Estado.id')
    reparto = db.relationship('Empresa', primaryjoin='Coleccion.reparto_id == Empresa.id')
    tienda = db.relationship('Tienda', primaryjoin='Coleccion.tienda_id == Tienda.id')

    def __init__(self, base, plataforma, edicion=None, idioma=None, region=None, estado_general=None, estado_caja=None,
                 reparto=None, fecha_reserva=None, fecha_compra=None, fecha_recibo=None, unidades=None, precio=None,
                 envio=None, coste=None, reparto_seguimiento=None, tienda=None, url=None, ig=None, notas=None, activado=None, codigo=None,
                 mascara_aux=None):
        self.base = base
        self.plataforma = plataforma
        self.edicion = edicion
        self.idioma = idioma
        self.region = region
        self.estado_general = estado_general
        self.estado_caja = estado_caja
        self.reparto = reparto
        self.fecha_reserva = fecha_reserva
        self.fecha_compra = fecha_compra
        self.fecha_recibo = fecha_recibo
        self.unidades = unidades
        self.precio = precio
        self.envio = envio
        self.coste = coste
        self.reparto_seguimiento = reparto_seguimiento
        self.tienda = tienda
        self.url = url
        self.ig = ig
        self.notas = notas
        self.activado = activado
        self.codigo = codigo
        self.mascara_aux = mascara_aux


class ColeccionSchema(Schema):
    base = fields.Nested(BaseSchema)
    edicion = fields.Nested(EdicionSchema)
    plataforma = fields.Nested(PlataformaSchema)
    idioma = fields.Nested(IdiomaSchema)
    region = fields.Nested(RegionSchema)
    estado_general = fields.Nested(EstadoSchema)
    estado_caja = fields.Nested(EstadoSchema)
    reparto = fields.Nested(EmpresaSchema)
    tienda = fields.Nested(TiendaSchema)

    class Meta:
        fields = (
            'id', 'base', 'edicion', 'plataforma', 'idioma', 'region', 'estado_general', 'estado_caja', 'reparto',
            'fecha_reserva', 'fecha_compra', 'fecha_recibo', 'unidades', 'precio', 'envio', 'coste', 'reparto_seguimiento', 'tienda', 'url',
            'ig', 'notas', 'activado', 'codigo', 'mascara_aux')
        include_relationships = True
