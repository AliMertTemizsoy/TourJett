// Mock modunu kapatın, gerçek API çağrıları yapın
const MOCK_MODE = true;
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
            // Diğer mock turlar...
        ];
    } else {
        try {
            const response = await fetch(`${API_BASE_URL}/turlar`);
            if (!response.ok) {
                throw new Error('API yanıt vermedi');
            }
            return await response.json();
        } catch (error) {
            console.error('Turlar alınamadı:', error);
            throw error;
        }
    }
}

// Diğer API fonksiyonları...

// Export fonksiyonları
window.getTurlar = getTurlar;
// Diğer export edilen fonksiyonlar...