from app import db
from app.models.vehicle import Vehicles
from datetime import datetime

class VehicleService:
    @staticmethod
    def get_all_vehicles():
        """Get all vehicles from the database."""
        return Vehicles.query.all()
    
    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        """Get a vehicle by its ID."""
        return Vehicles.query.get(vehicle_id)
    
    @staticmethod
    def get_available_vehicles():
        """Get all available vehicles."""
        return Vehicles.query.filter_by(status='available').all()
    
    @staticmethod
    def create_vehicle(data):
        """Create a new vehicle."""
        vehicle = Vehicles(
            type=data['type'],
            model=data['model'],
            capacity=data['capacity'],
            license_plate=data['license_plate'],
            status=data.get('status', 'available'),
            surucu_id=data.get('surucu_id')
        )
        
        if 'last_maintenance_date' in data:
            vehicle.last_maintenance_date = datetime.strptime(data['last_maintenance_date'], '%Y-%m-%d').date()
        
        if 'next_maintenance_date' in data:
            vehicle.next_maintenance_date = datetime.strptime(data['next_maintenance_date'], '%Y-%m-%d').date()
        
        if 'purchase_date' in data:
            vehicle.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
        
        db.session.add(vehicle)
        db.session.commit()
        return vehicle
    
    @staticmethod
    def update_vehicle(vehicle_id, data):
        """Update a vehicle by its ID."""
        vehicle = Vehicles.query.get(vehicle_id)
        if not vehicle:
            return None
        
        if 'type' in data:
            vehicle.type = data['type']
        if 'model' in data:
            vehicle.model = data['model']
        if 'capacity' in data:
            vehicle.capacity = data['capacity']
        if 'license_plate' in data:
            vehicle.license_plate = data['license_plate']
        if 'status' in data:
            vehicle.status = data['status']
        if 'surucu_id' in data:
            vehicle.surucu_id = data['surucu_id']
        if 'last_maintenance_date' in data:
            vehicle.last_maintenance_date = datetime.strptime(data['last_maintenance_date'], '%Y-%m-%d').date()
        if 'next_maintenance_date' in data:
            vehicle.next_maintenance_date = datetime.strptime(data['next_maintenance_date'], '%Y-%m-%d').date()
        if 'purchase_date' in data:
            vehicle.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        return vehicle
    
    @staticmethod
    def delete_vehicle(vehicle_id):
        """Delete a vehicle by its ID."""
        vehicle = Vehicles.query.get(vehicle_id)
        if not vehicle:
            return False
        
        db.session.delete(vehicle)
        db.session.commit()
        return True
    
    @staticmethod
    def assign_driver(vehicle_id, driver_id):
        """Assign a driver to a vehicle."""
        vehicle = Vehicles.query.get(vehicle_id)
        if not vehicle:
            return None
        
        vehicle.surucu_id = driver_id
        db.session.commit()
        return vehicle