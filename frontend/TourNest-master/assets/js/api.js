// API temel URL'i
const API_BASE_URL = 'http://localhost:5000'; // Backend portu 5000 varsayılan

// Araçlar için API çağrıları
async function getAraclar() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/araclar`);
        return await response.json();
    } catch (error) {
        console.error('Araçlar getirilirken hata oluştu:', error);
        return [];
    }
}

async function getAracById(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/araclar/${id}`);
        return await response.json();
    } catch (error) {
        console.error(`Araç ID=${id} getirilirken hata oluştu:`, error);
        return null;
    }
}

// Personel için API çağrıları
async function getPersonel() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/personel`);
        return await response.json();
    } catch (error) {
        console.error('Personel getirilirken hata oluştu:', error);
        return [];
    }
}

async function getPersonelById(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/personel/${id}`);
        return await response.json();
    } catch (error) {
        console.error(`Personel ID=${id} getirilirken hata oluştu:`, error);
        return null;
    }
}

// Rezervasyon oluşturma örneği
async function createRezervasyon(rezervasyonData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/rezervasyon`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(rezervasyonData)
        });
        return await response.json();
    } catch (error) {
        console.error('Rezervasyon oluşturulurken hata oluştu:', error);
        return { error: 'Rezervasyon yapılamadı' };
    }
}