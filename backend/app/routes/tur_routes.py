from flask import Blueprint, jsonify, request
from app import db
from app.models.tur import Tur, TurSeferi

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