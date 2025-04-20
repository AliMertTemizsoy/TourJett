from app import db
from datetime import datetime

class Degerlendirme(db.Model):
    __tablename__ = 'degerlendirmeler'
    
    id = db.Column(db.Integer, primary_key=True)
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'), nullable=False)
    tur_paketi_id = db.Column(db.Integer, db.ForeignKey('tur_paketleri.id'), nullable=False)
    puan = db.Column(db.Integer)  # 1-5 arası puanlama
    yorum = db.Column(db.Text)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    musteri = db.relationship('Musteri')
    tur_paketi = db.relationship('TurPaketi')
    
    def __repr__(self):
        return f'<Degerlendirme {self.id}>'