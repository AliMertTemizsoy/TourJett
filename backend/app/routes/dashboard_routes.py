from flask import Blueprint, jsonify
from app.models.rezervasyon import Rezervasyon
from app.models.tur import Tur, TurSeferi
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
        # Modified query to use select_from to make the starting point clear
        total_revenue_query = db.session.query(
            func.sum(Tur.fiyat * Rezervasyon.kisi_sayisi)
        ).select_from(Rezervasyon).join(Tur, Rezervasyon.tur_id == Tur.id).scalar()
        
        total_revenue = float(total_revenue_query or 0)
        
        # Calculate total profit (30% of revenue)
        total_profit = total_revenue * 0.3
        
        # Get active tours using the aktif field which is the correct one from the model
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
            Tur.fiyat.label('price')
        ).join(Musteri, Rezervasyon.musteri_id == Musteri.id, isouter=True)\
         .join(Tur, Rezervasyon.tur_id == Tur.id, isouter=True)\
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
            
            # Calculate profit (30% of amount)
            total_profit = amount * 0.3
            
            bookings_list.append({
                'id': booking.id,
                'customerName': booking.customerName or "Unknown Customer",
                'tourName': booking.tourName or "Unknown Tour",
                'bookingDate': booking_date or "",
                'amount': float(amount),
                'profit': float(total_profit),
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
        
        # Use TurSeferi model since it contains the actual tour dates and capacities
        upcoming_tours = db.session.query(
            TurSeferi.id.label('sefer_id'),
            Tur.id,
            Tur.adi.label('name'),
            TurSeferi.baslangic_tarihi.label('date'),
            TurSeferi.kontenjan.label('capacity'),
            TurSeferi.kalan_kontenjan.label('remaining_capacity'),
            TurSeferi.durum.label('status'),
            Destinasyon.id.label('location_id'),
            func.count(Rezervasyon.id).label('booking_count')
        ).join(Tur, TurSeferi.tur_id == Tur.id)\
         .outerjoin(Destinasyon, Tur.destinasyon_id == Destinasyon.id)\
         .outerjoin(Rezervasyon, Rezervasyon.tur_id == Tur.id)\
         .filter(TurSeferi.baslangic_tarihi >= today)\
         .group_by(TurSeferi.id, Tur.id, Tur.adi, TurSeferi.baslangic_tarihi, 
                  TurSeferi.kontenjan, TurSeferi.kalan_kontenjan, TurSeferi.durum, Destinasyon.id)\
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
                
            # Get the tour's price and calculate profit (30% of price)
            tour_price_query = db.session.query(Tur.fiyat).filter(Tur.id == tour.id).first()
            tour_price = tour_price_query[0] if tour_price_query else 0
            profit = tour_price * 0.3

            # Get vehicle information from TurSeferi
            vehicle_info = "Not specified"
            vehicle_query = db.session.query(TurSeferi).filter(TurSeferi.id == tour.sefer_id).first()
            if vehicle_query and vehicle_query.vehicle:
                vehicle_info = vehicle_query.vehicle.model
                
            tours_list.append({
                'id': tour.id,
                'sefer_id': tour.sefer_id,
                'name': tour.name or "Unnamed Tour",
                'destination': destination,
                'date': tour_date or "",
                'capacity': tour.capacity or 0,
                'bookings': tour.booking_count or 0,
                'status': tour.status or "aktif",
                'carType': vehicle_info,
                'guide': "Unassigned",  # No direct guide relationship in Tur model
                'driver': "Unassigned",  # No direct driver relationship in Tur model
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

@dashboard_bp.route('/sales-by-tour', methods=['GET'])
def get_sales_by_tour():
    """Get sales data by tour for charts"""
    try:
        # Query to get sales data by tour
        sales_by_tour = db.session.query(
            Tur.id,
            Tur.adi.label('name'),
            func.count(Rezervasyon.id).label('bookings'),
            func.sum(Rezervasyon.kisi_sayisi * Tur.fiyat).label('revenue')
        ).join(Rezervasyon, Rezervasyon.tur_id == Tur.id)\
         .group_by(Tur.id, Tur.adi)\
         .order_by(func.sum(Rezervasyon.kisi_sayisi * Tur.fiyat).desc())\
         .limit(10).all()
        
        # If no data, provide sample data
        if not sales_by_tour:
            sample_data = {
                'tours': ['Cappadocia', 'Istanbul', 'Antalya', 'Pamukkale', 'Izmir', 'Bodrum'],
                'bookings': [265, 248, 192, 137, 105, 98],
                'revenue': [583000, 496000, 422400, 246600, 189000, 215600],
                'ratings': [4.9, 4.7, 4.5, 4.8, 4.6, 4.7]
            }
            return jsonify(sample_data)
        
        # Process query results
        tours = []
        bookings = []
        revenue = []
        
        for tour in sales_by_tour:
            tours.append(tour.name)
            bookings.append(tour.bookings)
            revenue.append(float(tour.revenue or 0))
        
        # Add sample ratings as we may not have that data
        ratings = [round(4.5 + 0.5 * (i / len(tours)), 1) for i in range(len(tours))]
        
        return jsonify({
            'tours': tours,
            'bookings': bookings,
            'revenue': revenue,
            'ratings': ratings
        })
    except Exception as e:
        import traceback
        print(f"Error in get_sales_by_tour: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500