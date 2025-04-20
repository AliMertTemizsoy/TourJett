from app import db
from datetime import datetime

class Musteri(db.Model):
    __tablename__ = 'musteriler'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    telefon = db.Column(db.String(20))
    adres = db.Column(db.String(200))
    tc_kimlik = db.Column(db.String(11))
    dogum_tarihi = db.Column(db.Date)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    rezervasyonlar = db.relationship('Rezervasyon', backref='musteri', lazy=True)
    
    def __repr__(self):
        return f'<Musteri {self.ad} {self.soyad}>'

class Rezervasyon(db.Model):
    __tablename__ = 'rezervasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'), nullable=False)
    tur_seferi_id = db.Column(db.Integer, db.ForeignKey('tur_seferleri.id'), nullable=False)
    kisi_sayisi = db.Column(db.Integer, default=1)
    toplam_fiyat = db.Column(db.Float)
    rezervasyon_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    durum = db.Column(db.String(50))  # Onaylandı, beklemede, iptal edildi vb.
    odeme_durumu = db.Column(db.String(50))  # Ödendi, beklemede, kısmi ödeme vb.
    
    tur_seferi = db.relationship('TurSeferi')
    
    def __repr__(self):
        return f'<Rezervasyon {self.id}>'