document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.form-login');
    const signupForm = document.querySelector('.form-signup');
    const loginSwitcher = document.querySelector('.switcher-login');
    const signupSwitcher = document.querySelector('.switcher-signup');
    const forms = document.querySelector('.forms');
    
    // Form geçişleri
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
            
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            
            // Form validasyonu
            if (!email || !password) {
                showLoginError('Lütfen e-posta ve şifre alanlarını doldurun');
                return;
            }
            
            try {
                // API isteği yap
                const response = await fetch('http://localhost:5000/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Giriş yapılırken bir hata oluştu');
                }
                
                // Başarılı login işlemi
                loginSuccess(data);
                
            } catch (error) {
                console.error('Login error:', error);
                showLoginError(error.message);
            }
        });
    }
    
    // Signup form işleme
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const passwordConfirm = document.getElementById('signup-password-confirm').value;
            const ad = document.getElementById('name').value;
            const soyad = document.getElementById('surname').value;
            const tc_kimlik = document.getElementById('national-id').value;
            const dogum_tarihi = document.getElementById('birth-date').value;
            
            // Form validasyonu
            if (!email || !password || !ad || !soyad) {
                showSignupError('Lütfen tüm zorunlu alanları doldurun');
                return;
            }
            
            if (password !== passwordConfirm) {
                showSignupError('Şifreler eşleşmiyor');
                return;
            }
            
            try {
                // API isteği yap
                const response = await fetch('http://localhost:5000/api/auth/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email,
                        password,
                        ad,
                        soyad,
                        tc_kimlik,
                        dogum_tarihi
                    })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Kayıt olurken bir hata oluştu');
                }
                
                // Başarılı kayıt
                alert('Kayıt işlemi başarılı! Giriş yapabilirsiniz.');
                loginSuccess(data);
                
            } catch (error) {
                console.error('Signup error:', error);
                showSignupError(error.message);
            }
        });
    }
    
    // Yardımcı fonksiyonlar
    function showLoginError(message) {
        // Hata mesajı için bir div oluştur eğer yoksa
        let errorElement = document.getElementById('login-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = 'login-error';
            errorElement.classList.add('error-message');
            errorElement.style.color = 'red';
            errorElement.style.marginTop = '10px';
            
            const loginButton = document.querySelector('.btn-login');
            loginButton.parentNode.insertBefore(errorElement, loginButton);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    function showSignupError(message) {
        // Hata mesajı için bir div oluştur eğer yoksa
        let errorElement = document.getElementById('signup-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = 'signup-error';
            errorElement.classList.add('error-message');
            errorElement.style.color = 'red';
            errorElement.style.marginTop = '10px';
            
            const signupButton = document.querySelector('.btn-signup');
            signupButton.parentNode.insertBefore(errorElement, signupButton);
        }
        
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    function loginSuccess(userData) {
        // Kullanıcı bilgilerini localStorage'a kaydet
        localStorage.setItem('currentUser', JSON.stringify({
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
    
    // Oturum kontrolü - zaten giriş yapılmışsa ana sayfaya yönlendir
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
    if (currentUser.id) {
        window.location.href = 'index.html';
    }
});