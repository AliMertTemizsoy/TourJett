// Mock modunu kapat, gerçek API çağrıları yap
const MOCK_MODE = false;
const API_BASE_URL = 'http://localhost:5000/api';

// API fonksiyonları
async function getTurlar() {
    if (MOCK_MODE) {
        // Mock veriler
        return [
            {
                id: 1,
                adi: "Kapadokya Turu",
                sure: "3 Gün",
                fiyat: 3500,
                aciklama: "Muhteşem peri bacaları ve sıcak hava balonlarıyla unutulmaz bir deneyim",
                resim: "assets/images/packages/p1.jpg",
                kategori: "Kültür"
            },
            {
                id: 2,
                adi: "Antalya Sahil Turu",
                sure: "5 Gün",
                fiyat: 4200,
                aciklama: "Turkuaz deniz ve altın sahilleriyle mükemmel bir tatil",
                resim: "assets/images/packages/p2.jpg",
                kategori: "Deniz"
            },
            {
                id: 3,
                adi: "İstanbul Kültür Turu",
                sure: "4 Gün",
                fiyat: 3800,
                aciklama: "İki kıtayı birleştiren şehirde tarih ve kültür yolculuğu",
                resim: "assets/images/packages/p3.jpg",
                kategori: "Kültür"
            },
            {
                id: 4,
                adi: "Ege Adaları Turu",
                sure: "7 Gün",
                fiyat: 6500,
                aciklama: "Ege'nin incilerinde unutulmaz bir deniz tatili",
                resim: "assets/images/packages/p4.jpg",
                kategori: "Deniz"
            },
            {
                id: 5,
                adi: "Doğu Ekspresi Macerası",
                sure: "6 Gün",
                fiyat: 5200,
                aciklama: "Kars'tan Ankara'ya uzanan masalsı bir tren yolculuğu",
                resim: "assets/images/packages/p5.jpg",
                kategori: "Macera"
            },
            {
                id: 6,
                adi: "Karadeniz Yaylaları",
                sure: "5 Gün",
                fiyat: 4800,
                aciklama: "Yeşilin her tonunu görebileceğiniz yaylalar ve şelaleler",
                resim: "assets/images/packages/p6.jpg",
                kategori: "Doğa"
            }
        ];
    } else {
        try {
            // Endpoint'i backend yapınıza uygun olarak güncellendi
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
            adi: "Kapadokya Turu",
            sure: "3 Gün",
            fiyat: 3500,
            aciklama: "Muhteşem peri bacaları ve sıcak hava balonlarıyla unutulmaz bir deneyim",
            baslangic_tarihi: "2025-05-15",
            bitis_tarihi: "2025-05-18",
            baslangic_noktasi: "İstanbul",
            resim: "assets/images/packages/p1.jpg",
            kategori: "Kültür"
        };
    } else {
        try {
            // Endpoint'i backend yapınıza uygun olarak güncellendi
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

// Rezervasyon oluşturan fonksiyon
async function createRezervasyon(formData) {
    if (MOCK_MODE) {
        // Mock response
        return {
            success: true,
            message: 'Rezervasyon başarıyla oluşturuldu',
            booking_id: 'BK-' + Math.floor(Math.random() * 10000000)
        };
    } else {
        try {
            // Endpoint'i backend yapınıza uygun olarak güncellendi
            const response = await fetch(`${API_BASE_URL}/rezervasyonlar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
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

// Login ve signup fonksiyonları
async function loginUser(email, password) {
    if (MOCK_MODE) {
        return { success: true, message: 'Giriş başarılı' };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Login hatası:', error);
            return { error: 'Giriş sırasında bir hata oluştu' };
        }
    }
}

async function signupUser(email, password) {
    if (MOCK_MODE) {
        return { success: true, message: 'Kayıt başarılı! Lütfen giriş yapın.' };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            return await response.json();
        } catch (error) {
            console.error('Signup hatası:', error);
            return { error: 'Kayıt sırasında bir hata oluştu' };
        }
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