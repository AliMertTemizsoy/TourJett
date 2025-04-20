const switchers = [...document.querySelectorAll('.switcher')]

switchers.forEach(item => {
	item.addEventListener('click', function() {
		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
		this.parentElement.classList.add('is-active')
	})
})

// API BASE URL (api.js'den alınır)
const API_BASE_URL = 'http://localhost:5000';

// Giriş Fonksiyonu
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        if (data.success) {
            window.location.href = 'index.html'; // Giriş başarılı
        } else {
            alert('Hatalı giriş: ' + (data.message || 'Bilgilerinizi kontrol edin'));
        }
    } catch (error) {
        console.error('Giriş hatası:', error);
        alert('Sunucu hatası! Lütfen tekrar deneyin.');
    }
}

// Form Submit Eventi (HTML'deki form ID'si "login-form" olmalı)
document.getElementById('login-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    loginUser(email, password);
});
