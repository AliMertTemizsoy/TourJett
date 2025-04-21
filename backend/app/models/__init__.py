# backend/app/models/__init__.py
from app.models.user import User
from app.models.tur import Tur, TurSeferi
from app.models.konum import Konum
from app.models.rezervasyon import Rezervasyon
from app.models.musteri import Musteri
from app.models.bolge import Bolge, Destinasyon
from app.models.kaynak import Arac, Personel
from app.models.degerlendirme import Degerlendirme
from app.models.tur_paketi import TurPaketi, TurDestinasyon

# Burada modellerin hepsini doğru şekilde import edin