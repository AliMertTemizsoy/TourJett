from flask import Blueprint, request, jsonify
from app.services.tur_service import (
    get_all_tur_paketleri, get_tur_paketi_by_id, create_tur_paketi, update_tur_paketi, delete_tur_paketi,
    get_tur_destinasyonlari, add_destinasyon_to_tur, remove_destinasyon_from_tur,
    get_all_tur_seferleri, get_tur_seferleri_by_tur_id, get_tur_seferi_by_id, create_tur_seferi,
    update_tur_seferi, delete_tur_seferi
)
from datetime import datetime

tur_bp = Blueprint('tur', __name__)

# Tur Paketi route'ları
@tur_bp.route('/api/turlar', methods=['GET'])
def get_turlar():
    turlar = get_all_tur_paketleri()
    return jsonify([{
        'id': t.id,
        'ad': t.ad,
        'fiyat': t.fiyat,
        'sure': t.sure,
        'kapasite': t.kapasite,
        'durum': t.durum
    } for t in turlar])

@tur_bp.route('/api/turlar/<int:id>', methods=['GET'])
def get_tur(id):
    tur = get_tur_paketi_by_id(id)
    if tur:
        return jsonify({
            'id': tur.id,
            'ad': tur.ad,
            'aciklama': tur.aciklama,
            'fiyat': tur.fiyat,
            'sure': tur.sure,
            'kapasite': tur.kapasite,
            'baslangic_bolge_id': tur.baslangic_bolge_id,
            'durum': tur.durum
        })
    return jsonify({'error': 'Tur paketi bulunamadı'}), 404

@tur_bp.route('/api/turlar', methods=['POST'])
def add_tur():
    data = request.get_json()
    yeni_tur = create_tur_paketi(data)
    return jsonify({
        'message': 'Tur paketi başarıyla eklendi',
        'id': yeni_tur.id
    }), 201

@tur_bp.route('/api/turlar/<int:id>', methods=['PUT'])
def update_tur(id):
    data = request.get_json()
    result = update_tur_paketi(id, data)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@tur_bp.route('/api/turlar/<int:id>', methods=['DELETE'])
def delete_tur(id):
    result = delete_tur_paketi(id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

# Tur Destinasyon route'ları
@tur_bp.route('/api/turlar/<int:id>/destinasyonlar', methods=['GET'])
def get_tur_dest(id):
    destinasyonlar = get_tur_destinasyonlari(id)
    return jsonify([{
        'id': d.id,
        'destinasyon_id': d.destinasyon_id,
        'destinasyon_adi': d.destinasyon.ad if d.destinasyon else None,
        'siralama': d.siralama,
        'kalma_suresi': d.kalma_suresi
    } for d in destinasyonlar])

@tur_bp.route('/api/turlar/<int:tur_id>/destinasyonlar', methods=['POST'])
def add_destinasyon(tur_id):
    data = request.get_json()
    destinasyon_id = data.get('destinasyon_id')
    siralama = data.get('siralama')
    kalma_suresi = data.get('kalma_suresi', 24)
    
    result = add_destinasyon_to_tur(tur_id, destinasyon_id, siralama, kalma_suresi)
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 404
        
    return jsonify({
        'message': 'Destinasyon tura eklendi',
        'id': result.id
    }), 201

@tur_bp.route('/api/turlar/<int:tur_id>/destinasyonlar/<int:dest_id>', methods=['DELETE'])
def remove_destinasyon(tur_id, dest_id):
    result = remove_destinasyon_from_tur(tur_id, dest_id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

# Tur Seferi route'ları
@tur_bp.route('/api/seferler', methods=['GET'])
def get_seferler():
    tur_id = request.args.get('tur_id')
    
    if tur_id:
        seferler = get_tur_seferleri_by_tur_id(tur_id)
    else:
        seferler = get_all_tur_seferleri()
        
    return jsonify([{
        'id': s.id,
        'tur_paketi_id': s.tur_paketi_id,
        'tur_adi': s.tur_paketi.ad if s.tur_paketi else None,
        'baslangic_tarihi': s.baslangic_tarihi.isoformat() if s.baslangic_tarihi else None,
        'bitis_tarihi': s.bitis_tarihi.isoformat() if s.bitis_tarihi else None,
        'arac_id': s.arac_id,
        'rehber_id': s.rehber_id,
        'sofor_id': s.sofor_id,
        'durum': s.durum
    } for s in seferler])

@tur_bp.route('/api/seferler/<int:id>', methods=['GET'])
def get_sefer(id):
    sefer = get_tur_seferi_by_id(id)
    if sefer:
        return jsonify({
            'id': sefer.id,
            'tur_paketi_id': sefer.tur_paketi_id,
            'tur_adi': sefer.tur_paketi.ad if sefer.tur_paketi else None,
            'baslangic_tarihi': sefer.baslangic_tarihi.isoformat() if sefer.baslangic_tarihi else None,
            'bitis_tarihi': sefer.bitis_tarihi.isoformat() if sefer.bitis_tarihi else None,
            'arac_id': sefer.arac_id,
            'arac_plaka': sefer.arac.plaka if sefer.arac else None,
            'rehber_id': sefer.rehber_id,
            'rehber_adi': f"{sefer.rehber.ad} {sefer.rehber.soyad}" if sefer.rehber else None,
            'sofor_id': sefer.sofor_id,
            'sofor_adi': f"{sefer.sofor.ad} {sefer.sofor.soyad}" if sefer.sofor else None,
            'durum': sefer.durum
        })
    return jsonify({'error': 'Tur seferi bulunamadı'}), 404

@tur_bp.route('/api/seferler', methods=['POST'])
def add_sefer():
    data = request.get_json()
    
    # Tarihleri string'den datetime'a çevir
    if 'baslangic_tarihi' in data and isinstance(data['baslangic_tarihi'], str):
        data['baslangic_tarihi'] = datetime.fromisoformat(data['baslangic_tarihi'].replace('Z', '+00:00'))
    
    if 'bitis_tarihi' in data and isinstance(data['bitis_tarihi'], str):
        data['bitis_tarihi'] = datetime.fromisoformat(data['bitis_tarihi'].replace('Z', '+00:00'))
        
    yeni_sefer = create_tur_seferi(data)
    return jsonify({
        'message': 'Tur seferi başarıyla eklendi',
        'id': yeni_sefer.id
    }), 201

@tur_bp.route('/api/seferler/<int:id>', methods=['PUT'])
def update_sefer(id):
    data = request.get_json()
    
    # Tarihleri string'den datetime'a çevir
    if 'baslangic_tarihi' in data and isinstance(data['baslangic_tarihi'], str):
        data['baslangic_tarihi'] = datetime.fromisoformat(data['baslangic_tarihi'].replace('Z', '+00:00'))
    
    if 'bitis_tarihi' in data and isinstance(data['bitis_tarihi'], str):
        data['bitis_tarihi'] = datetime.fromisoformat(data['bitis_tarihi'].replace('Z', '+00:00'))
        
    result = update_tur_seferi(id, data)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)

@tur_bp.route('/api/seferler/<int:id>', methods=['DELETE'])
def delete_sefer(id):
    result = delete_tur_seferi(id)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)