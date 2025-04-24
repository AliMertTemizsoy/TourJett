document.addEventListener('DOMContentLoaded', function() {
    console.log('Login.js yüklendi!');
    
    // URL parametrelerini kontrol et
    const urlParams = new URLSearchParams(window.location.search);
    const logout = urlParams.get('logout');
    
    // Eğer logout=true parametresi varsa, oturumu sonlandır
    if (logout === 'true') {
        console.log('Oturum sonlandırılıyor...');
        sessionStorage.removeItem('currentUser');
        // URL'den logout parametresini kaldır
        window.history.replaceState({}, document.title, 'login.html');
    }
    
    const loginForm = document.querySelector('.form-login');
    const signupForm = document.querySelector('.form-signup');
    const loginSwitcher = document.querySelector('.switcher-login');
    const signupSwitcher = document.querySelector('.switcher-signup');
    
    // Form geçiş fonksiyonları
    if (signupSwitcher) {
        signupSwitcher.addEventListener('click', function() {
            console.log('Signup geçiş tıklandı');
            document.querySelector('.form-wrapper.is-active').classList.remove('is-active');
            document.querySelectorAll('.form-wrapper')[1].classList.add('is-active');
        });
    }
    
    if (loginSwitcher) {
        loginSwitcher.addEventListener('click', function() {
            console.log('Login geçiş tıklandı');
            document.querySelector('.form-wrapper.is-active').classList.remove('is-active');
            document.querySelectorAll('.form-wrapper')[0].classList.add('is-active');
        });
    }
    
    // Login form işleme
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Login form gönderildi');
            
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            
            // Form validasyonu
            if (!email || !password) {
                showLoginError('Lütfen e-posta ve şifre alanlarını doldurun');
                return;
            }
            
            try {
                // API.js'den loginUser fonksiyonunu çağırın
                if (typeof window.loginUser === 'function') {
                    const userData = await window.loginUser({
                        email: email,
                        password: password
                    });
                    
                    // Başarılı login
                    console.log('Login başarılı:', userData);
                    loginSuccess(userData);
                } else {
                    console.error('loginUser fonksiyonu API.js dosyasında bulunamadı!');
                    showLoginError('API bağlantısı kurulamadı');
                }
            } catch (error) {
                console.error('Login hatası:', error);
                showLoginError(error.message || 'Giriş yapılırken bir hata oluştu');
            }
        });
    }
    
    // Signup form işleme
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Signup form gönderildi');
            
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const passwordConfirm = document.getElementById('signup-password-confirm').value;
            const name = document.getElementById('name').value;
            const surname = document.getElementById('surname').value;
            
            // Form validasyonu
            if (!email || !password || !passwordConfirm || !name || !surname) {
                showSignupError('Lütfen tüm zorunlu alanları doldurun');
                return;
            }
            
            if (password !== passwordConfirm) {
                showSignupError('Şifreler eşleşmiyor');
                return;
            }
            
            try {
                // API.js'den signupUser fonksiyonunu çağırın
                if (typeof window.signupUser === 'function') {
                    const userData = await window.signupUser({
                        email: email,
                        password: password,
                        ad: name,
                        soyad: surname,
                        tc_kimlik: document.getElementById('national-id').value,
                        dogum_tarihi: document.getElementById('birth-date').value
                    });
                    
                    // Başarılı kayıt
                    console.log('Kayıt başarılı:', userData);
                    
                    // Kullanıcıyı bilgilendir
                    alert('Kayıt işlemi başarıyla tamamlandı!');
                    
                    // Oturum bilgilerini kaydet ve ana sayfaya yönlendir
                    loginOneTime(userData);
                } else {
                    console.error('signupUser fonksiyonu API.js dosyasında bulunamadı!');
                    showSignupError('API bağlantısı kurulamadı');
                }
            } catch (error) {
                console.error('Kayıt hatası:', error);
                showSignupError(error.message || 'Kayıt yapılırken bir hata oluştu');
            }
        });
    }
    
    // Hata mesajlarını gösterme fonksiyonları
    function showLoginError(message) {
        const errorElement = document.getElementById('login-error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        } else {
            console.error('Login error element bulunamadı');
            alert('Giriş hatası: ' + message);
        }
    }
    
    function showSignupError(message) {
        const errorElement = document.getElementById('signup-error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        } else {
            console.error('Signup error element bulunamadı');
            alert('Kayıt hatası: ' + message);
        }
    }
    
    // Login başarılı olduğunda bu fonksiyon çağrılır
	function loginSuccess(userData) {
		console.log('Login başarılı. Kaydedilecek kullanıcı bilgileri:', userData);
		
		// Kullanıcı bilgilerini sessionStorage'a kaydet
		sessionStorage.setItem('currentUser', JSON.stringify({
			id: userData.id,
			name: userData.ad, // API'den gelen alan adı "ad" olmalı
			surname: userData.soyad, // API'den gelen alan adı "soyad" olmalı
			email: userData.email,
			phone: userData.telefon, // API'den gelen alan adı "telefon" olmalı
			nationalId: userData.tc_kimlik  // API'den gelen alan adı "tc_kimlik" olmalı
		}));
		
		// Ana sayfaya yönlendir
		window.location.href = 'index.html';
	}
    
    function loginOneTime(userData) {
        // Kullanıcı bilgilerini sessionStorage'a kaydet
        sessionStorage.setItem('currentUser', JSON.stringify({
            id: userData.id,
            name: userData.ad, 
            surname: userData.soyad,
            email: userData.email,
            phone: userData.telefon,
            nationalId: userData.tc_kimlik
        }));
        
        // Ana sayfaya yönlendir
        window.location.href = 'index.html';
    }
    
    // Logout parametresi true ise kontrolü atla
    if (logout === 'true') {
        return; // Oturum zaten sonlandırıldı
    }
    
    // Oturum kontrolü - zaten giriş yapılmışsa ana sayfaya yönlendir
    const currentUser = JSON.parse(sessionStorage.getItem('currentUser') || '{}'); 
    if (currentUser.id) {
        // Kullanıcı zaten giriş yapmış, ana sayfaya yönlendir
        console.log('Kullanıcı zaten giriş yapmış, ana sayfaya yönlendiriliyor...');
        window.location.href = 'index.html';
    }
});