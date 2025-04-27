from app import db
from datetime import datetime

class Vehicles(db.Model):
    """
    Vehicles model to manage vehicle details.
    """
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)  # Vehicle type (e.g., Bus, Van, Car)
    model = db.Column(db.String(100), nullable=False)  # Vehicle model (e.g., Mercedes Sprinter)
    capacity = db.Column(db.Integer, nullable=False)  # Seating capacity
    license_plate = db.Column(db.String(50), unique=True, nullable=False)  # License plate number
    status = db.Column(db.String(50), default='available')  # Status (e.g., available, maintenance, in use)
    last_maintenance_date = db.Column(db.Date)  # Date of last maintenance
    next_maintenance_date = db.Column(db.Date)  # Date of next scheduled maintenance
    purchase_date = db.Column(db.Date)  # When the vehicle was purchased
    surucu_id = db.Column(db.Integer, db.ForeignKey('surucu.id'))  # Foreign key to Surucu model
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    surucu = db.relationship('Surucu', backref=db.backref('vehicles', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Vehicle {self.license_plate}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'model': self.model,
            'capacity': self.capacity,
            'license_plate': self.license_plate,
            'status': self.status,
            'surucu_id': self.surucu_id,
            'surucu_name': f"{self.surucu.ad} {self.surucu.soyad}" if self.surucu else None,
            'last_maintenance_date': self.last_maintenance_date.strftime('%Y-%m-%d') if self.last_maintenance_date else None,
            'next_maintenance_date': self.next_maintenance_date.strftime('%Y-%m-%d') if self.next_maintenance_date else None,
            'purchase_date': self.purchase_date.strftime('%Y-%m-%d') if self.purchase_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }