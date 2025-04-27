# backend/app/models/surucu.py
from app import db
from datetime import datetime

class Surucu(db.Model):
    __tablename__ = 'surucu'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    telefon = db.Column(db.String(20), nullable=False)
    ehliyet_no = db.Column(db.String(50), nullable=False)
    ehliyet_sinifi = db.Column(db.String(20)) # A, B, C, D, E etc.
    deneyim_yil = db.Column(db.Integer, default=0)
    dogum_tarihi = db.Column(db.Date)
    adres = db.Column(db.Text)
    uyruk = db.Column(db.String(50))
    aktif = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Surucu {self.ad} {self.soyad}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'soyad': self.soyad,
            'tam_ad': f"{self.ad} {self.soyad}",
            'email': self.email,
            'telefon': self.telefon,
            'ehliyet_no': self.ehliyet_no,
            'ehliyet_sinifi': self.ehliyet_sinifi,
            'deneyim_yil': self.deneyim_yil,
            'dogum_tarihi': self.dogum_tarihi.strftime('%Y-%m-%d') if self.dogum_tarihi else None,
            'adres': self.adres,
            'uyruk': self.uyruk,
            'aktif': self.aktif,
            'olusturma_tarihi': self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M:%S')
        }