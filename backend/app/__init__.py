from flask import Flask, jsonify  # jsonify'ı ekledik
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)
    
    # CORS yapılandırması - daha kapsamlı
    CORS(app, origins=["http://localhost:8080"], supports_credentials=True)
    
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
    
    # Route'ları kaydet
    from app.routes.auth_routes import auth_bp
    from app.routes.tur_routes import tur_bp
    from app.routes.bolge_routes import bolge_bp
    from app.routes.musteri_routes import musteri_bp
    from app.routes.rezervasyon_routes import rezervasyon_bp
    from app.routes.destinasyon_routes import destinasyon_bp
    from app.routes.kaynak_routes import kaynak_bp
    from app.routes.degerlendirme_routes import degerlendirme_bp
    from app.routes.tur_paketi_routes import tur_paketi_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tur_bp)
    app.register_blueprint(bolge_bp)
    app.register_blueprint(musteri_bp)
    app.register_blueprint(rezervasyon_bp)
    app.register_blueprint(destinasyon_bp)
    app.register_blueprint(kaynak_bp)
    app.register_blueprint(degerlendirme_bp)
    app.register_blueprint(tur_paketi_bp)
    
    # Test rotasını ekle
    @app.route('/test-db')
    def test_db():
        try:
            db.session.execute('SELECT 1')
            return jsonify({"message": "Veritabanı bağlantısı başarılı"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app  # Bu satır create_app fonksiyonunun en sonunda olmalı
