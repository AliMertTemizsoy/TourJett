# backend/app/models/tur_paketi.py
from app import db
from datetime import datetime

class TurPaketi(db.Model):
    __tablename__ = 'tur_paketleri'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)
    sure = db.Column(db.String(50))
    fiyat = db.Column(db.Float, default=0)
    kapasite = db.Column(db.Integer, default=20)
    baslangic_bolge_id = db.Column(db.Integer, db.ForeignKey('bolgeler.id'))
    durum = db.Column(db.String(50), default="Aktif")
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    baslangic_bolge = db.relationship('app.models.bolge.Bolge', foreign_keys=[baslangic_bolge_id])
    tur_destinasyonlar = db.relationship('TurDestinasyon', 
                                        backref='tur_paketi', 
                                        lazy=True, 
                                        cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<TurPaketi {self.ad}>'


class TurDestinasyon(db.Model):
    __tablename__ = 'tur_destinasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_paketi_id = db.Column(db.Integer, db.ForeignKey('tur_paketleri.id'), nullable=False)
    destinasyon_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'), nullable=False)
    siralama = db.Column(db.Integer, default=0)
    kalma_suresi = db.Column(db.Integer)
    not_bilgisi = db.Column(db.Text)
    
    # İlişkiler
    destinasyon = db.relationship('app.models.bolge.Destinasyon', foreign_keys=[destinasyon_id])
    
    def __repr__(self):
        return f'<TurDestinasyon {self.id}>'