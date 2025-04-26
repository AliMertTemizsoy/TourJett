from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    # Docker container içinde frontend klasörüne erişim sağlamak için static folder'ı ayarlayalım
    static_folder_path = '/frontend/TourNest-master'  # Docker içindeki yol
    
    # Docker içinden erişilemeyen durumlarda, yerel geliştirme için alternatif yol
    if not os.path.exists(static_folder_path):
        static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/TourNest-master'))
    
    app = Flask(__name__, static_folder=static_folder_path, static_url_path='/')
    
    # Debug bilgisi
    print(f"Static folder path: {static_folder_path}")
    print(f"Static folder exists: {os.path.exists(static_folder_path)}")
    if os.path.exists(static_folder_path):
        try:
            print(f"Files in static folder: {os.listdir(static_folder_path)}")
        except Exception as e:
            print(f"Error listing static folder: {e}")
    
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
        app.config['DEBUG'] = True  # Debug modunu açık tutalım
    
    # Veritabanı başlatma
    db.init_app(app)
    migrate.init_app(app, db)
    
    try:
        # Route'ları kaydet
        from app.routes.auth_routes import auth_bp
        from app.routes.tur_routes import tur_bp
        
        # Blueprint'leri kaydet
        app.register_blueprint(auth_bp)
        app.register_blueprint(tur_bp)
        
        # Diğer blueprint'leri kaydet (varsa)
        try:
            from app.routes.bolge_routes import bolge_bp
            app.register_blueprint(bolge_bp)
        except ImportError:
            print("bolge_routes import edilemedi")
            
        try:
            from app.routes.musteri_routes import musteri_bp
            app.register_blueprint(musteri_bp)
        except ImportError:
            print("musteri_routes import edilemedi")
            
        try:
            from app.routes.rezervasyon_routes import rezervasyon_bp
            app.register_blueprint(rezervasyon_bp)
        except ImportError:
            print("rezervasyon_routes import edilemedi")
        
        try:
            from app.routes.destinasyon_routes import destinasyon_bp
            app.register_blueprint(destinasyon_bp)
        except ImportError:
            print("destinasyon_routes import edilemedi")
            
        try:
            from app.routes.kaynak_routes import kaynak_bp
            app.register_blueprint(kaynak_bp)
        except ImportError:
            print("kaynak_routes import edilemedi")
            
        try:
            from app.routes.degerlendirme_routes import degerlendirme_bp
            app.register_blueprint(degerlendirme_bp)
        except ImportError:
            print("degerlendirme_routes import edilemedi")
            
        try:
            from app.routes.tur_paketi_routes import tur_paketi_bp
            app.register_blueprint(tur_paketi_bp)
        except ImportError:
            print("tur_paketi_routes import edilemedi")
            
        try:
            from app.routes.dashboard_routes import dashboard_bp
            app.register_blueprint(dashboard_bp)
        except ImportError:
            print("dashboard_routes import edilemedi")
            
        try:
            from app.routes.rehber_routes import rehber_bp
            app.register_blueprint(rehber_bp)
        except ImportError:
            print("rehber_routes import edilemedi")
            
        try:
            from app.routes.surucu_routes import surucu_bp
            app.register_blueprint(surucu_bp)
        except ImportError:
            print("surucu_routes import edilemedi")
            
        try:
            from app.routes.konum_routes import konum_bp
            app.register_blueprint(konum_bp)
        except ImportError:
            print("konum_routes import edilemedi")
    
    except Exception as e:
        print(f"Blueprint kayıt hatası: {str(e)}")
    
    # Ana sayfa rotası
    @app.route('/')
    def index():
        try:
            return app.send_static_file('index.html')
        except Exception as e:
            return f"Error serving index.html: {str(e)}", 500
    
    # Login sayfası rotası
    @app.route('/login.html')
    def login_page():
        try:
            return app.send_static_file('login.html')
        except Exception as e:
            return f"Error serving login.html: {str(e)}", 500
    
    # Dashboard sayfası rotası
    @app.route('/dashboard.html')
    def dashboard_page():
        try:
            return app.send_static_file('dashboard.html')
        except Exception as e:
            return f"Error serving dashboard.html: {str(e)}", 500
    
    # Test rotasını ekle
    @app.route('/test-db')
    def test_db():
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            return jsonify({"message": "Veritabanı bağlantısı başarılı"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Hello World rotası ekleyelim - CORS testi için
    @app.route('/hello')
    def hello():
        return jsonify({"message": "Hello from Flask!"})
    
    # Herhangi bir statik dosya için fallback
    @app.route('/<path:path>')
    def serve_static(path):
        try:
            return send_from_directory(app.static_folder, path)
        except Exception as e:
            return f"Error serving {path}: {str(e)}", 404
    
    return app