# backend/app/routes/surucu_routes.py
from flask import Blueprint, request, jsonify
from app.models.surucu import Surucu
from app import db
from datetime import datetime
import logging

# Set up blueprint
surucu_bp = Blueprint('surucu', __name__, url_prefix='/api/surucu')

# Get all drivers
@surucu_bp.route('/', methods=['GET'])
def get_all_suruculer():
    try:
        suruculer = Surucu.query.all()
        return jsonify([surucu.to_dict() for surucu in suruculer]), 200
    except Exception as e:
        logging.error(f"Error fetching drivers: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Get a specific driver by ID
@surucu_bp.route('/<int:surucu_id>', methods=['GET'])
def get_surucu(surucu_id):
    try:
        surucu = Surucu.query.get(surucu_id)
        if not surucu:
            return jsonify({"error": "Sürücü bulunamadı"}), 404
        return jsonify(surucu.to_dict()), 200
    except Exception as e:
        logging.error(f"Error fetching driver {surucu_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Create a new driver
@surucu_bp.route('/', methods=['POST'])
def create_surucu():
    try:
        data = request.get_json()
        
        # Convert date string to date object
        dogum_tarihi = None
        if data.get('dogum_tarihi'):
            dogum_tarihi = datetime.strptime(data.get('dogum_tarihi'), '%Y-%m-%d').date()
        
        # Create new driver
        surucu = Surucu(
            ad=data.get('ad'),
            soyad=data.get('soyad'),
            email=data.get('email'),
            telefon=data.get('telefon'),
            ehliyet_no=data.get('ehliyet_no'),
            ehliyet_sinifi=data.get('ehliyet_sinifi'),
            deneyim_yil=data.get('deneyim_yil', 0),
            dogum_tarihi=dogum_tarihi,
            adres=data.get('adres'),
            uyruk=data.get('uyruk'),
            aktif=data.get('aktif', True)
        )
        
        db.session.add(surucu)
        db.session.commit()
        
        return jsonify(surucu.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating driver: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Update a driver
@surucu_bp.route('/<int:surucu_id>', methods=['PUT'])
def update_surucu(surucu_id):
    try:
        surucu = Surucu.query.get(surucu_id)
        if not surucu:
            return jsonify({"error": "Sürücü bulunamadı"}), 404
        
        data = request.get_json()
        
        # Convert date string to date object if present
        if data.get('dogum_tarihi'):
            dogum_tarihi = datetime.strptime(data.get('dogum_tarihi'), '%Y-%m-%d').date()
            surucu.dogum_tarihi = dogum_tarihi
            
        # Update fields
        surucu.ad = data.get('ad', surucu.ad)
        surucu.soyad = data.get('soyad', surucu.soyad)
        surucu.email = data.get('email', surucu.email)
        surucu.telefon = data.get('telefon', surucu.telefon)
        surucu.ehliyet_no = data.get('ehliyet_no', surucu.ehliyet_no)
        surucu.ehliyet_sinifi = data.get('ehliyet_sinifi', surucu.ehliyet_sinifi)
        surucu.deneyim_yil = data.get('deneyim_yil', surucu.deneyim_yil)
        surucu.adres = data.get('adres', surucu.adres)
        surucu.uyruk = data.get('uyruk', surucu.uyruk)
        surucu.aktif = data.get('aktif', surucu.aktif)
        
        db.session.commit()
        
        return jsonify(surucu.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating driver {surucu_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Delete a driver
@surucu_bp.route('/<int:surucu_id>', methods=['DELETE'])
def delete_surucu(surucu_id):
    try:
        surucu = Surucu.query.get(surucu_id)
        if not surucu:
            return jsonify({"error": "Sürücü bulunamadı"}), 404
        
        db.session.delete(surucu)
        db.session.commit()
        
        return jsonify({"message": "Sürücü başarıyla silindi"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting driver {surucu_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500