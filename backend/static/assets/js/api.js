// API ayarları
const API_BASE_URL = 'http://localhost:5000/api';
const MOCK_MODE = false; // Mock mod kapalı (gerçek API kullan)

// Değerlendirmeleri getiren fonksiyon
async function getDegerlendirmeler(turId) {
    if (MOCK_MODE) {
        // Mock veri
        return [
            { 
                id: 1, 
                musteri_adi: "Ahmet Yılmaz", 
                puan: 5, 
                yorum: "Harika bir turdu!", 
                olusturma_tarihi: new Date().toISOString()
            },
            { 
                id: 2, 
                musteri_adi: "Ayşe Kaya", 
                puan: 4, 
                yorum: "Çok güzeldi ama biraz yorucuydu.", 
                olusturma_tarihi: new Date().toISOString() 
            }
        ];
    } else {
        try {
            console.log(`Değerlendirmeler alınıyor... Tur ID: ${turId}`);
            const response = await fetch(`${API_BASE_URL}/degerlendirmeler?tur_paketi_id=${turId}`);
            
            if (!response.ok) {
                console.error('API yanıt hata kodu:', response.status);
                throw new Error('Değerlendirmeler alınamadı');
            }
            
            const data = await response.json();
            console.log('Alınan değerlendirmeler:', data);
            return data;
        } catch (error) {
            console.error(`Tur ${turId} için değerlendirmeler alınamadı:`, error);
            throw error;
        }
    }
}

// Değerlendirme ekleyen fonksiyon
async function createDegerlendirme(data) {
    if (MOCK_MODE) {
        console.log('Mock değerlendirme oluşturuldu:', data);
        return { success: true, message: 'Değerlendirmeniz için teşekkürler!' };
    } else {
        try {
            console.log('Değerlendirme gönderiliyor:', data);
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

// Tur detaylarını getiren fonksiyon
async function getTurById(id) {
    if (MOCK_MODE) {
        // Mock veri
        return {
            id: id,
            ad: "Kapadokya Turu",
            sure: "3 Gün",
            fiyat: 3500,
            aciklama: "Muhteşem peri bacaları ve sıcak hava balonlarıyla unutulmaz bir deneyim",
            kapasite: 25,
            baslangic_bolge: "İstanbul"
        };
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/turpaketleri/${id}`);
            if (!response.ok) {
                throw new Error(`Tur bulunamadı: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Tur ${id} alınamadı:`, error);
            throw error;
        }
    }
}

// Global olarak fonksiyonları tanımla
window.getDegerlendirmeler = getDegerlendirmeler;
window.createDegerlendirme = createDegerlendirme;
window.getTurById = getTurById;