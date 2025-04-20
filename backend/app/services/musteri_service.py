from app import db
from app.models.musteri import Musteri, Rezervasyon
from app.models.tur import TurSeferi
from datetime import datetime

# Müşteri servisleri
def get_all_musteriler():
    return Musteri.query.all()

def get_musteri_by_id(musteri_id):
    return Musteri.query.get(musteri_id)

def get_musteri_by_email(email):
    return Musteri.query.filter_by(email=email).first()

def create_musteri(data):
    # Email benzersizliğini kontrol et
    email = data.get('email')
    if email and get_musteri_by_email(email):
        return {'error': 'Bu email adresi zaten kullanılıyor'}
    
    yeni_musteri = Musteri(
        ad=data.get('ad'),
        soyad=data.get('soyad'),
        email=email,
        telefon=data.get('telefon'),
        adres=data.get('adres'),
        tc_kimlik=data.get('tc_kimlik'),
        dogum_tarihi=data.get('dogum_tarihi')
    )
    
    db.session.add(yeni_musteri)
    db.session.commit()
    return yeni_musteri

def update_musteri(musteri_id, data):
    musteri = Musteri.query.get(musteri_id)
    if not musteri:
        return {'error': 'Müşteri bulunamadı'}
    
    # Email değiştiriliyorsa benzersizliğini kontrol et
    if 'email' in data and data['email'] != musteri.email:
        if get_musteri_by_email(data['email']):
            return {'error': 'Bu email adresi zaten kullanılıyor'}
    
    musteri.ad = data.get('ad', musteri.ad)
    musteri.soyad = data.get('soyad', musteri.soyad)
    musteri.email = data.get('email', musteri.email)
    musteri.telefon = data.get('telefon', musteri.telefon)
    musteri.adres = data.get('adres', musteri.adres)
    musteri.tc_kimlik = data.get('tc_kimlik', musteri.tc_kimlik)
    
    if 'dogum_tarihi' in data:
        musteri.dogum_tarihi = data['dogum_tarihi']
    
    db.session.commit()
    return {'message': 'Müşteri bilgileri güncellendi'}

def delete_musteri(musteri_id):
    musteri = Musteri.query.get(musteri_id)
    if not musteri:
        return {'error': 'Müşteri bulunamadı'}
    
    # Müşterinin rezervasyonlarını kontrol et
    if musteri.rezervasyonlar:
        return {'error': 'Bu müşteriye ait rezervasyonlar var, önce rezervasyonları silin'}
    
    db.session.delete(musteri)
    db.session.commit()
    return {'message': 'Müşteri silindi'}

# Rezervasyon servisleri
def get_all_rezervasyonlar():
    return Rezervasyon.query.all()

def get_rezervasyon_by_id(rezervasyon_id):
    return Rezervasyon.query.get(rezervasyon_id)

def get_rezervasyonlar_by_musteri(musteri_id):
    return Rezervasyon.query.filter_by(musteri_id=musteri_id).all()

def get_rezervasyonlar_by_sefer(tur_seferi_id):
    return Rezervasyon.query.filter_by(tur_seferi_id=tur_seferi_id).all()

def create_rezervasyon(data):
    # Müşteri ve tur seferinin varlığını kontrol et
    musteri_id = data.get('musteri_id')
    tur_seferi_id = data.get('tur_seferi_id')
    
    musteri = Musteri.query.get(musteri_id)
    if not musteri:
        return {'error': 'Müşteri bulunamadı'}
    
    tur_seferi = TurSeferi.query.get(tur_seferi_id)
    if not tur_seferi:
        return {'error': 'Tur seferi bulunamadı'}
    
    # Sefer kapasitesini kontrol et
    kisi_sayisi = data.get('kisi_sayisi', 1)
    mevcut_rezervasyonlar = get_rezervasyonlar_by_sefer(tur_seferi_id)
    toplam_kisi = sum(r.kisi_sayisi for r in mevcut_rezervasyonlar)
    
    if tur_seferi.tur_paketi and (toplam_kisi + kisi_sayisi) > tur_seferi.tur_paketi.kapasite:
        return {'error': 'Sefer kapasitesi dolu'}
    
    # Toplam fiyatı hesapla
    tur_fiyati = tur_seferi.tur_paketi.fiyat if tur_seferi.tur_paketi else 0
    toplam_fiyat = tur_fiyati * kisi_sayisi
    
    yeni_rezervasyon = Rezervasyon(
        musteri_id=musteri_id,
        tur_seferi_id=tur_seferi_id,
        kisi_sayisi=kisi_sayisi,
        toplam_fiyat=toplam_fiyat,
        durum=data.get('durum', 'Onaylandı'),
        odeme_durumu=data.get('odeme_durumu', 'Beklemede')
    )
    
    db.session.add(yeni_rezervasyon)
    db.session.commit()
    return yeni_rezervasyon

def update_rezervasyon(rezervasyon_id, data):
    rezervasyon = Rezervasyon.query.get(rezervasyon_id)
    if not rezervasyon:
        return {'error': 'Rezervasyon bulunamadı'}
    
    # Kişi sayısı değiştiriliyorsa, kapasite kontrolü yap
    if 'kisi_sayisi' in data and data['kisi_sayisi'] != rezervasyon.kisi_sayisi:
        tur_seferi = rezervasyon.tur_seferi
        if tur_seferi and tur_seferi.tur_paketi:
            mevcut_rezervasyonlar = get_rezervasyonlar_by_sefer(rezervasyon.tur_seferi_id)
            toplam_kisi = sum(r.kisi_sayisi for r in mevcut_rezervasyonlar if r.id != rezervasyon_id)
            
            if (toplam_kisi + data['kisi_sayisi']) > tur_seferi.tur_paketi.kapasite:
                return {'error': 'Sefer kapasitesi dolu'}
                
            # Toplam fiyatı güncelle
            tur_fiyati = tur_seferi.tur_paketi.fiyat
            rezervasyon.toplam_fiyat = tur_fiyati * data['kisi_sayisi']
            
        rezervasyon.kisi_sayisi = data['kisi_sayisi']
    
    rezervasyon.durum = data.get('durum', rezervasyon.durum)
    rezervasyon.odeme_durumu = data.get('odeme_durumu', rezervasyon.odeme_durumu)
    
    db.session.commit()
    return {'message': 'Rezervasyon güncellendi'}

def delete_rezervasyon(rezervasyon_id):
    rezervasyon = Rezervasyon.query.get(rezervasyon_id)
    if not rezervasyon:
        return {'error': 'Rezervasyon bulunamadı'}
    
    db.session.delete(rezervasyon)
    db.session.commit()
    return {'message': 'Rezervasyon silindi'}