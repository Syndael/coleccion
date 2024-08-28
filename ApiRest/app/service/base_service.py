import requests, re
from app.utils.datos import db
from app.model.base_model import Base, BaseSchema
from app.model.base_plataforma_model import BasePlataforma
from app.model.tipo_base_model import TipoBase
from bs4 import BeautifulSoup
from datetime import datetime
from flask import jsonify


class BaseService:
    _base_schema = BaseSchema()
    _bases_schema = BaseSchema(many=True)

    def get_bases(self, request):
        bases = Base.query.join(Base.tipo_base)
        orden_seleccionado = None
        if request.args:
            if request.args.get('tipo_base_id'):
                tipo_base_id = request.args.get('tipo_base_id')
                bases = bases.filter(Base.tipo_id == tipo_base_id)
            if request.args.get('tipo_base_descripcion'):
                bases = bases.filter(TipoBase.descripcion == request.args.get('tipo_base_descripcion'))
            if request.args.get('nombre'):
                nombre = request.args.get('nombre')
                bases = bases.filter(Base.nombre.ilike(f'%{nombre}%'))
            if request.args.get('saga'):
                saga = request.args.get('saga')
                bases = bases.filter(Base.saga.ilike(f'%{saga}%'))
            if request.args.get('plataforma_id'):
                plataforma = request.args.get('plataforma_id')
                bases = bases.join(BasePlataforma).filter(BasePlataforma.plataforma_id == plataforma)
            if request.args.get('orden'):
                orden_seleccionado = request.args.get('orden')
        if orden_seleccionado == 'Nombre':
            bases = bases.order_by(Base.nombre.asc()).all()
        else:
            bases = bases.order_by(Base.saga.asc(), Base.fecha_salida.asc(), TipoBase.descripcion.asc(), Base.nombre.asc()).all()
        result = self._bases_schema.dump(bases)
        return jsonify(result), 200

    def get_bases_by_nombre(self, nombre):
        bases = Base.query.filter(Base.nombre.ilike(f'%{nombre}%')).order_by(Base.nombre.asc()).all()
        result = self._bases_schema.dump(bases)
        return jsonify(result), 200

    def get_bases_by_id(self, id):
        base = Base.query.get(id)
        if not base:
            return jsonify({'message': 'Base no encontrado'}), 404
        base_dict = self._base_schema.dump(base)
        return jsonify(base_dict), 200

    def add_base(self, request):
        data = request.get_json()
        if 'tipo_base' not in data or data['tipo_base']['id'] is None:
            return jsonify({'message': 'Tipo no encontrado'}), 404
        tipo = TipoBase.query.get(data['tipo_base']['id'])
        if not tipo:
            return jsonify({'message': 'Tipo no encontrado'}), 404
        if 'nombre' not in data:
            return jsonify({'message': 'Nombre no encontrado'}), 404
        base = Base(tipo_base=tipo, nombre=data['nombre'])
        if 'saga' in data:
            base.saga = data['saga']
        if 'url' in data:
            base.url = data['url']
        if 'fecha_salida' in data:
            base.fecha_salida = data['fecha_salida']
        db.session.add(base)
        db.session.commit()

        base_dict = self._base_schema.dump(base)
        return jsonify(base_dict), 200

    def update_base(self, request, id):
        data = request.get_json()
        base = Base.query.get(id)

        if not base:
            return jsonify({'message': 'Base no encontrado'}), 404

        if 'tipo_base' in data and data['tipo_base']['id']:
            tipo = TipoBase.query.get(data['tipo_base']['id'])
            base.tipo_base = tipo
        base.nombre = data.get('nombre', base.nombre)
        if 'saga' in data and not data['saga'] == '':
            base.saga = data['saga']
        else:
            base.saga = None
        if 'url' in data:
            base.url = data['url']
        else:
            base.url = None
        if 'fecha_salida' in data and not data['fecha_salida'] == '':
            base.fecha_salida = data['fecha_salida']
        else:
            base.fecha_salida = None

        db.session.commit()

        base_dict = self._base_schema.dump(base)
        return jsonify(base_dict), 200

    def delete_base_by_id(self, id):
        base = Base.query.get(id)
        if base:
            try:
                db.session.delete(base)
                db.session.commit()
                return {'success': True}
            except Exception as ex:
                db.session.rollback()
                print(ex)
                return {'success': False}

        return {'success': False}


    def get_valores_vandal(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                titulo_element = soup.find('h1', class_='titulojuego')
                if titulo_element and titulo_element.a:
                    titulo_text = titulo_element.a.text
                    base = Base(tipo_base=0, nombre=titulo_text)
                    fichajuego = soup.find('div', class_='fichajuego')
                    if fichajuego and 'Fecha de lanzamiento' in str(fichajuego.contents):
                        pattern = r"Fecha de lanzamiento:\s*(\d{1,2}/\d{1,2}/\d{4})"
                        match = re.search(pattern, str(fichajuego.contents))
                        if match:
                             base.fecha_salida = datetime.strptime(match.group(1), "%d/%m/%Y").date()

                    base_dict = self._base_schema.dump(base)
                    return jsonify(base_dict), 200

        except requests.RequestException as e:
            return jsonify({'error': f'Error al hacer la solicitud: {str(e)}'}), 500