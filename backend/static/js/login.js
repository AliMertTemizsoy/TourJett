const switchers = [...document.querySelectorAll('.switcher')]

switchers.forEach(item => {
	item.addEventListener('click', function() {
		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
		this.parentElement.classList.add('is-active')
	})
})

// login.js dosyasına ekleyin - login başarılı olduğunda
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

// login.js içinde
const loginForm = document.querySelector('.form-login');
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        try {
            // API'den kullanıcı bilgilerini al
            const userData = await loginUser({ email, password });
            if (userData && userData.id) {
                loginSuccess(userData);
            } else {
                // Hata mesajı göster
                showLoginError('Kullanıcı adı veya şifre hatalı!');
            }
        } catch (error) {
            showLoginError('Giriş yapılırken bir hata oluştu.');
            console.error(error);
        }
    });
}
