# Cullinan Hotel Chatbot - Streamlit Web Uygulaması

## 🎯 Genel Bakış

Bu proje, Cullinan Hotel için yapay zeka destekli chatbot'un modern ve kullanıcı dostu web arayüzüdür. Streamlit framework'ü kullanılarak geliştirilmiştir.

## ✨ Özellikler

### 🤖 Ana Chatbot Arayüzü
- **Modern UI/UX**: Responsive ve mobile-friendly tasarım
- **Real-time Chat**: Anlık mesajlaşma deneyimi
- **Rezervasyon Akışı**: Adım adım rezervasyon rehberliği
- **Hızlı Aksiyonlar**: Önceden tanımlanmış soru butonları
- **Progress Tracking**: Rezervasyon ilerleme takibi

### 📊 Analytics Dashboard
- **Performance Metrikleri**: Yanıt süreleri ve sistem performansı
- **Hata Analizi**: Detaylı error tracking ve pattern detection
- **Intent Analytics**: AI model performance analizi
- **API Usage**: Token kullanımı ve maliyet takibi
- **Real-time Monitoring**: Canlı sistem izleme

### ⚙️ Admin Panel
- **Sistem Yönetimi**: Database ve log yönetimi
- **Konfigürasyon**: API ayarları ve UI customization
- **Backup/Restore**: Sistem yedekleme ve geri yükleme
- **Test Araçları**: Otomatik sistem testleri

## 📁 Dosya Yapısı

```
hotel_chatbot/
├── 🎯 Ana Uygulama
│   ├── app.py                 # Ana Streamlit chatbot uygulaması
│   ├── main.py               # Multi-page ana sayfa
│   └── run_streamlit.bat     # Windows başlatma scripti
│
├── 📊 Ek Sayfalar
│   └── pages/
│       ├── analytics.py      # Analytics dashboard
│       └── admin.py         # Admin panel
│
├── ⚙️ Konfigürasyon
│   ├── .streamlit/
│   │   └── config.toml      # Streamlit ayarları
│   └── requirements.txt     # Python dependencies
│
└── 🏗️ Backend (mevcut)
    ├── logging_config.py
    ├── router.py
    ├── chains/
    └── ...
```

## 🚀 Kurulum ve Çalıştırma

### Ön Gereksinimler
- Python 3.8+
- OpenAI API Key
- ChromaDB veritabanları (hotel_db, intent_db)

### 1. Hızlı Başlangıç (Windows)
```bash
# Basit çalıştırma
run_streamlit.bat
```

### 2. Manuel Kurulum
```bash
# 1. Gerekli kütüphaneleri yükle
pip install -r requirements.txt

# 2. API key'i ayarla (seçeneklerden biri)
# Ortam değişkeni:
set OPENAI_API_KEY=sk-your-key-here

# secrets.json dosyası:
echo {"OPENAI_API_KEY": "sk-your-key-here"} > secrets.json

# .env dosyası:
echo OPENAI_API_KEY=sk-your-key-here > .env

# 3. Uygulamayı başlat
streamlit run app.py
```

### 3. Multi-Page Uygulama
```bash
# Tüm sayfalarla birlikte
streamlit run main.py
```

## 🌐 Erişim Adresleri

- **Ana Chatbot**: http://localhost:8501
- **Analytics**: http://localhost:8501/analytics
- **Admin Panel**: http://localhost:8501/admin

## 📱 Kullanım Kılavuzu

### 💬 Chatbot Kullanımı

1. **Sohbet Başlatma**:
   - Ana sayfada chat input'una mesajınızı yazın
   - Hızlı aksiyon butonlarını kullanabilirsiniz

2. **Rezervasyon Yapma**:
   - "Rezervasyon yapmak istiyorum" deyin
   - Adım adım yönlendirmeleri takip edin
   - Progress bar'dan ilerlemenizi takip edin

3. **Özellikler**:
   - Mesaj geçmişi otomatik saklanır
   - Konuşmayı JSON olarak indirebilirsiniz
   - Debug bilgileri için sidebar'daki checkbox'ı aktifleştirin

### 📊 Analytics Kullanımı

1. **Dashboard Erişimi**:
   - Sidebar'dan "Analytics" sayfasına geçin
   - Zaman aralığını seçin (1-168 saat)

2. **Metrikler**:
   - **Error Analysis**: Hata türleri ve sıklığı
   - **Performance**: Yanıt süreleri ve bottleneck'ler
   - **Intent Analysis**: AI model doğruluğu
   - **API Usage**: Token kullanımı ve maliyet

3. **Export**:
   - JSON, CSV, Excel formatlarında veri export
   - Detaylı raporları txt olarak indirme

### ⚙️ Admin Panel Kullanımı

1. **Giriş**:
   - Şifre: `admin123` (production'da değiştirin!)
   - Güvenlik için gerçek authentication sistemi ekleyin

2. **Özellikler**:
   - **Sistem Durumu**: Real-time system health
   - **Database Management**: ChromaDB kontrol ve temizlik
   - **Log Management**: Log dosyalarını görüntüleme ve temizlik
   - **Configuration**: API keys ve UI ayarları
   - **Backup/Restore**: Sistem yedekleme
   - **Testing**: Otomatik test araçları

## 🎨 Özelleştirme

### Tema Değiştirme
`.streamlit/config.toml` dosyasını düzenleyin:

```toml
[theme]
primaryColor = "#1f4e79"        # Ana renk
backgroundColor = "#ffffff"      # Arka plan
secondaryBackgroundColor = "#f8f9fa"  # İkincil arka plan
textColor = "#333333"           # Metin rengi
font = "sans serif"             # Font
```

### CSS Özelleştirme
`app.py` dosyasındaki `st.markdown` CSS bölümünü düzenleyin.

### Yeni Hızlı Aksiyonlar
`show_quick_actions()` fonksiyonuna yeni butonlar ekleyin:

```python
if st.button("🆕 Yeni Özellik", use_container_width=True):
    st.session_state.messages.append({
        'role': 'user',
        'content': 'Özel mesaj',
        'timestamp': datetime.now().isoformat()
    })
    st.rerun()
```

## 🔒 Güvenlik

### Production Hazırlığı
1. **Authentication**:
   - Admin paneli için güçlü şifre
   - Gerçek authentication sistemi (OAuth, JWT)

2. **API Security**:
   - API key'leri environment variables'da saklayın
   - Rate limiting ekleyin

3. **Data Privacy**:
   - Kullanıcı verilerini encryption ile koruyun
   - GDPR compliance için data retention policies

4. **Network Security**:
   - HTTPS kullanın
   - Firewall rules ekleyin

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  chatbot:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./db:/app/db
      - ./logs:/app/logs
```

### Build ve Run
```bash
# Build
docker build -t hotel-chatbot .

# Run
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key hotel-chatbot
```

## ☁️ Cloud Deployment

### Streamlit Cloud
1. GitHub repo'yu Streamlit Cloud'a bağlayın
2. `secrets.toml` dosyasına API key ekleyin
3. Deploy edin

### Heroku
```bash
# requirements.txt ve Procfile oluşturun
echo "web: streamlit run app.py --server.port \$PORT" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### AWS/Azure/GCP
- EC2/VM instance oluşturun
- Docker container'ı deploy edin
- Load balancer ve SSL sertifikası ekleyin

## 📊 Monitoring ve Analytics

### Application Monitoring
```python
# Streamlit analytics
import streamlit.analytics as sta

# Custom metrics
sta.track_event("user_message", {"intent": intent, "length": len(message)})
sta.track_event("booking_completed", {"rooms": rooms, "duration": duration})
```

### External Monitoring
- **Prometheus + Grafana**: Metric collection ve visualization
- **New Relic/DataDog**: APM monitoring
- **Sentry**: Error tracking

## 🧪 Testing

### Manual Testing
```bash
# Logging system test
python test_logging.py

# Streamlit app test
streamlit run app.py --server.headless true
```

### Automated Testing
```python
# pytest ile test yazın
def test_chatbot_response():
    from app import process_user_message
    # Test implementation
```

## 🔧 Troubleshooting

### Yaygın Problemler

1. **Streamlit başlamıyor**:
   ```bash
   # Port kontrolü
   netstat -an | findstr 8501
   
   # Farklı port kullan
   streamlit run app.py --server.port 8502
   ```

2. **API key bulunamıyor**:
   - Environment variables kontrolü
   - secrets.json formatı kontrolü
   - File permissions kontrolü

3. **Database bağlantısı yok**:
   - ChromaDB dosyalarının varlığını kontrol edin
   - File permissions kontrol edin
   - db_test.py ile test edin

4. **Memory issues**:
   ```python
   # Cache temizle
   st.cache_data.clear()
   
   # Cache TTL ayarla
   @st.cache_data(ttl=60)
   def expensive_function():
       pass
   ```

### Debug Modu
```bash
# Verbose logging
streamlit run app.py --logger.level debug

# Development mode
streamlit run app.py --global.developmentMode true
```

## 📈 Performance Optimization

### Caching
```python
# Expensive operations için cache kullanın
@st.cache_data(ttl=300)  # 5 dakika cache
def load_heavy_data():
    return expensive_computation()

@st.cache_resource  # Singleton resources için
def init_model():
    return load_model()
```

### Session State Management
```python
# Gereksiz re-renders'ı önleyin
if 'key' not in st.session_state:
    st.session_state.key = initial_value
```

### Database Optimization
- Connection pooling kullanın
- Query optimization yapın
- Index'leri optimize edin

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 Support

- **Email**: support@cullinanhotels.com
- **Documentation**: Bu README dosyası
- **Issues**: GitHub Issues kullanın

---

🏨 **Cullinan Hotel Chatbot** - Yapay Zeka Destekli Müşteri Hizmetleri
*Modern web arayüzü ile gelişmiş chatbot deneyimi*
