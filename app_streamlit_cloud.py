"""
Cullinan Hotel Chatbot - Streamlit Community Cloud
==================================================
Basitleştirilmiş ve cloud-ready chatbot uygulaması
"""

import streamlit as st
import os
import sys
import time
import json
import uuid
from datetime import datetime
from pathlib import Path

# Streamlit sayfa ayarları
st.set_page_config(
    page_title="🏨 Cullinan Hotel Assistant",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit Cloud için ortam ayarları
def setup_environment():
    """Streamlit Cloud için ortam değişkenlerini ayarla"""
    try:
        # OpenAI API key kontrolü
        if "OPENAI_API_KEY" not in os.environ:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
            else:
                st.error("🔑 OpenAI API anahtarı bulunamadı!")
                st.info("Streamlit Cloud'da secrets ayarlarına OpenAI API anahtarınızı ekleyin.")
                st.stop()
        
        # Dizinleri oluştur
        for dir_name in ["logs", "db", "db/intent_db", "db/hotel_db", "db/booking_db"]:
            Path(dir_name).mkdir(parents=True, exist_ok=True)
        
        return True
    except Exception as e:
        st.error(f"Ortam ayarları yapılırken hata: {str(e)}")
        return False

# Ortamı ayarla
if not setup_environment():
    st.stop()

# Gerekli kütüphaneleri import et
try:
    import openai
    import chromadb
    from tenacity import retry, wait_random_exponential, stop_after_attempt
    
    # OpenAI client'ı başlat
    openai.api_key = os.environ["OPENAI_API_KEY"]
    client = openai.OpenAI()
    
except ImportError as e:
    st.error(f"Gerekli kütüphane bulunamadı: {str(e)}")
    st.info("requirements.txt dosyasındaki tüm kütüphanelerin yüklendiğinden emin olun.")
    st.stop()
except Exception as e:
    st.error(f"Başlatma hatası: {str(e)}")
    st.stop()

# CSS Styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px 40px;
        max-width: 80%;
        float: right;
        clear: both;
    }
    
    .bot-message {
        background: #f8f9fa;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 40px 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
        border-left: 4px solid #667eea;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .metric-container {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Session state başlatma
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'total_messages' not in st.session_state:
        st.session_state.total_messages = 0
    if 'booking_state' not in st.session_state:
        st.session_state.booking_state = {}
    if 'in_booking' not in st.session_state:
        st.session_state.in_booking = False
    if 'current_intent' not in st.session_state:
        st.session_state.current_intent = "unknown"

# Basit intent sınıflandırması
@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(3))
def classify_intent(user_input: str) -> str:
    """Basit intent sınıflandırması"""
    try:
        user_lower = user_input.lower()
        
        # Basit anahtar kelime tabanlı sınıflandırma
        if any(word in user_lower for word in ['merhaba', 'selam', 'hello', 'hi']):
            return 'greeting'
        elif any(word in user_lower for word in ['rezervasyon', 'booking', 'oda', 'room']):
            return 'booking'
        elif any(word in user_lower for word in ['fiyat', 'price', 'ücret', 'cost']):
            return 'pricing'
        elif any(word in user_lower for word in ['bilgi', 'info', 'nedir', 'what']):
            return 'information'
        elif any(word in user_lower for word in ['teşekkür', 'thank', 'sağol']):
            return 'thanks'
        elif any(word in user_lower for word in ['görüşürüz', 'bye', 'hoşça']):
            return 'goodbye'
        else:
            return 'general'
    except Exception:
        return 'general'

# Bot yanıtları
def get_bot_response(intent: str, user_input: str) -> str:
    """Intent'e göre bot yanıtı üret"""
    
    responses = {
        'greeting': [
            "Merhaba! Cullinan Hotel'e hoş geldiniz. Size nasıl yardımcı olabilirim?",
            "Selam! Otelimiz hakkında merak ettiğiniz bir şey var mı?",
            "Hoş geldiniz! Rezervasyon yapmak mı istiyorsunuz?"
        ],
        'booking': [
            "Rezervasyon yapmak istediğinizi anlıyorum. Hangi tarihler için oda arıyorsunuz?",
            "Tabii ki! Kaç kişi için ve hangi tarihte konaklama planlıyorsunuz?",
            "Rezervasyon için size yardımcı olabilirim. Check-in ve check-out tarihlerinizi söyleyebilir misiniz?"
        ],
        'pricing': [
            "Oda fiyatlarımız sezona ve oda tipine göre değişmektedir. Standart odalarımız 1500-2500 TL arasındadır.",
            "Fiyat bilgisi için tarih ve misafir sayısını belirtirseniz daha detaylı bilgi verebilirim.",
            "Güncel fiyatlarımız için rezervasyon talebinizi oluşturabilirim."
        ],
        'information': [
            "Cullinan Hotel, İstanbul'un kalbinde lüks konaklama hizmeti sunan 5 yıldızlı bir oteldir.",
            "Otelimizde spa, fitness center, kapalı havuz ve 3 restoran bulunmaktadır.",
            "24 saat room service, ücretsiz WiFi ve havaalanı transferi hizmetlerimiz mevcuttur."
        ],
        'thanks': [
            "Rica ederim! Başka sorularınız varsa çekinmeyin.",
            "Memnun oldum yardımcı olabildiğime. İyi günler!",
            "Teşekkür ederim! Size nasıl daha fazla yardımcı olabilirim?"
        ],
        'goodbye': [
            "Hoşça kalın! Tekrar görüşmek üzere.",
            "İyi günler! Cullinan Hotel'i tercih ettiğiniz için teşekkürler.",
            "Görüşürüz! Rezervasyon için bizi arayabilirsiniz."
        ],
        'general': [
            "Bu konuda size yardımcı olmaya çalışayım. Biraz daha detay verebilir misiniz?",
            "Anlıyorum. Otelimiz hakkında özel bir konuda mı bilgi almak istiyorsunuz?",
            "Tabii ki! Size nasıl yardımcı olabileceğimi açıklayabilir misiniz?"
        ]
    }
    
    import random
    return random.choice(responses.get(intent, responses['general']))

# Ana uygulama
init_session_state()

# Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: white; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
    <h1 style='color: #667eea; margin: 0;'>🏨 Cullinan Hotel Chatbot</h1>
    <p style='color: #666; margin: 5px 0 0 0;'>Size nasıl yardımcı olabilirim?</p>
</div>
""", unsafe_allow_html=True)

# Ana layout
col1, col2 = st.columns([3, 1])

with col1:
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Mesajları göster
        if not st.session_state.messages:
            st.markdown('<div class="bot-message">Merhaba! Cullinan Hotel asistanınızım. Size nasıl yardımcı olabilirim?</div>', unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_button = st.columns([4, 1])
        
        with col_input:
            user_input = st.text_input(
                "Mesajınızı yazın...",
                placeholder="Örn: Otel hakkında bilgi almak istiyorum",
                label_visibility="collapsed"
            )
        
        with col_button:
            submit_button = st.form_submit_button("Gönder", use_container_width=True)
    
    # Mesaj işleme
    if submit_button and user_input.strip():
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.total_messages += 1
        
        try:
            # Intent sınıflandır
            with st.spinner("Düşünüyorum..."):
                intent = classify_intent(user_input)
                response = get_bot_response(intent, user_input)
                st.session_state.current_intent = intent
            
            # Bot yanıtını ekle
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Sayfayı yenile
            st.rerun()
            
        except Exception as e:
            error_msg = f"Üzgünüm, bir hata oluştu: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()

with col2:
    # Sidebar
    st.markdown("### 📊 Sistem Durumu")
    st.success("✅ Aktif")
    
    # İstatistikler
    st.markdown("### 📈 İstatistikler")
    st.metric("Toplam Mesaj", st.session_state.total_messages)
    st.metric("Son Intent", st.session_state.current_intent.title())
    
    # Hızlı sorular
    st.markdown("### ⚡ Hızlı Sorular")
    
    quick_questions = [
        "Merhaba",
        "Rezervasyon yapmak istiyorum",
        "Oda fiyatları nedir?",
        "Otel hakkında bilgi",
        "Teşekkürler"
    ]
    
    for question in quick_questions:
        if st.button(question, key=f"quick_{question}", use_container_width=True):
            # Hızlı soruyu işle
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.total_messages += 1
            
            try:
                intent = classify_intent(question)
                response = get_bot_response(intent, question)
                st.session_state.current_intent = intent
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Hata: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            st.rerun()
    
    # Kontroller
    st.markdown("### 🛠️ Kontroller")
    
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_messages = 0
        st.session_state.current_intent = "unknown"
        st.rerun()
    
    # Debug modu
    if st.checkbox("🔍 Debug Modu"):
        st.markdown("### 🐛 Debug Bilgileri")
        st.json({
            "total_messages": st.session_state.total_messages,
            "current_intent": st.session_state.current_intent,
            "api_key_set": bool(os.environ.get("OPENAI_API_KEY")),
            "session_keys": list(st.session_state.keys())
        })

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 10px;'>
    <p>🏨 <strong>Cullinan Hotel</strong> - Lüks Konaklama Deneyimi</p>
    <p style='font-size: 0.8em;'>Powered by Streamlit & OpenAI</p>
</div>
""", unsafe_allow_html=True)
