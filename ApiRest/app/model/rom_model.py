from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.idioma_model import IdiomaSchema
from app.model.base_model import BaseSchema
from app.model.plataforma_model import PlataformaSchema
from app.model.region_model import RegionSchema
from app.model.tipo_rom_model import TipoRomSchema


class Rom(db.Model):
    __tablename__ = 'ROM'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('BASE.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    nombre_rom = db.Column(db.String(255))
    nombre_rom_ext = db.Column(db.String(255))
    update = db.Column(db.String(255))
    idioma_id = db.Column(db.Integer, db.ForeignKey('IDIOMA.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('REGION.id'))
    tipo_rom_id = db.Column(db.Integer, db.ForeignKey('TIPO_ROM.id'))
    fecha_descarga = db.Column(db.Date)

    base = db.relationship('Base', primaryjoin='Rom.base_id == Base.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Rom.plataforma_id == Plataforma.id')
    idioma = db.relationship('Idioma', primaryjoin='Rom.idioma_id == Idioma.id')
    region = db.relationship('Region', primaryjoin='Rom.region_id == Region.id')
    tipo_rom = db.relationship('TipoRom', primaryjoin='Rom.tipo_rom_id == TipoRom.id')

    def __init__(self, base, plataforma, nombre_rom=None, nombre_rom_ext=None, update=None, idioma=None, region=None, tipo_rom=None,
                 fecha_descarga=None):
        self.base = base
        self.plataforma = plataforma
        self.nombre_rom = nombre_rom
        self.nombre_rom_ext = nombre_rom_ext
        self.update = update
        self.idioma = idioma
        self.region = region
        self.tipo_rom = tipo_rom
        self.fecha_descarga = fecha_descarga


class RomSchema(Schema):
    base = fields.Nested(BaseSchema)
    plataforma = fields.Nested(PlataformaSchema)
    idioma = fields.Nested(IdiomaSchema)
    region = fields.Nested(RegionSchema)
    tipo_rom = fields.Nested(TipoRomSchema)

    class Meta:
        fields = (
        'id', 'base', 'plataforma', 'idioma', 'nombre_rom', 'nombre_rom_ext', 'update', 'region', 'tipo_rom', 'fecha_descarga')
        include_relationships = True
