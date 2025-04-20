// Sayfa yüklendiğinde çalışacak kod
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Turları API.js'den al (mock veya gerçek)
        const turlar = await getTurlar();
        
        // Tur listesinin gösterileceği bir div elementi bulun
        const turListesiContainer = document.querySelector('.package-cards-wrapper .row');
        
        // Eğer container varsa ve turlar yüklendiyse
        if (turListesiContainer && turlar && turlar.length > 0) {
            // Container'ı temizle
            turListesiContainer.innerHTML = '';
            
            // Her tur için HTML oluştur
            turlar.forEach(tur => {
                const turHTML = `
                    <div class="col-lg-4 col-md-6">
                        <div class="package-card">
                            <div class="package-thumb">
                                <img src="${tur.resim}" alt="${tur.adi}" />
                                <span class="p-price">${tur.fiyat}₺</span>
                            </div>
                            <div class="package-details">
                                <div class="p-details-title">
                                    <h3>${tur.adi}</h3>
                                    <p>${tur.sure}</p>
                                </div>
                                <div class="p-details-content">
                                    <p>${tur.aciklama}</p>
                                    <div class="p-buttons">
                                        <a href="tour-details.html?id=${tur.id}" class="btn-second">Detaylar</a>
                                        <a href="tour-booking.html?id=${tur.id}" class="btn-second">Rezervasyon</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                // Oluşturulan HTML'i container'a ekle
                turListesiContainer.innerHTML += turHTML;
            });
            
            console.log('Turlar başarıyla yüklendi!');
        } else {
            console.log('Turlar yüklenemedi veya tur listesi container\'ı bulunamadı.');
        }
    } catch (error) {
        console.error('Turlar yüklenirken hata oluştu:', error);
    }
});