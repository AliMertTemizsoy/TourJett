from flask import Blueprint, jsonify, request
from app import db
from app.models import Rezervasyon, Musteri, TurSeferi, Tur, TurPaketi
from datetime import datetime, timedelta

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
            'tur_paketi_id': r.tur_paketi_id,  # Yeni alan eklendi
            'tur_sefer_id': r.tur_sefer_id,
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
        tur_id = data.get('tur_id')
        tur_sefer_id = data.get('tur_sefer_id')
        
        # Ya tur_id ya da tur_paketi_id gerekli
        if not tur_id and not tur_paketi_id:
            return jsonify({'error': 'Tur ID veya Tur Paketi ID alanı gerekli'}), 400
            
        # Tur veya Tur Paketi kontrolü
        if tur_paketi_id:
            tur_paketi = TurPaketi.query.get(tur_paketi_id)
            if not tur_paketi:
                return jsonify({'error': 'Tur paketi bulunamadı'}), 404
        elif tur_id:
            tur = Tur.query.get(tur_id)
            if not tur:
                return jsonify({'error': 'Tur bulunamadı'}), 404
        
        # Tur seferi varsa kontrol et, yoksa oluştur
        if not tur_sefer_id:
            # Mevcut bir tur seferi bulmaya çalış
            if tur_id:
                # Tur ID'si varsa, bu tur için bir sefer bul
                tur_seferi = TurSeferi.query.filter_by(tur_id=tur_id, durum='aktif').first()
            else:
                # Sadece aktif herhangi bir sefer bul
                tur_seferi = TurSeferi.query.filter_by(durum='aktif').first()
            
            if not tur_seferi:
                print("Aktif tur seferi bulunamadı, yeni bir sefer oluşturuluyor...")
                bugun = datetime.now().date()
                bitis = bugun + timedelta(days=7)
                
                # Bir tur seferi için geçerli bir tur ID'si gerekli
                # Eğer tur_id yoksa, veritabanındaki ilk turu al
                if not tur_id:
                    default_tur = Tur.query.first()
                    if not default_tur:
                        # Eğer hiç tur yoksa bir tane oluştur
                        default_tur = Tur(
                            adi="Geçici Tur",
                            sure="1 gün",
                            fiyat=0,
                            aciklama="Sistem tarafından otomatik oluşturulmuş tur"
                        )
                        db.session.add(default_tur)
                        db.session.flush()
                    tur_id_for_sefer = default_tur.id
                else:
                    tur_id_for_sefer = tur_id
                
                yeni_sefer = TurSeferi(
                    tur_id=tur_id_for_sefer,
                    baslangic_tarihi=bugun,
                    bitis_tarihi=bitis,
                    kontenjan=20,
                    kalan_kontenjan=20,
                    durum='aktif'
                )
                db.session.add(yeni_sefer)
                db.session.flush()
                
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
        
        # Rezervasyon oluştur - artık tur_paketi_id alanımız var!
        rezervasyon = Rezervasyon(
            tur_id=tur_id,
            tur_paketi_id=tur_paketi_id,  # Yeni eklenen alan
            tur_sefer_id=tur_sefer_id,
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
            'tur_paketi_id': rezervasyon.tur_paketi_id,  # Yeni alan eklendi
            'tur_sefer_id': rezervasyon.tur_sefer_id,
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