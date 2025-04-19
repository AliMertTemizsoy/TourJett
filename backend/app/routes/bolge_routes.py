from flask import Blueprint, request, jsonify
from app.models.bolge import Bolge, Destinasyon
from app.services.bolge_service import get_all_bolgeler, get_bolge_by_id, create_bolge
from app import db

bolge_bp = Blueprint('bolge', __name__, url_prefix='/api/bolgeler')

@bolge_bp.route('/', methods=['GET'])
def get_bolgeler():
    """Tüm bölgeleri listeler"""
    bolgeler = get_all_bolgeler()
    return jsonify([{'id': b.id, 'ad': b.ad, 'ulke': b.ulke, 'sehir': b.sehir} for b in bolgeler])

@bolge_bp.route('/<int:id>', methods=['GET'])
def get_bolge(id):
    """ID'ye göre bölge getirir"""
    bolge = get_bolge_by_id(id)
    if bolge:
        return jsonify({
            'id': bolge.id, 
            'ad': bolge.ad, 
            'aciklama': bolge.aciklama,
            'ulke': bolge.ulke,
            'sehir': bolge.sehir
        })
    return jsonify({'error': 'Bölge bulunamadı'}), 404

@bolge_bp.route('/', methods=['POST'])
def add_bolge():
    """Yeni bölge ekler"""
    data = request.get_json()
    yeni_bolge = create_bolge(data)
    return jsonify({
        'message': 'Bölge başarıyla eklendi',
        'id': yeni_bolge.id
    }), 201