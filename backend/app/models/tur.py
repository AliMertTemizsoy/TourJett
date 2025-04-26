# backend/app/models/tur.py
from app import db
from datetime import datetime

class Tur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adi = db.Column(db.String(200), nullable=False)
    sure = db.Column(db.String(50), nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    kar = db.Column(db.Float, default=0)  # Tour profit amount
    aciklama = db.Column(db.Text)
    resim = db.Column(db.String(200))
    kategori = db.Column(db.String(100))
    konum_id = db.Column(db.Integer, db.ForeignKey('konum.id'))
    aktif = db.Column(db.Boolean, default=True)
    arac_tipi = db.Column(db.String(100))  # Car type for the tour
    surucu_id = db.Column(db.Integer, db.ForeignKey('surucu.id'))  # Driver assignment
    
    # İlişkiler
    konum = db.relationship('Konum', backref='turlar')
    surucu = db.relationship('Surucu', backref='turlar')
    
    def to_dict(self):
        return {
            'id': self.id,
            'adi': self.adi,
            'sure': self.sure,
            'fiyat': self.fiyat,
            'kar': self.kar,
            'aciklama': self.aciklama,
            'resim': self.resim,
            'kategori': self.kategori,
            'konum': self.konum.ad if self.konum else None,
            'aktif': self.aktif,
            'arac_tipi': self.arac_tipi,
            'surucu': self.surucu.to_dict() if self.surucu else None
        }

class TurSeferi(db.Model):
    __tablename__ = 'tur_seferi'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_id = db.Column(db.Integer, db.ForeignKey('tur.id'), nullable=False)
    baslangic_tarihi = db.Column(db.Date, nullable=False)
    bitis_tarihi = db.Column(db.Date, nullable=False)
    kontenjan = db.Column(db.Integer, default=30)
    kalan_kontenjan = db.Column(db.Integer)
    fiyat = db.Column(db.Float)  # Özel fiyat, null ise tur fiyatı kullanılır
    kar = db.Column(db.Float)  # Tour profit for specific departure
    durum = db.Column(db.String(20), default='aktif')  # aktif, iptal, tamamlandı
    rehber_id = db.Column(db.Integer, db.ForeignKey('rehber.id'))  # Guide assignment
    surucu_id = db.Column(db.Integer, db.ForeignKey('surucu.id'))  # Driver assignment
    
    # İlişkiler
    tur = db.relationship('Tur', backref='seferler')
    rehber = db.relationship('Rehber', backref='tur_seferleri')
    surucu = db.relationship('Surucu', backref='tur_seferleri')
    
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
            'kar': self.kar if self.kar is not None else (self.tur.kar if self.tur else 0),
            'durum': self.durum,
            'rehber_adi': self.rehber.ad if self.rehber else None,
            'surucu': self.surucu.to_dict() if self.surucu else None
        }