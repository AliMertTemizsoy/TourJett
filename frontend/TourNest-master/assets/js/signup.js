// signup.js içinde
const signupForm = document.querySelector('.form-signup');
if (signupForm) {
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        const name = document.getElementById('name').value;
        const surname = document.getElementById('surname').value;
        const nationalId = document.getElementById('national-id').value;
        const birthDate = document.getElementById('birth-date').value;
        // Telefon alanını ekleyin
        const phone = document.getElementById('signup-phone') ? document.getElementById('signup-phone').value : '';
        
        // Telefon numarası validasyonu (opsiyonel)
        if (phone && !validatePhone(phone)) {
            showSignupError('Lütfen geçerli bir telefon numarası girin (Örn: 05321234567)');
            return;
        }
        
        try {
            console.log('Kayıt bilgileri gönderiliyor:', { email, name, surname, phone });
            
            // API'ye kullanıcı kaydı gönder - telefon alanını ekleyin
            const userData = await signupUser({
                email,
                password,
                ad: name,
                soyad: surname,
                tc_kimlik: nationalId,
                dogum_tarihi: birthDate,
                telefon: phone // Telefon alanı eklendi
            });
            
            if (userData && userData.id) {
                // Kullanıcıya bildirim göster
                alert('Kayıt işlemi başarıyla tamamlandı! Giriş yapılıyor...');
                loginSuccess(userData);
            } else {
                showSignupError('Kayıt işleminde bir hata oluştu.');
            }
        } catch (error) {
            showSignupError(error.message || 'Kayıt işlemi başarısız.');
            console.error('Kayıt hatası:', error);
        }
    });
    
    // Telefon alanına input event listener ekleyin (opsiyonel)
    const phoneInput = document.getElementById('signup-phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            // Sadece rakamları tut
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
}

// Telefon validasyon fonksiyonu (opsiyonel)
function validatePhone(phone) {
    // Türkiye telefon numarası formatı: 05XX XXX XX XX
    const numericPhone = phone.replace(/\D/g, '');
    return numericPhone.length >= 10 && numericPhone.length <= 11;
}

function loginSuccess(userData) {
    console.log('Kullanıcı bilgileri kaydediliyor:', userData);
    
    // Kullanıcı bilgilerini localStorage'a kaydet
    localStorage.setItem('currentUser', JSON.stringify({
        id: userData.id,
        name: userData.ad,
        surname: userData.soyad,
        email: userData.email,
        phone: userData.telefon, // API yanıtından telefon bilgisini al
        nationalId: userData.tc_kimlik
    }));
    
    // SessionStorage'a da kaydet (login.js ile uyumlu olması için)
    sessionStorage.setItem('currentUser', JSON.stringify({
        id: userData.id,
        name: userData.ad,
        surname: userData.soyad,
        email: userData.email,
        phone: userData.telefon, // API yanıtından telefon bilgisini al
        nationalId: userData.tc_kimlik
    }));
    
    // Ana sayfaya yönlendir
    window.location.href = 'index.html';
}

function showSignupError(message) {
    const errorElement = document.getElementById('signup-error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    } else {
        console.error('Signup error:', message);
        alert('Signup error: ' + message);
    }
}