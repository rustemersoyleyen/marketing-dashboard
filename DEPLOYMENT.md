# Marketing Dashboard - Streamlit Cloud Deployment Rehberi

## 🎯 Genel Bakış

Bu rehber, Marketing Dashboard'u Streamlit Cloud'a deploy etmek için adım adım talimatlar içerir.

---

## 📋 Ön Gereksinimler

1. **GitHub Hesabı** - [github.com](https://github.com) 'da ücretsiz hesap
2. **Streamlit Cloud Hesabı** - [share.streamlit.io](https://share.streamlit.io) (GitHub ile giriş)

---

## 🚀 Deployment Adımları

### ADIM 1: GitHub Repository Oluşturma

1. [github.com](https://github.com) adresine gidin
2. Sağ üstteki **"+"** butonuna tıklayın → **"New repository"**
3. Repository ayarları:
   - **Repository name:** `marketing-dashboard`
   - **Description:** `Reklam Harcama vs Lead/Ciro Dashboard`
   - **Visibility:** `Public` (Streamlit Cloud ücretsiz plan için gerekli)
   - ✅ **Add a README file** işaretleyin
4. **"Create repository"** butonuna tıklayın

---

### ADIM 2: Kodu GitHub'a Yükleme

#### Seçenek A: GitHub Desktop (Kolay)

1. [GitHub Desktop](https://desktop.github.com/) indirin ve kurun
2. GitHub hesabınızla giriş yapın
3. **File → Clone Repository** → Oluşturduğunuz repo'yu seçin
4. `d:\Otomasyonlar\Marketing Mix Model\Marketing-Dashboard` klasöründeki tüm dosyaları klonlanan klasöre kopyalayın
5. **Commit to main** → **Push origin**

#### Seçenek B: Komut Satırı

```powershell
# Marketing-Dashboard klasörüne gidin
cd "d:\Otomasyonlar\Marketing Mix Model\Marketing-Dashboard"

# Git başlatın
git init
git add .
git commit -m "Initial commit - Marketing Dashboard"

# GitHub repo'nuzu bağlayın (kendi kullanıcı adınızı yazın)
git remote add origin https://github.com/KULLANICI_ADINIZ/marketing-dashboard.git
git branch -M main
git push -u origin main
```

---

### ADIM 3: Streamlit Cloud'a Giriş

1. [share.streamlit.io](https://share.streamlit.io) adresine gidin
2. **"Continue with GitHub"** butonuna tıklayın
3. GitHub hesabınızla giriş yapın
4. Streamlit'in GitHub'ınıza erişmesine izin verin

---

### ADIM 4: Yeni App Oluşturma

1. Dashboard'da **"New app"** butonuna tıklayın
2. Ayarları girin:
   - **Repository:** `KULLANICI_ADINIZ/marketing-dashboard`
   - **Branch:** `main`
   - **Main file path:** `dashboard/app.py`
3. **"Advanced settings"** tıklayın (önemli!)

---

### ADIM 5: Secrets (Gizli Bilgiler) Ekleme

**"Advanced settings"** içinde **"Secrets"** bölümüne aşağıdaki bilgileri girin:

```toml
[database]
driver = "ODBC Driver 17 for SQL Server"
server = "deep.konusarakogren.com"
database = "MemberPrime"
username = "sa"
password = "9FSmGvv!+BHY"

[google_ads]
developer_token = "GOOGLE_ADS_DEVELOPER_TOKEN"
client_id = "GOOGLE_ADS_CLIENT_ID"
client_secret = "GOOGLE_ADS_CLIENT_SECRET"
refresh_token = "GOOGLE_ADS_REFRESH_TOKEN"
login_customer_id = "7731368325"
customer_id = "7731368325"

[facebook_ads]
app_id = "813584908341021"
app_secret = "77758fa9b6d9e6be5516470d0608ee19"
access_token = "EAALj8390zx0BQIOamy1Ii3UWnjeMgHFFHPnTFnm8drQ3iXgJfwi82oBakM9uyf429Uu5fAKUUZBMZBAMw7EqVRyKx5RkXbGKNXVqzIcdTQkJhZB9VCjudsdH9ZBjzIiFtQkSYY1zep7yVDLAuZCvOog4703Cnvca3xQUMeZC8YGY4ZBHZBmj3a8lW7fIIjycmtIRDUwgnz4GMYWNFQQQ6Cty"
ad_account_id = "act_76604119"
```

> ⚠️ **ÖNEMLİ:** Google Ads bilgilerini `google-ads.yaml` dosyanızdan alın!

---

### ADIM 6: Deploy

1. **"Deploy!"** butonuna tıklayın
2. Birkaç dakika bekleyin (ilk build biraz uzun sürer)
3. Uygulama hazır olduğunda URL'niz aktif olur:
   ```
   https://kullaniciadi-marketing-dashboard-dashboard-app-xyz123.streamlit.app
   ```

---

## ⚠️ Önemli Notlar

### Veritabanı Erişimi
- MSSQL sunucunuz (`deep.konusarakogren.com`) internetten erişilebilir olmalı
- Firewall ayarlarını kontrol edin
- Streamlit Cloud IP adreslerinin erişimine izin verin

### Google Ads YAML Bilgileri
`google-ads.yaml` dosyanızdaki bilgileri secrets'a aktarın:
```yaml
developer_token: "xxxxx"
client_id: "xxxxx.apps.googleusercontent.com"
client_secret: "xxxxx"
refresh_token: "xxxxx"
login_customer_id: "7731368325"
```

### Hata Ayıklama
- Streamlit Cloud'da **"Manage app"** → **"Logs"** ile hataları görün
- Secrets formatını kontrol edin (TOML formatı)

---

## 🔄 Güncelleme

Kodu güncellemek için:
1. Değişiklikleri yapın
2. GitHub'a push edin
3. Streamlit Cloud otomatik olarak yeniden deploy eder

---

## 📞 Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| Database bağlantı hatası | Firewall ayarlarını kontrol edin |
| Module not found | `requirements.txt` dosyasını kontrol edin |
| Secrets hatası | TOML formatını doğrulayın |
| Timeout | Veritabanı sorgularını optimize edin |

---

## 🎉 Tamamlandı!

Dashboard'unuz artık 7/24 erişilebilir:
- ✅ Otomatik güncellemeler
- ✅ HTTPS güvenliği
- ✅ Paylaşılabilir link
