from app import db
from app.models.destinasyon import Destinasyon, Arac, Personel

# Destinasyon services
def get_all_destinasyonlar():
    """Get all destinations"""
    return Destinasyon.query.all()

def get_destinasyon_by_id(destinasyon_id):
    """Get destination by ID"""
    return Destinasyon.query.get(destinasyon_id)

def get_destinasyonlar_by_type(tur):
    """Get destinations by type"""
    return Destinasyon.query.filter_by(tur=tur).all()

def get_destinasyonlar_by_ulke(ulke):
    """Get destinations by country"""
    return Destinasyon.query.filter_by(ulke=ulke).all()

def get_destinasyonlar_by_parent(parent_id):
    """Get all child destinations of a parent"""
    return Destinasyon.query.filter_by(parent_id=parent_id).all()
    
def create_destinasyon(data):
    """Create a new destination"""
    yeni_destinasyon = Destinasyon(
        parent_id=data.get('parent_id'),
        ad=data.get('ad'),
        tur=data.get('tur'),
        aciklama=data.get('aciklama'),
        adres=data.get('adres'),
        ulke=data.get('ulke'),
        sehir=data.get('sehir'),
        fiyat=data.get('fiyat', 0),
        enlem=data.get('enlem'),
        boylam=data.get('boylam')
    )
    
    db.session.add(yeni_destinasyon)
    db.session.commit()
    return yeni_destinasyon

def update_destinasyon(destinasyon_id, data):
    """Update a destination"""
    destinasyon = get_destinasyon_by_id(destinasyon_id)
    if not destinasyon:
        return {'error': 'Destinasyon bulunamadı'}
        
    # Update fields if they exist in data
    if 'ad' in data:
        destinasyon.ad = data['ad']
    if 'tur' in data:
        destinasyon.tur = data['tur']
    if 'aciklama' in data:
        destinasyon.aciklama = data['aciklama']
    if 'adres' in data:
        destinasyon.adres = data['adres']
    if 'ulke' in data:
        destinasyon.ulke = data['ulke']
    if 'sehir' in data:
        destinasyon.sehir = data['sehir']
    if 'fiyat' in data:
        destinasyon.fiyat = data['fiyat']
    if 'enlem' in data:
        destinasyon.enlem = data['enlem']
    if 'boylam' in data:
        destinasyon.boylam = data['boylam']
    if 'parent_id' in data:
        destinasyon.parent_id = data['parent_id']
        
    db.session.commit()
    return destinasyon

def delete_destinasyon(destinasyon_id):
    """Delete a destination"""
    destinasyon = get_destinasyon_by_id(destinasyon_id)
    if not destinasyon:
        return {'error': 'Destinasyon bulunamadı'}
    
    db.session.delete(destinasyon)
    db.session.commit()
    return {'message': 'Destinasyon silindi'}

# Arac services (moved from kaynak_service.py)
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
    arac = get_arac_by_id(arac_id)
    if not arac:
        return {'error': 'Araç bulunamadı'}
    
    if 'plaka' in data:
        arac.plaka = data['plaka']
    if 'arac_turu' in data:
        arac.arac_turu = data['arac_turu']
    if 'koltuk_sayisi' in data:
        arac.koltuk_sayisi = data['koltuk_sayisi']
    if 'model' in data:
        arac.model = data['model']
    if 'durum' in data:
        arac.durum = data['durum']
    
    db.session.commit()
    return arac

def delete_arac(arac_id):
    arac = get_arac_by_id(arac_id)
    if not arac:
        return {'error': 'Araç bulunamadı'}
    
    db.session.delete(arac)
    db.session.commit()
    return {'message': 'Araç silindi'}

def get_araclar_by_tur(arac_turu):
    return Arac.query.filter_by(arac_turu=arac_turu).all()

# Personel services (moved from kaynak_service.py)
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
    personel = get_personel_by_id(personel_id)
    if not personel:
        return {'error': 'Personel bulunamadı'}
    
    if 'ad' in data:
        personel.ad = data['ad']
    if 'soyad' in data:
        personel.soyad = data['soyad']
    if 'email' in data:
        personel.email = data['email']
    if 'telefon' in data:
        personel.telefon = data['telefon']
    if 'pozisyon' in data:
        personel.pozisyon = data['pozisyon']
    if 'durum' in data:
        personel.durum = data['durum']
    
    db.session.commit()
    return personel

def delete_personel(personel_id):
    personel = get_personel_by_id(personel_id)
    if not personel:
        return {'error': 'Personel bulunamadı'}
    
    db.session.delete(personel)
    db.session.commit()
    return {'message': 'Personel silindi'}

def get_personel_by_pozisyon(pozisyon):
    return Personel.query.filter_by(pozisyon=pozisyon).all()