from app import db
from app.models.tur_paketi import TurPaketi
from app.models.tur import Tur
from app.models.destinasyon import Destinasyon
from app.models.rehber import Rehber
from app.models.surucu import Surucu
from app.models.vehicle import Vehicle
from app.models.rezervasyon import Rezervasyon
from app.models.degerlendirme import Degerlendirme
from app.models.musteri import Musteri

def temizle():
    """Veritabanındaki tüm kayıtları temizler ama tabloları korur."""
    print("Veritabanı temizleme işlemi başlatılıyor...")
    
    # Rezervasyonları ve değerlendirmeleri önce silmek gerekiyor (yabancı anahtar kısıtlamaları nedeniyle)
    print("Rezervasyonlar temizleniyor...")
    Rezervasyon.query.delete()
    
    print("Değerlendirmeler temizleniyor...")
    Degerlendirme.query.delete()
    
    print("Tur paketleri temizleniyor...")
    TurPaketi.query.delete()
    
    print("Turlar temizleniyor...")
    Tur.query.delete()
    
    print("Rehberler temizleniyor...")
    Rehber.query.delete()
    
    print("Sürücüler temizleniyor...")
    Surucu.query.delete()
    
    print("Araçlar temizleniyor...")
    Vehicle.query.delete()
    
    print("Destinasyonlar temizleniyor...")
    Destinasyon.query.delete()
    
    print("Müşteriler temizleniyor...")
    Musteri.query.delete()
    
    # Değişiklikleri kaydet
    db.session.commit()
    
    print("Veritabanı başarıyla temizlendi!")
    print("Uygulamayı yeniden başlatmanız önerilir.")

if __name__ == "__main__":
    temizle() 