# backend/app/services/surucu_service.py
from app.models.surucu import Surucu
from app import db
from datetime import datetime
import logging

class SurucuService:
    @staticmethod
    def get_all_suruculer():
        """Return all drivers"""
        try:
            return Surucu.query.all()
        except Exception as e:
            logging.error(f"Error fetching all drivers: {str(e)}")
            raise

    @staticmethod
    def get_surucu_by_id(surucu_id):
        """Return a specific driver by ID"""
        try:
            return Surucu.query.get(surucu_id)
        except Exception as e:
            logging.error(f"Error fetching driver {surucu_id}: {str(e)}")
            raise

    @staticmethod
    def create_surucu(surucu_data):
        """Create a new driver"""
        try:
            # Convert date string to date object if present
            dogum_tarihi = None
            if surucu_data.get('dogum_tarihi'):
                dogum_tarihi = datetime.strptime(surucu_data.get('dogum_tarihi'), '%Y-%m-%d').date()
                
            surucu = Surucu(
                ad=surucu_data.get('ad'),
                soyad=surucu_data.get('soyad'),
                email=surucu_data.get('email'),
                telefon=surucu_data.get('telefon'),
                ehliyet_no=surucu_data.get('ehliyet_no'),
                ehliyet_sinifi=surucu_data.get('ehliyet_sinifi'),
                deneyim_yil=surucu_data.get('deneyim_yil', 0),
                dogum_tarihi=dogum_tarihi,
                adres=surucu_data.get('adres'),
                uyruk=surucu_data.get('uyruk'),
                aktif=surucu_data.get('aktif', True)
            )
            
            db.session.add(surucu)
            db.session.commit()
            return surucu
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating driver: {str(e)}")
            raise

    @staticmethod
    def update_surucu(surucu_id, surucu_data):
        """Update an existing driver"""
        try:
            surucu = Surucu.query.get(surucu_id)
            if not surucu:
                raise ValueError("Sürücü bulunamadı")
            
            # Convert date string to date object if present
            if surucu_data.get('dogum_tarihi'):
                dogum_tarihi = datetime.strptime(surucu_data.get('dogum_tarihi'), '%Y-%m-%d').date()
                surucu.dogum_tarihi = dogum_tarihi
                
            # Update fields
            surucu.ad = surucu_data.get('ad', surucu.ad)
            surucu.soyad = surucu_data.get('soyad', surucu.soyad)
            surucu.email = surucu_data.get('email', surucu.email)
            surucu.telefon = surucu_data.get('telefon', surucu.telefon)
            surucu.ehliyet_no = surucu_data.get('ehliyet_no', surucu.ehliyet_no)
            surucu.ehliyet_sinifi = surucu_data.get('ehliyet_sinifi', surucu.ehliyet_sinifi)
            surucu.deneyim_yil = surucu_data.get('deneyim_yil', surucu.deneyim_yil)
            surucu.adres = surucu_data.get('adres', surucu.adres)
            surucu.uyruk = surucu_data.get('uyruk', surucu.uyruk)
            surucu.aktif = surucu_data.get('aktif', surucu.aktif)
            
            db.session.commit()
            return surucu
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating driver {surucu_id}: {str(e)}")
            raise

    @staticmethod
    def delete_surucu(surucu_id):
        """Delete a driver"""
        try:
            surucu = Surucu.query.get(surucu_id)
            if not surucu:
                raise ValueError("Sürücü bulunamadı")
            
            db.session.delete(surucu)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting driver {surucu_id}: {str(e)}")
            raise
            
    @staticmethod
    def get_active_suruculer():
        """Return all active drivers"""
        try:
            return Surucu.query.filter_by(aktif=True).all()
        except Exception as e:
            logging.error(f"Error fetching active drivers: {str(e)}")
            raise