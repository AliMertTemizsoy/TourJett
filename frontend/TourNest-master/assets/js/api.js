// API temel URL'i
const API_BASE_URL = 'http://localhost:5000'; // Backend portu 5000 varsayılan

// Mock veri modu (backend hazır olduğuna göre false yapıyoruz)
const MOCK_MODE = false;

// Araçlar için API çağrıları
async function getAraclar() {
    if (MOCK_MODE) return getMockAraclar();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/araclar`);
        return await response.json();
    } catch (error) {
        console.error('Araçlar getirilirken hata oluştu:', error);
        return [];
    }
}

async function getAracById(id) {
    if (MOCK_MODE) {
        const araclar = getMockAraclar();
        return araclar.find(a => a.id === parseInt(id)) || null;
    }
    
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
    if (MOCK_MODE) return getMockPersonel();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/personel`);
        return await response.json();
    } catch (error) {
        console.error('Personel getirilirken hata oluştu:', error);
        return [];
    }
}

async function getPersonelById(id) {
    if (MOCK_MODE) {
        const personel = getMockPersonel();
        return personel.find(p => p.id === parseInt(id)) || null;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/personel/${id}`);
        return await response.json();
    } catch (error) {
        console.error(`Personel ID=${id} getirilirken hata oluştu:`, error);
        return null;
    }
}

// Turlar için API çağrıları
async function getTurlar() {
    if (MOCK_MODE) return getMockTurlar();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/turlar`);
        return await response.json();
    } catch (error) {
        console.error('Turlar getirilirken hata oluştu:', error);
        return [];
    }
}

async function getTurById(id) {
    if (MOCK_MODE) {
        const turlar = getMockTurlar();
        return turlar.find(t => t.id === parseInt(id)) || null;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/tours/${id}`);
        return await response.json();
    } catch (error) {
        console.error(`Tur ID=${id} getirilirken hata oluştu:`, error);
        return null;
    }
}

// Login için API çağrısı
async function loginUser(email, password) {
    if (MOCK_MODE) {
        console.log("Login verileri (mock):", { email, password });
        return {
            success: true,
            message: "Giriş başarılı (test modu)",
            token: "mock-jwt-token"
        };
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        return await response.json();
    } catch (error) {
        console.error('Giriş sırasında hata oluştu:', error);
        return { error: 'Giriş yapılamadı' };
    }
}

// Signup için API çağrısı
async function signupUser(email, password) {
    if (MOCK_MODE) {
        console.log("Signup verileri (mock):", { email, password });
        return {
            success: true,
            message: "Kayıt başarılı (test modu)",
            userId: Math.floor(Math.random() * 1000) + 1
        };
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        return await response.json();
    } catch (error) {
        console.error('Kayıt sırasında hata oluştu:', error);
        return { error: 'Kayıt yapılamadı' };
    }
}

// Rezervasyon oluşturma API çağrısı
async function createRezervasyon(rezervasyonData) {
    if (MOCK_MODE) {
        console.log("Rezervasyon verileri (mock):", rezervasyonData);
        return {
            success: true,
            message: "Rezervasyon başarıyla kaydedildi (test modu)",
            booking_id: "BK-" + (Math.floor(Math.random() * 100000000)).toString().padStart(8, '0')
        };
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/book`, {
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

// MOCK VERİLER (Test amaçlı)
// --------------------------
function getMockAraclar() {
    return [
        {
            id: 1,
            arac_turu: "Otobüs",
            model: "Mercedes Travego",
            plaka: "34 TUR 01",
            koltuk_sayisi: 46,
            durum: "Aktif"
        },
        {
            id: 2,
            arac_turu: "Midibüs",
            model: "Isuzu Novo",
            plaka: "34 TUR 02",
            koltuk_sayisi: 27,
            durum: "Aktif"
        },
        {
            id: 3,
            arac_turu: "VIP Van",
            model: "Mercedes Sprinter",
            plaka: "34 TUR 03",
            koltuk_sayisi: 16,
            durum: "Bakımda"
        }
    ];
}

function getMockPersonel() {
    return [
        {
            id: 1,
            ad: "Ahmet",
            soyad: "Yılmaz",
            gorev: "Şoför",
            telefon: "555-1234567"
        },
        {
            id: 2,
            ad: "Mehmet",
            soyad: "Kaya",
            gorev: "Rehber",
            telefon: "555-2345678"
        },
        {
            id: 3,
            ad: "Ayşe",
            soyad: "Demir",
            gorev: "Operasyon Müdürü",
            telefon: "555-3456789"
        }
    ];
}

function getMockTurlar() {
    return [
        {
            id: 1,
            adi: "Kapadokya Turu",
            sure: "3 Gün",
            fiyat: 3500,
            aciklama: "Muhteşem peri bacaları ve sıcak hava balonlarıyla unutulmaz bir deneyim",
            resim: "assets/images/packages/p1.jpg"
        },
        {
            id: 2,
            adi: "Efes & Pamukkale Turu",
            sure: "4 Gün",
            fiyat: 4200,
            aciklama: "Antik kentler ve doğal travertenleri keşfedin",
            resim: "assets/images/packages/p2.jpg"
        },
        {
            id: 3,
            adi: "İstanbul Boğaz Turu",
            sure: "1 Gün",
            fiyat: 1200,
            aciklama: "Boğazın eşsiz manzarasında tekne turu",
            resim: "assets/images/packages/p3.jpg"
        }
    ];
}