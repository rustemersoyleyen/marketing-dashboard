# Marketing-Dashboard

Reklam harcamaları (Google Ads, Facebook Ads) ile Lead ve Ciro verilerini ilişkilendiren dashboard.

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

```bash
streamlit run dashboard/app.py
```

## Yapı

- `config/` - Konfigürasyon dosyaları
- `connectors/` - Reklam platformu API bağlantıları
- `database/` - Veritabanı bağlantı ve sorgular
- `services/` - İş mantığı servisleri
- `dashboard/` - Streamlit arayüzü
