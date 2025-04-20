from app import db
from datetime import datetime

class Arac(db.Model):
    __tablename__ = 'araclar'
    
    id = db.Column(db.Integer, primary_key=True)
    plaka = db.Column(db.String(20), nullable=False, unique=True)
    arac_turu = db.Column(db.String(50))  # Otobüs, minibüs vb.
    koltuk_sayisi = db.Column(db.Integer)
    model = db.Column(db.String(100))
    durum = db.Column(db.String(50))  # Aktif, bakımda, arızalı vb.
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Arac {self.plaka}>'

class Personel(db.Model):
    __tablename__ = 'personel'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    telefon = db.Column(db.String(20))
    pozisyon = db.Column(db.String(50))  # Şoför, rehber, operatör vb.
    durum = db.Column(db.String(50))  # Aktif, izinde, görevde vb.
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Personel {self.ad} {self.soyad}>'