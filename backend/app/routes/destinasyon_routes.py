from flask import Blueprint, request, jsonify
from app.models.bolge import Bolge, Destinasyon
from app import db

destinasyon_bp = Blueprint('destinasyon', __name__, url_prefix='/api/destinasyonlar')

@destinasyon_bp.route('/', methods=['GET'])
def get_destinasyonlar():
    destinasyonlar = Destinasyon.query.all()
    return jsonify([{
        'id': d.id, 
        'bolge_id': d.bolge_id,
        'ad': d.ad, 
        'tur': d.tur,
        'aciklama': d.aciklama,
        'adres': d.adres,
        'fiyat': d.fiyat
    } for d in destinasyonlar])

@destinasyon_bp.route('/<int:id>', methods=['GET'])
def get_destinasyon(id):
    destinasyon = Destinasyon.query.get(id)
    if destinasyon:
        return jsonify({
            'id': destinasyon.id, 
            'bolge_id': destinasyon.bolge_id,
            'ad': destinasyon.ad, 
            'tur': destinasyon.tur,
            'aciklama': destinasyon.aciklama,
            'adres': destinasyon.adres,
            'fiyat': destinasyon.fiyat
        })
    return jsonify({'error': 'Destinasyon bulunamadı'}), 404

@destinasyon_bp.route('/', methods=['POST'])
def add_destinasyon():
    data = request.get_json()
    
    # Bölgenin var olup olmadığını kontrol et
    bolge_id = data.get('bolge_id')
    bolge = Bolge.query.get(bolge_id)
    if not bolge:
        return jsonify({'error': 'Belirtilen bölge bulunamadı'}), 404
        
    yeni_destinasyon = Destinasyon(
        bolge_id=bolge_id,
        ad=data.get('ad'),
        tur=data.get('tur'),
        aciklama=data.get('aciklama'),
        adres=data.get('adres'),
        fiyat=data.get('fiyat', 0)
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
    destinasyon.tur = data.get('tur', destinasyon.tur)
    destinasyon.aciklama = data.get('aciklama', destinasyon.aciklama)
    destinasyon.adres = data.get('adres', destinasyon.adres)
    destinasyon.fiyat = data.get('fiyat', destinasyon.fiyat)
    
    # Bölge değiştirilecekse, yeni bölgenin var olduğunu kontrol et
    if 'bolge_id' in data:
        bolge = Bolge.query.get(data['bolge_id'])
        if not bolge:
            return jsonify({'error': 'Belirtilen bölge bulunamadı'}), 404
        destinasyon.bolge_id = data['bolge_id']
    
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