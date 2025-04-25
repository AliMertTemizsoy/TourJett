// api.js dosyasında createRezervasyon fonksiyonunu değiştirin:
async function createRezervasyon(formData) {
    if (MOCK_MODE) {
        console.log('Mock rezervasyon oluşturuldu:', formData);
        return { id: Math.floor(Math.random() * 10000), success: true };
    } else {
        try {
            console.log('API isteği gönderiliyor:', formData);
            
            // Önce tur ID'si ile turun var olup olmadığını kontrol et
            const turId = parseInt(formData.tur_id || formData.tur_paketi_id, 10);
            console.log(`${turId} ID'li tur kontrol ediliyor...`);
            
            try {
                // Tur var mı diye kontrol et
                const turBilgisi = await getTurById(turId);
                console.log('Tur bilgisi bulundu:', turBilgisi);
                
                // Tur bulunduysa, hangi ID'nin çalıştığını görmek için log'la
                console.log('Tur ID tipi:', typeof turBilgisi.id);
                console.log('Tur ID değeri:', turBilgisi.id);
                
                // Parametre anahtarlarını backend'in beklediği formata dönüştür
                const apiData = {
                    // Burayı değiştirin: Turdan alınan ID formatını kullan
                    tur_paketi_id: turBilgisi.id, // Öncelikle tur_paketi_id deneyin
                    tur_id: turBilgisi.id, // Veya tur_id'yi alternatif olarak gönder
                    
                    ad: formData.ad || formData.firstName,
                    soyad: formData.soyad || formData.lastName,
                    email: formData.email,
                    telefon: formData.telefon || formData.phone,
                    tc_kimlik: formData.tc_kimlik || formData.nationalId || '',
                    adres: formData.adres || formData.address || '',
                    kisi_sayisi: parseInt(formData.kisi_sayisi) || 1,
                    oda_tipi: formData.oda_tipi || formData.roomType || 'standard',
                    notlar: formData.notlar || formData.notes || ''
                };
                
                // Müşteri ID'si varsa ekle
                if (formData.musteri_id) {
                    apiData.musteri_id = formData.musteri_id;
                }
                
                console.log('Düzenlenmiş API verisi:', apiData);
                
                const response = await fetch(`${API_BASE_URL}/rezervasyonlar`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(apiData)
                });
                
                const data = await response.json();
                console.log('API yanıtı:', data);
                
                if (!response.ok) {
                    throw new Error(data.error || 'Rezervasyon oluşturulamadı');
                }
                
                return data;
            } catch (turError) {
                console.error(`Tur ID: ${turId} bulunamadı:`, turError);
                throw new Error(`Tur seferi bulunamadı: ${turId} ID'li tur mevcut değil.`);
            }
        } catch (error) {
            console.error('Rezervasyon oluşturma hatası:', error);
            throw error;
        }
    }
}