from app import db
from datetime import datetime

class TurPaketi(db.Model):
    __tablename__ = 'tur_paketleri'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(200), nullable=False)
    aciklama = db.Column(db.Text)
    fiyat = db.Column(db.Float, nullable=False)
    sure = db.Column(db.Integer)  # Gün sayısı
    kapasite = db.Column(db.Integer)
    baslangic_bolge_id = db.Column(db.Integer, db.ForeignKey('bolgeler.id'))
    durum = db.Column(db.String(50))  # Aktif, pasif, dolu vb.
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    baslangic_bolge = db.relationship('Bolge')
    destinasyonlar = db.relationship('TurDestinasyon', backref='tur_paketi', lazy=True)
    seferler = db.relationship('TurSeferi', backref='tur_paketi', lazy=True)
    
    def __repr__(self):
        return f'<TurPaketi {self.ad}>'

class TurDestinasyon(db.Model):
    __tablename__ = 'tur_destinasyonlar'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_paketi_id = db.Column(db.Integer, db.ForeignKey('tur_paketleri.id'), nullable=False)
    destinasyon_id = db.Column(db.Integer, db.ForeignKey('destinasyonlar.id'), nullable=False)
    siralama = db.Column(db.Integer)  # Tur içindeki sıralama
    kalma_suresi = db.Column(db.Integer)  # Saat cinsinden
    
    destinasyon = db.relationship('Destinasyon')
    
    def __repr__(self):
        return f'<TurDestinasyon {self.id}>'

class TurSeferi(db.Model):
    __tablename__ = 'tur_seferleri'
    
    id = db.Column(db.Integer, primary_key=True)
    tur_paketi_id = db.Column(db.Integer, db.ForeignKey('tur_paketleri.id'), nullable=False)
    baslangic_tarihi = db.Column(db.DateTime, nullable=False)
    bitis_tarihi = db.Column(db.DateTime, nullable=False)
    arac_id = db.Column(db.Integer, db.ForeignKey('araclar.id'))
    rehber_id = db.Column(db.Integer, db.ForeignKey('personel.id'))
    sofor_id = db.Column(db.Integer, db.ForeignKey('personel.id'))
    durum = db.Column(db.String(50))  # Planlandı, başladı, tamamlandı, iptal vb.
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    arac = db.relationship('Arac', foreign_keys=[arac_id])
    rehber = db.relationship('Personel', foreign_keys=[rehber_id])
    sofor = db.relationship('Personel', foreign_keys=[sofor_id])
    
    def __repr__(self):
        return f'<TurSeferi {self.id}>'