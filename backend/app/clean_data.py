from app import db, create_app
from app.models.surucu import Surucu
from app.models.vehicle import Vehicles
from app.models.rehber import Rehber
from app.models.destinasyon import Destinasyon
from app.models.tur import Tur, TurSeferi
from app.models.tur_paketi import TurPaketi, TurDestinasyon
import traceback

def clean_data():
    """Delete all data from the database tables."""
    app = create_app()
    with app.app_context():
        print("Starting data cleanup...")
        
        # Array to track which tables we successfully cleaned
        cleaned_tables = []
        
        # Delete TurDestinasyon records
        try:
            print("Deleting TurDestinasyon records...")
            count = db.session.query(TurDestinasyon).delete()
            db.session.commit()
            print(f"Deleted {count} TurDestinasyon records")
            cleaned_tables.append("TurDestinasyon")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting TurDestinasyon records: {str(e)}")
            print("Continuing with other tables...")
        
        # Delete TurPaketi records
        try:
            print("Deleting TurPaketi records...")
            # First try to find records that can be safely deleted
            # Get all TurPaketi IDs
            all_tur_paketi_ids = [tp.id for tp in TurPaketi.query.all()]
            deleted_count = 0
            
            # Try to delete each record individually
            for tp_id in all_tur_paketi_ids:
                try:
                    obj = TurPaketi.query.get(tp_id)
                    if obj:
                        db.session.delete(obj)
                        db.session.commit()
                        deleted_count += 1
                except Exception:
                    db.session.rollback()
                    # Skip this record and continue
                    pass
            
            print(f"Deleted {deleted_count} out of {len(all_tur_paketi_ids)} TurPaketi records")
            cleaned_tables.append("TurPaketi (partial)")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting TurPaketi records: {str(e)}")
            print("Continuing with other tables...")
        
        # Delete TurSeferi records
        try:
            print("Deleting TurSeferi records...")
            count = db.session.query(TurSeferi).delete()
            db.session.commit()
            print(f"Deleted {count} TurSeferi records")
            cleaned_tables.append("TurSeferi")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting TurSeferi records: {str(e)}")
            print("Continuing with other tables...")
        
        # Delete Tur records
        try:
            print("Deleting Tur records...")
            # First try to find records that can be safely deleted
            all_tur_ids = [t.id for t in Tur.query.all()]
            deleted_count = 0
            
            # Try to delete each record individually
            for tur_id in all_tur_ids:
                try:
                    obj = Tur.query.get(tur_id)
                    if obj:
                        db.session.delete(obj)
                        db.session.commit()
                        deleted_count += 1
                except Exception:
                    db.session.rollback()
                    # Skip this record and continue
                    pass
            
            print(f"Deleted {deleted_count} out of {len(all_tur_ids)} Tur records")
            cleaned_tables.append("Tur (partial)")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Tur records: {str(e)}")
            print("Continuing with other tables...")
        
        # Delete Destinasyon records
        try:
            print("Deleting Destinasyon records...")
            all_dest_ids = [d.id for d in Destinasyon.query.all()]
            deleted_count = 0
            
            # Try to delete each record individually
            for dest_id in all_dest_ids:
                try:
                    obj = Destinasyon.query.get(dest_id)
                    if obj:
                        db.session.delete(obj)
                        db.session.commit()
                        deleted_count += 1
                except Exception:
                    db.session.rollback()
                    # Skip this record and continue
                    pass
            
            print(f"Deleted {deleted_count} out of {len(all_dest_ids)} Destinasyon records")
            cleaned_tables.append("Destinasyon (partial)")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Destinasyon records: {str(e)}")
            print("Continuing with other tables...")
        
        # Delete Vehicles records
        try:
            print("Deleting Vehicles records...")
            all_vehicle_ids = [v.id for v in Vehicles.query.all()]
            deleted_count = 0
            
            # Try to delete each record individually
            for vehicle_id in all_vehicle_ids:
                try:
                    obj = Vehicles.query.get(vehicle_id)
                    if obj:
                        db.session.delete(obj)
                        db.session.commit()
                        deleted_count += 1
                except Exception:
                    db.session.rollback()
                    # Skip this record and continue
                    pass
            
            print(f"Deleted {deleted_count} out of {len(all_vehicle_ids)} Vehicles records")
            cleaned_tables.append("Vehicles (partial)")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Vehicles records: {str(e)}")
            print("Continuing with other tables...")
        
        # Delete Surucu records
        try:
            print("Deleting Surucu records...")
            all_surucu_ids = [s.id for s in Surucu.query.all()]
            deleted_count = 0
            
            # Try to delete each record individually
            for surucu_id in all_surucu_ids:
                try:
                    obj = Surucu.query.get(surucu_id)
                    if obj:
                        db.session.delete(obj)
                        db.session.commit()
                        deleted_count += 1
                except Exception:
                    db.session.rollback()
                    # Skip this record and continue
                    pass
            
            print(f"Deleted {deleted_count} out of {len(all_surucu_ids)} Surucu records")
            cleaned_tables.append("Surucu (partial)")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Surucu records: {str(e)}")
            print("Continuing with other tables...")
        
        # Delete Rehber records
        try:
            print("Deleting Rehber records...")
            all_rehber_ids = [r.id for r in Rehber.query.all()]
            deleted_count = 0
            
            # Try to delete each record individually
            for rehber_id in all_rehber_ids:
                try:
                    obj = Rehber.query.get(rehber_id)
                    if obj:
                        db.session.delete(obj)
                        db.session.commit()
                        deleted_count += 1
                except Exception:
                    db.session.rollback()
                    # Skip this record and continue
                    pass
            
            print(f"Deleted {deleted_count} out of {len(all_rehber_ids)} Rehber records")
            cleaned_tables.append("Rehber (partial)")
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting Rehber records: {str(e)}")
            print("Continuing with other tables...")
        
        print(f"Data cleanup completed. Successfully cleaned tables: {', '.join(cleaned_tables)}")

if __name__ == "__main__":
    clean_data() 