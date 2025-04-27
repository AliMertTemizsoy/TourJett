from app import db
from app.models.tur import TurPaketi, TurDestinasyon, TurSeferi
from app.models.destinasyon import Destinasyon

# Tur Paketi servisleri
def get_all_tur_paketleri():
    return TurPaketi.query.all()

def get_tur_paketi_by_id(tur_id):
    return TurPaketi.query.get(tur_id)

def create_tur_paketi(data):
    yeni_tur = TurPaketi(
        ad=data.get('ad'),
        aciklama=data.get('aciklama'),
        fiyat=data.get('fiyat'),
        sure=data.get('sure'),
        kapasite=data.get('kapasite'),
        baslangic_bolge_id=data.get('baslangic_bolge_id'),
        durum=data.get('durum', 'Aktif')
    )
    
    db.session.add(yeni_tur)
    db.session.commit()
    
    # Eğer destinasyonlar verilmişse, ekle
    destinasyonlar = data.get('destinasyonlar', [])
    for i, dest_id in enumerate(destinasyonlar):
        tur_dest = TurDestinasyon(
            tur_paketi_id=yeni_tur.id,
            destinasyon_id=dest_id,
            siralama=i+1,
            kalma_suresi=24  # Varsayılan 24 saat
        )
        db.session.add(tur_dest)
    
    db.session.commit()
    return yeni_tur

def update_tur_paketi(tur_id, data):
    tur = TurPaketi.query.get(tur_id)
    if not tur:
        return {'error': 'Tur paketi bulunamadı'}
    
    tur.ad = data.get('ad', tur.ad)
    tur.aciklama = data.get('aciklama', tur.aciklama)
    tur.fiyat = data.get('fiyat', tur.fiyat)
    tur.sure = data.get('sure', tur.sure)
    tur.kapasite = data.get('kapasite', tur.kapasite)
    tur.baslangic_bolge_id = data.get('baslangic_bolge_id', tur.baslangic_bolge_id)
    tur.durum = data.get('durum', tur.durum)
    
    db.session.commit()
    return {'message': 'Tur paketi güncellendi'}

def delete_tur_paketi(tur_id):
    tur = TurPaketi.query.get(tur_id)
    if not tur:
        return {'error': 'Tur paketi bulunamadı'}
    
    # İlişkili destinasyonları sil
    TurDestinasyon.query.filter_by(tur_paketi_id=tur_id).delete()
    
    # İlişkili seferleri sil
    TurSeferi.query.filter_by(tur_paketi_id=tur_id).delete()
    
    db.session.delete(tur)
    db.session.commit()
    return {'message': 'Tur paketi silindi'}

# Tur Destinasyon servisleri
def get_tur_destinasyonlari(tur_id):
    return TurDestinasyon.query.filter_by(tur_paketi_id=tur_id).order_by(TurDestinasyon.siralama).all()

def add_destinasyon_to_tur(tur_id, destinasyon_id, siralama=None, kalma_suresi=24):
    tur = TurPaketi.query.get(tur_id)
    destinasyon = Destinasyon.query.get(destinasyon_id)
    
    if not tur or not destinasyon:
        return {'error': 'Tur veya destinasyon bulunamadı'}
    
    # Eğer siralama verilmezse, en sona ekle
    if siralama is None:
        max_siralama = db.session.query(db.func.max(TurDestinasyon.siralama)).filter_by(tur_paketi_id=tur_id).scalar() or 0
        siralama = max_siralama + 1
    
    tur_dest = TurDestinasyon(
        tur_paketi_id=tur_id,
        destinasyon_id=destinasyon_id,
        siralama=siralama,
        kalma_suresi=kalma_suresi
    )
    
    db.session.add(tur_dest)
    db.session.commit()
    return tur_dest

def remove_destinasyon_from_tur(tur_id, destinasyon_id):
    tur_dest = TurDestinasyon.query.filter_by(tur_paketi_id=tur_id, destinasyon_id=destinasyon_id).first()
    
    if not tur_dest:
        return {'error': 'Tur destinasyonu bulunamadı'}
    
    db.session.delete(tur_dest)
    db.session.commit()
    return {'message': 'Destinasyon turdan kaldırıldı'}

# Tur Seferi servisleri
def get_all_tur_seferleri():
    return TurSeferi.query.all()

def get_tur_seferleri_by_tur_id(tur_id):
    return TurSeferi.query.filter_by(tur_paketi_id=tur_id).all()

def get_tur_seferi_by_id(sefer_id):
    return TurSeferi.query.get(sefer_id)

def create_tur_seferi(data):
    yeni_sefer = TurSeferi(
        tur_paketi_id=data.get('tur_paketi_id'),
        baslangic_tarihi=data.get('baslangic_tarihi'),
        bitis_tarihi=data.get('bitis_tarihi'),
        arac_id=data.get('arac_id'),
        rehber_id=data.get('rehber_id'),
        sofor_id=data.get('sofor_id'),
        durum=data.get('durum', 'Planlandı')
    )
    
    db.session.add(yeni_sefer)
    db.session.commit()
    return yeni_sefer

def update_tur_seferi(sefer_id, data):
    sefer = TurSeferi.query.get(sefer_id)
    if not sefer:
        return {'error': 'Tur seferi bulunamadı'}
    
    sefer.baslangic_tarihi = data.get('baslangic_tarihi', sefer.baslangic_tarihi)
    sefer.bitis_tarihi = data.get('bitis_tarihi', sefer.bitis_tarihi)
    sefer.arac_id = data.get('arac_id', sefer.arac_id)
    sefer.rehber_id = data.get('rehber_id', sefer.rehber_id)
    sefer.sofor_id = data.get('sofor_id', sefer.sofor_id)
    sefer.durum = data.get('durum', sefer.durum)
    
    db.session.commit()
    return {'message': 'Tur seferi güncellendi'}

def delete_tur_seferi(sefer_id):
    sefer = TurSeferi.query.get(sefer_id)
    if not sefer:
        return {'error': 'Tur seferi bulunamadı'}
    
    db.session.delete(sefer)
    db.session.commit()
    return {'message': 'Tur seferi silindi'}