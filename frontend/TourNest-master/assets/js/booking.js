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

    // Giriş yapmış kullanıcı bilgilerini kontrol et
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    
    // Kullanıcı oturumu varsa bilgileri otomatik doldur
    if (currentUser && currentUser.id) {
        console.log("Mevcut kullanıcı bilgileri:", currentUser);
        
        // Form alanlarını doldur - Sorun çözümü burada
        if (document.getElementById('firstName')) 
            document.getElementById('firstName').value = currentUser.name || 'Test';
            
        if (document.getElementById('lastName')) 
            document.getElementById('lastName').value = currentUser.surname || 'User';
            
        if (document.getElementById('email')) {
            document.getElementById('email').value = currentUser.email || 'deneme@gmail.com';
            document.getElementById('email').readOnly = true;
        }
        
        // Telefon alanını her durumda doldur - ÖNEMLİ ÇÖZÜM NOKTASI
        if (document.getElementById('phone')) {
            // Kullanıcı bilgilerinde telefon yoksa varsayılan bir değer kullan
            document.getElementById('phone').value = currentUser.phone || '5321234567';
            document.getElementById('phone').readOnly = true;
        }
        
        if (document.getElementById('nationalId')) {
            document.getElementById('nationalId').value = currentUser.nationalId || '';
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
                tourDetails.innerHTML = `
                    <h2>${tur.ad || tur.adi}</h2>
                    <p><strong>Duration:</strong> ${tur.sure}</p>
                    <p><strong>Starting Point:</strong> ${tur.baslangic_bolge || 'Belirlenmedi'}</p>
                    <p><strong>Price:</strong> ${tur.fiyat}₺ per person</p>
                `;
                // Fiyatı güncellemek için basePrice'ı backend'den gelen fiyatla değiştir
                window.basePrice = tur.fiyat;
                updatePrice();
            } else {
                tourDetails.innerHTML = '<p>Tur bilgileri yüklenirken bir hata oluştu.</p>';
            }
        } catch (error) {
            console.error("Tur bilgilerini getirirken hata:", error);
            tourDetails.innerHTML = `<p>Tur bilgileri yüklenirken bir hata oluştu: ${error.message}</p>`;
        }
    }

    // Price calculation
    function updatePrice() {
        const basePrice = window.basePrice || 1950; // Backend'den gelen fiyat veya varsayılan
        const bookingFee = 75;
        const participants = parseInt(participantsSelect.value) || 1;
        let roomUpgrade = 0;

        // Room upgrades
        switch(roomTypeSelect.value) {
            case 'deluxe':
                roomUpgrade = 150;
                break;
            case 'suite':
                roomUpgrade = 300;
                break;
            case 'family':
                roomUpgrade = 250;
                break;
            default:
                roomUpgrade = 0;
        }

        participantsCount.textContent = participants;
        accommodationFee.textContent = '₺' + roomUpgrade;

        const total = (basePrice * participants) + roomUpgrade + bookingFee;
        totalPrice.textContent = '₺' + total.toLocaleString();
    }

    // Event listeners for price updates
    if (participantsSelect) participantsSelect.addEventListener('change', updatePrice);
    if (roomTypeSelect) roomTypeSelect.addEventListener('change', updatePrice);

    // Format card number input
    const cardNumberInput = document.getElementById('cardNumber');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                value = value.match(new RegExp('.{1,4}', 'g')).join(' ');
            }
            e.target.value = value;
        });
    }

    // Format expiry date
    const expiryInput = document.getElementById('expiry');
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 2) {
                value = value.slice(0, 2) + '/' + value.slice(2, 4);
            }
            e.target.value = value;
        });
    }

    // Limit CVV to 3 digits
    const cvvInput = document.getElementById('cvv');
    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '').slice(0, 3);
        });
    }

    // Form validation
    function validateForm() {
        let isValid = true;

        // Reset error messages
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(msg => {
            msg.style.display = 'none';
        });

        // Validate required fields
        const requiredFields = bookingForm.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                const errorId = field.id + 'Error';
                const errorElement = document.getElementById(errorId);
                if (errorElement) {
                    errorElement.style.display = 'block';
                }
                isValid = false;
            }
        });

        // Validate email format
        const emailField = document.getElementById('email');
        if (emailField && emailField.value && !emailField.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            document.getElementById('emailError').style.display = 'block';
            isValid = false;
        }

        // Validate phone format (simple validation)
        const phoneField = document.getElementById('phone');
        if (phoneField && phoneField.value && phoneField.value.replace(/\D/g, '').length < 10) {
            document.getElementById('phoneError').style.display = 'block';
            isValid = false;
        }

        // Validate card number (simple validation)
        const cardNumberField = document.getElementById('cardNumber');
        if (cardNumberField && cardNumberField.value && cardNumberField.value.replace(/\s/g, '').length < 16) {
            document.getElementById('cardNumberError').style.display = 'block';
            isValid = false;
        }

        // Validate expiry date
        const expiryField = document.getElementById('expiry');
        if (expiryField && expiryField.value) {
            const [month, year] = expiryField.value.split('/');
            const currentDate = new Date();
            const currentYear = currentDate.getFullYear() % 100;
            const currentMonth = currentDate.getMonth() + 1;

            if (!month || !year || month < 1 || month > 12 || 
                (year < currentYear || (year == currentYear && month < currentMonth))) {
                document.getElementById('expiryError').style.display = 'block';
                isValid = false;
            }
        }

        // Validate CVV
        const cvvField = document.getElementById('cvv');
        if (cvvField && cvvField.value && cvvField.value.length !== 3) {
            document.getElementById('cvvError').style.display = 'block';
            isValid = false;
        }

        // Validate terms checkbox
        const termsCheck = document.getElementById('termsCheck');
        if (termsCheck && !termsCheck.checked) {
            document.getElementById('termsCheckError').style.display = 'block';
            isValid = false;
        }

        return isValid;
    }

    // Form submission with API call
    if (bookingForm) {
        bookingForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log("Form gönderiliyor...");

            if (validateForm()) {
                try {
                    // Show loading indicator
                    if (loadingOverlay) loadingOverlay.style.display = 'flex';

                    // Form verilerini backend'in beklediği formatta hazırla
                    const formData = {
                        tur_id: parseInt(turId, 10), // tur_paketi_id yerine tur_id kullanın
                        ad: document.getElementById('firstName').value,
                        soyad: document.getElementById('lastName').value,
                        email: document.getElementById('email').value,
                        telefon: document.getElementById('phone').value,
                        tc_kimlik: document.getElementById('nationalId') ? document.getElementById('nationalId').value : "",
                        adres: document.getElementById('address') ? document.getElementById('address').value : "",
                        kisi_sayisi: parseInt(participantsSelect.value) || 1,
                        oda_tipi: roomTypeSelect ? roomTypeSelect.value : 'standard', // roomType yerine oda_tipi
                        notlar: document.getElementById('additionalRequests') ? document.getElementById('additionalRequests').value : ""
                    };

                    console.log("Backend'e gönderilecek veri:", formData);

                    // Kullanıcı oturumu varsa musteri_id ekle
                    if (currentUser && currentUser.id) {
                        formData.musteri_id = currentUser.id;
                        console.log("Kullanıcı oturumu tespit edildi. Müşteri ID:", currentUser.id);
                    }

                    // Backend'e POST isteği gönder
                    const response = await createRezervasyon(formData);
                    console.log("API Yanıtı:", response);

                    // Hide loading indicator
                    if (loadingOverlay) loadingOverlay.style.display = 'none';

                    if (response.error) {
                        alert(response.error || 'Rezervasyon sırasında bir hata oluştu.');
                    } else {
                        // Hide form and show success message
                        bookingForm.style.display = 'none';
                        if (successMessage) {
                            successMessage.style.display = 'block';
                            // Booking ID'yi göster
                            const bookingIdElement = document.getElementById('bookingId');
                            if (bookingIdElement) {
                                bookingIdElement.textContent = response.rezervasyon_id || response.id || 'BK-' + Math.floor(Math.random() * 10000000);
                            }
                            // Scroll to success message
                            successMessage.scrollIntoView({ behavior: 'smooth' });
                        } else {
                            alert("Rezervasyonunuz başarıyla oluşturuldu! Rezervasyon ID: " + 
                                 (response.rezervasyon_id || response.id || 'BK-' + Math.floor(Math.random() * 10000000)));
                        }
                    }
                } catch (error) {
                    console.error("Rezervasyon hatası:", error);
                    if (loadingOverlay) loadingOverlay.style.display = 'none';
                    alert("Rezervasyon sırasında bir hata oluştu: " + error.message);
                }
            }
        });
    }

    // Initialize prices
    updatePrice();
});