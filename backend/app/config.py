import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-degistirin'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:sifre@localhost:5432/tatil_tur_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False