"""
Cullinan Hotel Chatbot - Qdrant Cloud (Basit Sürüm)
===================================================
"""
import streamlit as st
import openai
import os
from pathlib import Path

# Streamlit config
st.set_page_config(
    page_title="Cullinan Hotel Chatbot",
    page_icon="🏨",
    layout="wide"
)

# Environment setup
def load_environment():
    """Environment variables'ları yükle"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            try:
                if 'OPENAI_API_KEY' in st.secrets:
                    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
            except Exception:
                pass
            
            if not os.getenv("OPENAI_API_KEY"):
                st.error("🔑 OPENAI_API_KEY bulunamadı! Lütfen .env dosyasını kontrol edin.")
                st.stop()
        
        # Qdrant URL
        if not os.getenv("QDRANT_URL"):
            try:
                if 'QDRANT_URL' in st.secrets:
                    os.environ["QDRANT_URL"] = st.secrets["QDRANT_URL"]
            except Exception:
                pass
            
            if not os.getenv("QDRANT_URL"):
                st.error("🔗 QDRANT_URL bulunamadı! Lütfen .env dosyasını kontrol edin.")
                st.stop()
        
        # Qdrant API key  
        if not os.getenv("QDRANT_API_KEY"):
            try:
                if 'QDRANT_API_KEY' in st.secrets:
                    os.environ["QDRANT_API_KEY"] = st.secrets["QDRANT_API_KEY"]
            except Exception:
                pass
            
            if not os.getenv("QDRANT_API_KEY"):
                st.error("🔑 QDRANT_API_KEY bulunamadı! Lütfen .env dosyasını kontrol edin.")
                st.stop()
        
        # OpenAI setup
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        return True
        
    except Exception as e:
        st.error(f"Environment yükleme hatası: {e}")
        return False

@st.cache_resource
def initialize_system():
    """Sistem bileşenlerini başlat"""
    try:
        from chains.intent_classifier_qdrant import IntentClassifier
        from chains.rag_hotel_qdrant import answer_hotel_qdrant
        from chains.booking_dialog import handle_booking
        from chains.small_talk import respond_small_talk
        from chains.link_redirect import redirect
        from qdrant_config import get_qdrant_client
        
        # Components
        qdrant_client = get_qdrant_client()
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
        st.error(f"Sistem başlatma hatası: {e}")
        st.stop()

def get_bot_response(components, intent, question):
    """Bot yanıtını al"""
    try:
        # Intent kategorileri
        SMALL_TALK = {"selamla", "veda", "teşekkür", "yardım"}
        BOOKING_FLOW = {"fiyat_sorgulama", "rezervasyon_oluşturma"}
        LINK_INTENTS = {"rezervasyon_değiştirme", "rezervasyon_iptali", "rezervasyon_durumu"}
        
        if intent in SMALL_TALK:
            return components['respond_small_talk'](question)
        elif intent in BOOKING_FLOW:
            st.session_state.in_booking = True
            booking_state, reply, done = components['handle_booking'](st.session_state.booking_state, question)
            st.session_state.booking_state = booking_state
            if done:
                st.session_state.in_booking = False
            return reply
        elif intent in LINK_INTENTS:
            return components['redirect'](intent)
        else:
            return components['answer_hotel_qdrant'](question, components['qdrant_client'])
            
    except Exception as e:
        return f"Üzgünüm, bir hata oluştu: {str(e)}"

def main():
    """Ana uygulama"""
    
    # Environment yükle
    if not load_environment():
        return
    
    # Session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.booking_state = {}
        st.session_state.in_booking = False
    
    # Sistem başlat
    components = initialize_system()
    
    # UI
    st.title("🏨 Cullinan Hotel Chatbot")
    st.caption("Qdrant Cloud ile güçlendirilmiş AI asistan")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Hoş geldin mesajı
        if not st.session_state.messages:
            welcome = """Merhaba! Ben Cullinan Hotel'in AI asistanıyım. 🏨

Size nasıl yardımcı olabilirim?
• 🏨 Otel hakkında sorular
• 💰 Fiyat bilgileri  
• 📅 Rezervasyon işlemleri
• 🍽️ Restoran ve hizmetler"""
            
            st.chat_message("assistant").write(welcome)
        
        # Chat geçmişi
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    # User input
    if prompt := st.chat_input("Sorunuzu yazın..."):
        # Kullanıcı mesajı
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Bot yanıtı
        try:
            if st.session_state.in_booking:
                # Booking devam ediyor
                booking_state, response, done = components['handle_booking'](st.session_state.booking_state, prompt)
                st.session_state.booking_state = booking_state
                if done:
                    st.session_state.in_booking = False
            else:
                # Yeni intent classification
                intent, confidence = components['classifier'].classify(prompt)
                response = get_bot_response(components, intent, prompt)
            
            # Yanıtı göster
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)
                
        except Exception as e:
            error_msg = f"Hata: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.write(error_msg)
    
    # Sidebar - Sistem durumu
    with st.sidebar:
        st.header("📊 Sistem Durumu")
        
        try:
            collections = components['qdrant_client'].get_collections()
            st.success(f"✅ Qdrant: {len(collections.collections)} koleksiyon")
        except:
            st.error("❌ Qdrant bağlantı hatası")
        
        st.header("🛠️ Kontroller")
        
        if st.button("🗑️ Sohbeti Temizle"):
            st.session_state.messages = []
            st.session_state.booking_state = {}
            st.session_state.in_booking = False
            st.rerun()
        
        st.header("📈 İstatistikler")
        st.metric("Toplam Mesaj", len(st.session_state.messages))

if __name__ == "__main__":
    main()
