from app import db

class Tur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adi = db.Column(db.String(200), nullable=False)
    sure = db.Column(db.String(50), nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    aciklama = db.Column(db.Text)
    resim = db.Column(db.String(200))
    kategori = db.Column(db.String(100))
    konum_id = db.Column(db.Integer, db.ForeignKey('konum.id'))
    aktif = db.Column(db.Boolean, default=True)
    
    # İlişkiler
    konum = db.relationship('Konum', backref='turlar')
    
    def to_dict(self):
        return {
            'id': self.id,
            'adi': self.adi,
            'sure': self.sure,
            'fiyat': self.fiyat,
            'aciklama': self.aciklama,
            'resim': self.resim,
            'kategori': self.kategori,
            'konum': self.konum.ad if self.konum else None,
            'aktif': self.aktif
        }