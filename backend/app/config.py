import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-degistirin'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:sifre@localhost:5432/tatil_tur_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't', 'yes']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'tourjett@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'tourjett'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'TourJett <info@tourjett.com>'
    MAIL_ENABLE = os.environ.get('MAIL_ENABLE', 'False').lower() in ['true', '1', 't', 'yes']  # Enable/disable email sending