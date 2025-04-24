document.addEventListener('DOMContentLoaded', function() {
    console.log('Login.js loaded!');
    
    const loginForm = document.querySelector('.form-login');
    const signupForm = document.querySelector('.form-signup');
    const loginSwitcher = document.querySelector('.switcher-login');
    const signupSwitcher = document.querySelector('.switcher-signup');
    
    // Form geçiş işlevselliği
    if (signupSwitcher) {
        signupSwitcher.addEventListener('click', function() {
            document.querySelector('.form-wrapper.is-active').classList.remove('is-active');
            signupSwitcher.parentElement.classList.add('is-active');
        });
    }
    
    if (loginSwitcher) {
        loginSwitcher.addEventListener('click', function() {
            document.querySelector('.form-wrapper.is-active').classList.remove('is-active');
            loginSwitcher.parentElement.classList.add('is-active');
        });
    }
    
    // Login form işleme
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Login form submitted');
            
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            
            // Form validasyonu
            if (!email || !password) {
                showLoginError('Lütfen e-posta ve şifre alanlarını doldurun');
                return;
            }
            
            try {
                // API isteği yap
                const userData = await loginUser({
                    email: email,
                    password: password
                });
                
                // Başarılı login
                console.log('Login successful:', userData);
                loginSuccess(userData);
                
            } catch (error) {
                showLoginError(error.message);
            }
        });
    }
    
    // Signup form işleme
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Signup form submitted');
            
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const passwordConfirm = document.getElementById('signup-password-confirm').value;
            
            // Form validasyonu
            if (!email || !password) {
                showSignupError('Lütfen tüm zorunlu alanları doldurun');
                return;
            }
            
            if (password !== passwordConfirm) {
                showSignupError('Şifreler eşleşmiyor');
                return;
            }
            
            try {
                // API isteği yap - email ve password dışında 
                // name ve surname gibi alanlar login.html sayfanıza eklenmediği için
                // burada varsayılan değerler kullanıyoruz
                const userData = await signupUser({
                    email: email,
                    password: password,
                    ad: "Test",     // Bu alanları login.html'e eklerseniz buraya doğru değerlerle güncelleyin
                    soyad: "User"   // Bu alanları login.html'e eklerseniz buraya doğru değerlerle güncelleyin
                });
                
                // Başarılı kayıt
                console.log('Signup successful:', userData);
                alert('Kayıt işlemi başarılı!');
                
                // Doğrudan ana sayfaya yönlendir - kullanıcı bilgilerini kullan ama hatırlamayalım
                loginOneTime(userData); // sessionStorage'a kaydediyoruz, tarayıcı kapandığında silinecek
                
            } catch (error) {
                showSignupError(error.message);
            }
        });
    }
    
    // Hata mesajı gösterme fonksiyonları
    function showLoginError(message) {
        const errorElement = document.getElementById('login-error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        } else {
            console.error('Login error:', message);
            alert('Login error: ' + message);
        }
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
    
    function loginSuccess(userData) {
        // Kullanıcı bilgilerini sessionStorage'a kaydet (localStorage yerine)
        // sessionStorage tarayıcı kapandığında silinir
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
    
    // Tek seferlik giriş - localStorage kullanmadan sadece o oturum için giriş yap
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
    
    // Auto-login özelliğini kaldırıyoruz
    // Bu sayede sayfa açıldığında otomatik giriş yapılmayacak
    // localStorage.getItem('currentUser') yerine sessionStorage kullanabiliriz
    
    /* Otomatik giriş kodunu kaldırıyoruz
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    if (currentUser.id) {
        // Zaten giriş yapılmışsa ana sayfaya yönlendir
        window.location.href = 'index.html';
    }
    */
});