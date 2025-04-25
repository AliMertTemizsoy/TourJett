# backend/app/models/rezervasyon.py
from app import db
from datetime import datetime

class Rezervasyon(db.Model):
    __tablename__ = 'rezervasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_id = db.Column(db.Integer, db.ForeignKey('tur.id'), nullable=False)
    tur_sefer_id = db.Column(db.Integer, db.ForeignKey('tur_seferi.id'), nullable=True)  # Tur seferi ilişkisi eklendi
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'), nullable=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    tarih = db.Column(db.Date, nullable=False)
    kisi_sayisi = db.Column(db.Integer, nullable=False)
    oda_tipi = db.Column(db.String(50))
    ozel_istekler = db.Column(db.Text)
    durum = db.Column(db.String(20), default='onay_bekliyor')
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    tur = db.relationship('Tur', backref='rezervasyonlar')
    tur_seferi = db.relationship('TurSeferi', backref='rezervasyonlar')  # Yeni ilişki
    musteri = db.relationship('Musteri', backref='rezervasyonlar')
    
    def to_dict(self):
        return {
            'id': self.id,
            'tur_id': self.tur_id,
            'tur_sefer_id': self.tur_sefer_id,  # Yeni alan
            'ad': self.ad,
            'soyad': self.soyad,
            'email': self.email,
            'telefon': self.telefon,
            'tarih': self.tarih.strftime('%Y-%m-%d') if self.tarih else None,
            'kisi_sayisi': self.kisi_sayisi,
            'oda_tipi': self.oda_tipi,
            'ozel_istekler': self.ozel_istekler,
            'durum': self.durum,
            'olusturma_tarihi': self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M:%S')
        }