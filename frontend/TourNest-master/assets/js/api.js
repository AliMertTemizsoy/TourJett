// Mock modunu kapatın, gerçek API çağrıları yapın
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
            // Diğer mock veriler
        ];
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/turpaketleri/`);
            if (!response.ok) {
                throw new Error('API yanıt vermedi');
            }
            
            const data = await response.json();
            
            // Backend veri yapısını frontend formatına dönüştürme
            return data.map(paket => ({
                id: paket.id,
                adi: paket.ad,
                sure: paket.sure,
                fiyat: paket.fiyat,
                aciklama: paket.aciklama,
                resim: `assets/images/packages/p${(paket.id % 6) + 1}.jpg`, // Rastgele resim
                kategori: paket.baslangic_bolge || "Genel",
                baslangic_bolge: paket.baslangic_bolge
            }));
        } catch (error) {
            console.error('Turlar alınamadı:', error);
            // Hata durumunda mock verileri döndürebiliriz
            if (MOCK_MODE) {
                return getTurlar();
            }
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
            const response = await fetch(`${API_BASE_URL}/turpaketleri/${id}`);
            if (!response.ok) {
                throw new Error('API yanıt vermedi');
            }
            
            const data = await response.json();
            
            // Backend veri yapısını frontend formatına dönüştürme
            return {
                id: data.id,
                adi: data.ad,
                sure: data.sure,
                fiyat: data.fiyat,
                aciklama: data.aciklama,
                kapasite: data.kapasite,
                baslangic_bolge: data.baslangic_bolge,
                durum: data.durum,
                resim: `assets/images/packages/p${(data.id % 6) + 1}.jpg`,
                destinasyonlar: data.destinasyonlar || []
            };
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

// Yeni tur paketi oluşturan fonksiyon
async function createTurPaketi(formData) {
    if (MOCK_MODE) {
        return {
            success: true,
            message: 'Tur paketi başarıyla oluşturuldu',
            id: Math.floor(Math.random() * 1000) + 10
        };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/turpaketleri/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Tur paketi oluşturulamadı');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Tur paketi oluşturma hatası:', error);
            throw error;
        }
    }
}

// Tur paketini güncelleyen fonksiyon
async function updateTurPaketi(id, formData) {
    if (MOCK_MODE) {
        return {
            success: true,
            message: 'Tur paketi başarıyla güncellendi'
        };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/turpaketleri/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Tur paketi güncellenemedi');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Tur paketi güncelleme hatası:', error);
            throw error;
        }
    }
}

// Tur paketini silen fonksiyon
async function deleteTurPaketi(id) {
    if (MOCK_MODE) {
        return {
            success: true,
            message: 'Tur paketi başarıyla silindi'
        };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/turpaketleri/${id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Tur paketi silinemedi');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Tur paketi silme hatası:', error);
            throw error;
        }
    }
}

// Tur paketine destinasyon ekleyen fonksiyon
async function addDestinasyonToTurPaketi(turId, destinasyonData) {
    if (MOCK_MODE) {
        return {
            success: true,
            message: 'Destinasyon başarıyla eklendi',
            id: Math.floor(Math.random() * 1000) + 1
        };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/turpaketleri/${turId}/destinasyonlar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(destinasyonData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Destinasyon eklenemedi');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Destinasyon ekleme hatası:', error);
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
            const response = await fetch(`${API_BASE_URL}/login`, {
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
            const response = await fetch(`${API_BASE_URL}/signup`, {
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
            
            // Hata durumunda mock verileri döndürebiliriz
            return [
                { id: 1, ad: "Ege", ulke: "Türkiye" },
                { id: 2, ad: "Akdeniz", ulke: "Türkiye" },
                { id: 3, ad: "Karadeniz", ulke: "Türkiye" },
                { id: 4, ad: "İç Anadolu", ulke: "Türkiye" }
            ];
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
            
            // Hata durumunda mock verileri döndürebiliriz
            return [
                { id: 1, ad: "Bodrum", tur: "Plaj", bolge_id: 1 },
                { id: 2, ad: "Antalya", tur: "Plaj", bolge_id: 2 },
                { id: 3, ad: "Trabzon", tur: "Yayla", bolge_id: 3 },
                { id: 4, ad: "Nevşehir", tur: "Kültür", bolge_id: 4 }
            ];
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
            
            // Hata durumunda mock verileri döndürelim
            return [
                { id: 1, musteri_adi: "Ahmet Yılmaz", puan: 5, yorum: "Harika bir turdu!" },
                { id: 2, musteri_adi: "Ayşe Kaya", puan: 4, yorum: "Çok güzeldi ama biraz yorucuydu." }
            ];
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
window.createTurPaketi = createTurPaketi;
window.updateTurPaketi = updateTurPaketi;
window.deleteTurPaketi = deleteTurPaketi;
window.addDestinasyonToTurPaketi = addDestinasyonToTurPaketi;
window.loginUser = loginUser;
window.signupUser = signupUser;
window.getBolgeler = getBolgeler;
window.getDestinasyonlar = getDestinasyonlar;
window.getDegerlendirmeler = getDegerlendirmeler;
window.createDegerlendirme = createDegerlendirme;