# backend/app/services/rehber_service.py
from app.models.rehber import Rehber
from app import db
from datetime import datetime
import logging

class RehberService:
    @staticmethod
    def get_all_rehberler():
        """Return all guides"""
        try:
            return Rehber.query.all()
        except Exception as e:
            logging.error(f"Error fetching all guides: {str(e)}")
            raise

    @staticmethod
    def get_rehber_by_id(rehber_id):
        """Return a specific guide by ID"""
        try:
            return Rehber.query.get(rehber_id)
        except Exception as e:
            logging.error(f"Error fetching guide {rehber_id}: {str(e)}")
            raise

    @staticmethod
    def create_rehber(rehber_data):
        """Create a new guide"""
        try:
            rehber = Rehber(
                ad=rehber_data.get('ad'),
                soyad=rehber_data.get('soyad'),
                email=rehber_data.get('email'),
                telefon=rehber_data.get('telefon'),
                dil_bilgisi=rehber_data.get('dil_bilgisi'),
                deneyim_yili=rehber_data.get('deneyim_yili', 0),
                aciklama=rehber_data.get('aciklama'),
                aktif=rehber_data.get('aktif', True),
                olusturma_tarihi=datetime.utcnow()
            )
            
            db.session.add(rehber)
            db.session.commit()
            return rehber
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating guide: {str(e)}")
            raise

    @staticmethod
    def update_rehber(rehber_id, rehber_data):
        """Update an existing guide"""
        try:
            rehber = Rehber.query.get(rehber_id)
            if not rehber:
                raise ValueError("Rehber bulunamadı")
            
            # Update fields
            rehber.ad = rehber_data.get('ad', rehber.ad)
            rehber.soyad = rehber_data.get('soyad', rehber.soyad)
            rehber.email = rehber_data.get('email', rehber.email)
            rehber.telefon = rehber_data.get('telefon', rehber.telefon)
            rehber.dil_bilgisi = rehber_data.get('dil_bilgisi', rehber.dil_bilgisi)
            rehber.deneyim_yili = rehber_data.get('deneyim_yili', rehber.deneyim_yili)
            rehber.aciklama = rehber_data.get('aciklama', rehber.aciklama)
            rehber.aktif = rehber_data.get('aktif', rehber.aktif)
            
            db.session.commit()
            return rehber
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating guide {rehber_id}: {str(e)}")
            raise

    @staticmethod
    def delete_rehber(rehber_id):
        """Delete a guide"""
        try:
            rehber = Rehber.query.get(rehber_id)
            if not rehber:
                raise ValueError("Rehber bulunamadı")
            
            db.session.delete(rehber)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting guide {rehber_id}: {str(e)}")
            raise
            
    @staticmethod
    def get_active_rehberler():
        """Return all active guides"""
        try:
            return Rehber.query.filter_by(aktif=True).all()
        except Exception as e:
            logging.error(f"Error fetching active guides: {str(e)}")
            raise