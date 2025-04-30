from app import db
from app.models.tur_paketi import TurPaketi, TurDestinasyon
from app.models.tur import Tur
from datetime import datetime

# Tüm turları getir
def get_all_tur_paketleri(*args):  # *args ekleyerek esnek parametre yapısı
    return TurPaketi.query.all()

# ID'ye göre tur paketi getir
def get_tur_paketi_by_id(tur_paketi_id):
    return TurPaketi.query.get(tur_paketi_id)

# Yeni tur paketi oluştur
def create_tur_paketi(data):
    try:
        # Veri dönüşümlerini güvenli bir şekilde yap
        sure_value = str(data.get('sure')) if data.get('sure') is not None else None
        
        # Tur model referansı ile bilgileri doldur
        tur = None
        if data.get('tur_id'):
            tur = Tur.query.get(data['tur_id'])
        
        # Değerleri belirle
        ad = data.get('ad') or (tur.adi if tur else None)
        aciklama = data.get('aciklama') or (tur.aciklama if tur else None)
        sure = data.get('sure') or (tur.sure if tur else None)
        resim_url = data.get('resim_url') or (tur.resim if tur else None)
        
        # Tarih dönüşümü
        tur_tarihi = None
        if data.get('tur_tarihi'):
            try:
                tur_tarihi = datetime.strptime(data.get('tur_tarihi'), '%Y-%m-%d').date()
            except ValueError:
                pass
        
        yeni_paket = TurPaketi(
            ad=ad,
            aciklama=aciklama,
            sure=sure,
            kapasite=int(data.get('kapasite', 20)),
            tur_tarihi=tur_tarihi,
            resim_url=resim_url,
            durum=data.get('durum', 'Aktif'),
            surucu_id=data.get('surucu_id'),
            rehber_id=data.get('rehber_id'),
            vehicle_id=data.get('vehicle_id'),
            tur_id=data.get('tur_id')
        )
        
        db.session.add(yeni_paket)
        db.session.commit()
        return yeni_paket
    except Exception as e:
        db.session.rollback()
        print(f"Hata: {str(e)}")
        raise

# Tur paketini güncelle
def update_tur_paketi(tur_paketi_id, data):
    tur_paketi = get_tur_paketi_by_id(tur_paketi_id)
    if not tur_paketi:
        return None
    
    if 'ad' in data:
        tur_paketi.ad = data['ad']
    if 'aciklama' in data:
        tur_paketi.aciklama = data['aciklama']
    if 'sure' in data:
        tur_paketi.sure = str(data['sure'])
    if 'kapasite' in data:
        tur_paketi.kapasite = int(data['kapasite'])
    if 'durum' in data:
        tur_paketi.durum = data['durum']
    if 'surucu_id' in data:
        tur_paketi.surucu_id = data['surucu_id']
    if 'rehber_id' in data:
        tur_paketi.rehber_id = data['rehber_id']
    if 'vehicle_id' in data:
        tur_paketi.vehicle_id = data['vehicle_id']
    if 'tur_id' in data:
        tur_paketi.tur_id = data['tur_id']
    if 'tur_tarihi' in data and data['tur_tarihi']:
        try:
            tur_paketi.tur_tarihi = datetime.strptime(data['tur_tarihi'], '%Y-%m-%d').date()
        except ValueError:
            print("Geçersiz tarih formatı")
    if 'resim_url' in data:
        tur_paketi.resim_url = data['resim_url']
    
    db.session.commit()
    return tur_paketi

# Tur paketini sil
def delete_tur_paketi(tur_paketi_id):
    tur_paketi = get_tur_paketi_by_id(tur_paketi_id)
    if not tur_paketi:
        return False
    
    db.session.delete(tur_paketi)
    db.session.commit()
    return True

# Eksik olan fonksiyon: Tur destinasyonlarını getir
def get_tur_destinasyonlari(tur_paketi_id):
    return TurDestinasyon.query.filter_by(tur_paketi_id=tur_paketi_id).all()

# Diğer fonksiyonlar
def add_tur_destinasyon(tur_paketi_id, data):
    tur_paketi = get_tur_paketi_by_id(tur_paketi_id)
    if not tur_paketi:
        return None
    
    yeni_destinasyon = TurDestinasyon(
        tur_paketi_id=tur_paketi_id,
        destinasyon_id=int(data.get('destinasyon_id')),
        siralama=int(data.get('siralama', 0)),
        kalma_suresi=int(data.get('kalma_suresi', 1)),
        not_bilgisi=data.get('not_bilgisi', '')
    )
    
    db.session.add(yeni_destinasyon)
    db.session.commit()
    return yeni_destinasyon

# Tura göre paketleri getir
def get_tur_paketleri_by_tur(tur_id):
    return TurPaketi.query.filter_by(tur_id=tur_id).all()

# Tarihe göre paketleri getir
def get_tur_paketleri_by_date(date):
    return TurPaketi.query.filter_by(tur_tarihi=date).all()

# Rehbere göre paketleri getir
def get_tur_paketleri_by_rehber(rehber_id):
    return TurPaketi.query.filter_by(rehber_id=rehber_id).all()

# Sürücüye göre paketleri getir
def get_tur_paketleri_by_surucu(surucu_id):
    return TurPaketi.query.filter_by(surucu_id=surucu_id).all()

# Araca göre paketleri getir
def get_tur_paketleri_by_vehicle(vehicle_id):
    return TurPaketi.query.filter_by(vehicle_id=vehicle_id).all()