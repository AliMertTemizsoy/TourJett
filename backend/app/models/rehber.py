# backend/app/models/rehber.py
from app import db
from datetime import datetime

class Rehber(db.Model):
    __tablename__ = 'rehber'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    telefon = db.Column(db.String(20))
    dil_bilgisi = db.Column(db.String(200))  # Dil bilgisi, örn: "Türkçe, İngilizce, Almanca"
    deneyim_yili = db.Column(db.Integer, default=0)
    aciklama = db.Column(db.Text)
    aktif = db.Column(db.Boolean, default=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Rehber {self.ad} {self.soyad}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'soyad': self.soyad,
            'email': self.email,
            'telefon': self.telefon,
            'dil_bilgisi': self.dil_bilgisi,
            'deneyim_yili': self.deneyim_yili,
            'aciklama': self.aciklama,
            'aktif': self.aktif,
            'olusturma_tarihi': self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M:%S')
        }