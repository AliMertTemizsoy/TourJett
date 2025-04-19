from app import db
from datetime import datetime

class Bolge(db.Model):
    __tablename__ = 'bolgeler'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)
    ulke = db.Column(db.String(100))
    sehir = db.Column(db.String(100))
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Bolge {self.ad}>'

class Destinasyon(db.Model):
    __tablename__ = 'destinasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    bolge_id = db.Column(db.Integer, db.ForeignKey('bolgeler.id'), nullable=False)
    ad = db.Column(db.String(100), nullable=False)
    tur = db.Column(db.String(50))  # Otel, plaj, müze, tarihi yer vb.
    aciklama = db.Column(db.Text)
    adres = db.Column(db.String(200))
    fiyat = db.Column(db.Float)
    enlem = db.Column(db.Float)
    boylam = db.Column(db.Float)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    bolge = db.relationship('Bolge', backref='destinasyonlar')
    
    def __repr__(self):
        return f'<Destinasyon {self.ad}>'