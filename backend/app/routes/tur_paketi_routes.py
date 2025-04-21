# backend/app/routes/tur_paketi_routes.py
from flask import Blueprint, request, jsonify
from app.services.tur_paketi_service import (
    get_all_tur_paketleri, get_tur_paketi_by_id,
    create_tur_paketi, update_tur_paketi, delete_tur_paketi,
    get_tur_destinasyonlari
)

tur_paketi_bp = Blueprint('tur_paketi', __name__, url_prefix='/api/turpaketleri')

@tur_paketi_bp.route('/', methods=['GET'])
def get_tur_paketleri():
    """Tüm tur paketlerini listeler"""
    aktif_filtresi = request.args.get('aktif', 'true').lower() == 'true'
    paketler = get_all_tur_paketleri(aktif_filtresi)
    
    return jsonify([{
        'id': p.id,
        'ad': p.ad,
        'aciklama': p.aciklama,
        'sure': p.sure,
        'fiyat': p.fiyat,
        'kapasite': p.kapasite,
        'baslangic_bolge_id': p.baslangic_bolge_id,
        'baslangic_bolge': p.baslangic_bolge.ad if p.baslangic_bolge else None,
        'durum': p.durum,
        'destinasyon_sayisi': len(p.tur_destinasyonlar)
    } for p in paketler])

@tur_paketi_bp.route('/<int:id>', methods=['GET'])
def get_tur_paketi(id):
    """ID'ye göre tur paketi getirir"""
    paket = get_tur_paketi_by_id(id)
    if not paket:
        return jsonify({'error': 'Tur paketi bulunamadı'}), 404
    
    # Destinasyonları al
    destinasyonlar = []
    for td in get_tur_destinasyonlari(id):
        destinasyonlar.append({
            'id': td.id,
            'destinasyon_id': td.destinasyon_id,
            'destinasyon_adi': td.destinasyon.ad if td.destinasyon else None,
            'siralama': td.siralama,
            'kalma_suresi': td.kalma_suresi,
            'not_bilgisi': td.not_bilgisi
        })
    
    return jsonify({
        'id': paket.id,
        'ad': paket.ad,
        'aciklama': paket.aciklama,
        'sure': paket.sure,
        'fiyat': paket.fiyat,
        'kapasite': paket.kapasite,
        'baslangic_bolge_id': paket.baslangic_bolge_id,
        'baslangic_bolge': paket.baslangic_bolge.ad if paket.baslangic_bolge else None,
        'durum': paket.durum,
        'destinasyonlar': destinasyonlar
    })

@tur_paketi_bp.route('/', methods=['POST'])
def add_tur_paketi():
    """Yeni tur paketi ekler"""
    data = request.get_json()
    
    # Gerekli alanların varlığını kontrol et
    if not data.get('ad'):
        return jsonify({'error': 'Tur paketi adı gereklidir'}), 400
    
    yeni_paket = create_tur_paketi(data)
    return jsonify({
        'message': 'Tur paketi başarıyla oluşturuldu',
        'id': yeni_paket.id
    }), 201

@tur_paketi_bp.route('/<int:id>', methods=['PUT'])
def update_tur_paketi_route(id):
    """Tur paketini günceller"""
    data = request.get_json()
    result = update_tur_paketi(id, data)
    
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 404
    
    return jsonify({'message': 'Tur paketi başarıyla güncellendi'})

@tur_paketi_bp.route('/<int:id>', methods=['DELETE'])
def delete_tur_paketi_route(id):
    """Tur paketini siler"""
    result = delete_tur_paketi(id)
    
    if 'error' in result:
        return jsonify(result), 404
    
    return jsonify(result)

@tur_paketi_bp.route('/<int:id>/destinasyonlar', methods=['GET'])
def get_tur_destinasyonlar(id):
    """Tur paketinin destinasyonlarını getirir"""
    paket = get_tur_paketi_by_id(id)
    if not paket:
        return jsonify({'error': 'Tur paketi bulunamadı'}), 404
    
    destinasyonlar = []
    for td in get_tur_destinasyonlari(id):
        destinasyonlar.append({
            'id': td.id,
            'destinasyon_id': td.destinasyon_id,
            'destinasyon_adi': td.destinasyon.ad if td.destinasyon else None,
            'siralama': td.siralama,
            'kalma_suresi': td.kalma_suresi,
            'not_bilgisi': td.not_bilgisi
        })
    
    return jsonify(destinasyonlar)