from flask import jsonify
from app.utils.datos import db
from app.model.rom_model import Rom, RomSchema
from app.model.idioma_model import Idioma
from app.model.juego_model import Juego
from app.model.plataforma_model import Plataforma
from app.model.region_model import Region
from app.model.tipo_rom_model import TipoRom


class RomService:
    _rom_schema = RomSchema()
    _roms_schema = RomSchema(many=True)

    def get_roms(self):
        roms = Rom.query.join(Rom.plataforma).join(Rom.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._roms_schema.dump(roms)
        return jsonify(result), 200

    def get_rom_by_id(self, id):
        rom = Rom.query.get(id)
        if not rom:
            return jsonify({'message': 'ROM no encontrada'}), 404
        rom_dict = self._rom_schema.dump(rom)
        return jsonify(rom_dict), 200


    def add_rom(self, request):
        data = request.get_json()

        if 'juego' not in data or data['juego']['id'] is None or 'plataforma' not in data or data['plataforma']['id'] is None:
            return jsonify({'message': 'Juego o plataforma no encontrado'}), 404
        juego = Juego.query.get(data['juego']['id'])
        if juego is None:
            return jsonify({'message': 'Juego no encontrado'}), 404
        plataforma = Plataforma.query.get(data['plataforma']['id'])
        if plataforma is None:
            return jsonify({'message': 'Plataforma no encontrada'}), 404

        rom = Rom(juego=juego, plataforma=plataforma)

        if 'idioma' in data and data['idioma']['id']:
            rom.idioma = Idioma.query.get(data['idioma']['id'])
        if 'region' in data and data['region']['id']:
            rom.region = Region.query.get(data['region']['id'])
        if 'tipo_rom' in data and data['tipo_rom']['id']:
            rom.tipo_rom = TipoRom.query.get(data['tipo_rom']['id'])
        if 'fecha_descarga' in data:
            rom.fecha_descarga = data['fecha_descarga']

        db.session.add(rom)
        db.session.commit()
        rom_dict = self._rom_schema.dump(rom)
        return jsonify(rom_dict), 200

    def update_rom(self, request, id):
        data = request.get_json()
        rom = Rom.query.get(id)

        if not rom:
            return jsonify({'message': 'ROM no encontrada'}), 404

        if 'idioma' in data and data['idioma']['id']:
            if rom.idioma is None or not rom.idioma.id == data['idioma']['id']:
                rom.idioma = Idioma.query.get(data['idioma']['id'])
        else:
            rom.idioma = None
        if 'juego' in data and data['juego']['id']:
            if rom.juego is None or not rom.juego.id == data['juego']['id']:
                rom.juego = Juego.query.get(data['juego']['id'])
        if 'plataforma' in data and data['plataforma']['id']:
            if rom.plataforma is None or not rom.plataforma.id == data['plataforma']['id']:
                rom.plataforma = Plataforma.query.get(data['plataforma']['id'])
        if 'region' in data and data['region']['id']:
            if rom.region is None or not rom.region.id == data['region']['id']:
                rom.region = Region.query.get(data['region']['id'])
        else:
            rom.region = None
        if 'tipo_rom' in data and data['tipo_rom']['id']:
            if rom.tipo_rom is None or not rom.tipo_rom.id == data['tipo_rom']['id']:
                rom.tipo_rom = TipoRom.query.get(data['tipo_rom']['id'])
        else:
            rom.tipo_rom = None
        if 'fecha_descarga' in data and not data['fecha_descarga'] == '':
            rom.fecha_descarga = data['fecha_descarga']
        else:
            rom.fecha_descarga = None

        db.session.commit()

        rom_dict = self._rom_schema.dump(rom)
        return jsonify(rom_dict), 200