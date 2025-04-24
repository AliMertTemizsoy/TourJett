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
        
        try {
            // API'ye kullanıcı kaydı gönder
            const userData = await signupUser({
                email,
                password,
                ad: name,
                soyad: surname,
                tc_kimlik: nationalId,
                dogum_tarihi: birthDate
            });
            
            if (userData && userData.id) {
                loginSuccess(userData);
            } else {
                showSignupError('Kayıt işleminde bir hata oluştu.');
            }
        } catch (error) {
            showSignupError('Kayıt işlemi başarısız.');
            console.error(error);
        }
    });
}