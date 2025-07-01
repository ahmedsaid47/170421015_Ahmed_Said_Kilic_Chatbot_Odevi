"""
Cullinan Hotel Chatbot - Qdrant Cloud Streamlit Uygulaması (Gelişmiş)
====================================================================
Bu uygulama Qdrant Cloud vektör veritabanını kullanarak gelişmiş otel asistanı hizmeti sunar.
"""
import streamlit as st
import openai
import time
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Streamlit config - en başta olmalı
st.set_page_config(
    page_title="Cullinan Hotel Chatbot - Professional",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Logging sistemini basitleştir - HTTP loglarını gizle
logging.basicConfig(level=logging.ERROR)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Session state kontrolleri - en başta
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.messages = []
    st.session_state.total_messages = 0
    st.session_state.booking_state = {}
    st.session_state.in_booking = False
    st.session_state.current_intent = "unknown"

@st.cache_resource
def setup_environment():
    """Ortam değişkenlerini bir kez ayarla"""
    # .env dosyasını yükle
    from dotenv import load_dotenv
    load_dotenv()
    
    # OpenAI API key kontrolü
    if "OPENAI_API_KEY" not in os.environ:
        try:
            # Streamlit secrets kontrolü - güvenli şekilde
            import streamlit as st
            if 'OPENAI_API_KEY' in st.secrets:
                os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        except Exception:
            # Secrets dosyası yoksa sessizce devam et
            pass
        
        # Hala yoksa hata ver
        if "OPENAI_API_KEY" not in os.environ:
            st.error("🔑 OpenAI API anahtarı bulunamadı!")
            st.info("Lütfen .env dosyasında OPENAI_API_KEY'i ayarlayın.")
            st.stop()
    
    # Qdrant Cloud ayarları
    try:
        if "QDRANT_URL" not in os.environ and 'QDRANT_URL' in st.secrets:
            os.environ["QDRANT_URL"] = st.secrets["QDRANT_URL"]
        
        if "QDRANT_API_KEY" not in os.environ and 'QDRANT_API_KEY' in st.secrets:
            os.environ["QDRANT_API_KEY"] = st.secrets["QDRANT_API_KEY"]
    except Exception:
        # Secrets hatası varsa sessiz geç
        pass
    
    # Log dizini
    Path("logs").mkdir(exist_ok=True)
    
    return True

@st.cache_resource  
def initialize_components():
    """Qdrant bileşenlerini bir kez başlat"""
    try:
        # Import'ları burada yap
        from chains.intent_classifier_qdrant import IntentClassifier
        from chains.rag_hotel_qdrant import answer_hotel_qdrant
        from chains.booking_dialog import handle_booking
        from chains.small_talk import respond_small_talk
        from chains.link_redirect import redirect
        from qdrant_config import get_qdrant_client
        
        # OpenAI setup
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Qdrant client
        qdrant_client = get_qdrant_client()
        
        # Intent classifier
        classifier = IntentClassifier()
        
        return {
            'qdrant_client': qdrant_client,
            'classifier': classifier,
            'answer_hotel_qdrant': answer_hotel_qdrant,
            'handle_booking': handle_booking,
            'respond_small_talk': respond_small_talk,
            'redirect': redirect
        }
        
    except Exception as e:
        st.error(f"Sistem başlatma hatası: {str(e)}")
        st.stop()

# CSS Styling - Modern ve profesyonel
st.markdown("""
<style>
    /* Ana sayfa stili */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Chat container styling */
    .stChatFloatingInputContainer {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Chat mesaj stilleri */
    [data-testid="stChatMessage"] {
        margin: 0.5rem 0;
        animation: fadeIn 0.3s ease-in;
    }
    
    /* Animasyon efektleri */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Buton stilleri */
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Metric kartları */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 5px 0;
        backdrop-filter: blur(5px);
    }
    
    /* Başlık styling */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Success/error mesajları */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
</style>
""", unsafe_allow_html=True)

def get_bot_response(intent: str, question: str) -> str:
    """Bot yanıtını al (Qdrant destekli)"""
    try:
        components = initialize_components()
        
        # Niyet kümeleri
        SMALL_TALK = {"selamla", "veda", "teşekkür", "yardım"}
        HOTEL_INFO = {"otel_bilgi", "hizmetler", "genel"}
        BOOKING = {"rezervasyon", "booking"}
        REDIRECT = {"link", "yönlendirme"}
        
        if intent in SMALL_TALK:
            return components['respond_small_talk'](question)
        elif intent in HOTEL_INFO:
            return components['answer_hotel_qdrant'](question)
        elif intent in BOOKING:
            st.session_state.in_booking = True
            return "🏨 Rezervasyon yapmak istediğinizi anlıyorum! Size yardımcı olmak için birkaç soru soracağım."
        elif intent in REDIRECT:
            return components['redirect'](question)
        else:
            # Varsayılan olarak hotel bilgisi ver
            return components['answer_hotel_qdrant'](question)
            
    except Exception as e:
        return f"Üzgünüm, bir hata oluştu: {str(e)}"

def main():
    """Ana uygulama"""
    # Başlangıç kontrolleri
    if not setup_environment():
        return
    
    # Qdrant bileşenlerini başlat
    components = initialize_components()
    
    # Sayfa başlığı
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: white; margin: 0;'>🏨 Cullinan Hotel Chatbot</h1>
        <p style='color: #f0f0f0; margin: 5px 0;'>Qdrant Cloud ile Güçlendirilmiş Professional AI Asistan</p>
        <p style='color: #d0d0d0; margin: 0; font-size: 0.9em;'>💡 Gelişmiş vektör veritabanı teknolojisi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Ana layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat header
        st.markdown("### 💬 Profesyonel Sohbet Asistanı")
        
        # Chat container - sabit yükseklik ve scroll
        chat_container = st.container(height=500)
        
        with chat_container:
            # Hoş geldin mesajı - sadece ilk açılışta göster
            if not st.session_state.messages:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown("""
                    **Merhaba! Ben Cullinan Hotel'in Professional AI asistanıyım.** 🏨
                    
                    Size nasıl yardımcı olabilirim?
                    
                    🏨 **Otel hakkında detaylı sorular**  
                    💰 **Fiyat bilgileri ve paket seçenekleri**  
                    📅 **Profesyonel rezervasyon işlemleri**  
                    🍽️ **Restoran ve menü bilgileri**  
                    🏊‍♂️ **SPA ve wellness hizmetleri**  
                    🎯 **Özel etkinlik organizasyonları**
                    
                    *Qdrant Cloud ile güçlendirilmiş gelişmiş yapay zeka teknolojisi kullanıyorum.*
                    """)
            
            # Chat geçmişini göster - en son mesajlar en altta
            for i, message in enumerate(st.session_state.messages):
                avatar = "👤" if message["role"] == "user" else "🤖"
                with st.chat_message(message["role"], avatar=avatar):
                    # Timestamp göster (varsa)
                    if "timestamp" in message and len(st.session_state.messages) > 1:
                        st.caption(f"🕐 {message['timestamp']}")
                    st.write(message["content"])

    with col2:
        # Sistem Durumu - Kompakt görünüm
        st.markdown("### 📊 Sistem Durumu")
        
        # Qdrant bağlantı durumu
        try:
            collections_info = components['qdrant_client'].get_collections()
            st.success(f"🟢 Qdrant Cloud Bağlı ({len(collections_info.collections)} koleksiyon)")
        except Exception as e:
            st.error(f"🔴 Qdrant Bağlantı Hatası")
            st.caption(f"Hata: {str(e)[:50]}...")
        
        # Sohbet İstatistikleri
        st.markdown("### 📈 İstatistikler")
        
        # Metrikler - kompakt
        st.metric("💬 Toplam Mesaj", st.session_state.total_messages)
        st.metric("🎯 Son Intent", st.session_state.current_intent.replace("_", " ").title())
        
        # Booking durumu
        if st.session_state.in_booking:
            st.info("📅 Rezervasyon Modu Aktif")
        
        # Hızlı Aksiyonlar
        st.markdown("### ⚡ Hızlı Aksiyonlar")
        
        # Temizleme butonu
        if st.button("🗑️ Sohbeti Temizle", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.total_messages = 0
            st.session_state.booking_state = {}
            st.session_state.in_booking = False
            st.session_state.current_intent = "unknown"
            st.success("🧹 Sohbet temizlendi!")
            time.sleep(1)
            st.rerun()
        
        # Hızlı sorular
        st.markdown("### 💡 Hızlı Sorular")
        
        quick_questions = [
            "🏨 Otel olanakları nelerdir?",
            "💰 Fiyat listesini göster",
            "📅 Rezervasyon yapmak istiyorum",
            "🍽️ Restoran menüsü",
            "🏊‍♂️ SPA hizmetleri"
        ]
        
        for question in quick_questions:
            if st.button(question, use_container_width=True, key=f"quick_{question}"):
                # Hızlı soruyu otomatik gönder
                st.session_state.messages.append({
                    "role": "user", 
                    "content": question,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                st.session_state.total_messages += 1
                
                # Yanıt üret
                try:
                    intent, confidence = components['classifier'].classify(question)
                    response = get_bot_response(intent, question)
                    st.session_state.current_intent = intent
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Hata: {str(e)}")
        
        # Debug modu - sadece geliştiriciler için
        with st.expander("🔍 Geliştirici Modu"):
            if st.checkbox("Debug Bilgileri Göster"):
                debug_info = {
                    "total_messages": st.session_state.total_messages,
                    "current_intent": st.session_state.current_intent,
                    "in_booking": st.session_state.in_booking,
                    "api_key_set": bool(os.environ.get("OPENAI_API_KEY")),
                    "qdrant_url_set": bool(os.environ.get("QDRANT_URL")),
                    "booking_state": st.session_state.booking_state,
                    "message_count": len(st.session_state.messages)
                }
                st.json(debug_info)

    # Chat input - Modern ve kullanıcı dostu (Sayfanın en altında)
    if prompt := st.chat_input(
        "💬 Mesajınızı yazın... (Örn: Otel hakkında bilgi almak istiyorum)", 
        key="chat_input",
        max_chars=1000
    ):
        # Input validation
        prompt = prompt.strip()
        if not prompt:
            st.warning("⚠️ Lütfen bir mesaj yazın.")
            st.stop()
        
        # Kullanıcı mesajını timestamp ile ekle
        current_time = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": current_time
        })
        st.session_state.total_messages += 1
        
        # Typing indicator göster
        with st.spinner("🤖 Yanıt hazırlanıyor..."):
            try:
                if st.session_state.in_booking:
                    # Booking flow devam ediyor
                    booking_state, response, done = components['handle_booking'](
                        st.session_state.booking_state, prompt
                    )
                    st.session_state.booking_state = booking_state
                    if done:
                        st.session_state.in_booking = False
                        response += "\n\n✅ Rezervasyon süreci tamamlandı!"
                else:
                    # Yeni intent classification
                    intent, confidence = components['classifier'].classify(prompt)
                    response = get_bot_response(intent, prompt)
                    st.session_state.current_intent = intent
                    
                    # Booking başlatılacaksa işaretle
                    if intent == "rezervasyon":
                        st.session_state.in_booking = True
                
                # Bot yanıtını timestamp ile ekle
                response_time = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": response_time
                })
                
            except Exception as e:
                error_msg = f"⚠️ Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.\n\nHata detayı: {str(e)}"
                error_time = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg,
                    "timestamp": error_time
                })
        
        # Sayfayı yenile - en son mesaj görünsün
        st.rerun()

if __name__ == "__main__":
    main()
