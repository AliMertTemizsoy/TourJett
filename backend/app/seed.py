from app import db, create_app
from app.models.surucu import Surucu
from app.models.vehicle import Vehicles
from app.models.rehber import Rehber
from app.models.destinasyon import Destinasyon
from app.models.tur import Tur, TurSeferi
from app.models.tur_paketi import TurPaketi, TurDestinasyon
from datetime import datetime, timedelta
import random
from faker import Faker
import os
import sqlalchemy

fake = Faker(['tr_TR'])

def seed_data():
    """Seed the database with dummy data."""
    app = create_app()
    with app.app_context():
        # We no longer delete existing data
        print("Seeding data...")
        
        # Create 5 drivers (Surucu)
        drivers = []
        for i in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            driver = Surucu(
                ad=first_name,
                soyad=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}@example.com",
                telefon=fake.bothify(text='05#########')[:20],  # Make sure phone number is under 20 chars
                ehliyet_no=fake.bothify(text='?####-#####')[:20],  # Make sure license number is shorter
                ehliyet_sinifi=random.choice(['B', 'C', 'D', 'E']),
                deneyim_yil=random.randint(1, 20),
                dogum_tarihi=fake.date_of_birth(minimum_age=25, maximum_age=60),
                adres=fake.address(),
                uyruk="Türkiye",
                aktif=True
            )
            db.session.add(driver)
            drivers.append(driver)
        
        # Create 5 guides (Rehber)
        guides = []
        languages = ['Türkçe, İngilizce', 'Türkçe, Almanca', 'Türkçe, Fransızca', 
                    'Türkçe, Rusça', 'Türkçe, Arapça']
        
        for i in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            guide = Rehber(
                ad=first_name,
                soyad=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}@rehber.com",
                telefon=fake.bothify(text='05#########')[:20],  # Ensure under 20 chars
                dil_bilgisi=languages[i],
                deneyim_yili=random.randint(1, 15),
                aciklama=fake.paragraph(),
                aktif=True
            )
            db.session.add(guide)
            guides.append(guide)
        
        # Create 5 vehicles
        vehicle_types = ['Otobüs', 'Minibüs', 'Van', 'Jeep', 'Sedan']
        vehicle_models = ['Mercedes Travego', 'Mercedes Sprinter', 'Volkswagen Transporter', 
                         'Land Rover Discovery', 'Toyota Corolla']
        capacities = [45, 16, 8, 5, 4]
        
        vehicles = []
        for i in range(5):
            vehicle = Vehicles(
                type=vehicle_types[i],
                model=vehicle_models[i],
                capacity=capacities[i],
                license_plate=fake.bothify(text='## ?? ###')[:10],  # Ensure under character limit
                status='available',
                last_maintenance_date=fake.date_this_year(),
                next_maintenance_date=fake.date_between(start_date='today', end_date='+6m'),
                purchase_date=fake.date_between(start_date='-5y', end_date='-1y'),
                surucu_id=drivers[i].id
            )
            db.session.add(vehicle)
            vehicles.append(vehicle)
        
        # Commit to get IDs for drivers and vehicles
        db.session.commit()
        
        # Create 10 destinations
        destinations = []
        cities = ['İstanbul', 'Antalya', 'Kapadokya', 'İzmir', 'Bodrum', 
                 'Pamukkale', 'Efes', 'Mardin', 'Trabzon', 'Çanakkale']
        
        for i in range(10):
            dest = Destinasyon(
                ad=cities[i],
                aciklama=fake.paragraph(),
                ulke='Türkiye',
                sehir=cities[i],
                adres=fake.address(),
                enlem=float(fake.latitude()),
                boylam=float(fake.longitude())
            )
            db.session.add(dest)
            destinations.append(dest)
        
        # Commit to get IDs for destinations
        db.session.commit()
        
        # Create 20 tours (Tur)
        tours = []
        tour_categories = ['Kültür', 'Doğa', 'Tarih', 'Deniz', 'Gastronomi']
        tour_durations = ['1 gün', '2 gün', '3 gün', '5 gün', '7 gün', '10 gün']
        
        for i in range(20):
            tour_name = f"{random.choice(['Muhteşem', 'Büyülü', 'Eşsiz', 'Klasik', 'Özel'])} {random.choice(cities)} Turu"
            tour = Tur(
                adi=tour_name,
                sure=random.choice(tour_durations),
                fiyat=random.randint(500, 5000),
                aciklama=fake.paragraph(),
                resim=f"assets/images/tours/tour{i+1}.jpg",  # Update with correct path to tour images
                kategori=random.choice(tour_categories),
                destinasyon_id=random.choice(destinations).id,
                aktif=True
            )
            db.session.add(tour)
            tours.append(tour)
        
        # Commit to get IDs for tours
        db.session.commit()
        
        # Reset sequences for TurPaketi to ensure IDs start from 1
        try:
            db.session.execute(sqlalchemy.text("ALTER SEQUENCE tur_paketleri_id_seq RESTART WITH 1"))
            db.session.commit()
            print("Reset TurPaketi ID sequence to 1")
        except Exception as e:
            print(f"Could not reset sequence: {e}")
            # Continue anyway
        
        # Create 40 tour packages (TurPaketi)
        tour_packages = []
        statuses = ["Aktif", "Yakında", "Tamamlandı", "İptal Edildi"]
        
        for i in range(40):
            # We want image numbers to start from 1 and match our index
            image_number = i + 1
            # For images > 30, cycle back to ensure we stay within available images
            if image_number > 30:
                image_number = image_number % 30
                if image_number == 0:
                    image_number = 30  # Handle the case where index is a multiple of 30
            
            # Randomly select entities for relations
            random_tour = random.choice(tours)
            random_driver = random.choice(drivers)
            random_guide = random.choice(guides)
            random_vehicle = random.choice(vehicles)
            random_destination = random.choice(destinations)
            
            # Calculate a future date for the tour
            tour_date = datetime.now() + timedelta(days=random.randint(10, 365))
            
            # Create tour package with full image path
            package = TurPaketi(
                ad=f"{random_tour.adi} - Paket {i+1}",
                aciklama=fake.paragraph(),
                sure=random_tour.sure,
                kapasite=min(random_vehicle.capacity, random.randint(10, 30)),
                tur_id=random_tour.id,
                durum=random.choice(statuses),
                surucu_id=random_driver.id,
                rehber_id=random_guide.id,
                vehicle_id=random_vehicle.id,
                tur_tarihi=tour_date.date(),
                resim_url=f"{image_number}.jpg"  # Just the image number, frontend will add the path
            )
            db.session.add(package)
            tour_packages.append(package)
        
        # Commit to get IDs for tour packages
        db.session.commit()
        
        # Add one destination to each tour package (TurDestinasyon)
        for package in tour_packages:
            # Add exactly one destination to each package
            dest = random.choice(destinations)
            tur_dest = TurDestinasyon(
                tur_paketi_id=package.id,
                destinasyon_id=dest.id,
                siralama=1,  # Always first since there's only one
                kalma_suresi=random.randint(1, 5),
                not_bilgisi=fake.paragraph(nb_sentences=2)
            )
            db.session.add(tur_dest)
        
        db.session.commit()
        print("Seeding completed successfully!")

if __name__ == "__main__":
    seed_data() 