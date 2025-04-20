from flask import Blueprint, request, jsonify
from app.services.musteri_service import (
    get_all_musteriler, get_musteri_by_id, create_musteri, update_musteri, delete_musteri,
    get_all_rezervasyonlar, get_rezervasyon_by_id, get_rezervasyonlar_by_musteri,
    create_rezervasyon, update_rezervasyon, delete_rezervasyon
)
from datetime import datetime

musteri_bp = Blueprint('musteri', __name__)

# Müşteri route'ları
@musteri_bp.route('/api/musteriler', methods=['GET'])
def get_musteriler():
    musteriler = get_all_musteriler()
    return jsonify([{
        'id': m.id,
        'ad': m.ad,
        'soyad': m.soyad,
        'email': m.email,
        'telefon': m.telefon
    } for m in musteriler])

@musteri_bp.route('/api/musteriler/<int:id>', methods=['GET'])
def get_musteri(id):
    musteri = get_musteri_by_id(id)
    if musteri:
        return jsonify({
            'id': musteri.id,
            'ad': musteri.ad,
            'soyad': musteri.soyad,
            'email': musteri.email,
            'telefon': musteri.telefon,
            'adres': musteri.adres,
            'tc_kimlik': musteri.tc_kimlik,
            'dogum_tarihi': musteri.dogum_tarihi.isoformat() if musteri.dogum_tarihi else None
        })
    return jsonify({'error': 'Müşteri bulunamadı'}), 404

@musteri_bp.route('/api/musteriler', methods=['POST'])
def add_musteri():
    data = request.get_json()
    
    # Doğum tarihini datetime formatına çevir
    if 'dogum_tarihi' in data and isinstance(data['dogum_tarihi'], str):
        try:
            data['dogum_tarihi'] = datetime.fromisoformat(data['dogum_tarihi'].replace('Z', '+00:00')).date()
        except ValueError:
            return jsonify({'error': 'Geçersiz tarih formatı'}), 400
    
    result = create_musteri(data)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
        
    return jsonify({
        'message': 'Müşteri başarıyla eklendi',
        'id': result.id
    }), 201

@musteri_bp.route('/api/musteriler/<int:id>', methods=['PUT'])
def update_musteri_route(id):
    data = request.get_json()
    
    # Doğum tarihini datetime formatına çevir
    if 'dogum_tarihi' in data and isinstance(data['dogum_tarihi'], str):
        try:
            data['dogum_tarihi'] = datetime.fromisoformat(data['dogum_tarihi'].replace('Z', '+00:00')).date()
        except ValueError:
            return jsonify({'error': 'Geçersiz tarih formatı'}), 400
    
    result = update_musteri(id, data)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@musteri_bp.route('/api/musteriler/<int:id>', methods=['DELETE'])
def delete_musteri_route(id):
    result = delete_musteri(id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

# Rezervasyon route'ları
@musteri_bp.route('/api/rezervasyonlar', methods=['GET'])
def get_rezervasyonlar():
    musteri_id = request.args.get('musteri_id')
    
    if musteri_id:
        rezervasyonlar = get_rezervasyonlar_by_musteri(musteri_id)
    else:
        rezervasyonlar = get_all_rezervasyonlar()
        
    return jsonify([{
        'id': r.id,
        'musteri_id': r.musteri_id,
        'musteri_adi': f"{r.musteri.ad} {r.musteri.soyad}" if r.musteri else None,
        'tur_seferi_id': r.tur_seferi_id,
        'kisi_sayisi': r.kisi_sayisi,
        'toplam_fiyat': r.toplam_fiyat,
        'rezervasyon_tarihi': r.rezervasyon_tarihi.isoformat(),
        'durum': r.durum,
        'odeme_durumu': r.odeme_durumu
    } for r in rezervasyonlar])

@musteri_bp.route('/api/rezervasyonlar/<int:id>', methods=['GET'])
def get_rezervasyon(id):
    rezervasyon = get_rezervasyon_by_id(id)
    if rezervasyon:
        return jsonify({
            'id': rezervasyon.id,
            'musteri_id': rezervasyon.musteri_id,
            'musteri_adi': f"{rezervasyon.musteri.ad} {rezervasyon.musteri.soyad}" if rezervasyon.musteri else None,
            'tur_seferi_id': rezervasyon.tur_seferi_id,
            'tur_adi': rezervasyon.tur_seferi.tur_paketi.ad if rezervasyon.tur_seferi and rezervasyon.tur_seferi.tur_paketi else None,
            'kisi_sayisi': rezervasyon.kisi_sayisi,
            'toplam_fiyat': rezervasyon.toplam_fiyat,
            'rezervasyon_tarihi': rezervasyon.rezervasyon_tarihi.isoformat(),
            'durum': rezervasyon.durum,
            'odeme_durumu': rezervasyon.odeme_durumu
        })
    return jsonify({'error': 'Rezervasyon bulunamadı'}), 404

@musteri_bp.route('/api/rezervasyonlar', methods=['POST'])
def add_rezervasyon():
    data = request.get_json()
    result = create_rezervasyon(data)
    
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 400
        
    return jsonify({
        'message': 'Rezervasyon başarıyla eklendi',
        'id': result.id
    }), 201

@musteri_bp.route('/api/rezervasyonlar/<int:id>', methods=['PUT'])
def update_rezervasyon_route(id):
    data = request.get_json()
    result = update_rezervasyon(id, data)
    
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@musteri_bp.route('/api/rezervasyonlar/<int:id>', methods=['DELETE'])
def delete_rezervasyon_route(id):
    result = delete_rezervasyon(id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)