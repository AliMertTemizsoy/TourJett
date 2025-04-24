from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__, static_folder='../../frontend/TourNest-master', static_url_path='/')
    
    # CORS yapılandırması - geliştirme için basitleştirilmiş
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Konfigürasyon ayarları
    if config:
        app.config.from_object(config)
    else:
        # Varsayılan konfigürasyonu yükle
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/tourjett'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Veritabanı başlatma
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Route'ları import et
    from app.routes.auth_routes import auth_bp
    from app.routes.rezervasyon_routes import rezervasyon_bp
    from app.routes.tur_routes import tur_bp
    
    # Blueprint'leri kaydet
    app.register_blueprint(auth_bp)
    app.register_blueprint(rezervasyon_bp)
    app.register_blueprint(tur_bp)
    
    try:
        # Diğer blueprint'leri kaydet (varsa)
        from app.routes.bolge_routes import bolge_bp
        app.register_blueprint(bolge_bp)
    except ImportError:
        pass
    
    try:
        from app.routes.musteri_routes import musteri_bp
        app.register_blueprint(musteri_bp)
    except ImportError:
        pass
    
    try:
        from app.routes.destinasyon_routes import destinasyon_bp
        app.register_blueprint(destinasyon_bp)
    except ImportError:
        pass
    
    try:
        from app.routes.kaynak_routes import kaynak_bp
        app.register_blueprint(kaynak_bp)
    except ImportError:
        pass
    
    try:
        from app.routes.degerlendirme_routes import degerlendirme_bp
        app.register_blueprint(degerlendirme_bp)
    except ImportError:
        pass
    
    try:
        from app.routes.tur_paketi_routes import tur_paketi_bp
        app.register_blueprint(tur_paketi_bp)
    except ImportError:
        pass
    
    # Ana sayfa rotası
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    # Login sayfası rotası
    @app.route('/login.html')
    def login_page():
        return app.send_static_file('login.html')
    
    # Herhangi bir statik dosya için fallback
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    return app