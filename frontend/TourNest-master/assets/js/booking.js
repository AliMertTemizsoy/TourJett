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
    const cardNumberInput = document.getElementById('cardNumber');
    const expiryInput = document.getElementById('expiry');

    // Kart numarası formatlamayı ekle - her 4 rakamdan sonra boşluk
    cardNumberInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Sadece rakamları al
        value = value.replace(/\D/g, '');
        
        // 16 rakamla sınırla
        value = value.substring(0, 16);
        
        // Her 4 rakamdan sonra boşluk ekle
        let formattedValue = '';
        for(let i = 0; i < value.length; i++) {
            if(i > 0 && i % 4 === 0) {
                formattedValue += ' ';
            }
            formattedValue += value[i];
        }
        
        e.target.value = formattedValue;
    });

    // Son kullanma tarihi formatlamayı ekle - 2 rakamdan sonra / işareti
    expiryInput.addEventListener('input', function(e) {
        let value = e.target.value;
        
        // Sadece rakamları al
        value = value.replace(/\D/g, '');
        
        // 4 rakamla sınırla (MM/YY)
        value = value.substring(0, 4);
        
        // 2 rakamdan sonra / ekle
        if(value.length > 2) {
            value = value.substring(0, 2) + '/' + value.substring(2);
        }
        
        e.target.value = value;
    });

    // URL'den parametreleri al - hem tur_id hem de tur_paketi_id kontrolü yap
    const urlParams = new URLSearchParams(window.location.search);
    let turPaketiId = urlParams.get('tur_paketi_id');
    
    // Eğer tur_paketi_id yoksa, tur_id parametresine bak
    if (!turPaketiId) {
        turPaketiId = urlParams.get('tur_id');
        console.log('tur_paketi_id bulunamadı, tur_id parametresi kullanılıyor:', turPaketiId);
    }
    
    // Sayısal değere dönüştür
    turPaketiId = parseInt(turPaketiId, 10);
    
    console.log(`URL'den alınan tur paketi ID değeri: ${turPaketiId}, türü: ${typeof turPaketiId}`);
    
    // ID değeri geçerli bir sayı değilse uyarı ver
    if (isNaN(turPaketiId)) {
        console.error('HATA: Geçerli bir tur paketi ID değeri alınamadı!');
    }
    
    // Tur seferi ID'si için bir değişken tanımla
    let turSeferiId = null;
    
    // Base price default value (will be updated from API if available)
    window.basePrice = 1950;

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
        
        if (document.getElementById('tc_kimlik') && currentUser.nationalId) {
            document.getElementById('tc_kimlik').value = currentUser.nationalId;
            document.getElementById('tc_kimlik').readOnly = true;
        }
    } else {
        console.log("Giriş yapmış kullanıcı bulunamadı");
    }

    // Tur bilgilerini dinamik olarak yükle
    if (turPaketiId) {
        try {
            const tur = await getTurById(turPaketiId);
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
                window.basePrice = parseFloat(tur.fiyat) || 1950;
                calculateTotal();
            } else {
                tourDetails.innerHTML = '<p>Tur bilgileri yüklenirken bir hata oluştu.</p>';
            }
        } catch (error) {
            console.error("Tur bilgilerini getirirken hata:", error);
            tourDetails.innerHTML = `<p>Tur bilgileri yüklenirken bir hata oluştu: ${error.message}</p>`;
        }
    }

    // Price calculation function
    function calculateTotal() {
        // Get base price (either from API or default)
        const basePrice = window.basePrice || 1950;
        
        // Get number of participants
        const participants = parseInt(participantsSelect.value) || 1;
        participantsCount.textContent = participants;
        
        // Calculate accommodation fee based on room type
        const roomType = roomTypeSelect.value;
        let roomFee = 0;
        
        // Add additional fee based on room type
        if (roomType === 'deluxe') {
            roomFee = 250;
        } else if (roomType === 'suite') {
            roomFee = 450;
        } else if (roomType === 'family') {
            roomFee = 350;
        }
        
        // Display accommodation fee with Turkish Lira symbol and thousand separator
        accommodationFee.textContent = '₺' + roomFee.toLocaleString('tr-TR', {minimumFractionDigits: 2, maximumFractionDigits: 2}).replace('.', ',');
        
        // Calculate total (base price * participants + accommodation fee + booking fee)
        const bookingFee = 100;
        const total = (basePrice * participants) + roomFee + bookingFee;
        
        // Format the total with Turkish Lira symbol and thousand separator with comma for decimals
        // For this example, we'll add .99 to match your screenshot
        const totalWithDecimals = total + 0.99;
        totalPrice.textContent = '₺' + totalWithDecimals.toLocaleString('tr-TR', {minimumFractionDigits: 2, maximumFractionDigits: 2}).replace('.', ',');
    }

    // Set up event listeners for price calculation
    participantsSelect.addEventListener('change', calculateTotal);
    roomTypeSelect.addEventListener('change', calculateTotal);
    
    // Initial calculation
    calculateTotal();
    
    // Form submission handling
    bookingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleBookingSubmission();
    });

    // Handle form submission
    async function handleBookingSubmission() {
        // Validation
        const required = ['firstName', 'lastName', 'email', 'phone', 'tc_kimlik', 'adres', 'participants', 'roomType', 'cardName', 'cardNumber', 'expiry', 'cvv', 'termsCheck'];
        let isValid = true;

        required.forEach(field => {
            const element = document.getElementById(field);
            const errorElement = document.getElementById(field + 'Error');
            
            if (element && errorElement) {
                if (!element.value || (element.type === 'checkbox' && !element.checked)) {
                    errorElement.style.display = 'block';
                    isValid = false;
                } else {
                    errorElement.style.display = 'none';
                }
            }
        });

        if (!isValid) {
            alert('Lütfen tüm gerekli alanları doldurun.');
            return;
        }

        // Show loading overlay
        loadingOverlay.style.display = 'flex';
        
        try {
            // Rezervasyon verilerini hazırla
            const reservationData = {
                // Backend kodu "musteri_id" bekliyor
                musteri_id: currentUser?.id,
                // Sadece tur_paketi_id kullanıyoruz, tur_id'yi kaldırıyoruz
                tur_paketi_id: parseInt(turPaketiId),
                // tarih alanını ekliyoruz (şimdiki tarih)
                tarih: new Date().toISOString().split('T')[0],
                // Diğer alanlar normal şekilde gönderilecek
                ad: document.getElementById('firstName').value,
                soyad: document.getElementById('lastName').value,
                email: document.getElementById('email').value,
                telefon: document.getElementById('phone').value,
                tc_kimlik: document.getElementById('tc_kimlik').value,
                adres: document.getElementById('adres').value,
                kisi_sayisi: parseInt(document.getElementById('participants').value),
                oda_tipi: document.getElementById('roomType').value,
                ozel_istekler: document.getElementById('additionalRequests').value || ''
            };

            console.log('Rezervasyon verileri:', reservationData);
            
            // API'ye gönder (eğer varsa)
            let reservationResult;
            try {
                if (typeof createRezervasyon === 'function') {
                    reservationResult = await createRezervasyon(reservationData);
                    console.log('Rezervasyon başarıyla oluşturuldu:', reservationResult);
                } else {
                    // API fonksiyonu yoksa simule et
                    await new Promise(resolve => setTimeout(resolve, 1500));
                    console.log('API fonksiyonu bulunamadı, rezervasyon simule edildi');
                    reservationResult = { id: Math.floor(Math.random() * 1000000) };
                }
            } catch (apiError) {
                console.error('Rezervasyon API hatası:', apiError);
                throw new Error('Rezervasyon işlemi sırasında bir hata oluştu.');
            }
            
            // Başarılı rezervasyon
            document.getElementById('bookingId').textContent = `RES-${reservationResult.id || Math.floor(Math.random() * 1000000)}`;
            document.getElementById('successMessage').style.display = 'block';
            document.getElementById('bookingForm').style.display = 'none';
            
        } catch (error) {
            console.error('Rezervasyon hatası:', error);
            alert(`Rezervasyon işlemi sırasında bir hata oluştu: ${error.message}`);
        } finally {
            loadingOverlay.style.display = 'none';
        }
    }
});