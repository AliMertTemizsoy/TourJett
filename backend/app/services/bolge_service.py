from app.models.bolge import Bolge, Destinasyon
from app import db

def get_all_bolgeler():
    """Tüm bölgeleri getirir"""
    return Bolge.query.all()

def get_bolge_by_id(bolge_id):
    """ID'ye göre bölge getirir"""
    return Bolge.query.get(bolge_id)

def create_bolge(data):
    """Yeni bölge oluşturur"""
    yeni_bolge = Bolge(
        ad=data['ad'],
        aciklama=data.get('aciklama', ''),
        ulke=data.get('ulke', ''),
        sehir=data.get('sehir', '')
    )
    
    db.session.add(yeni_bolge)
    db.session.commit()
    return yeni_bolge