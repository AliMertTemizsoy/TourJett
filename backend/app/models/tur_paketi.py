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
    kapasite = db.Column(db.Integer, default=20)
    baslangic_bolge_id = db.Column(db.Integer, db.ForeignKey('bolgeler.id'), nullable=True)  # nullable=True ekleyin
    durum = db.Column(db.String(50), default="Aktif")
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    # JSON format için ekleyin
    tur_tarihi = db.Column(db.Date, nullable=True)  # Nullable olarak ekleyin
    resim_url = db.Column(db.String(255), nullable=True)  # Resim URL'si için
    konum = db.Column(db.String(100), nullable=True)  # Frontend'in kullandığı konum alanı
    max_katilimci = db.Column(db.Integer, default=20)  # max_katilimci alanını ekleyin

    # İlişkiler
    baslangic_bolge = db.relationship('Bolge', foreign_keys=[baslangic_bolge_id])
    tur_destinasyonlar = db.relationship('TurDestinasyon', 
                                        backref='tur_paketi', 
                                        lazy=True, 
                                        cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<TurPaketi {self.ad}>'
    def to_dict(self):
        """Model verilerini JSON'a uygun sözlük olarak döndürür"""
        return {
            'id': self.id,
            'ad': self.ad,
            'aciklama': self.aciklama,
            'sure': self.sure,
            'fiyat': float(self.fiyat),
            'kapasite': self.kapasite,
            'konum': self.konum,
            'max_katilimci': self.max_katilimci,
            'tur_tarihi': self.tur_tarihi.strftime('%Y-%m-%d') if self.tur_tarihi else None,
            'resim_url': self.resim_url,
            'durum': self.durum,
            'baslangic_bolge_id': self.baslangic_bolge_id
        }

class TurDestinasyon(db.Model):
    __tablename__ = 'tur_destinasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_paketi_id = db.Column(db.Integer, db.ForeignKey('tur_paketleri.id'), nullable=False)
    destinasyon_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'), nullable=False)
    siralama = db.Column(db.Integer, default=0)
    kalma_suresi = db.Column(db.Integer)
    not_bilgisi = db.Column(db.Text)
    
   # İlişkiler
    destinasyon = db.relationship('Destinasyon', foreign_keys=[destinasyon_id])
    def __repr__(self):
        return f'<TurDestinasyon {self.id}>'