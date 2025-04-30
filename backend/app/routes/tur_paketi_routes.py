from flask import Blueprint, request, jsonify
from app import db
from app.models.tur_paketi import TurPaketi
from app.models.tur import Tur  # Access Tur model
from datetime import datetime
import traceback  # Hata izleme için

tur_paketi_bp = Blueprint('tur_paketi', __name__, url_prefix='/api/turpaketleri')

@tur_paketi_bp.route('/', methods=['GET'])
def get_tur_paketleri():
    """Tüm tur paketlerini listeler"""
    try:
        paketler = TurPaketi.query.all()
        return jsonify([paket.to_dict() for paket in paketler])
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tur_paketi_bp.route('/<int:id>', methods=['GET'])
def get_tur_paketi(id):
    """Belirli bir tur paketinin detaylarını getirir"""
    try:
        paket = TurPaketi.query.get(id)
        if not paket:
            return jsonify({'error': 'Tur paketi bulunamadı'}), 404
        return jsonify(paket.to_dict())
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tur_paketi_bp.route('/', methods=['POST'])
def create_tur_paketi():
    """Yeni bir tur paketi oluşturur"""
    try:
        data = request.get_json()
        print(f"Gelen veri: {data}")

        # Zorunlu alanlar kontrolü
        if not data.get('ad') and not data.get('tur_id'):
            return jsonify({'error': 'Tur paketi adı veya tur_id gereklidir'}), 400
        
        if data.get('tur_id') is None:
            return jsonify({'error': 'Tur (tur_id) gereklidir'}), 400

        if data.get('rehber_id') is None:
            return jsonify({'error': 'Rehber (rehber_id) gereklidir'}), 400

        if data.get('surucu_id') is None:
            return jsonify({'error': 'Sürücü (surucu_id) gereklidir'}), 400

        if data.get('vehicle_id') is None:
            return jsonify({'error': 'Vehicle (vehicle_id) gereklidir'}), 400

        tur = None
        if data.get('tur_id'):
            tur = Tur.query.get(data['tur_id'])
            if not tur:
                return jsonify({'error': 'Belirtilen Tur bulunamadı'}), 404
        
        ad = data.get('ad') or (tur.adi if tur else None)
        sure = data.get('sure') or (tur.sure if tur else None)
        resim_url = data.get('resim_url') or (tur.resim if tur else None)

        kapasite = int(data.get('kapasite', 20))
        durum = data.get('durum', 'Aktif')
        surucu_id = data.get('surucu_id')
        rehber_id = data.get('rehber_id')
        vehicle_id = data.get('vehicle_id')
        tur_id = data.get('tur_id')

        tur_tarihi = None
        if data.get('tur_tarihi'):
            try:
                tur_tarihi = datetime.strptime(data.get('tur_tarihi'), '%Y-%m-%d').date()
            except ValueError:
                print("Geçersiz tarih formatı")
        
        yeni_paket = TurPaketi(
            ad=ad,
            aciklama=data.get('aciklama', tur.aciklama if tur else None),
            sure=sure,
            kapasite=kapasite,
            tur_tarihi=tur_tarihi,
            resim_url=resim_url,
            durum=durum,
            surucu_id=surucu_id,
            rehber_id=rehber_id,
            vehicle_id=vehicle_id,
            tur_id=tur_id
        )

        db.session.add(yeni_paket)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Tur paketi başarıyla oluşturuldu',
            'id': yeni_paket.id,
            'data': yeni_paket.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Tur paketi oluşturma hatası: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@tur_paketi_bp.route('/<int:id>', methods=['PUT'])
def update_tur_paketi(id):
    """Belirli bir tur paketini günceller"""
    try:
        paket = TurPaketi.query.get(id)
        if not paket:
            return jsonify({'error': 'Tur paketi bulunamadı'}), 404
            
        data = request.get_json()
        
        # Güncellenebilir alanlar
        if 'ad' in data:
            paket.ad = data['ad']
        if 'aciklama' in data:
            paket.aciklama = data['aciklama']
        if 'sure' in data:
            paket.sure = data['sure']
        if 'kapasite' in data:
            paket.kapasite = int(data['kapasite'])
        if 'durum' in data:
            paket.durum = data['durum']
        if 'surucu_id' in data:
            paket.surucu_id = data['surucu_id']
        if 'rehber_id' in data:
            paket.rehber_id = data['rehber_id']
        if 'vehicle_id' in data:
            paket.vehicle_id = data['vehicle_id']
        if 'tur_id' in data:
            paket.tur_id = data['tur_id']
        if 'tur_tarihi' in data and data['tur_tarihi']:
            try:
                paket.tur_tarihi = datetime.strptime(data['tur_tarihi'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Geçersiz tarih formatı'}), 400
        if 'resim_url' in data:
            paket.resim_url = data['resim_url']
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tur paketi başarıyla güncellendi',
            'data': paket.to_dict()
        })
            
    except Exception as e:
        db.session.rollback()
        print(f"Tur paketi güncelleme hatası: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@tur_paketi_bp.route('/<int:id>', methods=['DELETE'])
def delete_tur_paketi(id):
    """Belirli bir tur paketini siler"""
    try:
        paket = TurPaketi.query.get(id)
        if not paket:
            return jsonify({'error': 'Tur paketi bulunamadı'}), 404
            
        db.session.delete(paket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tur paketi başarıyla silindi'
        })
            
    except Exception as e:
        db.session.rollback()
        print(f"Tur paketi silme hatası: {str(e)}")
        return jsonify({'error': str(e)}), 500