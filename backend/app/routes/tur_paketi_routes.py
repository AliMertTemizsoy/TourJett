from flask import Blueprint, request, jsonify
from app.services.tur_paketi_service import (
    get_all_tur_paketleri, get_tur_paketi_by_id,
    create_tur_paketi, update_tur_paketi, delete_tur_paketi,
    get_tur_destinasyonlari, add_tur_destinasyon
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
    try:
        data = request.get_json()
        
        # Gerekli alanların varlığını kontrol et
        if not data.get('ad'):
            return jsonify({'error': 'Tur paketi adı gereklidir'}), 400
        
        # Direkt olarak TurPaketi modeli oluştur, service layer bypass
        yeni_paket = TurPaketi(
            ad=data.get('ad'),
            aciklama=data.get('aciklama'),
            sure=data.get('sure'),
            fiyat=float(data.get('fiyat', 0)) if data.get('fiyat') else 0.0,
            kapasite=int(data.get('max_katilimci', 20)) if data.get('max_katilimci') else 20,
            konum=data.get('konum'),
            tur_tarihi=datetime.strptime(data.get('tur_tarihi'), '%Y-%m-%d').date() if data.get('tur_tarihi') else None,
            resim_url=data.get('resim_url'),
            max_katilimci=int(data.get('max_katilimci', 20)) if data.get('max_katilimci') else 20
        )
        
        db.session.add(yeni_paket)
        db.session.commit()
        
        return jsonify({
            'message': 'Tur paketi başarıyla oluşturuldu',
            'id': yeni_paket.id,
            'ad': yeni_paket.ad
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@tur_paketi_bp.route('/<int:id>/destinasyonlar', methods=['POST'])
def add_destinasyon_to_tur(id):
    """Tur paketine destinasyon ekler"""
    # Tur paketinin var olduğunu kontrol et
    paket = get_tur_paketi_by_id(id)
    if not paket:
        return jsonify({'error': 'Tur paketi bulunamadı'}), 404
    
    data = request.get_json()
    # Gerekli alanların varlığını kontrol et
    if not data.get('destinasyon_id'):
        return jsonify({'error': 'Destinasyon ID gereklidir'}), 400
    
    try:
        yeni_destinasyon = add_tur_destinasyon(id, data)
        return jsonify({
            'message': 'Destinasyon başarıyla eklendi',
            'destinasyon': {
                'id': yeni_destinasyon.id,
                'destinasyon_id': yeni_destinasyon.destinasyon_id,
                'siralama': yeni_destinasyon.siralama,
                'kalma_suresi': yeni_destinasyon.kalma_suresi,
                'not_bilgisi': yeni_destinasyon.not_bilgisi
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@tur_paketi_bp.route('/<int:id>', methods=['PUT'])
def update_tur_paketi_route(id):
    """Tur paketini günceller"""
    data = request.get_json()
    result = update_tur_paketi(id, data)
    
    if not result:
        return jsonify({'error': 'Tur paketi bulunamadı'}), 404
    
    return jsonify({
        'message': 'Tur paketi başarıyla güncellendi',
        'tur_paketi': {
            'id': result.id,
            'ad': result.ad,
            'aciklama': result.aciklama,
            'sure': result.sure,
            'fiyat': result.fiyat,
            'kapasite': result.kapasite
        }
    })

@tur_paketi_bp.route('/<int:id>', methods=['DELETE'])
def delete_tur_paketi_route(id):
    """Tur paketini siler"""
    # Service fonksiyonunu boolean değer döndürecek şekilde kullanıyoruz
    tur_paketi = get_tur_paketi_by_id(id)
    if not tur_paketi:
        return jsonify({'error': 'Tur paketi bulunamadı'}), 404
        
    try:
        delete_success = delete_tur_paketi(id)
        if delete_success:
            return jsonify({
                'message': 'Tur paketi başarıyla silindi',
                'id': id
            })
        else:
            return jsonify({'error': 'Tur paketi silinemedi'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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