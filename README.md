# 🏨 Cullinan Hotel Chatbot

![Cullinan Hotel Chatbot](resim.png)

*Modern ve akıllı otel asistanı - OpenAI GPT destekli doğal dil işleme ile 7/24 müşteri hizmetleri*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 İçindekiler

- [🌟 Özellikler](#-özellikler)
- [🛠️ Teknolojiler](#️-teknolojiler)
- [🚀 Hızlı Başlangıç](#-hızlı-başlangıç)
- [📥 Kurulum](#-kurulum)
- [⚙️ Konfigürasyon](#️-konfigürasyon)
- [💻 Kullanım](#-kullanım)
- [📚 API Dokümantasyonu](#-api-dokümantasyonu)
- [📊 Logging Sistemi](#-logging-sistemi)
- [🌐 Deployment](#-deployment)
- [👨‍💻 Geliştirme](#-geliştirme)
- [🐛 Sorun Giderme](#-sorun-giderme)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)
- [📄 Lisans](#-lisans)

## 🌟 Özellikler

### 🤖 Akıllı Sohbet Sistemi
- **Doğal Dil İşleme**: OpenAI GPT-3.5/4 modelleri ile gelişmiş anlama
- **Intent Sınıflandırma**: Kullanıcı niyetlerini otomatik algılama ve yönlendirme
- **Çok Dilli Destek**: Türkçe ve İngilizce tam desteği
- **Kontekst Yönetimi**: Konuşma geçmişini takip etme ve bağlamsal yanıtlar
- **Session Management**: Kullanıcı oturumlarını güvenli yönetim

### 🏨 Otel Hizmetleri
- **Otel Bilgi Sistemi**: RAG (Retrieval Augmented Generation) ile detaylı bilgiler
  - Oda tipleri ve özellikleri
  - Otel olanakları (SPA, fitness, havuz, restoranlar)
  - Fiyat bilgileri ve paket seçenekleri
  - Konum ve ulaşım bilgileri
- **Rezervasyon Asistanı**: Adım adım rezervasyon rehberliği
  - Tarih ve misafir sayısı sorgulama
  - Oda tipi önerileri
  - Fiyat hesaplama
  - Özel isteklerin alınması
- **Müşteri Hizmetleri**: 7/24 anlık yardım ve destek
- **Hızlı Aksiyonlar**: Önceden tanımlı sık sorulan sorulara hızlı erişim

### 📊 Analytics ve Monitoring
- **Gerçek Zamanlı İstatistikler**: 
  - Toplam konuşma sayısı
  - Intent dağılımı
  - Kullanıcı memnuniyet oranları
  - Peak usage saatleri
- **Performance Monitoring**: 
  - API yanıt süreleri
  - Sistem kaynak kullanımı
  - Hata oranları
  - Throughput metrikleri
- **Error Tracking**: Detaylı hata takibi ve raporlama
- **Usage Analytics**: API kullanımı ve maliyet analizi

### 🎨 Modern Web Arayüzü
- **Responsive Tasarım**: Tüm cihazlarda uyumlu çalışma (Desktop, Tablet, Mobile)
- **Gradient Temalar**: Modern ve göz alıcı profesyonel tasarım
- **Real-time Chat**: WhatsApp benzeri anlık mesajlaşma deneyimi
- **Quick Actions**: Hızlı erişim butonları
- **Dark/Light Mode**: Kullanıcı tercihleri (gelecek sürümde)
- **Progressive Web App**: Offline çalışma desteği (gelecek sürümde)

### 🔒 Güvenlik ve Güvenilirlik
- **API Key Security**: Güvenli API anahtar yönetimi
- **Rate Limiting**: API kullanım limitlerini koruma
- **Error Handling**: Robust hata yönetimi ve fallback'ler
- **Data Privacy**: Kullanıcı verilerinin güvenliği
- **Logging Security**: Hassas bilgilerin log'lanmaması

## 🛠️ Teknolojiler

### Core Technologies
| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| **Python** | 3.8+ | Ana programlama dili |
| **OpenAI API** | 1.0+ | GPT modelleri ve embeddings |
| **Streamlit** | 1.28+ | Web framework ve UI |
| **LangChain** | 0.1+ | LLM orchestration framework |
| **ChromaDB** | 0.4+ | Vector database for embeddings |

### Supporting Libraries
| Kütüphane | Amaç |
|-----------|------|
| **Tenacity** | Retry logic ve error recovery |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive charts |
| **UUID** | Unique request tracking |
| **JSON** | Data serialization |

### Development & DevOps
| Tool | Kullanım |
|------|---------|
| **Git** | Version control |
| **GitHub Actions** | CI/CD pipeline |
| **Docker** | Containerization |
| **pytest** | Unit testing |
| **Black** | Code formatting |
| **Flake8** | Code linting |

## 🚀 Hızlı Başlangıç

### Gereksinimler
```
✅ Python 3.8+ yüklü
✅ Git yüklü
✅ OpenAI API Key
✅ 2GB RAM (minimum)
✅ 1GB disk alanı
✅ İnternet bağlantısı
```

### Hızlı Kurulum (5 Dakika)
```bash
# 1. Repository'yi klonlayın
git clone https://github.com/yourusername/hotel_chatbot.git
cd hotel_chatbot

# 2. Virtual environment oluşturun
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Paketleri yükleyin
pip install -r requirements.txt

# 4. API anahtarını ayarlayın
echo OPENAI_API_KEY=your-api-key-here > .env

# 5. Uygulamayı çalıştırın
streamlit run app.py
```

### 🎯 İlk Test
1. Tarayıcınızda `http://localhost:8501` açılacak
2. "Merhaba!" yazın
3. Chatbot'un yanıtını bekleyin
4. "Rezervasyon yapmak istiyorum" deneyin

## 📥 Kurulum

### Detaylı Kurulum Adımları

#### 1. Repository'yi İndirin
```bash
# HTTPS ile
git clone https://github.com/yourusername/hotel_chatbot.git

# SSH ile (önerilen)
git clone git@github.com:yourusername/hotel_chatbot.git

cd hotel_chatbot
```

#### 2. Python Virtual Environment
```bash
# Python 3.8+ olduğunu kontrol edin
python --version

# Virtual environment oluşturun
python -m venv venv

# Aktifleştirin
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate

# Virtual environment aktif mi kontrol edin
which python  # macOS/Linux
where python   # Windows
```

#### 3. Dependencies Yükleme
```bash
# Temel paketleri yükleyin
pip install --upgrade pip

# Proje bağımlılıklarını yükleyin
pip install -r requirements.txt

# Kurulumu doğrulayın
pip list

# Önemli paketleri test edin
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
python -c "import openai; print('OpenAI:', openai.__version__)"
python -c "import chromadb; print('ChromaDB:', chromadb.__version__)"
```

#### 4. Ortam Değişkenleri Ayarlama

##### A. `.env` Dosyası Oluşturma
```bash
# Proje kök dizininde .env dosyası oluşturun
touch .env  # macOS/Linux
type nul > .env  # Windows
```

##### B. API Anahtarlarını Ekleme
```env
# .env dosyasının içeriği
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000

# Logging Configuration
LOG_LEVEL=INFO
LOG_DIR=logs
ENABLE_CONSOLE_LOGGING=true
ENABLE_FILE_LOGGING=true

# Database Configuration
CHROMA_PERSIST_DIRECTORY=./db

# Application Configuration
APP_NAME=cullinan_hotel_chatbot
APP_VERSION=1.0.0
DEBUG=false
```

##### C. OpenAI API Key Alma
1. [OpenAI Platform](https://platform.openai.com/) hesabı oluşturun
2. **Billing** bölümüne gidin ve ödeme yöntemi ekleyin
3. **API Keys** bölümüne gidin
4. **"Create new secret key"** butonuna tıklayın
5. Anahtarı kopyalayın ve `.env` dosyasına ekleyin
6. **Önemli**: API anahtarınızı asla GitHub'a commit etmeyin!

#### 5. Veritabanı Kurulumu
```bash
# Veritabanı dizinlerini oluşturun
mkdir -p db/hotel_db db/intent_db db/booking_db

# Test verilerini yükleyin
python db_test.py

# Veritabanı bağlantısını test edin
python -c "
import chromadb
client = chromadb.PersistentClient(path='db/hotel_db')
print('ChromaDB connection successful!')
print('Collections:', client.list_collections())
"
```

#### 6. İlk Çalıştırma
```bash
# Streamlit uygulamasını başlatın
streamlit run app.py

# Alternatif olarak Python router'ı test edin
python router.py

# Windows için batch script
run_streamlit.bat
```

### Kurulum Doğrulama
```bash
# Sistem durumu kontrolü
python -c "
import sys
print('Python version:', sys.version)

import streamlit as st
print('Streamlit version:', st.__version__)

import openai
print('OpenAI library version:', openai.__version__)

import chromadb
print('ChromaDB version:', chromadb.__version__)

from pathlib import Path
print('Database exists:', Path('db').exists())
print('Logs directory exists:', Path('logs').exists())

import os
print('API key configured:', bool(os.getenv('OPENAI_API_KEY')))
"
```

## ⚙️ Konfigürasyon

### Ana Konfigürasyon Dosyası (`config.py`)
```python
import os
from pathlib import Path

class Config:
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    
    # Database Settings
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./db")
    
    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    ENABLE_CONSOLE_LOGGING = os.getenv("ENABLE_CONSOLE_LOGGING", "true").lower() == "true"
    ENABLE_FILE_LOGGING = os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true"
    
    # Application Settings
    APP_NAME = os.getenv("APP_NAME", "cullinan_hotel_chatbot")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

### Streamlit Konfigürasyonu (`.streamlit/config.toml`)
```toml
[global]
developmentMode = false
showWarningOnDirectExecution = false

[server]
port = 8501
address = "localhost"
maxUploadSize = 200
maxMessageSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
showErrorDetails = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8fafc"
textColor = "#1e293b"
font = "sans serif"

[runner]
magicEnabled = true
installTracer = false
fixMatplotlib = true

[logger]
level = "info"
messageFormat = "%(asctime)s %(message)s"
```

### Streamlit Secrets (`.streamlit/secrets.toml`)
```toml
# Bu dosyayı .gitignore'a ekleyin!
[secrets]
OPENAI_API_KEY = "sk-your-openai-api-key-here"

[database]
CHROMA_PERSIST_DIRECTORY = "./db"

[logging]
LOG_LEVEL = "INFO"
ENABLE_CONSOLE_LOGGING = true
ENABLE_FILE_LOGGING = true
```

## 💻 Kullanım

### Web Arayüzü Kullanımı

#### 1. Uygulamayı Başlatma
```bash
# Terminal'de
streamlit run app.py

# Otomatik olarak tarayıcıda açılacak
# Açılmazsa manuel olarak gidin: http://localhost:8501
```

#### 2. Ana Arayüz Bileşenleri

![Arayüz Bileşenleri](resim.png)

**Ana Chat Alanı (Sol)**
- Konuşma geçmişi
- Mesaj yazma kutusu
- Gönder butonu
- Typing indicator

**Kontrol Paneli (Sağ)**
- Sistem durumu
- Hızlı sorular
- İstatistikler
- Debug modu
- Temizle butonu

#### 3. Sohbet Etme
```
👤 Kullanıcı: "Merhaba!"
🤖 Bot: "Merhaba! Cullinan Hotel'e hoş geldiniz. Size nasıl yardımcı olabilirim?"

👤 Kullanıcı: "Oda fiyatları nedir?"
🤖 Bot: "Oda fiyatlarımız sezona ve oda tipine göre değişmektedir. 
        Standart odalarımız 1500-2500 TL arasında..."

👤 Kullanıcı: "Rezervasyon yapmak istiyorum"
🤖 Bot: "Tabii ki! Rezervasyon için hangi tarihler arasında 
        konaklama planlıyorsunuz?"
```

### Hızlı Komutlar ve Kısayollar

| Komut | Açıklama |
|-------|----------|
| `Ctrl + Enter` | Mesaj gönder |
| `Escape` | Input alanını temizle |
| `F5` | Sayfayı yenile |
| `Ctrl + Shift + R` | Hard refresh |

### Örnek Kullanım Senaryoları

#### Senaryo 1: Genel Bilgi Alma
```
👤 "Otel hakkında bilgi verir misin?"
🤖 "Cullinan Hotel, İstanbul'un kalbinde yer alan 5 yıldızlı..."

👤 "Hangi olanaklar var?"
🤖 "Otelimizde şu olanaklar bulunmaktadır:
    • SPA ve Wellness Merkezi
    • Kapalı Yüzme Havuzu
    • Fitness Center
    • 3 Restoran..."
```

#### Senaryo 2: Rezervasyon İşlemi
```
👤 "Rezervasyon yapmak istiyorum"
🤖 "Harika! Size yardımcı olmak için şu bilgilere ihtiyacım var:
    1. Check-in tarihi
    2. Check-out tarihi
    3. Misafir sayısı"

👤 "15 Mayıs'tan 20 Mayıs'a kadar, 2 kişi"
🤖 "15-20 Mayıs arası 2 kişilik konaklama için uygun odalarımız:
    • Deluxe Room: 2,200 TL/gece
    • Suite Room: 3,500 TL/gece..."
```

#### Senaryo 3: Özel İstekler
```
👤 "Engelli erişimi var mı?"
🤖 "Evet, otelimiz engelli erişimi konusunda tam donanımlıdır..."

👤 "Pet-friendly misiniz?"
🤖 "Maalesef evcil hayvan kabul etmiyoruz, ancak..."
```

## 📚 API Dokümantasyonu

### ChatbotRouter Sınıfı

```python
from router import ChatbotRouter
from config import Config

# Router'ı başlatma
config = Config()
router = ChatbotRouter(config)

# Mesaj gönderme
response = router.route_message("Merhaba!")
print(response)

# Session yönetimi
session_id = router.create_session()
response = router.route_message("Rezervasyon istiyorum", session_id)
```

### Intent Classification API

```python
from chains.intent_classifier import IntentClassifier

# Classifier'ı başlatma
classifier = IntentClassifier()

# Intent sınıflandırma
intent, confidence = classifier.classify("Rezervasyon yapmak istiyorum")
print(f"Intent: {intent}, Confidence: {confidence}")

# Sonuç: Intent: reservation, Confidence: 0.95
```

### RAG (Retrieval Augmented Generation) API

```python
from chains.rag_hotel import HotelRAG

# RAG sistemini başlatma
rag = HotelRAG()

# Otel bilgisi sorgulama
response = rag.answer("Otel olanakları neler?")
print(response)

# Similarity search
similar_docs = rag.similarity_search("SPA hizmetleri", k=3)
```

### Rezervasyon Dialog API

```python
from chains.booking_dialog import BookingDialog

# Booking dialog başlatma
booking = BookingDialog()

# Booking state'i
booking_state = {}

# Mesaj işleme
booking_state, response, is_complete = booking.handle_message(
    "2 kişilik oda istiyorum", 
    booking_state
)

print(f"Response: {response}")
print(f"Complete: {is_complete}")
print(f"State: {booking_state}")
```

### Logging API

```python
from logging_config import ChatbotLogger

# Logger başlatma
logger = ChatbotLogger()

# Konuşma başlatma
request_id = logger.start_conversation("Merhaba!")

# Intent classification logging
logger.log_intent_classification("Merhaba!", "greeting", 0.98, 150.5)

# Response logging
logger.log_response("Merhaba! Nasıl yardımcı olabilirim?", "greeting", 250.2)

# Error logging
try:
    # Some operation
    pass
except Exception as e:
    logger.log_error(e, "operation_context", "user input")
```

## 📊 Logging Sistemi

### Log Dosya Yapısı
```
logs/
├── hotel_chatbot.json.log          # Ana JSON log dosyası
├── hotel_chatbot_errors.log        # Sadece error log'ları
├── hotel_chatbot.json.log.1        # Rotasyon dosyası 1
├── hotel_chatbot.json.log.2        # Rotasyon dosyası 2
└── ...
```

### Log Formatları

#### JSON Format (Dosya)
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "level": "INFO",
  "logger": "hotel_chatbot",
  "message": "Intent classified: reservation",
  "module": "intent_classifier",
  "function": "classify",
  "line": 45,
  "thread_id": 123456,
  "process_id": 7890,
  "request_id": "uuid-123-456-789",
  "user_input": "Rezervasyon yapmak istiyorum",
  "intent": "reservation",
  "confidence": 0.95,
  "execution_time": 150.2,
  "event_type": "intent_classification"
}
```

#### Console Format (Renkli)
```
[INFO] 10:30:45 hotel_chatbot:classify:45 - Intent classified: reservation [req_id=uuid-123, intent=reservation, time=150.2ms]
```

### Log Analizi

#### Otomatik Log Analizi
```bash
# Son 24 saatlik analiz
python log_analyzer.py --mode analyze --hours 24

# Gerçek zamanlı monitoring
python log_analyzer.py --mode monitor

# Error pattern analizi
python log_analyzer.py --mode error_analysis

# Performance analizi
python log_analyzer.py --mode performance
```

#### Manuel Log Analizi
```python
from log_analyzer import LogAnalyzer

analyzer = LogAnalyzer()

# Performans raporu
performance_report = analyzer.analyze_performance()
print(performance_report)

# Error trend analizi
error_trends = analyzer.analyze_errors()

# Intent dağılımı
intent_distribution = analyzer.analyze_intents()
```

### Log Monitoring Dashboard

Log verilerini görsel olarak takip etmek için:
```bash
# Analytics sayfasını açın
streamlit run pages/analytics.py

# Admin panelini açın
streamlit run pages/admin.py
```

## 🌐 Deployment

### Streamlit Community Cloud

#### 1. GitHub Repository Hazırlama
```bash
# Repository'yi public yapın
git remote -v

# Tüm dosyaları push edin
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

#### 2. Streamlit Cloud Deploy
1. [share.streamlit.io](https://share.streamlit.io) adresine gidin
2. GitHub hesabınızla giriş yapın
3. **"New app"** butonuna tıklayın
4. Repository'nizi seçin: `yourusername/hotel_chatbot`
5. **Branch**: `main`
6. **Main file path**: `app.py`
7. **"Deploy"** butonuna tıklayın

#### 3. Secrets Konfigürasyonu
Streamlit Cloud dashboard'da **"Secrets"** bölümüne:
```toml
[secrets]
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"

[database]
CHROMA_PERSIST_DIRECTORY = "./db"

[app]
DEBUG = false
LOG_LEVEL = "INFO"
```

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Başlangıç komutu
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

#### Docker Commands
```bash
# Build
docker build -t hotel-chatbot .

# Run
docker run -d \
  --name hotel-chatbot \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your-api-key \
  hotel-chatbot

# Logs
docker logs hotel-chatbot

# Stop
docker stop hotel-chatbot
```

#### Docker Compose
```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./db:/app/db
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Heroku Deployment

#### Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### Heroku Commands
```bash
# Login
heroku login

# Create app
heroku create your-hotel-chatbot

# Set environment variables
heroku config:set OPENAI_API_KEY=your-api-key
heroku config:set LOG_LEVEL=INFO

# Deploy
git push heroku main

# Open
heroku open
```

### AWS EC2 Deployment

#### EC2 Setup
```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Clone repository
git clone https://github.com/yourusername/hotel_chatbot.git
cd hotel_chatbot

# Install dependencies
pip3 install -r requirements.txt

# Set environment variables
echo "export OPENAI_API_KEY=your-api-key" >> ~/.bashrc
source ~/.bashrc

# Run with nohup
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

## 👨‍💻 Geliştirme

### Proje Yapısı
```
hotel_chatbot/
│
├── 📁 Main Application Files
│   ├── app.py                      # Ana Streamlit uygulaması
│   ├── router.py                   # Mesaj yönlendirici ve orchestrator
│   ├── config.py                   # Konfigürasyon yönetimi
│   ├── logging_config.py           # Merkezi logging sistemi
│   └── db_test.py                  # Veritabanı test ve setup
│
├── 📁 chains/                      # LangChain modülleri
│   ├── __init__.py
│   ├── intent_classifier.py       # Intent sınıflandırma
│   ├── rag_hotel.py               # RAG sistem (hotel bilgileri)
│   ├── booking_dialog.py          # Rezervasyon dialog yönetimi
│   ├── small_talk.py              # Genel sohbet
│   └── link_redirect.py           # External link yönlendirme
│
├── 📁 pages/                       # Streamlit multi-page
│   ├── analytics.py               # Analytics dashboard
│   └── admin.py                   # Admin panel
│
├── 📁 db/                          # Vector veritabanları
│   ├── hotel_db/                  # Otel bilgi embeddings
│   ├── intent_db/                 # Intent örnekleri
│   └── booking_db/                # Rezervasyon log'ları
│
├── 📁 logs/                        # Log dosyaları
│   ├── hotel_chatbot.json.log     # Ana log
│   └── hotel_chatbot_errors.log   # Error log
│
├── 📁 .streamlit/                  # Streamlit config
│   ├── config.toml                # UI ve server ayarları
│   └── secrets.toml               # API keys (DO NOT COMMIT)
│
├── 📁 tests/                       # Test dosyaları
│   ├── test_router.py
│   ├── test_intent_classifier.py
│   └── test_logging.py
│
├── 📁 data/                        # Raw data files
│   ├── hotel_info.txt             # Otel bilgi metinleri
│   ├── intents.json               # Intent training data
│   └── sample_conversations.json
│
├── 📁 docs/                        # Dokümantasyon
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
│
├── 📄 Configuration Files
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example               # Environment variables template
│   ├── .gitignore                 # Git ignore rules
│   ├── Dockerfile                 # Docker container
│   ├── docker-compose.yml         # Docker Compose
│   └── Procfile                   # Heroku deployment
│
├── 📄 Scripts
│   ├── run_streamlit.bat          # Windows başlatma scripti
│   ├── setup.sh                   # Linux/macOS setup script
│   └── log_analyzer.py            # Log analiz tool
│
└── 📄 Documentation
    ├── README.md                   # Bu dosya
    ├── LICENSE                     # MIT License
    └── resim.png                   # Arayüz screenshot
```

### Development Workflow

#### 1. Environment Setup
```bash
# Clone and setup
git clone https://github.com/yourusername/hotel_chatbot.git
cd hotel_chatbot

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Dependencies
pip install -r requirements.txt

# Pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

#### 2. Code Style & Linting
```bash
# Code formatting
black . --line-length 88

# Linting
flake8 . --max-line-length 88 --ignore E203,W503

# Type checking (optional)
mypy . --ignore-missing-imports
```

#### 3. Testing
```bash
# Unit tests
python -m pytest tests/ -v

# Specific test
python -m pytest tests/test_router.py::test_greeting_intent -v

# Coverage
python -m pytest --cov=. --cov-report=html

# Integration tests
python -m pytest tests/integration/ -v
```

### Yeni Özellik Ekleme

#### 1. Yeni Intent Ekleme
```python
# chains/intent_classifier.py içinde

# Intent patterns'e ekleyin
INTENT_PATTERNS = {
    "restaurant_info": [
        "restoran bilgisi",
        "yemek menüsü",
        "restaurant menu",
        "dining options",
        "food information"
    ],
    # ... existing intents
}

# Intent handler'ı router.py'a ekleyin
def route_message(self, message):
    intent, confidence = self.intent_classifier.classify(message)
    
    if intent == "restaurant_info":
        return self.handle_restaurant_info(message)
    # ... existing routes
```

#### 2. Yeni Chain Oluşturma
```python
# chains/restaurant_info.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from logging_config import ChatbotLogger

class RestaurantInfoChain:
    def __init__(self, llm):
        self.llm = llm
        self.logger = ChatbotLogger("restaurant_chain")
        self.chain = self._create_chain()
    
    def _create_chain(self):
        prompt = PromptTemplate(
            input_variables=["question"],
            template="""
            Sen Cullinan Hotel'in restoran uzmanısın.
            
            Kullanıcı sorusu: {question}
            
            Restoran bilgilerini detaylı ve yardımcı bir şekilde açıkla:
            - 3 restoran: Ana Restoran, Rooftop Bar, Café
            - Açılış saatleri
            - Mutfak türleri
            - Rezervasyon gerekliliği
            
            Yanıt:
            """
        )
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def handle_message(self, message: str) -> str:
        request_id = self.logger.start_conversation(message)
        
        try:
            response = self.chain.run(question=message)
            self.logger.log_response(response, "restaurant_info", 0)
            return response
        except Exception as e:
            self.logger.log_error(e, "restaurant_info_chain", message)
            return "Restoran bilgileri hakkında bir sorun oluştu. Lütfen tekrar deneyin."
```

#### 3. UI Geliştirme
```python
# app.py içinde sidebar'a yeni özellik ekleyin

with col2:  # Sidebar
    # ... existing code ...
    
    # Yeni section ekleyin
    st.markdown("### 🍽️ Restoran Bilgileri")
    
    restaurant_questions = [
        "Restoran menüsü",
        "Açılış saatleri",
        "Rezervasyon gerekli mi?",
        "Özel diyet seçenekleri"
    ]
    
    for question in restaurant_questions:
        if st.button(question, key=f"restaurant_{question}", use_container_width=True):
            # Handle restaurant question
            pass
```

### Database Operations

#### Yeni Collection Ekleme
```python
# db_test.py'e yeni collection ekleyin

def setup_restaurant_db():
    """Restoran bilgileri için vector database oluştur"""
    client = chromadb.PersistentClient(path="db/restaurant_db")
    collection = client.get_or_create_collection("restaurant_info")
    
    restaurant_data = [
        {
            "id": "main_restaurant",
            "document": "Ana Restoran: Türk ve dünya mutfağından seçkin lezzetler...",
            "metadata": {"type": "restaurant", "category": "main"}
        },
        # ... more restaurant data
    ]
    
    for data in restaurant_data:
        collection.add(
            documents=[data["document"]],
            metadatas=[data["metadata"]],
            ids=[data["id"]]
        )
```

### API Endpoints (Gelecek)

Gelecekte REST API desteği için:
```python
# api/routes.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Router'ı kullan
    router = ChatbotRouter()
    response = router.route_message(request.message)
    
    return ChatResponse(
        response=response,
        intent="detected_intent",
        confidence=0.95,
        session_id=request.session_id or "new_session"
    )
```

## 🐛 Sorun Giderme

### Yaygın Kurulum Hataları

#### 1. "OpenAI API key not found"
```bash
# Kontrol edin:
echo $OPENAI_API_KEY  # Linux/macOS
echo %OPENAI_API_KEY% # Windows

# Çözüm:
export OPENAI_API_KEY=sk-your-key  # Linux/macOS
set OPENAI_API_KEY=sk-your-key     # Windows

# .env dosyasında olduğundan emin olun
cat .env
```

#### 2. "Module not found" Hatası
```bash
# Virtual environment aktif mi?
which python
# Sonuç: /path/to/venv/bin/python olmalı

# Değilse aktifleştirin:
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Paketleri yeniden yükleyin:
pip install -r requirements.txt
```

#### 3. "ChromaDB connection error"
```bash
# Database dizini var mı?
ls -la db/

# Yoksa oluşturun:
mkdir -p db/hotel_db db/intent_db db/booking_db

# Database'i test edin:
python db_test.py
```

#### 4. "Port already in use"
```bash
# Port 8501 kullanımda mı kontrol edin:
netstat -an | grep 8501  # Linux/macOS
netstat -an | findstr 8501  # Windows

# Farklı port kullanın:
streamlit run app.py --server.port 8502

# Veya kullanımdaki process'i öldürün:
lsof -ti:8501 | xargs kill  # macOS/Linux
```

### Runtime Hataları

#### 1. "API rate limit exceeded"
```python
# config.py'de retry ayarları:
OPENAI_RETRY_ATTEMPTS = 3
OPENAI_RETRY_DELAY = 1

# Veya daha düşük rate kullanın:
OPENAI_TEMPERATURE = 0.3
OPENAI_MAX_TOKENS = 500
```

#### 2. "Memory issues"
```bash
# RAM kullanımını kontrol edin:
top  # Linux/macOS
taskmgr  # Windows

# ChromaDB için SSD kullanın:
export CHROMA_PERSIST_DIRECTORY=/path/to/ssd/db
```

#### 3. "Streamlit connection error"
```bash
# Cache'i temizleyin:
streamlit cache clear

# Browser cache'i temizleyin:
Ctrl+Shift+R (hard refresh)

# Yeni browser session:
Ctrl+Shift+N (incognito)
```

### Debug Modu Kullanımı

#### 1. Streamlit Debug
```python
# app.py'de debug flag'i aktifleştirin
DEBUG = True

# Sidebar'da debug checkbox'ı işaretleyin
if st.checkbox("🔍 Debug Modu"):
    st.json({
        "session_state": st.session_state,
        "environment": dict(os.environ),
        "system_info": get_system_info()
    })
```

#### 2. Logging Debug
```bash
# Log seviyesini DEBUG'a alın:
export LOG_LEVEL=DEBUG

# Veya .env dosyasında:
LOG_LEVEL=DEBUG

# Console logging'i aktifleştirin:
ENABLE_CONSOLE_LOGGING=true
```

#### 3. Python Debug
```python
# Code'a breakpoint ekleyin:
import pdb; pdb.set_trace()

# Veya:
breakpoint()  # Python 3.7+

# IPython debug (daha gelişmiş):
from IPython import embed; embed()
```

### Performance Sorunları

#### 1. Yavaş Yanıt Süreleri
```python
# OpenAI ayarlarını optimize edin:
OPENAI_TEMPERATURE = 0.1  # Daha hızlı
OPENAI_MAX_TOKENS = 300   # Daha kısa yanıtlar

# Cache kullanın:
@st.cache_data
def expensive_operation():
    # Pahalı işlem
    pass
```

#### 2. Memory Leaks
```python
# Session state'i düzenli temizleyin:
if len(st.session_state.messages) > 50:
    st.session_state.messages = st.session_state.messages[-25:]

# ChromaDB client'ı yeniden kullanın:
@st.cache_resource
def get_chroma_client():
    return chromadb.PersistentClient(path="db")
```

### Log Analizi ile Debug

```bash
# Error pattern'lerini bulun:
grep -E "ERROR|CRITICAL" logs/hotel_chatbot.json.log | tail -20

# Yavaş işlemleri bulun:
grep "execution_time" logs/hotel_chatbot.json.log | jq 'select(.execution_time > 1000)'

# Intent dağılımını analiz edin:
grep "intent_classification" logs/hotel_chatbot.json.log | jq .intent | sort | uniq -c
```

### Streamlit Cloud Deployment Sorunları

#### 1. "Repository access denied"
```bash
# Repository public mi?
# GitHub → Settings → General → Public repository

# Branch doğru mu?
git branch -a
```

#### 2. "Build failed"
```bash
# requirements.txt güncel mi?
pip freeze > requirements.txt

# Python version uyumlu mu?
# Streamlit Cloud Python 3.7-3.11 destekler
```

#### 3. "Secrets not working"
```toml
# .streamlit/secrets.toml format doğru mu?
[secrets]
OPENAI_API_KEY = "sk-your-key"  # Tırnak içinde olmalı

# Streamlit Cloud dashboard'da da aynı format:
OPENAI_API_KEY = "sk-your-key"
```

## 🤝 Katkıda Bulunma

### Geliştirici Rehberi

#### 1. Development Environment
```bash
# Fork the repository
git clone https://github.com/yourusername/hotel_chatbot.git

# Create feature branch
git checkout -b feature/amazing-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install
```

#### 2. Code Standards

**Python Style Guide**
- **PEP 8** uyumlu kod yazın
- **Black** formatter kullanın (line length: 88)
- **Type hints** ekleyin
- **Docstrings** yazın (Google style)

```python
def classify_intent(user_input: str) -> Tuple[str, float]:
    """
    Kullanıcı girişini intent'e sınıflandırır.
    
    Args:
        user_input: Kullanıcının mesajı
        
    Returns:
        Intent adı ve confidence score tuple'ı
        
    Raises:
        ValueError: Geçersiz input için
        APIError: OpenAI API hatası için
    """
    pass
```

**Commit Message Format**
```
feat: add restaurant information chain
fix: resolve intent classification bug
docs: update API documentation
style: format code with black
refactor: optimize database queries
test: add unit tests for booking dialog
chore: update dependencies
```

#### 3. Testing Requirements

```python
# Test dosyası örneği: tests/test_intent_classifier.py
import unittest
from unittest.mock import patch, MagicMock

class TestIntentClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_greeting_intent(self):
        intent, confidence = self.classifier.classify("Merhaba!")
        self.assertEqual(intent, "greeting")
        self.assertGreater(confidence, 0.8)
    
    @patch('openai.OpenAI')
    def test_api_error_handling(self, mock_openai):
        mock_openai.side_effect = Exception("API Error")
        
        intent, confidence = self.classifier.classify("test")
        self.assertEqual(intent, "unknown")
```

#### 4. Pull Request Süreci

1. **Issue oluşturun** (yeni özellik/bug için)
2. **Branch oluşturun** (`feature/issue-123` formatında)
3. **Kod yazın** ve test edin
4. **Commit** edin (anlamlı mesajlarla)
5. **Push** edin ve **Pull Request** açın
6. **Code review** bekleyin
7. **Feedback**'leri uygulayın
8. **Merge** onayını bekleyin

#### 5. Review Kriterleri

**Code Quality**
- ✅ Kod PEP 8 uyumlu
- ✅ Type hints mevcut
- ✅ Docstrings eklenmiş
- ✅ Error handling yapılmış
- ✅ Logging eklnenmiş

**Testing**
- ✅ Unit tests yazılmış
- ✅ Integration tests (gerekirse)
- ✅ Test coverage %80+
- ✅ Edge cases test edilmiş

**Documentation**
- ✅ README güncellenmiş
- ✅ API documentation eklenmiş
- ✅ Changelog güncellenmiş
- ✅ Comments yeterli

### Katkı Alanları

#### 🐛 Bug Fixes
- Intent classification hataları
- Memory leak'ler
- UI/UX sorunları
- Performance optimizasyonları

#### ✨ Yeni Özellikler
- Yeni intent'ler (SPA, fitness, etc.)
- Çok dilli destek geliştirme
- Voice interface
- Mobile app
- Admin dashboard

#### 📚 Documentation
- API documentation
- Tutorial'lar
- Video guides
- Translation (EN/TR)

#### 🧪 Testing
- Unit test coverage artırma
- Integration tests
- Performance tests
- Load testing

### Community

#### Discord Server
[Community Discord](https://discord.gg/yourserver) - Günlük sohbet ve destek

#### GitHub Discussions
[GitHub Discussions](https://github.com/yourusername/hotel_chatbot/discussions) - Özellik önerileri ve tartışmalar

#### Weekly Meetings
Her Çarşamba 20:00 - Online development meeting

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır.

```
MIT License

Copyright (c) 2024 Cullinan Hotel Chatbot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🎓 Academic Information

**Proje Bilgileri**
- **Öğrenci Numarası**: 170421015
- **Öğrenci Adı**: Ahmed Said Kılıç
- **Proje Konusu**: Otel Chatbot Uygulaması
- **Ders**: Yapay Zeka ve Doğal Dil İşleme
- **Dönem**: 2024-2025 Güz

**Teknoloji Stack**
- **Backend**: Python 3.8+, LangChain, OpenAI API
- **Frontend**: Streamlit, HTML/CSS, JavaScript
- **Database**: ChromaDB (Vector Database)
- **Deployment**: Streamlit Cloud, Docker
- **Monitoring**: Custom Logging System

## 👥 Takım ve İletişim

### Geliştirici
- **Ad**: Ahmed Said Kılıç
- **Email**: ahmed.said@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **LinkedIn**: [Ahmed Said Kılıç](https://linkedin.com/in/yourprofile)

### Destek
- **GitHub Issues**: [Issue Tracker](https://github.com/yourusername/hotel_chatbot/issues)
- **Email Support**: support@cullinanhotelchatbot.com
- **Discord**: [Community Server](https://discord.gg/yourserver)

## 🙏 Teşekkürler

### Open Source Projeler
- **OpenAI**: GPT modelleri ve API
- **Streamlit**: Web framework
- **LangChain**: LLM orchestration
- **ChromaDB**: Vector database
- **Python Community**: Ecosystem support

### Inspirations
- ChatGPT'nin kullanıcı deneyimi
- Slack'in bot interface'i
- WhatsApp'ın chat tasarımı
- Booking.com'un rezervasyon sistemi

### Beta Testers
- University AI Lab
- Hotel Management Students
- Open Source Community

---

<div align="center">

**🏨 Cullinan Hotel Chatbot**

*Modern otel deneyimi için yapay zeka destekli asistan*

[🌐 Live Demo](https://your-app.streamlit.app) • [📖 Docs](https://docs.your-app.com) • [🐛 Report Bug](https://github.com/yourusername/hotel_chatbot/issues) • [💡 Request Feature](https://github.com/yourusername/hotel_chatbot/discussions)

Made with ❤️ using **Python** & **Streamlit**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=yourusername.hotel_chatbot)
![GitHub stars](https://img.shields.io/github/stars/yourusername/hotel_chatbot?style=social)

</div>
