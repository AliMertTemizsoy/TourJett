from app import db
from datetime import datetime

class Tur(db.Model):
    """
    Tur model cleaned: Removed rehber_id, surucu_id, kar and arac_tipi.
    """
    id = db.Column(db.Integer, primary_key=True)
    adi = db.Column(db.String(200), nullable=False)
    sure = db.Column(db.String(50), nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    aciklama = db.Column(db.Text)
    resim = db.Column(db.String(200))
    kategori = db.Column(db.String(100))
    destinasyon_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'))
    aktif = db.Column(db.Boolean, default=True)
    
    # Relationships
    destinasyon = db.relationship('Destinasyon', backref='turlar')
    
    def to_dict(self):
        return {
            'id': self.id,
            'adi': self.adi,
            'sure': self.sure,
            'fiyat': self.fiyat,
            'aciklama': self.aciklama,
            'resim': self.resim,
            'kategori': self.kategori,
            'destinasyon': self.destinasyon.ad if self.destinasyon else None,
            'aktif': self.aktif
        }

class TurSeferi(db.Model):
    """
    TurSeferi model.
    """
    __tablename__ = 'tur_seferi'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_id = db.Column(db.Integer, db.ForeignKey('tur.id'), nullable=False)
    baslangic_tarihi = db.Column(db.Date, nullable=False)
    bitis_tarihi = db.Column(db.Date, nullable=False)
    kontenjan = db.Column(db.Integer, default=30)
    kalan_kontenjan = db.Column(db.Integer)
    fiyat = db.Column(db.Float)
    durum = db.Column(db.String(20), default='aktif')
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))  # only vehicle relationship
    
    # Relationships
    tur = db.relationship('Tur', backref='seferler')
    vehicle = db.relationship('Vehicles', backref='tur_seferleri')

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
            'durum': self.durum,
            'vehicle_id': self.vehicle_id,
            'vehicle_info': f"{self.vehicle.model} ({self.vehicle.license_plate})" if self.vehicle else None
        }
