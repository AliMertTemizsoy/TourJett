# backend/app/routes/rehber_routes.py
from flask import Blueprint, request, jsonify
from app.models.rehber import Rehber
from app import db
from datetime import datetime
import logging

# Set up blueprint
rehber_bp = Blueprint('rehber', __name__, url_prefix='/api/rehber')

# Get all guides
@rehber_bp.route('/', methods=['GET'])
def get_all_rehberler():
    try:
        rehberler = Rehber.query.all()
        return jsonify([rehber.to_dict() for rehber in rehberler]), 200
    except Exception as e:
        logging.error(f"Error fetching guides: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Get a specific guide by ID
@rehber_bp.route('/<int:rehber_id>', methods=['GET'])
def get_rehber(rehber_id):
    try:
        rehber = Rehber.query.get(rehber_id)
        if not rehber:
            return jsonify({"error": "Rehber bulunamadı"}), 404
        return jsonify(rehber.to_dict()), 200
    except Exception as e:
        logging.error(f"Error fetching guide {rehber_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Create a new guide
@rehber_bp.route('/', methods=['POST'])
def create_rehber():
    try:
        data = request.get_json()
        
        # Create new guide
        rehber = Rehber(
            ad=data.get('ad'),
            soyad=data.get('soyad'),
            email=data.get('email'),
            telefon=data.get('telefon'),
            dil_bilgisi=data.get('dil_bilgisi'),
            deneyim_yili=data.get('deneyim_yili', 0),
            aciklama=data.get('aciklama'),
            aktif=data.get('aktif', True),
            olusturma_tarihi=datetime.utcnow()
        )
        
        db.session.add(rehber)
        db.session.commit()
        
        return jsonify(rehber.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating guide: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Update a guide
@rehber_bp.route('/<int:rehber_id>', methods=['PUT'])
def update_rehber(rehber_id):
    try:
        rehber = Rehber.query.get(rehber_id)
        if not rehber:
            return jsonify({"error": "Rehber bulunamadı"}), 404
        
        data = request.get_json()
        
        # Update fields
        rehber.ad = data.get('ad', rehber.ad)
        rehber.soyad = data.get('soyad', rehber.soyad)
        rehber.email = data.get('email', rehber.email)
        rehber.telefon = data.get('telefon', rehber.telefon)
        rehber.dil_bilgisi = data.get('dil_bilgisi', rehber.dil_bilgisi)
        rehber.deneyim_yili = data.get('deneyim_yili', rehber.deneyim_yili)
        rehber.aciklama = data.get('aciklama', rehber.aciklama)
        rehber.aktif = data.get('aktif', rehber.aktif)
        
        db.session.commit()
        
        return jsonify(rehber.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating guide {rehber_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Delete a guide
@rehber_bp.route('/<int:rehber_id>', methods=['DELETE'])
def delete_rehber(rehber_id):
    try:
        rehber = Rehber.query.get(rehber_id)
        if not rehber:
            return jsonify({"error": "Rehber bulunamadı"}), 404
        
        db.session.delete(rehber)
        db.session.commit()
        
        return jsonify({"message": "Rehber başarıyla silindi"}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting guide {rehber_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500