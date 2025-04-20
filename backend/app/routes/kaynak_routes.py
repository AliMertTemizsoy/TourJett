from flask import Blueprint, request, jsonify
from app.models.kaynak import Arac, Personel
from app.services.kaynak_service import (
    get_all_araclar, get_arac_by_id, create_arac, update_arac, delete_arac,
    get_all_personel, get_personel_by_id, create_personel, update_personel, delete_personel,
    get_araclar_by_tur, get_personel_by_pozisyon
)

kaynak_bp = Blueprint('kaynak', __name__)

# Araç route'ları
@kaynak_bp.route('/api/araclar', methods=['GET'])
def get_araclar():
    arac_turu = request.args.get('arac_turu')
    if arac_turu:
        araclar = get_araclar_by_tur(arac_turu)
    else:
        araclar = get_all_araclar()
    return jsonify([{
        'id': a.id, 
        'plaka': a.plaka, 
        'arac_turu': a.arac_turu,
        'koltuk_sayisi': a.koltuk_sayisi,
        'model': a.model,
        'durum': a.durum
    } for a in araclar])

@kaynak_bp.route('/api/araclar/<int:id>', methods=['GET'])
def get_arac(id):
    arac = get_arac_by_id(id)
    if arac:
        return jsonify({
            'id': arac.id, 
            'plaka': arac.plaka, 
            'arac_turu': arac.arac_turu,
            'koltuk_sayisi': arac.koltuk_sayisi,
            'model': arac.model,
            'durum': arac.durum
        })
    return jsonify({'error': 'Araç bulunamadı'}), 404

@kaynak_bp.route('/api/araclar', methods=['POST'])
def add_arac():
    data = request.get_json()
    yeni_arac = create_arac(data)
    return jsonify({
        'message': 'Araç başarıyla eklendi',
        'id': yeni_arac.id
    }), 201

@kaynak_bp.route('/api/araclar/<int:id>', methods=['PUT'])
def update_arac_route(id):
    data = request.get_json()
    result = update_arac(id, data)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@kaynak_bp.route('/api/araclar/<int:id>', methods=['DELETE'])
def delete_arac_route(id):
    result = delete_arac(id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

# Personel route'ları
@kaynak_bp.route('/api/personel', methods=['GET'])
def get_personeller():
    pozisyon = request.args.get('pozisyon')
    if pozisyon:
        personeller = get_personel_by_pozisyon(pozisyon)
    else:
        personeller = get_all_personel()
    return jsonify([{
        'id': p.id, 
        'ad': p.ad, 
        'soyad': p.soyad,
        'email': p.email,
        'telefon': p.telefon,
        'pozisyon': p.pozisyon,
        'durum': p.durum
    } for p in personeller])

@kaynak_bp.route('/api/personel/<int:id>', methods=['GET'])
def get_personel(id):
    personel = get_personel_by_id(id)
    if personel:
        return jsonify({
            'id': personel.id, 
            'ad': personel.ad, 
            'soyad': personel.soyad,
            'email': personel.email,
            'telefon': personel.telefon,
            'pozisyon': personel.pozisyon,
            'durum': personel.durum
        })
    return jsonify({'error': 'Personel bulunamadı'}), 404

@kaynak_bp.route('/api/personel', methods=['POST'])
def add_personel():
    data = request.get_json()
    yeni_personel = create_personel(data)
    return jsonify({
        'message': 'Personel başarıyla eklendi',
        'id': yeni_personel.id
    }), 201

@kaynak_bp.route('/api/personel/<int:id>', methods=['PUT'])
def update_personel_route(id):
    data = request.get_json()
    result = update_personel(id, data)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@kaynak_bp.route('/api/personel/<int:id>', methods=['DELETE'])
def delete_personel_route(id):
    result = delete_personel(id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)