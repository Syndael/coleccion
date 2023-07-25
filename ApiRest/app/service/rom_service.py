from flask import jsonify
from app.model.rom_model import Rom, RomSchema
from app.model.juego_model import Juego
from app.model.plataforma_model import Plataforma


class RomService:
    _rom_schema = RomSchema(many=True)

    def get_roms(self):
        roms = Rom.query.join(Rom.plataforma).join(Rom.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._rom_schema.dump(roms)
        return jsonify(result)

    def get_rom_by_id(self, id):
        roms = Rom.query.filter(Rom.id == id).join(Rom.plataforma).join(Rom.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._rom_schema.dump(roms)
        return jsonify(result)
