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
    
    // Yeni sayfa yapısına göre form seçicilerini güncelliyoruz
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginTab = document.getElementById('loginTab');
    const signupTab = document.getElementById('signupTab');
    
    // Tab geçiş kontrolleri zaten HTML içinde JavaScript olarak eklendi
    
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
            
            // Admin girişi kontrolü - updated with proper email format
            if ((email === 'admin@admin.com' || email === 'admin') && password === 'admin') {
                console.log('Admin girişi tespit edildi');
                // Admin bilgilerini sessionStorage'a kaydet
                sessionStorage.setItem('currentUser', JSON.stringify({
                    id: 'admin',
                    name: 'Admin',
                    surname: 'User',
                    email: 'admin@admin.com',
                    role: 'admin'
                }));
                
                // Dashboard sayfasına yönlendir
                window.location.href = 'dashboard.html';
                return;
            }
            
            try {
                // API.js'den loginUser fonksiyonunu çağırın
                if (typeof window.loginUser === 'function') {
                    console.log("Login işlemi başlatılıyor...");
                    
                    // Test amaçlı basit bir admin girişini doğrudan kabul edelim
                    if (email === "admin" && password === "admin") {
                        console.log("Demo modu: Admin girişi tespit edildi");
                        sessionStorage.setItem('currentUser', JSON.stringify({
                            id: 'admin123',
                            name: 'Admin',
                            surname: 'User',
                            email: 'admin@admin.com',
                            role: 'admin'
                        }));
                        window.location.href = 'index_loggedinuser.html';
                        return;
                    }
                    
                    // Demo kullanıcı girişi (geçici çözüm)
                    if (email === "user@example.com" && password === "password") {
                        console.log("Demo modu: Test kullanıcısı tespit edildi");
                        sessionStorage.setItem('currentUser', JSON.stringify({
                            id: 'user123',
                            name: 'Demo',
                            surname: 'User',
                            email: 'user@example.com',
                            role: 'user'
                        }));
                        window.location.href = 'index_loggedinuser.html';
                        return;
                    }
                    
                    // Gerçek API çağrısı
                    try {
                        const userData = await window.loginUser({
                            email: email,
                            password: password
                        });
                        
                        // Başarılı login
                        console.log('Login başarılı:', userData);
                        loginSuccess(userData);
                    } catch (apiError) {
                        console.error('API hatası:', apiError);
                        showLoginError(apiError.message || 'Giriş yapılırken bir hata oluştu. API erişilemez olabilir.');
                    }
                } else {
                    console.error('loginUser fonksiyonu API.js dosyasında bulunamadı!');
                    showLoginError('API bağlantısı kurulamadı - loginUser fonksiyonu eksik');
                }
            } catch (error) {
                console.error('Login hatası:', error);
                showLoginError(error.message || 'Giriş yapılırken beklenmeyen bir hata oluştu');
            }
        });
    } else {
        console.error('Login form bulunamadı!');
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
    } else {
        console.error('Signup form bulunamadı!');
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
        
        // Giriş yapan kullanıcı için özel ana sayfaya yönlendir
        window.location.href = 'index_loggedinuser.html';
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
        
        // Giriş yapan kullanıcı için özel ana sayfaya yönlendir
        window.location.href = 'index_loggedinuser.html';
    }
    
    // Logout parametresi true ise kontrolü atla
    if (logout === 'true') {
        return; // Oturum zaten sonlandırıldı
    }
    
    // Oturum kontrolü - zaten giriş yapılmışsa ana sayfaya yönlendir
    const currentUser = JSON.parse(sessionStorage.getItem('currentUser') || '{}'); 
    if (currentUser.id) {
        // Kullanıcı zaten giriş yapmış, giriş yapan kullanıcı için özel ana sayfaya yönlendir
        console.log('Kullanıcı zaten giriş yapmış, giriş yapan kullanıcı için özel ana sayfaya yönlendiriliyor...');
        window.location.href = 'index_loggedinuser.html';
    }
});