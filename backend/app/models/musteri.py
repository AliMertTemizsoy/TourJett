from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Musteri(db.Model):
    __tablename__ = 'musteriler'
    
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Şifre hash'i ekleyin
    telefon = db.Column(db.String(20), nullable=True)
    adres = db.Column(db.String(200))
    tc_kimlik = db.Column(db.String(11))
    dogum_tarihi = db.Column(db.Date)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Musteri {self.ad} {self.soyad}>'
    
    def set_password(self, password):
        """Şifreyi hash'leyerek saklar."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Verilen şifre ile hash'i karşılaştırır."""
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False

    def to_dict(self):
        """Müşteri bilgilerini API yanıtı için dict'e dönüştürür."""
        return {
            'id': self.id,
            'ad': self.ad,
            'soyad': self.soyad,
            'email': self.email,
            'telefon': self.telefon,
            'adres': self.adres,
            'tc_kimlik': self.tc_kimlik,
            'dogum_tarihi': self.dogum_tarihi.strftime('%Y-%m-%d') if self.dogum_tarihi else None,
            'olusturma_tarihi': self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M:%S')
        }