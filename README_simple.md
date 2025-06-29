# 🏨 Cullinan Hotel Chatbot

![Cullinan Hotel Chatbot](resim.png)

Modern otel hizmetleri için AI destekli chatbot uygulaması.

## 🚀 Özellikler

- **AI Sohbet**: OpenAI GPT modelleri ile doğal konuşma
- **Otel Bilgileri**: Oda, hizmet ve fiyat sorguları
- **Rezervasyon**: Otomatik rezervasyon rehberliği
- **Web Arayüzü**: Streamlit ile modern tasarım
- **Logging**: Detaylı sistem takibi

## 🛠️ Teknolojiler

- **Backend**: Python 3.8+
- **LLM**: OpenAI GPT-3.5/GPT-4
- **Web Framework**: Streamlit
- **Vector DB**: ChromaDB
- **Logging**: JSON structured logging

## 📋 Kurulum

### 1. Projeyi İndirin
```bash
git clone https://github.com/yourusername/hotel_chatbot.git
cd hotel_chatbot
```

### 2. Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### 3. API Anahtarını Ayarlayın
`.env` dosyası oluşturun:
```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 4. Uygulamayı Çalıştırın
```bash
streamlit run app.py
```

Tarayıcınızda http://localhost:8501 adresini açın.

## 🏗️ Mimari

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │     Router      │    │   AI Chains     │
│   (Frontend)    │◄──►│  (Controller)   │◄──►│   (Backend)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   ChromaDB      │
                       │  (Vector Store) │
                       └─────────────────┘
```

### Bileşenler
- **app.py**: Streamlit web arayüzü
- **router.py**: Mesaj yönlendirici
- **chains/**: AI işleme modülleri
  - Intent sınıflandırma
  - RAG sistemi
  - Rezervasyon diyalogu
- **logging_config.py**: Sistem takibi

## 🤖 LLM Kullanımı

**OpenAI GPT Modelleri**:
- **Intent Classification**: Kullanıcı niyetlerini anlama
- **Response Generation**: Doğal yanıtlar üretme
- **Hotel Information**: RAG ile bilgi sorgulama
- **Booking Assistance**: Rezervasyon süreç yönetimi

## 🔧 Konfigürasyon

### API Anahtarı
[OpenAI Platform](https://platform.openai.com/) üzerinden API key alın.

### Ortam Değişkenleri
```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-3.5-turbo
LOG_LEVEL=INFO
```

## 📱 Kullanım

1. Uygulamayı başlatın
2. Sohbet kutusuna mesajınızı yazın
3. Hızlı aksiyonları kullanın
4. Rezervasyon için rehberliği takip edin

## 🌐 Deployment

### Streamlit Cloud
1. GitHub'a push edin
2. [share.streamlit.io](https://share.streamlit.io) adresinden deploy edin
3. Secrets'a API key ekleyin

### Docker
```bash
docker build -t hotel-chatbot .
docker run -p 8501:8501 hotel-chatbot
```

## 📊 Monitoring

Logs dizininde JSON formatında kayıtlar:
- Konuşma kayıtları
- Performance metrikleri
- Hata takibi

## 🐛 Sorun Giderme

- **API Key Hatası**: `.env` dosyasını kontrol edin
- **Import Hatası**: `pip install -r requirements.txt` çalıştırın
- **Port Sorunu**: Farklı port kullanın: `streamlit run app.py --server.port 8502`

## 📄 Lisans

MIT License

---

**🏨 Cullinan Hotel** - AI ile güçlendirilmiş otel deneyimi
