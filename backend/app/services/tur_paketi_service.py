# backend/app/services/tur_paketi_service.py
from app import db
from app.models.tur_paketi import TurPaketi, TurDestinasyon
from app.models.bolge import Destinasyon

def get_all_tur_paketleri(aktif_filtresi=True):
    """Tüm tur paketlerini getirir"""
    if aktif_filtresi:
        return TurPaketi.query.filter_by(durum="Aktif").all()
    return TurPaketi.query.all()

def get_tur_paketi_by_id(id):
    """ID'ye göre tur paketi getirir"""
    return TurPaketi.query.get(id)

def create_tur_paketi(data):
    """Yeni tur paketi oluşturur"""
    # Baslangic bölgesinin varlığını kontrol et
    baslangic_bolge_id = data.get('baslangic_bolge_id')
    
    yeni_tur = TurPaketi(
        ad=data.get('ad'),
        aciklama=data.get('aciklama'),
        sure=data.get('sure'),
        fiyat=data.get('fiyat', 0),
        kapasite=data.get('kapasite', 20),
        baslangic_bolge_id=baslangic_bolge_id,
        durum=data.get('durum', 'Aktif')
    )
    
    db.session.add(yeni_tur)
    db.session.commit()
    
    # Eğer destinasyonlar verilmişse, ekle
    destinasyonlar = data.get('destinasyonlar', [])
    for i, dest_data in enumerate(destinasyonlar):
        dest_id = dest_data.get('destinasyon_id')
        # Destinasyonun varlığını kontrol et
        destinasyon = Destinasyon.query.get(dest_id)
        if not destinasyon:
            continue
            
        tur_dest = TurDestinasyon(
            tur_paketi_id=yeni_tur.id,
            destinasyon_id=dest_id,
            siralama=i + 1,
            kalma_suresi=dest_data.get('kalma_suresi', 24),
            not_bilgisi=dest_data.get('not_bilgisi', '')
        )
        db.session.add(tur_dest)
    
    db.session.commit()
    return yeni_tur

def update_tur_paketi(id, data):
    """Tur paketini günceller"""
    tur = TurPaketi.query.get(id)
    if not tur:
        return {'error': 'Tur paketi bulunamadı'}
    
    tur.ad = data.get('ad', tur.ad)
    tur.aciklama = data.get('aciklama', tur.aciklama)
    tur.sure = data.get('sure', tur.sure)
    tur.fiyat = data.get('fiyat', tur.fiyat)
    tur.kapasite = data.get('kapasite', tur.kapasite)
    tur.durum = data.get('durum', tur.durum)
    
    if 'baslangic_bolge_id' in data:
        tur.baslangic_bolge_id = data['baslangic_bolge_id']
    
    # Destinasyonları güncelle
    if 'destinasyonlar' in data:
        # Mevcut destinasyonları temizle
        TurDestinasyon.query.filter_by(tur_paketi_id=id).delete()
        
        # Yeni destinasyonları ekle
        destinasyonlar = data['destinasyonlar']
        for i, dest_data in enumerate(destinasyonlar):
            dest_id = dest_data.get('destinasyon_id')
            # Destinasyonun varlığını kontrol et
            destinasyon = Destinasyon.query.get(dest_id)
            if not destinasyon:
                continue
                
            tur_dest = TurDestinasyon(
                tur_paketi_id=tur.id,
                destinasyon_id=dest_id,
                siralama=i + 1,
                kalma_suresi=dest_data.get('kalma_suresi', 24),
                not_bilgisi=dest_data.get('not_bilgisi', '')
            )
            db.session.add(tur_dest)
    
    db.session.commit()
    return tur

def delete_tur_paketi(id):
    """Tur paketini siler"""
    tur = TurPaketi.query.get(id)
    if not tur:
        return {'error': 'Tur paketi bulunamadı'}
    
    db.session.delete(tur)
    db.session.commit()
    return {'message': 'Tur paketi başarıyla silindi'}

def get_tur_destinasyonlari(tur_id):
    """Tur paketinin destinasyonlarını getirir"""
    return TurDestinasyon.query.filter_by(tur_paketi_id=tur_id).order_by(TurDestinasyon.siralama).all()