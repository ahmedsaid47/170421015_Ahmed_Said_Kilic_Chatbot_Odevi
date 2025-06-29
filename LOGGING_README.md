# Cullinan Hotel Chatbot - Kapsamlı Logging Sistemi

Bu proje, Cullinan Hotel chatbot uygulaması için eksiksiz bir logging ve monitoring sistemi içermektedir.

## 🚀 Özellikler

### 📝 Logging Özellikleri
- **Structured Logging**: JSON formatında detaylı loglar
- **Seviye Bazlı Filtreleme**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Dosya Rotasyonu**: Otomatik log dosyası yönetimi
- **Renkli Konsol Çıktısı**: Geliştirilmiş debugging deneyimi
- **Performance Tracking**: Fonksiyon execution time monitoring
- **Error Tracking**: Detaylı hata analizi ve stack trace
- **API Call Logging**: OpenAI API çağrıları ve token kullanımı

### 🔍 Log Analiz Araçları
- **Real-time Monitoring**: Canlı log takibi
- **Performance Analytics**: Yanıt süreleri ve bottleneck analizi
- **Error Pattern Detection**: Hata trendleri ve sık karşılaşılan problemler
- **Intent Classification Analytics**: AI model performance analizi
- **API Usage Tracking**: Token kullanımı ve maliyet takibi
- **User Interaction Patterns**: Kullanıcı davranış analizi

## 📁 Dosya Yapısı

```
hotel_chatbot/
├── config.py                 # Konfigürasyon + logging
├── router.py                 # Ana chatbot router + kapsamlı logging
├── logging_config.py         # Merkezi logging konfigürasyonu
├── log_analyzer.py          # Log analiz ve monitoring aracı
├── logs/                    # Log dosyaları
│   ├── hotel_chatbot.json.log     # Ana JSON loglar
│   └── hotel_chatbot_errors.log   # Sadece hatalar
└── chains/
    ├── intent_classifier.py  # Intent sınıflandırma + logging
    ├── rag_hotel.py          # RAG chain + logging
    ├── booking_dialog.py     # Rezervasyon diyaloğu + logging
    ├── small_talk.py         # Küçük sohbet + logging
    └── link_redirect.py      # Link yönlendirme + logging
```

## 🛠️ Kurulum

### Gereksinimler
```bash
pip install openai chromadb tenacity matplotlib pandas
```

### Logging Sistemini Başlatma
```python
from logging_config import setup_logging, ChatbotLogger

# Basit kurulum
logger = setup_logging()

# Gelişmiş kurulum
logger = setup_logging(
    app_name="hotel_chatbot",
    log_level="INFO",
    log_dir="logs",
    enable_console=True,
    enable_file=True
)
```

## 📊 Kullanım Örnekleri

### 1. Chatbot Logger Kullanımı
```python
from logging_config import ChatbotLogger

chatbot_logger = ChatbotLogger()

# Konuşma başlatma
request_id = chatbot_logger.start_conversation("Merhaba!")

# Intent sınıflandırma loglama
chatbot_logger.log_intent_classification(
    user_input="Rezervasyon yapmak istiyorum",
    intent="rezervasyon_oluşturma",
    confidence=0.95,
    execution_time=150.2
)

# Rezervasyon durumu loglama
chatbot_logger.log_booking_state(
    state={"giris_tarihi": "2024-01-15", "oda_sayisi": 2},
    user_input="2 oda istiyorum",
    is_complete=False
)

# Yanıt loglama
chatbot_logger.log_response(
    response="Hangi tarihler için rezervasyon yapmak istiyorsunuz?",
    response_type="booking_dialog",
    execution_time=250.5
)

# Hata loglama
try:
    # Some operation
    pass
except Exception as e:
    chatbot_logger.log_error(e, "booking_process", "kullanıcı inputu")
```

### 2. Decorator Kullanımı
```python
from logging_config import log_execution_time, log_api_call

@log_execution_time("database_query")
def query_database():
    # Database operations
    pass

@log_api_call("OpenAI GPT")
def call_openai_api():
    # API call
    pass
```

### 3. Log Analizi
```bash
# Son 24 saatlik analiz raporu
python log_analyzer.py --mode analyze --hours 24

# Real-time monitoring
python log_analyzer.py --mode monitor --refresh 5

# Raporu dosyaya kaydetme
python log_analyzer.py --mode analyze --hours 48 --output report.txt
```

## 📈 Log Analiz Raporu Örneği

```
================================================================================
CULLINAN HOTEL CHATBOT - LOG ANALİZ RAPORU
Rapor Tarihi: 2024-01-15 14:30:00
Analiz Periyodu: Son 24 saat
================================================================================

📊 HATA ANALİZİ
----------------------------------------
Toplam Hata: 12
Hata Oranı: 2.35%

En Sık Hata Tipleri:
  • ConnectionError: 7
  • ValidationError: 3
  • TimeoutError: 2

⚡ PERFORMANCE ANALİZİ
----------------------------------------
Toplam İşlem: 1,247
Ortalama Süre: 245.67ms
P95 Süre: 850.32ms
En Yavaş: 2,150.45ms

İşlem Bazında Performance:
  • intent_classification: 125.32ms (avg), 487 işlem
  • rag_query: 380.45ms (avg), 234 işlem
  • booking_dialog: 290.12ms (avg), 156 işlem

🎯 INTENT ANALİZİ
----------------------------------------
Toplam Sınıflandırma: 487
Düşük Güven Skoru: 23

Intent Dağılımı:
  • rezervasyon_oluşturma: 145 (%89.2 güven)
  • selamla: 98 (%94.5 güven)
  • fiyat_sorgulama: 87 (%86.7 güven)

🌐 API KULLANIMI
----------------------------------------
Toplam API Çağrısı: 892
Toplam Token: 125,436
Tahmini Maliyet: $0.0234

👥 KULLANICI ETKİLEŞİMLERİ
----------------------------------------
Toplam Konuşma: 256
Saatlik Ortalama: 10.7
En Yoğun Saat: 14:00 (28 konuşma)
```

## 🎯 Log Seviyeleri ve Anlamları

### DEBUG
- Detaylı debugging bilgileri
- Fonksiyon entry/exit
- Variable değerleri
- Development ortamında kullanılır

### INFO
- Normal işlem akışı bilgileri
- Başarılı operasyonlar
- User interactions
- API çağrıları

### WARNING
- Beklenmeyen durumlar
- Düşük confidence skorları
- Yavaş yanıt süreleri
- Fallback kullanımları

### ERROR
- Hata durumları
- API çağrısı başarısızlıkları
- Database bağlantı problemleri
- Validation hataları

### CRITICAL
- Sistem düzeyinde kritik hatalar
- Uygulama çökmelerine neden olabilecek durumlar
- Güvenlik problemleri

## 📋 Log Entry Örneği

```json
{
  "timestamp": "2024-01-15T14:30:45.123456",
  "level": "INFO",
  "logger": "hotel_chatbot.router",
  "message": "Intent classification completed",
  "module": "router",
  "function": "main",
  "line": 65,
  "thread_id": 12345,
  "process_id": 6789,
  "request_id": "req_abc123def456",
  "user_input": "Rezervasyon yapmak istiyorum",
  "intent": "rezervasyon_oluşturma",
  "confidence": 0.95,
  "execution_time": 150.2,
  "event_type": "intent_classification"
}
```

## 🔧 Konfigürasyon Seçenekleri

### Logging Config
```python
setup_logging(
    app_name="hotel_chatbot",        # Uygulama adı
    log_level="INFO",                # Minimum log seviyesi
    log_dir="logs",                  # Log dizini
    enable_console=True,             # Konsol çıktısı
    enable_file=True,                # Dosya çıktısı
    max_bytes=10*1024*1024,         # Max dosya boyutu (10MB)
    backup_count=5                   # Eski dosya sayısı
)
```

### ChatbotLogger Özelleştirme
```python
chatbot_logger = ChatbotLogger("custom_logger_name")

# Özel event logging
chatbot_logger.log_performance(
    operation="custom_operation",
    execution_time=123.45,
    custom_metric=42,
    user_id="user123"
)
```

## 🚨 Hata Ayıklama

### Yaygın Problemler

1. **Log dosyası oluşturulmuyor**
   - Dizin izinlerini kontrol edin
   - Log dizininin var olduğundan emin olun

2. **Console output görünmüyor**
   - Log level'ı kontrol edin
   - `enable_console=True` olduğundan emin olun

3. **JSON parse hataları**
   - Log dosyasının bozuk olmadığını kontrol edin
   - Manual edit yapılmış satırları temizleyin

4. **Performance yavaşlığı**
   - Log level'ı yükseltin (INFO -> WARNING)
   - Dosya I/O'yu azaltın

### Debug Mode Kullanımı
```python
# Debug mode'da başlatma
logger = setup_logging(log_level="DEBUG")

# Spesifik modül için debug
import logging
logging.getLogger("hotel_chatbot.rag_hotel").setLevel(logging.DEBUG)
```

## 📊 Monitoring ve Alerting

### Real-time Monitoring
```bash
# Terminal 1: Log monitoring
python log_analyzer.py --mode monitor

# Terminal 2: Error pattern detection
python log_analyzer.py --mode analyze --hours 1 | grep -i error
```

### Automated Alerts (Script Örneği)
```python
import subprocess
import time

def check_error_rate():
    result = subprocess.run([
        "python", "log_analyzer.py", 
        "--mode", "analyze", "--hours", "1"
    ], capture_output=True, text=True)
    
    # Parse error rate from output
    if "Hata Oranı:" in result.stdout:
        # Extract error rate and send alert if > threshold
        pass

# Her 5 dakikada kontrol et
while True:
    check_error_rate()
    time.sleep(300)
```

## 🎨 Log Görselleştirme

### Matplotlib Dashboard (Opsiyonel)
```bash
pip install matplotlib pandas seaborn

# Dashboard başlatma
python log_analyzer.py --mode dashboard
```

### Grafana Integration
```yaml
# docker-compose.yml
version: '3'
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - ./logs:/var/log/hotel_chatbot
```

## 🔒 Güvenlik ve Privacy

### Sensitive Data Handling
- Kullanıcı kişisel bilgileri loglanmaz
- API key'ler maskelenir
- Request ID'ler hash'lenir

### Log Retention
- Dosya rotasyonu ile eski loglar otomatik silinir
- GDPR compliance için 30 günlük retention
- Kritik hatalar ayrı dosyada daha uzun süre saklanır

## 🤝 Katkıda Bulunma

1. Yeni log event tipleri eklerken `event_type` alanını kullanın
2. Performance kritik yerler için `@log_execution_time` decorator kullanın
3. Hata durumlarında context bilgisi ekleyin
4. Log analiz raporu için yeni metrikler ekleyebilirsiniz

## 📞 Destek

- Log analiz sorunları için `log_analyzer.py --help`
- Logging config için `logging_config.py` dokümanlarına bakın
- Performance sorunları için DEBUG mode kullanın

---

Bu logging sistemi ile chatbot'unuzun her adımını izleyebilir, performansını optimize edebilir ve proaktif olarak sorunları tespit edebilirsiniz. 🚀
