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

    // Tur bilgilerini dinamik olarak yükle
    if (turId) {
        const tur = await getTurById(turId);
        if (tur) {
            tourDetails.innerHTML = `
                <h2>${tur.adi}</h2>
                <p><strong>Date:</strong> ${tur.baslangic_tarihi} - ${tur.bitis_tarihi}</p>
                <p><strong>Duration:</strong> ${tur.sure}</p>
                <p><strong>Starting Point:</strong> ${tur.baslangic_noktasi}</p>
                <p><strong>Price:</strong> $${tur.fiyat} per person</p>
            `;
            // Fiyatı güncellemek için basePrice'ı backend'den gelen fiyatla değiştir
            window.basePrice = tur.fiyat;
            updatePrice();
        } else {
            tourDetails.innerHTML = '<p>Tur bilgileri yüklenirken bir hata oluştu.</p>';
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
        accommodationFee.textContent = '$' + roomUpgrade;

        const total = (basePrice * participants) + roomUpgrade + bookingFee;
        totalPrice.textContent = '$' + total.toLocaleString();
    }

    // Event listeners for price updates
    participantsSelect.addEventListener('change', updatePrice);
    roomTypeSelect.addEventListener('change', updatePrice);

    // Format card number input
    const cardNumberInput = document.getElementById('cardNumber');
    cardNumberInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 0) {
            value = value.match(new RegExp('.{1,4}', 'g')).join(' ');
        }
        e.target.value = value;
    });

    // Format expiry date
    const expiryInput = document.getElementById('expiry');
    expiryInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 2) {
            value = value.slice(0, 2) + '/' + value.slice(2, 4);
        }
        e.target.value = value;
    });

    // Limit CVV to 3 digits
    const cvvInput = document.getElementById('cvv');
    cvvInput.addEventListener('input', function(e) {
        e.target.value = e.target.value.replace(/\D/g, '').slice(0, 3);
    });

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
        if (emailField.value && !emailField.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            document.getElementById('emailError').style.display = 'block';
            isValid = false;
        }

        // Validate phone format (simple validation)
        const phoneField = document.getElementById('phone');
        if (phoneField.value && phoneField.value.replace(/\D/g, '').length < 10) {
            document.getElementById('phoneError').style.display = 'block';
            isValid = false;
        }

        // Validate card number (simple validation)
        const cardNumberField = document.getElementById('cardNumber');
        if (cardNumberField.value && cardNumberField.value.replace(/\s/g, '').length < 16) {
            document.getElementById('cardNumberError').style.display = 'block';
            isValid = false;
        }

        // Validate expiry date
        const expiryField = document.getElementById('expiry');
        if (expiryField.value) {
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
        if (cvvField.value && cvvField.value.length !== 3) {
            document.getElementById('cvvError').style.display = 'block';
            isValid = false;
        }

        // Validate terms checkbox
        const termsCheck = document.getElementById('termsCheck');
        if (!termsCheck.checked) {
            document.getElementById('termsCheckError').style.display = 'block';
            isValid = false;
        }

        return isValid;
    }

    // Form submission with API call
    bookingForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        if (validateForm()) {
            // Show loading indicator
            loadingOverlay.style.display = 'flex';

            // Form verilerini topla
            const formData = {
                turId: turId,
                firstName: document.getElementById('firstName').value,
                lastName: document.getElementById('lastName').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                participants: participantsSelect.value,
                roomType: roomTypeSelect.value,
                additionalRequests: document.getElementById('additionalRequests').value,
                cardName: document.getElementById('cardName').value,
                cardNumber: document.getElementById('cardNumber').value,
                expiry: document.getElementById('expiry').value,
                cvv: document.getElementById('cvv').value
            };

            // Backend'e POST isteği gönder
            const response = await createRezervasyon(formData);

            // Hide loading indicator
            loadingOverlay.style.display = 'none';

            if (response.error) {
                alert(response.error || 'Rezervasyon sırasında bir hata oluştu.');
            } else {
                // Hide form and show success message
                bookingForm.style.display = 'none';
                successMessage.style.display = 'block';

                // Booking ID'yi göster
                document.getElementById('bookingId').textContent = response.booking_id;

                // Scroll to success message
                successMessage.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });

    // Initialize prices
    updatePrice();
});