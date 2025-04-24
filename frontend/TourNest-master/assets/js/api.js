// Mock modunu kapat, gerçek API çağrıları yap
const MOCK_MODE = false;
const API_BASE_URL = 'http://localhost:5000/api'; // Doğru API yolu

// API fonksiyonları
async function getTurlar() {
    if (MOCK_MODE) {
        // Mock veriler
        return [
            {
                id: 1,
                ad: "Kapadokya Turu", // adi -> ad (model uyumluluğu)
                sure: "3 Gün",
                fiyat: 3500,
                aciklama: "Muhteşem peri bacaları ve sıcak hava balonlarıyla unutulmaz bir deneyim",
                resim_url: "assets/images/packages/p1.jpg", // resim -> resim_url
                konum: "Nevşehir" // Konum değeri ekledim
            },
            // Diğer mock veriler...
        ];
    } else {
        try {
            // Endpointte /api/ prefixi eklendi
            const response = await fetch(`${API_BASE_URL}/turpaketleri/`);
            if (!response.ok) {
                throw new Error(`API yanıt vermedi: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Turlar alınamadı:', error);
            throw error;
        }
    }
}

// Tur detaylarını getiren fonksiyon
async function getTurById(id) {
    if (MOCK_MODE) {
        // Mock veri
        return {
            id: id,
            ad: "Kapadokya Turu", // adi -> ad
            sure: "3 Gün",
            fiyat: 3500,
            aciklama: "Muhteşem peri bacaları ve sıcak hava balonlarıyla unutulmaz bir deneyim",
            tur_tarihi: "2025-05-15", // tarih alanını modeldeki ile eşleştirdim
            konum: "Nevşehir", // konum ekledim
            resim_url: "assets/images/packages/p1.jpg", // resim -> resim_url
            max_katilimci: 20 // max_katilimci ekledim
        };
    } else {
        try {
            // Endpointte /api/ prefixi eklendi
            const response = await fetch(`${API_BASE_URL}/turpaketleri/${id}`);
            if (!response.ok) {
                throw new Error(`API yanıt vermedi: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Tur ${id} alınamadı:`, error);
            throw error;
        }
    }
}

// api.js - createRezervasyon fonksiyonunu güncelleyin
async function createRezervasyon(formData) {
    if (MOCK_MODE) {
        // Mock veriler...
        return { success: true, id: 1, message: "Rezervasyon başarıyla oluşturuldu" };
    } else {
        try {
            // Eğer kullanıcı girişi yapılmışsa, kullanıcı ID'sini ekle
            const currentUser = JSON.parse(sessionStorage.getItem('currentUser') || '{}');
            
            // Doğru alan adlarıyla veriyi hazırla
            const apiData = {
                tur_id: parseInt(formData.tur_paketi_id),
                ad: formData.ad,
                soyad: formData.soyad,
                email: formData.email,
                telefon: formData.telefon,
                kisi_sayisi: parseInt(formData.kisi_sayisi || 1),
                tarih: new Date().toISOString().split('T')[0],
                oda_tipi: formData.roomType || 'standard',
                ozel_istekler: formData.notlar || '',
                // Kullanıcı giriş yapmışsa ID'sini ekle
                musteri_id: currentUser.id || null // null kullanarak opsiyonel olduğunu belirt
            };

            console.log("Backend'e gönderilen veri:", apiData);
            
            const response = await fetch(`${API_BASE_URL}/rezervasyonlar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(apiData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Rezervasyon oluşturulamadı');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Rezervasyon oluşturma hatası:', error);
            throw error;
        }
    }
}

// Login işlemi için fonksiyon
async function loginUser(credentials) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Giriş başarısız');
        }
        
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// Kayıt işlemi için fonksiyon
async function signupUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Kayıt başarısız');
        }
        
        return data;
    } catch (error) {
        console.error('Signup error:', error);
        throw error;
    }
}

// Bölgeleri getiren fonksiyon
async function getBolgeler() {
    if (MOCK_MODE) {
        return [
            { id: 1, ad: "Ege", ulke: "Türkiye" },
            { id: 2, ad: "Akdeniz", ulke: "Türkiye" },
            { id: 3, ad: "Karadeniz", ulke: "Türkiye" },
            { id: 4, ad: "İç Anadolu", ulke: "Türkiye" }
        ];
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/bolgeler`);
            if (!response.ok) {
                throw new Error('Bölgeler alınamadı');
            }
            return await response.json();
        } catch (error) {
            console.error('Bölgeler alınamadı:', error);
            throw error;
        }
    }
}

// Destinasyonları getiren fonksiyon
async function getDestinasyonlar(bolgeId = null) {
    let url = `${API_BASE_URL}/destinasyonlar`;
    if (bolgeId) {
        url += `?bolge_id=${bolgeId}`;
    }
    
    if (MOCK_MODE) {
        return [
            { id: 1, ad: "Bodrum", tur: "Plaj", bolge_id: 1 },
            { id: 2, ad: "Antalya", tur: "Plaj", bolge_id: 2 },
            { id: 3, ad: "Trabzon", tur: "Yayla", bolge_id: 3 },
            { id: 4, ad: "Nevşehir", tur: "Kültür", bolge_id: 4 }
        ];
    } else {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Destinasyonlar alınamadı');
            }
            return await response.json();
        } catch (error) {
            console.error('Destinasyonlar alınamadı:', error);
            throw error;
        }
    }
}

// Değerlendirmeleri getiren fonksiyon
async function getDegerlendirmeler(turId) {
    if (MOCK_MODE) {
        return [
            { id: 1, musteri_adi: "Ahmet Yılmaz", puan: 5, yorum: "Harika bir turdu!" },
            { id: 2, musteri_adi: "Ayşe Kaya", puan: 4, yorum: "Çok güzeldi ama biraz yorucuydu." }
        ];
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/degerlendirmeler?tur_paketi_id=${turId}`);
            if (!response.ok) {
                throw new Error('Değerlendirmeler alınamadı');
            }
            return await response.json();
        } catch (error) {
            console.error(`Tur ${turId} için değerlendirmeler alınamadı:`, error);
            throw error;
        }
    }
}

// Değerlendirme ekleyen fonksiyon
async function createDegerlendirme(data) {
    if (MOCK_MODE) {
        return { success: true, message: 'Değerlendirmeniz için teşekkürler!' };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/degerlendirmeler`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Değerlendirme eklenemedi');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Değerlendirme ekleme hatası:', error);
            throw error;
        }
    }
}

// Export fonksiyonları
window.getTurlar = getTurlar;
window.getTurById = getTurById;
window.createRezervasyon = createRezervasyon;
window.loginUser = loginUser;
window.signupUser = signupUser;
window.getBolgeler = getBolgeler;
window.getDestinasyonlar = getDestinasyonlar;
window.getDegerlendirmeler = getDegerlendirmeler;
window.createDegerlendirme = createDegerlendirme;