from app import db
from app.models.tur_paketi import TurPaketi, TurDestinasyon
# Diğer importlar...

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
        
        yeni_paket = TurPaketi(
            ad=data.get('ad'),
            aciklama=data.get('aciklama'),
            sure=sure_value,  # String olarak dönüştürülmüş değer
            fiyat=float(data.get('fiyat', 0)),
            kapasite=int(data.get('kapasite', 20)),
            baslangic_bolge_id=int(data.get('baslangic_bolge_id')),
            durum=data.get('durum', 'Aktif')
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
    if 'fiyat' in data:
        tur_paketi.fiyat = float(data['fiyat'])
    if 'kapasite' in data:
        tur_paketi.kapasite = int(data['kapasite'])
    if 'baslangic_bolge_id' in data:
        tur_paketi.baslangic_bolge_id = int(data['baslangic_bolge_id'])
    if 'durum' in data:
        tur_paketi.durum = data['durum']
    
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
    tur_paketi = get_tur_paketi_by_id(tur_paketi_id)
    if not tur_paketi:
        return []
    return tur_paketi.tur_destinasyonlar

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