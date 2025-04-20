from flask import Blueprint, jsonify, request
from app import db
from app.models import Tur

tur_bp = Blueprint('tur', __name__, url_prefix='/api')

@tur_bp.route('/turlar', methods=['GET'])
def get_turlar():
    turlar = Tur.query.filter_by(aktif=True).all()
    return jsonify([tur.to_dict() for tur in turlar])

@tur_bp.route('/turlar/<int:id>', methods=['GET'])
def get_tur(id):
    tur = Tur.query.get_or_404(id)
    return jsonify(tur.to_dict())

@tur_bp.route('/turlar', methods=['POST'])
def create_tur():
    data = request.get_json()
    
    if not data or not data.get('adi') or not data.get('sure') or not data.get('fiyat'):
        return jsonify({'error': 'Ad, süre ve fiyat gerekli'}), 400
    
    tur = Tur(
        adi=data['adi'],
        sure=data['sure'],
        fiyat=float(data['fiyat']),
        aciklama=data.get('aciklama', ''),
        resim=data.get('resim', ''),
        kategori=data.get('kategori', ''),
        konum_id=data.get('konum_id')
    )
    
    db.session.add(tur)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Tur başarıyla eklendi',
        'tur': tur.to_dict()
    }), 201