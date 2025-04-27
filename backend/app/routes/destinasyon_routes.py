from flask import Blueprint, request, jsonify
from app.models.destinasyon import Destinasyon
from app import db

destinasyon_bp = Blueprint('destinasyon', __name__, url_prefix='/api/destinasyonlar')

@destinasyon_bp.route('/', methods=['GET'])
def get_destinasyonlar():
    destinasyonlar = Destinasyon.query.all()
    return jsonify([{
        'id': d.id,
        'parent_id': d.parent_id,
        'ad': d.ad,
        'aciklama': d.aciklama,
        'adres': d.adres,
        'ulke': d.ulke,
        'sehir': d.sehir,
        'enlem': d.enlem,
        'boylam': d.boylam
    } for d in destinasyonlar])

@destinasyon_bp.route('/<int:id>', methods=['GET'])
def get_destinasyon(id):
    destinasyon = Destinasyon.query.get(id)
    if destinasyon:
        return jsonify({
            'id': destinasyon.id,
            'parent_id': destinasyon.parent_id,
            'ad': destinasyon.ad,
            'aciklama': destinasyon.aciklama,
            'adres': destinasyon.adres,
            'ulke': destinasyon.ulke,
            'sehir': destinasyon.sehir,
            'enlem': destinasyon.enlem,
            'boylam': destinasyon.boylam
        })
    return jsonify({'error': 'Destinasyon bulunamadı'}), 404

@destinasyon_bp.route('/', methods=['POST'])
def add_destinasyon():
    data = request.get_json()

    parent_id = data.get('parent_id')
    if parent_id:
        parent = Destinasyon.query.get(parent_id)
        if not parent:
            return jsonify({'error': 'Belirtilen üst destinasyon bulunamadı'}), 404

    yeni_destinasyon = Destinasyon(
        parent_id=parent_id,
        ad=data.get('ad'),
        aciklama=data.get('aciklama'),
        adres=data.get('adres'),
        ulke=data.get('ulke'),
        sehir=data.get('sehir'),
        enlem=data.get('enlem'),
        boylam=data.get('boylam')
    )

    db.session.add(yeni_destinasyon)
    db.session.commit()

    return jsonify({
        'message': 'Destinasyon başarıyla eklendi',
        'id': yeni_destinasyon.id
    }), 201

@destinasyon_bp.route('/<int:id>', methods=['PUT'])
def update_destinasyon(id):
    destinasyon = Destinasyon.query.get(id)
    if not destinasyon:
        return jsonify({'error': 'Destinasyon bulunamadı'}), 404

    data = request.get_json()

    destinasyon.ad = data.get('ad', destinasyon.ad)
    destinasyon.aciklama = data.get('aciklama', destinasyon.aciklama)
    destinasyon.adres = data.get('adres', destinasyon.adres)
    destinasyon.ulke = data.get('ulke', destinasyon.ulke)
    destinasyon.sehir = data.get('sehir', destinasyon.sehir)
    destinasyon.enlem = data.get('enlem', destinasyon.enlem)
    destinasyon.boylam = data.get('boylam', destinasyon.boylam)

    if 'parent_id' in data:
        if data['parent_id']:
            parent = Destinasyon.query.get(data['parent_id'])
            if not parent:
                return jsonify({'error': 'Belirtilen üst destinasyon bulunamadı'}), 404
        destinasyon.parent_id = data['parent_id']

    db.session.commit()
    return jsonify({'message': 'Destinasyon güncellendi'})

@destinasyon_bp.route('/<int:id>', methods=['DELETE'])
def delete_destinasyon(id):
    destinasyon = Destinasyon.query.get(id)
    if not destinasyon:
        return jsonify({'error': 'Destinasyon bulunamadı'}), 404

    db.session.delete(destinasyon)
    db.session.commit()
    return jsonify({'message': 'Destinasyon silindi'})
