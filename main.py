"""
Streamlit Multi-Page App - Ana sayfa navigation
"""

import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Cullinan Hotel - Ana Sayfa",
    page_icon="🏨",
    layout="wide"
)

# Ana sayfa içeriği
st.markdown("""
# 🏨 Cullinan Hotel Chatbot Uygulaması

Hoş geldiniz! Bu uygulama şu özellikleri sunmaktadır:

## 📱 Mevcut Sayfalar

### 1. 🤖 Ana Chatbot (app.py)
- Ana sohbet arayüzü
- Rezervasyon işlemleri  
- Otel bilgileri
- Gerçek zamanlı yanıtlar

### 2. 📊 Log Analizi (pages/analytics.py)
- Performance metrikleri
- Hata analizi
- Kullanıcı etkileşim raporları
- Real-time monitoring

### 3. ⚙️ Admin Paneli (pages/admin.py)
- Sistem ayarları
- Veritabanı yönetimi
- Log konfigürasyonu
- Backup & restore

## 🚀 Başlangıç

Ana chatbot'u kullanmak için:
```bash
streamlit run app.py
```

Tüm sayfaları çalıştırmak için:
```bash
# Bu dosyayı çalıştırın
streamlit run main.py
```

## 📋 Gereksinimler

requirements.txt dosyasındaki tüm kütüphanelerin yüklü olduğundan emin olun:
```bash
pip install -r requirements.txt
```

## 🔗 Hızlı Linkler
""")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🤖 Chatbot'u Başlat", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("📊 Analytics Sayfası", use_container_width=True):
        st.switch_page("pages/analytics.py")

with col3:
    if st.button("⚙️ Admin Paneli", use_container_width=True):
        st.switch_page("pages/admin.py")
