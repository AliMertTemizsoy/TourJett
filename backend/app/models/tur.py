# backend/app/models/tur.py
from app import db
from datetime import datetime

class Tur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adi = db.Column(db.String(200), nullable=False)
    sure = db.Column(db.String(50), nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    aciklama = db.Column(db.Text)
    resim = db.Column(db.String(200))
    kategori = db.Column(db.String(100))
    konum_id = db.Column(db.Integer, db.ForeignKey('konum.id'))
    aktif = db.Column(db.Boolean, default=True)
    
    # İlişkiler
    konum = db.relationship('Konum', backref='turlar')
    
    def to_dict(self):
        return {
            'id': self.id,
            'adi': self.adi,
            'sure': self.sure,
            'fiyat': self.fiyat,
            'aciklama': self.aciklama,
            'resim': self.resim,
            'kategori': self.kategori,
            'konum': self.konum.ad if self.konum else None,
            'aktif': self.aktif
        }

class TurSeferi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tur_id = db.Column(db.Integer, db.ForeignKey('tur.id'), nullable=False)
    baslangic_tarihi = db.Column(db.Date, nullable=False)
    bitis_tarihi = db.Column(db.Date, nullable=False)
    kontenjan = db.Column(db.Integer, default=30)
    kalan_kontenjan = db.Column(db.Integer)
    fiyat = db.Column(db.Float)  # Özel fiyat, null ise tur fiyatı kullanılır
    durum = db.Column(db.String(20), default='aktif')  # aktif, iptal, tamamlandı
    
    # İlişkiler
    tur = db.relationship('Tur', backref='seferler')
    
    def __init__(self, **kwargs):
        super(TurSeferi, self).__init__(**kwargs)
        if self.kalan_kontenjan is None and self.kontenjan is not None:
            self.kalan_kontenjan = self.kontenjan
    
    def to_dict(self):
        return {
            'id': self.id,
            'tur_id': self.tur_id,
            'tur_adi': self.tur.adi if self.tur else None,
            'baslangic_tarihi': self.baslangic_tarihi.strftime('%Y-%m-%d'),
            'bitis_tarihi': self.bitis_tarihi.strftime('%Y-%m-%d'),
            'kontenjan': self.kontenjan,
            'kalan_kontenjan': self.kalan_kontenjan,
            'fiyat': self.fiyat if self.fiyat else (self.tur.fiyat if self.tur else None),
            'durum': self.durum
        }

# TurPaketi sınıfını kaldırın veya buradan silin