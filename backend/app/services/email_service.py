# backend/app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import logging
from app.models import TurPaketi, Surucu, Rehber, Tur

def send_email(recipient, subject, html_content):
    """
    Sends an email using SMTP
    
    Args:
        recipient: Email recipient
        subject: Email subject
        html_content: HTML content of the email
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Get email settings from config
        smtp_server = current_app.config.get('MAIL_SERVER', 'smtp.gmail.com')
        smtp_port = current_app.config.get('MAIL_PORT', 587)
        smtp_username = current_app.config.get('MAIL_USERNAME', 'your-email@example.com')
        smtp_password = current_app.config.get('MAIL_PASSWORD', 'your-password')
        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'TourJett <info@tourjett.com>')
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient, message.as_string())
            
        logging.info(f"Email sent to {recipient}: {subject}")
        return True
        
    except Exception as e:
        logging.error(f"Email sending failed: {str(e)}")
        return False

def send_reservation_notification_to_driver(reservation):
    """Send notification email to the driver about a new reservation"""
    try:
        # Get the tour package info which contains driver info
        if not reservation.tur_paketi_id:
            logging.warning("No tour package ID in reservation, cannot notify driver")
            return False
            
        # Get tour package, which has the driver relationship
        tour_package = TurPaketi.query.get(reservation.tur_paketi_id)
        if not tour_package or not tour_package.surucu_id:
            logging.warning("Tour package not found or has no driver assigned")
            return False
            
        # Get driver contact info
        driver = Surucu.query.get(tour_package.surucu_id)
        if not driver or not driver.email:
            logging.warning(f"Driver not found or has no email: ID {tour_package.surucu_id}")
            return False
            
        # Create email content
        subject = f"Yeni Rezervasyon: {tour_package.ad} turu için"
        
        # Format the date properly
        reservation_date = reservation.tarih.strftime('%d.%m.%Y') if reservation.tarih else "Belirtilmemiş"
        
        html_content = f"""
        <html>
            <body>
                <h2>Yeni bir tur rezervasyonu oluşturuldu</h2>
                <p>Sayın {driver.ad} {driver.soyad},</p>
                <p>Sizin sürücü olarak görevlendirildiğiniz bir tur için yeni bir rezervasyon yapıldı.</p>
                
                <h3>Rezervasyon Detayları:</h3>
                <ul>
                    <li><strong>Tur Paketi:</strong> {tour_package.ad}</li>
                    <li><strong>Rezervasyon ID:</strong> REZ-{reservation.id}</li>
                    <li><strong>Tarih:</strong> {reservation_date}</li>
                    <li><strong>Müşteri:</strong> {reservation.ad} {reservation.soyad}</li>
                    <li><strong>Kişi Sayısı:</strong> {reservation.kisi_sayisi}</li>
                </ul>
                
                <p>Bu rezervasyonla ilgili detayları TourJett sisteminden görebilirsiniz.</p>
                
                <p>İyi çalışmalar dileriz,<br>
                TourJett Ekibi</p>
            </body>
        </html>
        """
        
        return send_email(driver.email, subject, html_content)
        
    except Exception as e:
        logging.error(f"Error sending driver notification email: {str(e)}")
        return False

def send_reservation_notification_to_guide(reservation):
    """Send notification email to the guide about a new reservation"""
    try:
        # Get the tour package info which contains guide info
        if not reservation.tur_paketi_id:
            logging.warning("No tour package ID in reservation, cannot notify guide")
            return False
            
        # Get tour package, which has the guide relationship
        tour_package = TurPaketi.query.get(reservation.tur_paketi_id)
        if not tour_package or not tour_package.rehber_id:
            logging.warning("Tour package not found or has no guide assigned")
            return False
            
        # Get guide contact info
        guide = Rehber.query.get(tour_package.rehber_id)
        if not guide or not guide.email:
            logging.warning(f"Guide not found or has no email: ID {tour_package.rehber_id}")
            return False
            
        # Create email content
        subject = f"Yeni Rezervasyon: {tour_package.ad} turu için"
        
        # Format the date properly
        reservation_date = reservation.tarih.strftime('%d.%m.%Y') if reservation.tarih else "Belirtilmemiş"
        
        html_content = f"""
        <html>
            <body>
                <h2>Yeni bir tur rezervasyonu oluşturuldu</h2>
                <p>Sayın {guide.ad} {guide.soyad},</p>
                <p>Sizin rehber olarak görevlendirildiğiniz bir tur için yeni bir rezervasyon yapıldı.</p>
                
                <h3>Rezervasyon Detayları:</h3>
                <ul>
                    <li><strong>Tur Paketi:</strong> {tour_package.ad}</li>
                    <li><strong>Rezervasyon ID:</strong> REZ-{reservation.id}</li>
                    <li><strong>Tarih:</strong> {reservation_date}</li>
                    <li><strong>Müşteri:</strong> {reservation.ad} {reservation.soyad}</li>
                    <li><strong>Kişi Sayısı:</strong> {reservation.kisi_sayisi}</li>
                    <li><strong>Müşteri İletişim:</strong> {reservation.email}, {reservation.telefon}</li>
                    <li><strong>Özel İstekler:</strong> {reservation.ozel_istekler or 'Belirtilmemiş'}</li>
                </ul>
                
                <p>Bu rezervasyonla ilgili detayları TourJett sisteminden görebilirsiniz.</p>
                
                <p>İyi çalışmalar dileriz,<br>
                TourJett Ekibi</p>
            </body>
        </html>
        """
        
        return send_email(guide.email, subject, html_content)
        
    except Exception as e:
        logging.error(f"Error sending guide notification email: {str(e)}")
        return False