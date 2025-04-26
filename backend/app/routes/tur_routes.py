from flask import Blueprint, jsonify, request
from app import db
from app.models.tur import Tur, TurSeferi
import traceback

tur_bp = Blueprint('tur', __name__, url_prefix='/api')

@tur_bp.route('/turlar', methods=['GET'])
def get_turlar():
    turlar = Tur.query.filter_by(aktif=True).all()
    return jsonify([tur.to_dict() for tur in turlar])

@tur_bp.route('/turlar/<int:id>', methods=['GET'])
def get_tur(id):
    tur = Tur.query.get_or_404(id)
    return jsonify(tur.to_dict())

@tur_bp.route('/turlar/<int:id>/seferler', methods=['GET'])
def get_tur_seferler(id):
    seferler = TurSeferi.query.filter_by(tur_id=id, durum='aktif').all()
    return jsonify([sefer.to_dict() for sefer in seferler])

@tur_bp.route('/tur', methods=['POST'])
def create_tur():
    """Create a new tour"""
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug
        
        # Check required fields
        if not data.get('adi'):
            return jsonify({'error': 'Tour name (adi) is required'}), 400
            
        if not data.get('sure'):
            return jsonify({'error': 'Tour duration (sure) is required'}), 400
            
        # Safe type conversions
        try:
            fiyat = float(data.get('fiyat', 0))
        except (ValueError, TypeError):
            fiyat = 0.0
            
        try:
            kar = float(data.get('kar', 0))
        except (ValueError, TypeError):
            kar = 0.0
        
        # Create new tour with all fields including profit, driver and car type
        new_tour = Tur(
            adi=data.get('adi'),
            sure=data.get('sure'),
            fiyat=fiyat,
            kar=kar,
            aciklama=data.get('aciklama'),
            resim=data.get('resim'),
            kategori=data.get('kategori'),
            konum_id=data.get('konum_id'),
            aktif=data.get('aktif', True),
            arac_tipi=data.get('arac_tipi'),
            surucu_id=data.get('surucu_id')
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
        
        # Check required fields
        if not data.get('tur_id'):
            return jsonify({'error': 'Tour ID is required'}), 400
            
        if not data.get('baslangic_tarihi') or not data.get('bitis_tarihi'):
            return jsonify({'error': 'Start and end dates are required'}), 400
        
        # Convert date strings to date objects
        from datetime import datetime
        baslangic_tarihi = datetime.strptime(data.get('baslangic_tarihi'), '%Y-%m-%d').date()
        bitis_tarihi = datetime.strptime(data.get('bitis_tarihi'), '%Y-%m-%d').date()
        
        # Safe type conversions
        try:
            kontenjan = int(data.get('kontenjan', 30))
        except (ValueError, TypeError):
            kontenjan = 30
            
        try:
            fiyat = float(data.get('fiyat', 0))
        except (ValueError, TypeError):
            fiyat = 0.0
            
        try:
            kar = float(data.get('kar', 0))
        except (ValueError, TypeError):
            kar = 0.0
            
        # Create new tour departure
        new_sefer = TurSeferi(
            tur_id=data.get('tur_id'),
            baslangic_tarihi=baslangic_tarihi,
            bitis_tarihi=bitis_tarihi,
            kontenjan=kontenjan,
            kalan_kontenjan=data.get('kalan_kontenjan', kontenjan),
            fiyat=fiyat,
            kar=kar,
            durum=data.get('durum', 'aktif'),
            rehber_id=data.get('rehber_id'),
            surucu_id=data.get('surucu_id')
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