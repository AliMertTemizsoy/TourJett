from app import db

class Konum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    ulke = db.Column(db.String(100))
    aciklama = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ad': self.ad,
            'ulke': self.ulke,
            'aciklama': self.aciklama
        }