from flask import Blueprint, request, jsonify
from app.services.vehicle_service import VehicleService

# Create a blueprint for vehicle routes
vehicle_bp = Blueprint('vehicle', __name__, url_prefix='/api/vehicles')

@vehicle_bp.route('/', methods=['GET'])
def get_all_vehicles():
    """Get all vehicles."""
    vehicles = VehicleService.get_all_vehicles()
    return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200

@vehicle_bp.route('/available', methods=['GET'])
def get_available_vehicles():
    """Get all available vehicles."""
    vehicles = VehicleService.get_available_vehicles()
    return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200

@vehicle_bp.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    """Get a vehicle by its ID."""
    vehicle = VehicleService.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    return jsonify(vehicle.to_dict()), 200

@vehicle_bp.route('/', methods=['POST'])
def create_vehicle():
    """Create a new vehicle."""
    if not request.is_json:
        return jsonify({'error': 'Invalid content type, expected JSON'}), 400
        
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['type', 'model', 'capacity', 'license_plate']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create vehicle
    try:
        vehicle = VehicleService.create_vehicle(data)
        return jsonify(vehicle.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vehicle_bp.route('/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    """Update a vehicle by its ID."""
    if not request.is_json:
        return jsonify({'error': 'Invalid content type, expected JSON'}), 400
        
    data = request.get_json()
    
    # Update vehicle
    try:
        vehicle = VehicleService.update_vehicle(vehicle_id, data)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        return jsonify(vehicle.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@vehicle_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """Delete a vehicle by its ID."""
    result = VehicleService.delete_vehicle(vehicle_id)
    if not result:
        return jsonify({'error': 'Vehicle not found'}), 404
    return jsonify({'message': 'Vehicle deleted successfully'}), 200

@vehicle_bp.route('/<int:vehicle_id>/assign-driver/<int:driver_id>', methods=['PUT'])
def assign_driver(vehicle_id, driver_id):
    """Assign a driver to a vehicle."""
    vehicle = VehicleService.assign_driver(vehicle_id, driver_id)
    if not vehicle:
        return jsonify({'error': 'Vehicle not found'}), 404
    return jsonify(vehicle.to_dict()), 200