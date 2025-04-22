# backend/app/models/musteri.py
from app import db
from datetime import datetime

class Musteri(db.Model):
    __tablename__ = 'musteriler'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=True)  # unique ve nullable değiştirildi
    telefon = db.Column(db.String(20), nullable=True)  # nullable=True eklendi
    adres = db.Column(db.String(200))
    tc_kimlik = db.Column(db.String(11))
    dogum_tarihi = db.Column(db.Date)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Rezervasyon ilişkisini artık burada tanımlamayacağız
    # Rezervasyonlar Rezervasyon modelinde tanımlanacak
    
    def __repr__(self):
        return f'<Musteri {self.ad} {self.soyad}>'

# Not: Eski Rezervasyon sınıfını kaldırıyoruz
# class Rezervasyon(db.Model): ...