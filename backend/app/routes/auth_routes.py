from flask import Blueprint, request, jsonify
from app import db
from app.models import Musteri
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Geçersiz veri'}), 400
            
        email = data.get('email', '')
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'E-posta ve şifre gerekli'}), 400
        
        # Kullanıcıyı e-posta ile bul
        musteri = Musteri.query.filter_by(email=email).first()
        
        if not musteri:
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
            
        # Şifre kontrolü
        if not musteri.password_hash:
            return jsonify({'error': 'Kullanıcı hesabı tam oluşturulmamış'}), 400
            
        if not check_password_hash(musteri.password_hash, password):
            return jsonify({'error': 'Geçersiz şifre'}), 401
            
        # Başarılı login
        return jsonify({
            'success': True,
            'id': musteri.id,
            'ad': musteri.ad,
            'soyad': musteri.soyad,
            'email': musteri.email,
            'telefon': musteri.telefon,
            'tc_kimlik': musteri.tc_kimlik
        })
        
    except Exception as e:
        print("Login hatası:", str(e))
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Geçersiz veri'}), 400
            
        email = data.get('email', '')
        password = data.get('password', '')
        ad = data.get('ad', '')
        soyad = data.get('soyad', '')
        
        if not email or not password or not ad or not soyad:
            return jsonify({'error': 'Tüm zorunlu alanları doldurun'}), 400
            
        # E-posta zaten kayıtlı mı kontrol et
        if Musteri.query.filter_by(email=email).first():
            return jsonify({'error': 'Bu e-posta adresi zaten kullanılıyor'}), 400
            
        # Yeni müşteri oluştur
        try:
            dogum_tarihi = datetime.strptime(data.get('dogum_tarihi', '1990-01-01'), '%Y-%m-%d').date()
        except:
            dogum_tarihi = datetime(1990, 1, 1).date()
            
        yeni_musteri = Musteri(
            ad=ad,
            soyad=soyad,
            email=email,
            telefon=data.get('telefon', ''),
            adres=data.get('adres', ''),
            tc_kimlik=data.get('tc_kimlik', ''),
            dogum_tarihi=dogum_tarihi,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(yeni_musteri)
        db.session.commit()
        
        # Başarılı kayıt
        return jsonify({
            'success': True,
            'message': 'Kayıt başarılı',
            'id': yeni_musteri.id,
            'ad': yeni_musteri.ad,
            'soyad': yeni_musteri.soyad,
            'email': yeni_musteri.email,
            'telefon': yeni_musteri.telefon,
            'tc_kimlik': yeni_musteri.tc_kimlik
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print("Signup hatası:", str(e))
        return jsonify({'error': str(e)}), 500