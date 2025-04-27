from app import db
from datetime import datetime

class Destinasyon(db.Model):
    """
    Cleaned-up Destinasyon model without the 'tur' field.
    """
    __tablename__ = 'destinasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)
    ulke = db.Column(db.String(100))  # Country
    sehir = db.Column(db.String(100))  # City
    adres = db.Column(db.String(200))  # Address
    enlem = db.Column(db.Float)  # Latitude
    boylam = db.Column(db.Float)  # Longitude
    
    # Hierarchical destinations
    parent_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'), nullable=True)
    alt_destinasyonlar = db.relationship('Destinasyon', 
                                         backref=db.backref('ust_destinasyon', remote_side=[id]),
                                         lazy='dynamic')
    
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Destinasyon {self.ad}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'aciklama': self.aciklama,
            'ulke': self.ulke,
            'sehir': self.sehir,
            'adres': self.adres,
            'enlem': self.enlem,
            'boylam': self.boylam,
            'parent_id': self.parent_id,
            'olusturma_tarihi': self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M:%S') if self.olusturma_tarihi else None
        }