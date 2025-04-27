# backend/app/models/tur_paketi.py
from app import db
from datetime import datetime

# backend/app/models/tur_paketi.py
from app import db
from datetime import datetime

class TurPaketi(db.Model):
    __tablename__ = 'tur_paketleri'

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)
    sure = db.Column(db.String(50))
    fiyat = db.Column(db.Float, nullable=False, default=0)
    kar = db.Column(db.Float, nullable=False, default=0)
    kapasite = db.Column(db.Integer, default=20)
    baslangic_destinasyon_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'), nullable=True)
    durum = db.Column(db.String(50), default="Aktif")
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    surucu_id = db.Column(db.Integer, db.ForeignKey('surucu.id'), nullable=True)
    rehber_id = db.Column(db.Integer, db.ForeignKey('rehber.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)  # ✅ NEW required field

    tur_tarihi = db.Column(db.Date, nullable=True)
    resim_url = db.Column(db.String(255), nullable=True)
    destinasyon_detay = db.Column(db.String(100), nullable=True)
    max_katilimci = db.Column(db.Integer, default=20)

    # Relationships
    baslangic_destinasyon = db.relationship('Destinasyon', foreign_keys=[baslangic_destinasyon_id])
    surucu = db.relationship('Surucu', backref='tur_paketleri')
    rehber = db.relationship('Rehber', backref='tur_paketleri')
    vehicle = db.relationship('Vehicles', backref='tur_paketleri')  # ✅ New relationship
    tur_destinasyonlar = db.relationship(
        'TurDestinasyon',
        backref='tur_paketi',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<TurPaketi {self.ad}>'

    def to_dict(self):
        """Model verilerini JSON formatında döndürür"""
        return {
            'id': self.id,
            'ad': self.ad,
            'aciklama': self.aciklama,
            'sure': self.sure,
            'fiyat': float(self.fiyat),
            'kar': float(self.kar),
            'kapasite': self.kapasite,
            'destinasyon_detay': self.destinasyon_detay,
            'max_katilimci': self.max_katilimci,
            'tur_tarihi': self.tur_tarihi.strftime('%Y-%m-%d') if self.tur_tarihi else None,
            'resim_url': self.resim_url,
            'durum': self.durum,
            'baslangic_destinasyon_id': self.baslangic_destinasyon_id,
            'surucu': self.surucu.to_dict() if self.surucu else None,
            'rehber': self.rehber.to_dict() if self.rehber else None,
            'vehicle': self.vehicle.to_dict() if self.vehicle else None  # ✅ Include vehicle in output
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
