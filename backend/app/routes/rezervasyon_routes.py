from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models import Rezervasyon, Musteri, Tur, TurPaketi
from datetime import datetime
from app.services.email_service import send_reservation_notification_to_driver, send_reservation_notification_to_guide
import logging

rezervasyon_bp = Blueprint('rezervasyon', __name__, url_prefix='/api')

@rezervasyon_bp.route('/rezervasyonlar', methods=['GET'])
@rezervasyon_bp.route('/rezervasyon', methods=['GET'])
def get_rezervasyonlar():
    """Tüm rezervasyonları listeler"""
    try:
        # İsteğe bağlı filtreler
        musteri_id = request.args.get('musteri_id')
        tur_id = request.args.get('tur_id')
        tur_paketi_id = request.args.get('tur_paketi_id')
        
        # Sorgu oluştur
        query = Rezervasyon.query
        
        # Filtreler uygulanır
        if musteri_id:
            query = query.filter_by(musteri_id=musteri_id)
        if tur_id:
            query = query.filter_by(tur_id=tur_id)
        if tur_paketi_id:
            query = query.filter_by(tur_paketi_id=tur_paketi_id)
            
        # Rezervasyonları al
        rezervasyonlar = query.all()
        
        # JSON formatında döndür
        return jsonify([{
            'id': r.id,
            'tur_id': r.tur_id,
            'tur_paketi_id': r.tur_paketi_id,
            'musteri_id': r.musteri_id,
            'ad': r.ad,
            'soyad': r.soyad,
            'email': r.email,
            'telefon': r.telefon,
            'tarih': r.tarih.strftime('%Y-%m-%d') if r.tarih else None,
            'kisi_sayisi': r.kisi_sayisi,
            'oda_tipi': r.oda_tipi,
            'ozel_istekler': r.ozel_istekler
        } for r in rezervasyonlar])
        
    except Exception as e:
        print(f"Rezervasyon listeleme hatası: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@rezervasyon_bp.route('/rezervasyonlar', methods=['POST'])
@rezervasyon_bp.route('/rezervasyon', methods=['POST'])
def create_rezervasyon():
    try:
        data = request.get_json()
        print("GELEN VERİ:", data)  # Debug log
        
        # Frontend'den gelen değerleri alma
        tur_paketi_id = data.get('tur_paketi_id')
        
        # Sadece tur_paketi_id kontrolü yap
        if not tur_paketi_id:
            return jsonify({'error': 'Tur Paketi ID alanı gerekli'}), 400
            
        # Tur Paketi kontrolü
        tur_paketi = TurPaketi.query.get(tur_paketi_id)
        if not tur_paketi:
            return jsonify({'error': 'Tur paketi bulunamadı'}), 404
            
        # ÖNEMLİ: Önce müşteriyi kontrol et, yoksa oluştur
        email = data.get('email', '')
        telefon = data.get('telefon', '')
        
        # Müşteriyi e-posta veya telefonla bulmaya çalış
        musteri = None
        if email:
            musteri = Musteri.query.filter_by(email=email).first()
        if not musteri and telefon:
            musteri = Musteri.query.filter_by(telefon=telefon).first()
            
        # Müşteri bulunamadıysa, otomatik olarak oluştur
        if not musteri:
            print("Müşteri bulunamadı, yeni oluşturuluyor...")
            musteri = Musteri(
                ad=data.get('ad', 'İsimsiz'),
                soyad=data.get('soyad', 'Müşteri'),
                email=email or 'otomatic@example.com',
                telefon=telefon or '5550000000',
                tc_kimlik=data.get('tc_kimlik', '00000000000'),
                adres=data.get('adres', 'Otomatik oluşturuldu'),
                dogum_tarihi=datetime(1990, 1, 1)  # Varsayılan doğum tarihi
            )
            db.session.add(musteri)
            db.session.flush()  # ID oluşturmak için flush yapın
            print(f"Yeni müşteri oluşturuldu. ID: {musteri.id}")
        
        # Tarih işleme
        try:
            if 'tarih' in data and data['tarih']:
                tarih = datetime.strptime(data['tarih'], '%Y-%m-%d').date()
            else:
                tarih = datetime.now().date()
        except ValueError:
            tarih = datetime.now().date()
        
        # Rezervasyon oluştur - artık sadece tur_paketi_id ile
        rezervasyon = Rezervasyon(
            tur_paketi_id=tur_paketi_id,
            musteri_id=musteri.id,
            ad=data.get('ad', 'İsimsiz'),
            soyad=data.get('soyad', 'Müşteri'),
            email=email or 'otomatic@example.com',
            telefon=telefon or '5550000000',
            tarih=tarih,
            kisi_sayisi=int(data.get('kisi_sayisi', 1)),
            oda_tipi=data.get('oda_tipi') or data.get('roomType', 'standard'),
            ozel_istekler=data.get('ozel_istekler') or data.get('notlar', '')
        )
        
        # Eğer tur_id yoksa None olarak bırak
        if data.get('tur_id'):
            rezervasyon.tur_id = data.get('tur_id')
        
        print("REZERVASYON OLUŞTURULACAK:", {
            'tur_paketi_id': rezervasyon.tur_paketi_id,
            'ad': rezervasyon.ad,
            'soyad': rezervasyon.soyad,
            'email': rezervasyon.email,
            'tarih': rezervasyon.tarih,
            'kisi_sayisi': rezervasyon.kisi_sayisi,
            'musteri_id': musteri.id
        })  # Debug log
        
        db.session.add(rezervasyon)
        db.session.commit()
        
        print("REZERVASYON OLUŞTURULDU. ID:", rezervasyon.id)  # Debug log
        
        return jsonify({
            'success': True,
            'message': 'Rezervasyon başarıyla oluşturuldu',
            'id': rezervasyon.id,
            'rezervasyon_id': f'REZ-{rezervasyon.id}'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print("REZERVASYON HATASI:", str(e))  # Debug log
        import traceback
        traceback.print_exc()  # Daha detaylı hata bilgisi
        
        # Daha açıklayıcı hata mesajları
        error_msg = str(e)
        return jsonify({'error': f'Rezervasyon oluşturulamadı: {error_msg}'}), 500