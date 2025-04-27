from flask import Blueprint, jsonify
from app.models.rezervasyon import Rezervasyon, TurSeferi
from app.models.tur import Tur
from app.models.musteri import Musteri
from app.models.rehber import Rehber
from app.models.surucu import Surucu
from app.models.destinasyon import Destinasyon
from app import db
from sqlalchemy import func, desc, or_
from datetime import datetime, timedelta

# Blueprint for dashboard API endpoints
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint to verify the dashboard blueprint is working"""
    return jsonify({"message": "Dashboard API is working!"})

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get total bookings
        total_bookings = db.session.query(func.count(Rezervasyon.id)).scalar() or 0
        
        # Calculate total revenue based on booking counts and tour prices
        # Join rezervasyon with tur through tur_id to get the actual prices
        total_revenue_query = db.session.query(
            func.sum(Tur.fiyat * Rezervasyon.kisi_sayisi)
        ).join(Tur, Rezervasyon.tur_id == Tur.id).scalar()
        
        total_revenue = float(total_revenue_query or 0)
        
        # Calculate total profit
        total_profit_query = db.session.query(
            func.sum(Tur.kar * Rezervasyon.kisi_sayisi)
        ).join(Tur, Rezervasyon.tur_id == Tur.id).scalar()
        
        total_profit = float(total_profit_query or 0)
        
        # Get active tours - check the aktif field instead of durum
        active_tours = db.session.query(func.count(Tur.id)).filter(
            Tur.aktif == True
        ).scalar() or 0
        
        # Get total customers
        total_customers = db.session.query(func.count(Musteri.id)).scalar() or 0
        
        # Get total guides
        total_guides = db.session.query(func.count(Rehber.id)).scalar() or 0
        
        # Get total drivers
        total_drivers = db.session.query(func.count(Surucu.id)).scalar() or 0
        
        return jsonify({
            'totalBookings': total_bookings,
            'totalRevenue': total_revenue,
            'totalProfit': total_profit,
            'activeTours': active_tours,
            'totalCustomers': total_customers,
            'totalGuides': total_guides,
            'totalDrivers': total_drivers
        })
    except Exception as e:
        import traceback
        print(f"Error in get_dashboard_stats: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/recent-bookings', methods=['GET'])
def get_recent_bookings():
    """Get recent bookings"""
    try:
        # Get recent bookings with join to get customer and tour names
        recent_bookings = db.session.query(
            Rezervasyon.id,
            Musteri.ad.label('customerName'),
            Tur.adi.label('tourName'),
            Rezervasyon.tarih.label('bookingDate'),
            Rezervasyon.kisi_sayisi.label('personCount'),
            Rezervasyon.durum.label('status'),
            Tur.fiyat.label('price'),
            Tur.kar.label('profit'),
            Tur.arac_tipi.label('carType'),
            func.concat(Surucu.ad, ' ', Surucu.soyad).label('driver_name')
        ).join(Musteri, Rezervasyon.musteri_id == Musteri.id, isouter=True)\
         .join(Tur, Rezervasyon.tur_id == Tur.id, isouter=True)\
         .outerjoin(Surucu, Tur.surucu_id == Surucu.id)\
         .order_by(desc(Rezervasyon.olusturma_tarihi))\
         .limit(5).all()
        
        # Convert to list of dicts
        bookings_list = []
        for booking in recent_bookings:
            booking_date = booking.bookingDate
            if booking_date:
                booking_date = booking_date.strftime('%Y-%m-%d')
            
            # Calculate actual amount based on price from tour and person count
            price_per_person = booking.price or 0
            amount = (booking.personCount or 1) * price_per_person
            
            # Calculate profit
            profit_per_person = booking.profit or 0
            total_profit = (booking.personCount or 1) * profit_per_person
            
            bookings_list.append({
                'id': booking.id,
                'customerName': booking.customerName or "Unknown Customer",
                'tourName': booking.tourName or "Unknown Tour",
                'bookingDate': booking_date or "",
                'amount': float(amount),
                'profit': float(total_profit),
                'carType': booking.carType or "Not specified",
                'driver': booking.driver_name or "Not assigned",
                'status': booking.status or "onay_bekliyor"
            })
        
        return jsonify(bookings_list)
    except Exception as e:
        import traceback
        print(f"Error in get_recent_bookings: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/upcoming-tours', methods=['GET'])
def get_upcoming_tours():
    """Get upcoming tours"""
    try:
        # Get current date
        today = datetime.now().date()
        
        # Get upcoming tours using TurSeferi for dates and capacity
        upcoming_tours = db.session.query(
            Tur.id,
            Tur.adi.label('name'),
            TurSeferi.id.label('sefer_id'),
            TurSeferi.baslangic_tarihi.label('date'),
            TurSeferi.kontenjan.label('capacity'),
            TurSeferi.kalan_kontenjan.label('remaining_capacity'),
            TurSeferi.durum.label('status'),
            Tur.arac_tipi.label('carType'),
            Tur.destinasyon_id.label('location_id'),
            func.concat(Rehber.ad, ' ', Rehber.soyad).label('guide_name'),
            func.concat(Surucu.ad, ' ', Surucu.soyad).label('driver_name'),
            func.count(Rezervasyon.id).label('booking_count')
        ).join(TurSeferi, Tur.id == TurSeferi.tur_id)\
         .outerjoin(Rehber, TurSeferi.rehber_id == Rehber.id)\
         .outerjoin(Surucu, TurSeferi.surucu_id == Surucu.id)\
         .outerjoin(Rezervasyon, TurSeferi.id == Rezervasyon.tur_sefer_id)\
         .filter(TurSeferi.baslangic_tarihi >= today)\
         .group_by(Tur.id, TurSeferi.id, Rehber.ad, Rehber.soyad, Surucu.ad, Surucu.soyad, Tur.adi, 
                  TurSeferi.baslangic_tarihi, TurSeferi.kontenjan, TurSeferi.kalan_kontenjan, 
                  TurSeferi.durum, Tur.arac_tipi, Tur.destinasyon_id)\
         .order_by(TurSeferi.baslangic_tarihi)\
         .all()
        
        print(f"Found {len(upcoming_tours)} upcoming tours")
        
        # If there are no upcoming tours, create some sample data
        if not upcoming_tours:
            # Sample tour data remains the same...
            sample_tours = [
                {
                    'id': 1,
                    'name': 'Cappadocia Hot Air Balloon',
                    'destination': 'Nevşehir',
                    'date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
                    'capacity': 15,
                    'bookings': 12,
                    'status': 'aktif',
                    'carType': 'Minibus',
                    'guide': 'Hakan Yılmaz',
                    'driver': 'Ahmet Demir',
                    'profit': 3000
                },
                {
                    'id': 2,
                    'name': 'Ephesus Ancient City',
                    'destination': 'İzmir',
                    'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'capacity': 20,
                    'bookings': 18,
                    'status': 'aktif',
                    'carType': 'Midibus',
                    'guide': 'Elif Kara',
                    'driver': 'Mehmet Yıldız',
                    'profit': 5000
                },
                {
                    'id': 3,
                    'name': 'Blue Cruise',
                    'destination': 'Fethiye',
                    'date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
                    'capacity': 10,
                    'bookings': 8,
                    'status': 'onay_bekliyor',
                    'carType': 'VIP Van',
                    'guide': 'Mustafa Demir',
                    'driver': 'Ali Can',
                    'profit': 6000
                }
            ]
            return jsonify(sample_tours)
        
        # Convert to list of dicts
        tours_list = []
        for tour in upcoming_tours:
            # Get location for each tour
            destination = "Unknown Location"
            if tour.location_id:
                location = db.session.query(Destinasyon.ad).filter(Destinasyon.id == tour.location_id).first()
                if location:
                    destination = location[0]
            
            # Format the date
            tour_date = tour.date
            if tour_date:
                tour_date = tour_date.strftime('%Y-%m-%d')
                
            # Get tour's profit
            profit_query = db.session.query(Tur.kar).filter(Tur.id == tour.id).first()
            profit = profit_query[0] if profit_query else 0
                
            tours_list.append({
                'id': tour.id,
                'sefer_id': tour.sefer_id,
                'name': tour.name or "Unnamed Tour",
                'destination': destination,
                'date': tour_date or "",
                'capacity': tour.capacity or 0,
                'bookings': tour.booking_count or 0,
                'status': tour.status or "aktif",
                'carType': tour.carType or "Not specified",
                'guide': tour.guide_name or "Unassigned",
                'driver': tour.driver_name or "Unassigned",
                'profit': float(profit or 0)
            })
        
        return jsonify(tours_list)
    except Exception as e:
        import traceback
        print(f"Error in get_upcoming_tours: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/revenue', methods=['GET'])
def get_revenue_data():
    """Get revenue data for charts"""
    try:
        # For now, generate dummy data as we may not have enough real data for a chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [12000, 19000, 15000, 22000, 18000, 24000]
        profit = [3600, 5700, 4500, 6600, 5400, 7200]
        
        revenue_data = {
            'labels': months,
            'revenue': revenue,
            'profit': profit
        }
        
        return jsonify(revenue_data)
    except Exception as e:
        import traceback
        print(f"Error in get_revenue_data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500