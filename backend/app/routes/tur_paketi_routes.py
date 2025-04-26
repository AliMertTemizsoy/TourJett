from flask import Blueprint, request, jsonify
from app import db
from app.models.tur_paketi import TurPaketi
from datetime import datetime
import traceback  # Hata izleme için

tur_paketi_bp = Blueprint('tur_paketi', __name__, url_prefix='/api/turpaketleri')

@tur_paketi_bp.route('/', methods=['GET'])
def get_tur_paketleri():
    """Tüm tur paketlerini listeler"""
    try:
        paketler = TurPaketi.query.all()
        return jsonify([paket.to_dict() for paket in paketler])
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tur_paketi_bp.route('/<int:id>', methods=['GET'])
def get_tur_paketi(id):
    """Belirli bir tur paketinin detaylarını getirir"""
    try:
        paket = TurPaketi.query.get(id)
        if not paket:
            return jsonify({'error': 'Tur paketi bulunamadı'}), 404
        return jsonify(paket.to_dict())
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tur_paketi_bp.route('/', methods=['POST'])
def create_tur_paketi():
    """Yeni bir tur paketi oluşturur"""
    try:
        data = request.get_json()
        print(f"Gelen veri: {data}")  # Debug için
        
        # Gerekli kontroller
        if not data.get('ad'):
            return jsonify({'error': 'Tur paketi adı gereklidir'}), 400
        
        # Veri dönüşümleri güvenli hale getirildi
        try:
            fiyat = float(data.get('fiyat', 0))
        except (ValueError, TypeError):
            fiyat = 0.0
            
        try:
            kapasite = int(data.get('kapasite', 20))
        except (ValueError, TypeError):
            kapasite = 20
            
        try:
            max_katilimci = int(data.get('max_katilimci', 20))
        except (ValueError, TypeError):
            max_katilimci = 20
            
        # Tarih dönüşümü
        tur_tarihi = None
        if data.get('tur_tarihi'):
            try:
                tur_tarihi = datetime.strptime(data.get('tur_tarihi'), '%Y-%m-%d').date()
            except ValueError:
                print("Geçersiz tarih formatı")
                tur_tarihi = None
        
        # Yeni tur paketi oluştur - tüm alanlar güvenli şekilde belirtildi
        yeni_paket = TurPaketi(
            ad=data.get('ad'),
            aciklama=data.get('aciklama'),
            sure=data.get('sure'),
            fiyat=fiyat,
            kapasite=kapasite,
            baslangic_bolge_id=data.get('baslangic_bolge_id'),
            konum=data.get('konum'),
            tur_tarihi=tur_tarihi,
            resim_url=data.get('resim_url'),
            max_katilimci=max_katilimci,
            durum=data.get('durum', 'Aktif')
        )
        
        db.session.add(yeni_paket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tur paketi başarıyla oluşturuldu',
            'id': yeni_paket.id,
            'data': yeni_paket.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Tur paketi oluşturma hatası: {str(e)}")
        traceback.print_exc()  # Detaylı hata çıktısı
        return jsonify({'error': str(e)}), 500