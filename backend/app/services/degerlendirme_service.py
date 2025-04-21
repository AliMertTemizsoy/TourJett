from app import db
from app.models.degerlendirme import Degerlendirme
from app.models.musteri import Musteri
from app.models.tur_paketi import TurPaketi

def get_all_degerlendirmeler():
    return Degerlendirme.query.all()

def get_degerlendirme_by_id(degerlendirme_id):
    return Degerlendirme.query.get(degerlendirme_id)

def get_degerlendirmeler_by_tur(tur_paketi_id):
    return Degerlendirme.query.filter_by(tur_paketi_id=tur_paketi_id).all()

def get_degerlendirmeler_by_musteri(musteri_id):
    return Degerlendirme.query.filter_by(musteri_id=musteri_id).all()

def create_degerlendirme(data):
    # Müşteri ve tur paketinin varlığını kontrol et
    musteri_id = data.get('musteri_id')
    tur_paketi_id = data.get('tur_paketi_id')
    
    musteri = Musteri.query.get(musteri_id)
    if not musteri:
        return {'error': 'Müşteri bulunamadı'}
        
    tur_paketi = TurPaketi.query.get(tur_paketi_id)
    if not tur_paketi:
        return {'error': 'Tur paketi bulunamadı'}
    
    # Puanlamayı kontrol et (1-5 arası olmalı)
    puan = data.get('puan')
    if puan is not None and (puan < 1 or puan > 5):
        return {'error': 'Puan 1 ile 5 arasında olmalıdır'}
    
    # Müşterinin aynı tur paketi için daha önce değerlendirme yapıp yapmadığını kontrol et
    mevcut_degerlendirme = Degerlendirme.query.filter_by(
        musteri_id=musteri_id, 
        tur_paketi_id=tur_paketi_id
    ).first()
    
    if mevcut_degerlendirme:
        return {'error': 'Bu tur paketi için zaten bir değerlendirme yapmışsınız'}
    
    yeni_degerlendirme = Degerlendirme(
        musteri_id=musteri_id,
        tur_paketi_id=tur_paketi_id,
        puan=puan,
        yorum=data.get('yorum')
    )
    
    db.session.add(yeni_degerlendirme)
    db.session.commit()
    
    return yeni_degerlendirme

def update_degerlendirme(degerlendirme_id, data):
    degerlendirme = Degerlendirme.query.get(degerlendirme_id)
    if not degerlendirme:
        return {'error': 'Değerlendirme bulunamadı'}
    
    # Puanlamayı kontrol et (1-5 arası olmalı)
    if 'puan' in data:
        puan = data['puan']
        if puan < 1 or puan > 5:
            return {'error': 'Puan 1 ile 5 arasında olmalıdır'}
        degerlendirme.puan = puan
    
    if 'yorum' in data:
        degerlendirme.yorum = data['yorum']
    
    db.session.commit()
    return {'message': 'Değerlendirme güncellendi'}

def delete_degerlendirme(degerlendirme_id):
    degerlendirme = Degerlendirme.query.get(degerlendirme_id)
    if not degerlendirme:
        return {'error': 'Değerlendirme bulunamadı'}
    
    db.session.delete(degerlendirme)
    db.session.commit()
    return {'message': 'Değerlendirme silindi'}

def get_tur_ortalama_puan(tur_paketi_id):
    degerlendirmeler = get_degerlendirmeler_by_tur(tur_paketi_id)
    if not degerlendirmeler:
        return {'tur_paketi_id': tur_paketi_id, 'ortalama_puan': 0, 'degerlendirme_sayisi': 0}
    
    toplam_puan = sum(d.puan for d in degerlendirmeler if d.puan is not None)
    degerlendirme_sayisi = len([d for d in degerlendirmeler if d.puan is not None])
    
    if degerlendirme_sayisi == 0:
        ortalama_puan = 0
    else:
        ortalama_puan = toplam_puan / degerlendirme_sayisi
    
    return {
        'tur_paketi_id': tur_paketi_id,
        'ortalama_puan': ortalama_puan,
        'degerlendirme_sayisi': degerlendirme_sayisi
    }