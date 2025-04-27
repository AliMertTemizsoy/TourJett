# backend/app/models/degerlendirme.py
from app import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class Degerlendirme(db.Model):
    __tablename__ = 'degerlendirmeler'
    
    id = db.Column(db.Integer, primary_key=True)
    musteri_id = db.Column(db.Integer, db.ForeignKey('musteriler.id'), nullable=False)
    tur_paketi_id = db.Column(db.Integer, db.ForeignKey('tur_paketleri.id'), nullable=True)
    tur_id = db.Column(db.Integer, db.ForeignKey('tur.id'), nullable=True)
    puan = db.Column(db.Integer)  # 1-5 arası puanlama
    yorum = db.Column(db.Text)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkileri tam modül yoluyla tanımlayın
    musteri = db.relationship('app.models.musteri.Musteri')
    tur_paketi = db.relationship('app.models.tur_paketi.TurPaketi')
    tur = db.relationship('app.models.tur.Tur')
    
    def __repr__(self):
        return f'<Degerlendirme {self.id}>'
    
    # Her değerlendirmenin ya tur_id ya da tur_paketi_id'sine sahip olması gerekmektedir
    __table_args__ = (
        db.CheckConstraint('(tur_paketi_id IS NOT NULL) OR (tur_id IS NOT NULL)', name='check_degerlendirme_tur_relation'),
    )
    
    @hybrid_property
    def tur_adi(self):
        """Değerlendirmenin hangi tura ait olduğunu döndürür"""
        if self.tur_paketi:
            return self.tur_paketi.ad
        elif self.tur:
            return self.tur.adi
        return None