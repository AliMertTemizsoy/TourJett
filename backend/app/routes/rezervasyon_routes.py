from flask import Blueprint, jsonify, request
from app import db
from app.models import Rezervasyon
from datetime import datetime

rezervasyon_bp = Blueprint('rezervasyon', __name__, url_prefix='/api')

@rezervasyon_bp.route('/rezervasyon', methods=['POST'])
def create_rezervasyon():
    data = request.get_json()
    
    # Zorunlu alanları kontrol et
    required_fields = ['tur_id', 'ad', 'soyad', 'email', 'telefon', 'tarih', 'kisi_sayisi']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} alanı gerekli'}), 400
    
    try:
        # Tarih formatını düzelt
        tarih = datetime.strptime(data['tarih'], '%Y-%m-%d').date()
        
        # Rezervasyon oluştur
        rezervasyon = Rezervasyon(
            tur_id=data['tur_id'],
            ad=data['ad'],
            soyad=data['soyad'],
            email=data['email'],
            telefon=data['telefon'],
            tarih=tarih,
            kisi_sayisi=int(data['kisi_sayisi']),
            oda_tipi=data.get('roomType'),  # Front-end'den gelen roomType alanı
            ozel_istekler=data.get('notlar')  # Front-end'den gelen notlar alanı
        )
        
        db.session.add(rezervasyon)
        db.session.commit()
        
        # Başarılı yanıt
        return jsonify({
            'success': True,
            'message': 'Rezervasyon başarıyla oluşturuldu',
            'id': rezervasyon.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@rezervasyon_bp.route('/rezervasyon/<int:id>', methods=['GET'])
def get_rezervasyon(id):
    rezervasyon = Rezervasyon.query.get_or_404(id)
    return jsonify(rezervasyon.to_dict())