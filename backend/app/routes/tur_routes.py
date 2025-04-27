from flask import Blueprint, jsonify, request
from app import db
from app.models.tur import Tur, TurSeferi
from app.models.destinasyon import Destinasyon
import traceback

tur_bp = Blueprint('tur', __name__, url_prefix='/api')

@tur_bp.route('/turlar', methods=['GET'])
def get_turlar():
    turlar = Tur.query.filter_by(aktif=True).all()
    return jsonify([tur.to_dict() for tur in turlar])

@tur_bp.route('/turlar/<int:id>', methods=['GET'])
def get_tur(id):
    try:
        tur = Tur.query.get(id)
        if not tur:
            return jsonify({'error': 'Tour not found'}), 404
        
        seferler = TurSeferi.query.filter_by(tur_id=id).all()
        result = tur.to_dict()
        result['seferler'] = [sefer.to_dict() for sefer in seferler] if seferler else []
        
        if hasattr(tur, 'destinasyon_id') and tur.destinasyon_id:
            destinasyon = Destinasyon.query.get(tur.destinasyon_id)
            if destinasyon:
                result['destinasyon_adi'] = destinasyon.ad
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error retrieving tour with ID {id}: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@tur_bp.route('/turlar', methods=['POST'])
def create_tur():
    """Create a new tour"""
    try:
        data = request.get_json()
        
        if not data.get('adi'):
            return jsonify({'error': 'Tour name (adi) is required'}), 400
        if not data.get('sure'):
            return jsonify({'error': 'Tour duration (sure) is required'}), 400
        if not data.get('destinasyon_id'):
            return jsonify({'error': 'Destination (destinasyon_id) is required'}), 400
        
        try:
            fiyat = float(data.get('fiyat', 0))
        except (ValueError, TypeError):
            fiyat = 0.0
        
        new_tour = Tur(
            adi=data.get('adi'),
            sure=data.get('sure'),
            fiyat=fiyat,
            aciklama=data.get('aciklama'),
            resim=data.get('resim'),
            kategori=data.get('kategori'),
            destinasyon_id=data.get('destinasyon_id'),
            aktif=data.get('aktif', True)
        )
        
        db.session.add(new_tour)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tour created successfully',
            'id': new_tour.id,
            'data': new_tour.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating tour: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@tur_bp.route('/tur-seferi', methods=['POST'])
def create_tur_seferi():
    """Create a new tour departure"""
    try:
        data = request.get_json()
        
        if not data.get('tur_id'):
            return jsonify({'error': 'Tour ID is required'}), 400
        if not data.get('baslangic_tarihi') or not data.get('bitis_tarihi'):
            return jsonify({'error': 'Start and end dates are required'}), 400
        
        from datetime import datetime
        baslangic_tarihi = datetime.strptime(data.get('baslangic_tarihi'), '%Y-%m-%d').date()
        bitis_tarihi = datetime.strptime(data.get('bitis_tarihi'), '%Y-%m-%d').date()
        
        try:
            kontenjan = int(data.get('kontenjan', 30))
        except (ValueError, TypeError):
            kontenjan = 30
        
        try:
            fiyat = float(data.get('fiyat', 0))
        except (ValueError, TypeError):
            fiyat = 0.0
        
        new_sefer = TurSeferi(
            tur_id=data.get('tur_id'),
            baslangic_tarihi=baslangic_tarihi,
            bitis_tarihi=bitis_tarihi,
            kontenjan=kontenjan,
            kalan_kontenjan=data.get('kalan_kontenjan', kontenjan),
            fiyat=fiyat,
            durum=data.get('durum', 'aktif'),
            vehicle_id=data.get('vehicle_id')  # New: Only vehicle id needed
        )
        
        db.session.add(new_sefer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tour departure created successfully',
            'id': new_sefer.id,
            'data': new_sefer.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating tour departure: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
