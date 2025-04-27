document.addEventListener('DOMContentLoaded', async function() {
    // Form elements
    const bookingForm = document.getElementById('bookingForm');
    const participantsSelect = document.getElementById('participants');
    const roomTypeSelect = document.getElementById('roomType');
    const participantsCount = document.getElementById('participantsCount');
    const accommodationFee = document.getElementById('accommodationFee');
    const totalPrice = document.getElementById('totalPrice');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const successMessage = document.getElementById('successMessage');
    const tourDetails = document.querySelector('.tour-details');

    // URL'den tur_id parametresini al
    const urlParams = new URLSearchParams(window.location.search);
    const turId = urlParams.get('tur_id');
    
    // Tur seferi ID'si için bir değişken tanımla
    let turSeferiId = null;

    // Giriş yapmış kullanıcı bilgilerini kontrol et - localStorage ve sessionStorage'dan kontrol et
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || sessionStorage.getItem('currentUser') || '{}');
    
    // Kullanıcı oturumu varsa bilgileri otomatik doldur
    if (currentUser && currentUser.id) {
        console.log("Mevcut kullanıcı bilgileri:", currentUser);
        
        // Form alanlarını doldur - Sadece mevcut bilgileri kullan, varsayılan değer kullanma
        if (document.getElementById('firstName') && currentUser.name) {
            document.getElementById('firstName').value = currentUser.name;
        }
            
        if (document.getElementById('lastName') && currentUser.surname) {
            document.getElementById('lastName').value = currentUser.surname;
        }
            
        if (document.getElementById('email') && currentUser.email) {
            document.getElementById('email').value = currentUser.email;
            document.getElementById('email').readOnly = true;
        }
        
        if (document.getElementById('phone') && currentUser.phone) {
            document.getElementById('phone').value = currentUser.phone;
            document.getElementById('phone').readOnly = true;
        }
        
        if (document.getElementById('nationalId') && currentUser.nationalId) {
            document.getElementById('nationalId').value = currentUser.nationalId;
            document.getElementById('nationalId').readOnly = true;
        }
    } else {
        console.log("Giriş yapmış kullanıcı bulunamadı");
    }

    // Tur bilgilerini dinamik olarak yükle
    if (turId) {
        try {
            const tur = await getTurById(turId);
            if (tur) {
                console.log("Yüklenen tur bilgisi:", tur);
                
                // Tur seferi ID varsa onu al (API dönüşümü farklı olabilir)
                if (tur.sefer_id) {
                    turSeferiId = tur.sefer_id;
                    console.log("Tur seferi ID bulundu:", turSeferiId);
                }
                
                // Eğer API tur_seferleri diye bir dizi dönüyorsa, ilk aktif seferi al
                if (tur.tur_seferleri && tur.tur_seferleri.length > 0) {
                    const aktifSefer = tur.tur_seferleri.find(sefer => sefer.durum === 'aktif');
                    if (aktifSefer) {
                        turSeferiId = aktifSefer.id;
                        console.log("Aktif tur seferi ID bulundu:", turSeferiId);
                    }
                }
                
                tourDetails.innerHTML = `
                    <h2>${tur.ad || tur.adi}</h2>
                    <p><strong>Duration:</strong> ${tur.sure}</p>
                    <p><strong>Starting Point:</strong> ${tur.baslangic_bolge || 'Belirlenmedi'}</p>
                    <p><strong>Price:</strong> ${tur.fiyat}₺ per person</p>
                `;
                // Fiyatı güncellemek için basePrice'ı backend'den gelen fiyatla değiştir
                window.basePrice = tur.fiyat;
                calculateTotal();
            } else {
                tourDetails.innerHTML = '<p>Tur bilgileri yüklenirken bir hata oluştu.</p>';
            }
        } catch (error) {
            console.error("Tur bilgilerini getirirken hata:", error);
            tourDetails.innerHTML = `<p>Tur bilgileri yüklenirken bir hata oluştu: ${error.message}</p>`;
        }
    }

    // Price calculation functions
    function calculateTotal() {
        // Base price is ₺1.950
        const basePrice = 1950;
        
        // Get number of participants
        const participants = parseInt(document.getElementById('participants').value) || 1;
        document.getElementById('participantsCount').textContent = participants;
        
        // Calculate accommodation fee based on room type
        const roomType = document.getElementById('roomType').value;
        let accommodationFee = 0;
        
        // Add additional fee based on room type
        if (roomType === 'deluxe') {
            accommodationFee = 150;
        } else if (roomType === 'suite') {
            accommodationFee = 300;
        } else if (roomType === 'family') {
            accommodationFee = 250;
        }
        
        // Display accommodation fee with Turkish Lira symbol and thousand separator
        document.getElementById('accommodationFee').textContent = '₺' + accommodationFee.toLocaleString('tr-TR');
        
        // Calculate total (base price * participants + accommodation fee + booking fee)
        const bookingFee = 75;
        const total = (basePrice * participants) + accommodationFee + bookingFee;
        
        // Format the total with Turkish Lira symbol and thousand separator with comma for decimals
        document.getElementById('totalPrice').textContent = '₺' + total.toLocaleString('tr-TR');
    }

    // Initialize on document load
    document.addEventListener('DOMContentLoaded', function() {
        // Set up event listeners for price calculation
        document.getElementById('participants').addEventListener('change', calculateTotal);
        document.getElementById('roomType').addEventListener('change', calculateTotal);
        
        // Initial calculation
        calculateTotal();
        
        // Form submission handling
        document.getElementById('bookingForm').addEventListener('submit', function(e) {
            e.preventDefault();
            handleBookingSubmission();
        });
    });

    // Handle form submission
    async function handleBookingSubmission() {
        // Show loading overlay
        document.getElementById('loadingOverlay').style.display = 'flex';
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        try {
            // Get form data
            const formData = {
                firstName: document.getElementById('firstName').value,
                lastName: document.getElementById('lastName').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                tc_kimlik: document.getElementById('tc_kimlik').value,
                adres: document.getElementById('adres').value,
                participants: document.getElementById('participants').value,
                roomType: document.getElementById('roomType').value,
                additionalRequests: document.getElementById('additionalRequests').value,
                // Payment details would be handled securely in a real application
            };
            
            // Generate a random booking ID for demo purposes
            const bookingId = 'BK-' + Math.floor(Math.random() * 1000000);
            
            // Display success message with booking ID
            document.getElementById('bookingId').textContent = bookingId;
            document.getElementById('successMessage').style.display = 'block';
            document.getElementById('bookingForm').style.display = 'none';
            
            // Log the booking data (for demo purposes only)
            console.log('Booking submitted:', formData);
            
        } catch (error) {
            // Handle errors
            console.error('Booking submission failed:', error);
            alert('There was an error processing your booking. Please try again.');
        } finally {
            // Hide loading overlay
            document.getElementById('loadingOverlay').style.display = 'none';
        }
    }
});