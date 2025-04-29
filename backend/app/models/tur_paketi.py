# backend/app/models/tur_paketi.py
from app import db
from datetime import datetime

class TurPaketi(db.Model):
    __tablename__ = 'tur_paketleri'

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)
    sure = db.Column(db.String(50))
    kapasite = db.Column(db.Integer, default=20)
    destinasyon_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'), nullable=True)
    durum = db.Column(db.String(50), default="Aktif")
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    surucu_id = db.Column(db.Integer, db.ForeignKey('surucu.id'), nullable=True)
    rehber_id = db.Column(db.Integer, db.ForeignKey('rehber.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    tur_id = db.Column(db.Integer, db.ForeignKey('tur.id'), nullable=True)  # ✅ Added reference to Tur model

    tur_tarihi = db.Column(db.Date, nullable=True)
    resim_url = db.Column(db.String(255), nullable=True)
    destinasyon_detay = db.Column(db.String(100), nullable=True)

    # Relationships
    destinasyon = db.relationship('Destinasyon', foreign_keys=[destinasyon_id])
    surucu = db.relationship('Surucu', backref='tur_paketleri')
    rehber = db.relationship('Rehber', backref='tur_paketleri')
    vehicle = db.relationship('Vehicles', backref='tur_paketleri')  
    tur = db.relationship('Tur', backref='tur_paketleri')  # ✅ Added relationship with Tur model

    def __repr__(self):
        return f'<TurPaketi {self.ad}>'

    def to_dict(self):
        """Model verilerini JSON formatında döndürür"""
        return {
            'id': self.id,
            'ad': self.ad,
            'aciklama': self.aciklama,
            'sure': self.sure,
            'kapasite': self.kapasite,
            'destinasyon_detay': self.destinasyon_detay,
            'tur_tarihi': self.tur_tarihi.strftime('%Y-%m-%d') if self.tur_tarihi else None,
            'resim_url': self.resim_url,
            'durum': self.durum,
            'destinasyon_id': self.destinasyon_id,
            'surucu_id': self.surucu_id,
            'rehber_id': self.rehber_id,
            'vehicle_id': self.vehicle_id,
            'tur_id': self.tur_id,
            'surucu': self.surucu.to_dict() if self.surucu else None,
            'rehber': self.rehber.to_dict() if self.rehber else None,
            'vehicle': self.vehicle.to_dict() if self.vehicle else None,
            'tur': self.tur.to_dict() if self.tur else None  # ✅ Added tur to the dictionary output
        }


class TurDestinasyon(db.Model):
    __tablename__ = 'tur_destinasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_paketi_id = db.Column(db.Integer, db.ForeignKey('tur_paketleri.id'), nullable=False)
    destinasyon_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'), nullable=False)
    siralama = db.Column(db.Integer, default=0)
    kalma_suresi = db.Column(db.Integer)
    not_bilgisi = db.Column(db.Text)

    destinasyon = db.relationship('Destinasyon', foreign_keys=[destinasyon_id])

    def __repr__(self):
        return f'<TurDestinasyon {self.id}>'
        
    def to_dict(self):
        """Model verilerini JSON formatında döndürür"""
        return {
            'id': self.id,
            'tur_paketi_id': self.tur_paketi_id,
            'destinasyon_id': self.destinasyon_id,
            'siralama': self.siralama,
            'kalma_suresi': self.kalma_suresi,
            'not_bilgisi': self.not_bilgisi,
            'destinasyon': self.destinasyon.to_dict() if self.destinasyon else None
        }