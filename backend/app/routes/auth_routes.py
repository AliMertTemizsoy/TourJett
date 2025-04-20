from flask import Blueprint, request, jsonify
from app import db
from app.models import User
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email ve şifre gerekli'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Geçersiz email veya şifre'}), 401
    
    # Burada JWT token oluşturup döndürebilirsiniz, ama şimdilik basit tutalım
    return jsonify({
        'success': True,
        'message': 'Giriş başarılı',
        'token': 'sample-token',  # Gerçek uygulamada JWT token kullanın
        'user': user.to_dict()
    })

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email ve şifre gerekli'}), 400
    
    # Email formatı kontrolü
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, data['email']):
        return jsonify({'error': 'Geçerli bir email adresi girin'}), 400
    
    # Şifre uzunluk kontrolü
    if len(data['password']) < 6:
        return jsonify({'error': 'Şifre en az 6 karakter olmalı'}), 400
    
    # Email adresi kullanılıyor mu kontrolü
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Bu email adresi zaten kullanılıyor'}), 400
    
    # Kullanıcı adı email'den türetilmiş olabilir
    username = data.get('username', data['email'].split('@')[0])
    
    # Yeni kullanıcı oluştur
    user = User(email=data['email'], username=username)
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Kayıt başarılı! Giriş yapabilirsiniz.',
        'userId': user.id
    })