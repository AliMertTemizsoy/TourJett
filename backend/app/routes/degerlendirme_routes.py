from flask import Blueprint, request, jsonify
from app.services.degerlendirme_service import (
    get_all_degerlendirmeler, get_degerlendirme_by_id, 
    get_degerlendirmeler_by_tur, get_degerlendirmeler_by_musteri,
    create_degerlendirme, update_degerlendirme, delete_degerlendirme,
    get_tur_ortalama_puan
)

degerlendirme_bp = Blueprint('degerlendirme', __name__)

@degerlendirme_bp.route('/api/degerlendirmeler', methods=['GET'])
def get_degerlendirmeler():
    tur_paketi_id = request.args.get('tur_paketi_id')
    musteri_id = request.args.get('musteri_id')
    
    if tur_paketi_id:
        degerlendirmeler = get_degerlendirmeler_by_tur(tur_paketi_id)
    elif musteri_id:
        degerlendirmeler = get_degerlendirmeler_by_musteri(musteri_id)
    else:
        degerlendirmeler = get_all_degerlendirmeler()
    
    return jsonify([{
        'id': d.id,
        'musteri_id': d.musteri_id,
        'musteri_adi': f"{d.musteri.ad} {d.musteri.soyad}" if d.musteri else None,
        'tur_paketi_id': d.tur_paketi_id,
        'tur_adi': d.tur_paketi.ad if d.tur_paketi else None,
        'puan': d.puan,
        'yorum': d.yorum,
        'olusturma_tarihi': d.olusturma_tarihi.isoformat()
    } for d in degerlendirmeler])

@degerlendirme_bp.route('/api/degerlendirmeler/<int:id>', methods=['GET'])
def get_degerlendirme(id):
    degerlendirme = get_degerlendirme_by_id(id)
    if degerlendirme:
        return jsonify({
            'id': degerlendirme.id,
            'musteri_id': degerlendirme.musteri_id,
            'musteri_adi': f"{degerlendirme.musteri.ad} {degerlendirme.musteri.soyad}" if degerlendirme.musteri else None,
            'tur_paketi_id': degerlendirme.tur_paketi_id,
            'tur_adi': degerlendirme.tur_paketi.ad if degerlendirme.tur_paketi else None,
            'puan': degerlendirme.puan,
            'yorum': degerlendirme.yorum,
            'olusturma_tarihi': degerlendirme.olusturma_tarihi.isoformat()
        })
    return jsonify({'error': 'Değerlendirme bulunamadı'}), 404

@degerlendirme_bp.route('/api/degerlendirmeler', methods=['POST'])
def add_degerlendirme():
    data = request.get_json()
    result = create_degerlendirme(data)
    
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
        
    return jsonify({
        'message': 'Değerlendirme başarıyla eklendi',
        'id': result.id
    }), 201

@degerlendirme_bp.route('/api/degerlendirmeler/<int:id>', methods=['PUT'])
def update_degerlendirme_route(id):
    data = request.get_json()
    result = update_degerlendirme(id, data)
    
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@degerlendirme_bp.route('/api/degerlendirmeler/<int:id>', methods=['DELETE'])
def delete_degerlendirme_route(id):
    result = delete_degerlendirme(id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@degerlendirme_bp.route('/api/turlar/<int:id>/puan', methods=['GET'])
def get_tur_puan(id):
    result = get_tur_ortalama_puan(id)
    return jsonify(result)