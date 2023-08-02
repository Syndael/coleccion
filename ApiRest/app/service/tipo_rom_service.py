from flask import jsonify
from app.model.tipo_rom_model import TipoRom, TipoRomSchema


class TipoRomService:
    _tipo_rom_schema = TipoRomSchema()
    _tipos_rom_schema = TipoRomSchema(many=True)

    def get_tipos_rom(self):
        tipos_rom = TipoRom.query.order_by(TipoRom.extension.asc()).all()
        result = self._tipos_rom_schema.dump(tipos_rom)
        return jsonify(result), 200
