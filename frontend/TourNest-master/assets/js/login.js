// Formlar arasında geçiş
const switchers = [...document.querySelectorAll('.switcher')];

switchers.forEach(item => {
    item.addEventListener('click', function() {
        switchers.forEach(item => item.parentElement.classList.remove('is-active'));
        this.parentElement.classList.add('is-active');
    });
});

// Login ve Signup işlemleri
document.addEventListener('DOMContentLoaded', function() {
    // Login formu
    const loginForm = document.querySelector('.form-login');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            const response = await loginUser(email, password);

            if (response.error) {
                alert(response.error || 'Giriş başarısız. Lütfen bilgilerinizi kontrol edin.');
            } else {
                alert(response.message || 'Giriş başarılı!');
                // Başarılı girişten sonra yönlendirme (örneğin, ana sayfaya)
                window.location.href = 'index.html';
            }
        });
    }

    // Signup formu
    const signupForm = document.querySelector('.form-signup');
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('signup-password-confirm').value;

            // Şifre doğrulama
            if (password !== confirmPassword) {
                alert('Şifreler eşleşmiyor!');
                return;
            }

            const response = await signupUser(email, password);

            if (response.error) {
                alert(response.error || 'Kayıt başarısız. Lütfen tekrar deneyin.');
            } else {
                alert(response.message || 'Kayıt başarılı! Lütfen giriş yapın.');
                // Kayıt başarılıysa login formuna geç
                switchers.forEach(item => item.parentElement.classList.remove('is-active'));
                document.querySelector('.switcher-login').parentElement.classList.add('is-active');
            }
        });
    }
});