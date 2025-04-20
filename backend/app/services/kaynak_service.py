from app.models.kaynak import Arac, Personel
from app import db

# Araç servisleri
def get_all_araclar():
    return Arac.query.all()

def get_arac_by_id(arac_id):
    return Arac.query.get(arac_id)

def create_arac(data):
    yeni_arac = Arac(
        plaka=data.get('plaka'),
        arac_turu=data.get('arac_turu'),
        koltuk_sayisi=data.get('koltuk_sayisi'),
        model=data.get('model'),
        durum=data.get('durum', 'Aktif')
    )
    
    db.session.add(yeni_arac)
    db.session.commit()
    return yeni_arac

def update_arac(arac_id, data):
    arac = Arac.query.get(arac_id)
    if not arac:
        return {'error': 'Araç bulunamadı'}
    
    arac.plaka = data.get('plaka', arac.plaka)
    arac.arac_turu = data.get('arac_turu', arac.arac_turu)
    arac.koltuk_sayisi = data.get('koltuk_sayisi', arac.koltuk_sayisi)
    arac.model = data.get('model', arac.model)
    arac.durum = data.get('durum', arac.durum)
    
    db.session.commit()
    return {'message': 'Araç güncellendi'}

def delete_arac(arac_id):
    arac = Arac.query.get(arac_id)
    if not arac:
        return {'error': 'Araç bulunamadı'}
    
    db.session.delete(arac)
    db.session.commit()
    return {'message': 'Araç silindi'}

# Personel servisleri
def get_all_personel():
    return Personel.query.all()

def get_personel_by_id(personel_id):
    return Personel.query.get(personel_id)

def create_personel(data):
    yeni_personel = Personel(
        ad=data.get('ad'),
        soyad=data.get('soyad'),
        email=data.get('email'),
        telefon=data.get('telefon'),
        pozisyon=data.get('pozisyon'),
        durum=data.get('durum', 'Aktif')
    )
    
    db.session.add(yeni_personel)
    db.session.commit()
    return yeni_personel

def update_personel(personel_id, data):
    personel = Personel.query.get(personel_id)
    if not personel:
        return {'error': 'Personel bulunamadı'}
    
    personel.ad = data.get('ad', personel.ad)
    personel.soyad = data.get('soyad', personel.soyad)
    personel.email = data.get('email', personel.email)
    personel.telefon = data.get('telefon', personel.telefon)
    personel.pozisyon = data.get('pozisyon', personel.pozisyon)
    personel.durum = data.get('durum', personel.durum)
    
    db.session.commit()
    return {'message': 'Personel güncellendi'}

def delete_personel(personel_id):
    personel = Personel.query.get(personel_id)
    if not personel:
        return {'error': 'Personel bulunamadı'}
    
    db.session.delete(personel)
    db.session.commit()
    return {'message': 'Personel silindi'}

# Filtreleme fonksiyonları
def get_araclar_by_tur(arac_turu):
    return Arac.query.filter_by(arac_turu=arac_turu).all()

def get_personel_by_pozisyon(pozisyon):
    return Personel.query.filter_by(pozisyon=pozisyon).all()