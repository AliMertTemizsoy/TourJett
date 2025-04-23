// Reusable function to switch forms
function switchToForm(switcherClass) {
    document.querySelectorAll('.switcher').forEach(item => 
        item.parentElement.classList.remove('is-active')
    );
    document.querySelector(switcherClass).parentElement.classList.add('is-active');
}

// Form switching
document.querySelectorAll('.switcher').forEach(item => {
    item.addEventListener('click', function() {
        switchToForm(`.${this.className.split(' ')[1]}`);
    });
});

// Login and Signup handlers
document.addEventListener('DOMContentLoaded', function() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Login form
    const loginForm = document.querySelector('.form-login');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            const loginButton = loginForm.querySelector('.btn-login');
            const errorDiv = loginForm.querySelector('.error-message') || document.createElement('div');

            // Validation
            if (!emailRegex.test(email)) {
                errorDiv.textContent = 'Geçerli bir e-posta adresi girin!';
                errorDiv.style.color = 'red';
                loginForm.appendChild(errorDiv);
                return;
            }

            // Loading state
            loginButton.disabled = true;
            loginButton.textContent = 'Yükleniyor...';

            try {
                const response = await loginUser(email, password);
                if (response.error) {
                    errorDiv.textContent = response.error || 'Giriş başarısız. Lütfen bilgilerinizi kontrol edin.';
                    errorDiv.style.color = 'red';
                    loginForm.appendChild(errorDiv);
                } else {
                    alert(response.message || 'Giriş başarılı!');
                    window.location.href = 'index.html';
                }
            } catch (error) {
                errorDiv.textContent = 'Bir hata oluştu. Lütfen tekrar deneyin.';
                errorDiv.style.color = 'red';
                loginForm.appendChild(errorDiv);
                console.error('Login error:', error);
            } finally {
                loginButton.disabled = false;
                loginButton.textContent = 'Login';
            }
        });
    }

    // Signup form
    const signupForm = document.querySelector('.form-signup');
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('signup-password-confirm').value;
            const signupButton = signupForm.querySelector('.btn-signup');
            const errorDiv = signupForm.querySelector('.error-message') || document.createElement('div');

            // Validation
            if (!emailRegex.test(email)) {
                errorDiv.textContent = 'Geçerli bir e-posta adresi girin!';
                errorDiv.style.color = 'red';
                signupForm.appendChild(errorDiv);
                return;
            }
            if (password.length < 6) {
                errorDiv.textContent = 'Şifre en az 6 karakter olmalı!';
                errorDiv.style.color = 'red';
                signupForm.appendChild(errorDiv);
                return;
            }
            if (password !== confirmPassword) {
                errorDiv.textContent = 'Şifreler eşleşmiyor!';
                errorDiv.style.color = 'red';
                signupForm.appendChild(errorDiv);
                return;
            }

            // Loading state
            signupButton.disabled = true;
            signupButton.textContent = 'Yükleniyor...';

            try {
                const response = await signupUser(email, password);
                if (response.error) {
                    errorDiv.textContent = response.error || 'Kayıt başarısız. Lütfen tekrar deneyin.';
                    errorDiv.style.color = 'red';
                    signupForm.appendChild(errorDiv);
                } else {
                    alert(response.message || 'Kayıt başarılı! Lütfen giriş yapın.');
                    switchToForm('.switcher-login');
                }
            } catch (error) {
                errorDiv.textContent = 'Bir hata oluştu. Lütfen tekrar deneyin.';
                errorDiv.style.color = 'red';
                signupForm.appendChild(errorDiv);
                console.error('Signup error:', error);
            } finally {
                signupButton.disabled = false;
                signupButton.textContent = 'Continue';
            }
        });
    }
});