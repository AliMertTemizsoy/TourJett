# backend/app/routes/konum_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.konum import Konum
import traceback

konum_bp = Blueprint('konum', __name__, url_prefix='/api')

@konum_bp.route('/konum', methods=['GET'])
def get_konumlar():
    """Get all locations"""
    try:
        konumlar = Konum.query.all()
        return jsonify([{
            'id': k.id,
            'ad': k.ad,
            'ulke': k.ulke,
            'aciklama': k.aciklama
        } for k in konumlar])
    except Exception as e:
        print(f"Error getting locations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@konum_bp.route('/konum/<int:konum_id>', methods=['GET'])
def get_konum(konum_id):
    """Get a specific location"""
    try:
        konum = Konum.query.get(konum_id)
        if not konum:
            return jsonify({'error': 'Location not found'}), 404
        return jsonify({
            'id': konum.id,
            'ad': konum.ad,
            'ulke': konum.ulke,
            'aciklama': konum.aciklama
        })
    except Exception as e:
        print(f"Error getting location: {str(e)}")
        return jsonify({'error': str(e)}), 500

@konum_bp.route('/konum', methods=['POST'])
def create_konum():
    """Create a new location"""
    try:
        data = request.get_json()
        
        # Check required fields
        if not data.get('ad'):
            return jsonify({'error': 'Location name is required'}), 400
            
        # Create new location
        konum = Konum(
            ad=data.get('ad'),
            ulke=data.get('ulke'),
            aciklama=data.get('aciklama')
        )
        
        db.session.add(konum)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Location created successfully',
            'id': konum.id,
            'data': {
                'id': konum.id,
                'ad': konum.ad,
                'ulke': konum.ulke,
                'aciklama': konum.aciklama
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating location: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@konum_bp.route('/konum/<int:konum_id>', methods=['PUT'])
def update_konum(konum_id):
    """Update a location"""
    try:
        konum = Konum.query.get(konum_id)
        if not konum:
            return jsonify({'error': 'Location not found'}), 404
            
        data = request.get_json()
        
        # Update fields
        if 'ad' in data:
            konum.ad = data['ad']
        if 'ulke' in data:
            konum.ulke = data['ulke']
        if 'aciklama' in data:
            konum.aciklama = data['aciklama']
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Location updated successfully',
            'data': {
                'id': konum.id,
                'ad': konum.ad,
                'ulke': konum.ulke,
                'aciklama': konum.aciklama
            }
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error updating location: {str(e)}")
        return jsonify({'error': str(e)}), 500

@konum_bp.route('/konum/<int:konum_id>', methods=['DELETE'])
def delete_konum(konum_id):
    """Delete a location"""
    try:
        konum = Konum.query.get(konum_id)
        if not konum:
            return jsonify({'error': 'Location not found'}), 404
            
        db.session.delete(konum)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Location deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting location: {str(e)}")
        return jsonify({'error': str(e)}), 500