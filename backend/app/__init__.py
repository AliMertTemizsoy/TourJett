from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Ana test route'u
    @app.route('/test')
    def test_page():
        return {'message': 'Tatil Turu Yönetim Sistemi API çalışıyor!'}
    
    # Blueprint'leri kaydet
    from app.routes.bolge_routes import bolge_bp
    from app.routes.kaynak_routes import kaynak_bp
    from app.routes.tur_routes import tur_bp
    from app.routes.destinasyon_routes import destinasyon_bp
    from app.routes.musteri_routes import musteri_bp
    from app.routes.degerlendirme_routes import degerlendirme_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.rezervasyon_routes import rezervasyon_bp
    
    app.register_blueprint(bolge_bp)
    app.register_blueprint(kaynak_bp)
    app.register_blueprint(tur_bp)
    app.register_blueprint(destinasyon_bp)
    app.register_blueprint(musteri_bp)
    app.register_blueprint(degerlendirme_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(rezervasyon_bp)
    
    return app