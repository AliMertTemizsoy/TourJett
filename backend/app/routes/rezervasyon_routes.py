from flask import Blueprint, jsonify, request
from app import db
from app.models import Rezervasyon, Musteri, TurSeferi, Tur  # Add Tur import
from datetime import datetime, timedelta  # Add timedelta import

rezervasyon_bp = Blueprint('rezervasyon', __name__, url_prefix='/api')

@rezervasyon_bp.route('/rezervasyonlar', methods=['POST'])
@rezervasyon_bp.route('/rezervasyon', methods=['POST'])
def create_rezervasyon():
    try:
        data = request.get_json()
        print("GELEN VERİ:", data)  # Debug log
        
        # Frontend'den gelen değerleri alma
        tur_id = data.get('tur_paketi_id') or data.get('tur_id')
        tur_sefer_id = data.get('tur_sefer_id')  # Yeni eklenen parametre
        
        if not tur_id:
            return jsonify({'error': 'Tur ID alanı gerekli'}), 400
            
        # Tur varlığını kontrol et
        tur = Tur.query.get(tur_id)
        if not tur:
            return jsonify({'error': 'Tur bulunamadı'}), 404
            
        # Tur Seferi varsa kontrol et
        if tur_sefer_id:
            tur_seferi = TurSeferi.query.get(tur_sefer_id)
            if not tur_seferi:
                return jsonify({'error': 'Tur seferi bulunamadı'}), 404
            # Tur seferinden tur_id'yi al
            tur_id = tur_seferi.tur_id
        else:
            # Turla ilişkili aktif bir sefer bul
            tur_seferi = TurSeferi.query.filter_by(tur_id=tur_id, durum='aktif').first()
            
            # Aktif sefer yoksa yeni bir tane oluştur
            if not tur_seferi:
                print("Aktif tur seferi bulunamadı, yeni bir sefer oluşturuluyor...")
                # Bugünden başlayarak 7 gün sonrası için bir sefer oluştur
                bugun = datetime.now().date()
                bitis = bugun + timedelta(days=7)
                
                yeni_sefer = TurSeferi(
                    tur_id=tur_id,
                    baslangic_tarihi=bugun,
                    bitis_tarihi=bitis,
                    kontenjan=20,  # Varsayılan kontenjan
                    kalan_kontenjan=20,
                    durum='aktif'
                )
                db.session.add(yeni_sefer)
                db.session.flush()  # ID oluşturmak için flush yap
                
                print(f"Yeni tur seferi oluşturuldu. ID: {yeni_sefer.id}")
                tur_seferi = yeni_sefer
                
            tur_sefer_id = tur_seferi.id
            
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
                # Diğer müşteri alanlarını ekleyin
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
        
        # Rezervasyon oluştur - Tur Seferi ID'sini de ekle
        rezervasyon = Rezervasyon(
            tur_id=tur_id,
            tur_sefer_id=tur_sefer_id,  # Tur seferi ID'sini ekle
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
        
        print("REZERVASYON OLUŞTURULACAK:", {
            'tur_id': rezervasyon.tur_id,
            'tur_sefer_id': rezervasyon.tur_sefer_id,  # Log'a tur_sefer_id ekle
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