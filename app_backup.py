"""
Cullinan Hotel Assistant - Professional Streamlit Interface
=========================================================
Clean, professional web interface for hotel chatbot
"""

import streamlit as st
import time
import json
from datetime import datetime
from pathlib import Path
import sys

# Proje kök dizinini path'e ekle
sys.path.append(str(Path(__file__).parent))

try:
    from logging_config import setup_logging, ChatbotLogger
    from chains.intent_classifier import IntentClassifier
    from chains.rag_hotel import answer_hotel
    from chains.booking_dialog import handle_booking
    from chains.small_talk import respond_small_talk
    from chains.link_redirect import redirect
    from config import load_api_key
    import chromadb
    import openai
except ImportError as e:
    st.error(f"Import hatası: {e}")
    st.stop()

# Page config
st.set_page_config(
    page_title="Cullinan Hotel Asistanı",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://cullinanhotels.com/destek',
        'Report a bug': 'https://cullinanhotels.com/bug-report',
        'About': """
        # Cullinan Hotel Akıllı Asistanı
        
        Bu asistan size otelle ilgili sorularınızda yardımcı olur:
        - Oda rezervasyonları
        - Otel hizmetleri
        - Fiyat bilgileri
        - Genel sorular
        
        Yapay zeka destekli sistem ile 7/24 hizmetinizdeyiz!
        """
    }
)

# Custom CSS
st.markdown("""
<style>
    /* Ana tema renkleri */
    :root {
        --primary-color: #1f4e79;
        --secondary-color: #f8f9fa;
        --accent-color: #ffd700;
        --text-color: #333333;
        --border-color: #e1e5e9;
    }
    
    /* Header stil */
    .main-header {
        background: linear-gradient(135deg, #1f4e79 0%, #2c5aa0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Chat messages */
    .chat-message {
        margin: 1rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .chat-message.user {
        flex-direction: row-reverse;
    }
    
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .chat-message.user .avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .chat-message.bot .avatar {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1f4e79;
    }
    
    .chat-message .content {
        background: #f8f9fa;
        padding: 1rem 1.25rem;
        border-radius: 18px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .chat-message.user .content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .chat-message.bot .content {
        background: white;
        border: 1px solid var(--border-color);
        color: var(--text-color);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-warning {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    /* Input area */
    .input-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        border: 2px solid var(--border-color);
        margin-top: 1rem;
    }
    
    /* Booking progress */
    .booking-progress {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        color: #666;
        font-style: italic;
    }
    
    .typing-dots {
        display: flex;
        gap: 2px;
    }
    
    .typing-dots span {
        width: 6px;
        height: 6px;
        background: #666;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
    .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { opacity: 0.3; }
        40% { opacity: 1; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .chat-message .content {
            max-width: 85%;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
    }
    
    /* Quick actions */
    .quick-action-btn {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid var(--border-color);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: var(--text-color);
        text-decoration: none;
        display: inline-block;
        margin: 0.25rem;
        transition: all 0.2s ease;
        cursor: pointer;
        font-size: 0.9rem;
    }
    
    .quick-action-btn:hover {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Session state'i başlat"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'booking_state' not in st.session_state:
        st.session_state.booking_state = {}
    
    if 'in_booking' not in st.session_state:
        st.session_state.in_booking = False
    
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    
    if 'total_messages' not in st.session_state:
        st.session_state.total_messages = 0
    
    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = datetime.now()

@st.cache_resource
def initialize_chatbot():
    """Chatbot'u başlat (cache'li)"""
    try:
        # Logging sistemi
        logger = setup_logging(app_name="streamlit_chatbot", log_level="INFO")
        chatbot_logger = ChatbotLogger("streamlit_chatbot")
        
        # OpenAI API
        openai.api_key = load_api_key()
        
        # ChromaDB bağlantıları
        intent_db = chromadb.PersistentClient(path="db/intent_db")
        hotel_db = chromadb.PersistentClient(path="db/hotel_db")
        
        intent_col = intent_db.get_or_create_collection("user_intents")
        hotel_col = hotel_db.get_or_create_collection("hotel_facts")
        
        # Intent classifier
        classifier = IntentClassifier(intent_col)
        
        return {
            'logger': logger,
            'chatbot_logger': chatbot_logger,
            'classifier': classifier,
            'hotel_col': hotel_col,
            'status': 'success'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def display_chat_message(role: str, content: str, metadata: Dict = None):
    """Chat mesajını görüntüle"""
    avatar = "👤" if role == "user" else "🤖"
    css_class = "user" if role == "user" else "bot"
    
    message_html = f"""
    <div class="chat-message {css_class}">
        <div class="avatar">{avatar}</div>
        <div class="content">
            {content}
        </div>
    </div>
    """
    
    st.markdown(message_html, unsafe_allow_html=True)
    
    # Metadata göster (debug için)
    if metadata and st.sidebar.checkbox("Debug Bilgilerini Göster", key=f"debug_{len(st.session_state.messages)}"):
        with st.expander("🔍 Debug Bilgileri"):
            st.json(metadata)

def show_typing_indicator():
    """Typing indicator göster"""
    typing_html = """
    <div class="typing-indicator">
        <span>🤖 Yanıt yazıyor</span>
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    """
    return st.markdown(typing_html, unsafe_allow_html=True)

def process_user_message(user_input: str, chatbot_components: Dict) -> Tuple[str, str, Dict]:
    """Kullanıcı mesajını işle"""
    chatbot_logger = chatbot_components['chatbot_logger']
    classifier = chatbot_components['classifier']
    hotel_col = chatbot_components['hotel_col']
    
    # Request ID oluştur
    request_id = chatbot_logger.start_conversation(user_input)
    
    metadata = {
        'request_id': request_id,
        'timestamp': datetime.now().isoformat(),
        'processing_steps': []
    }
    
    try:
        # Niyet kümeleri
        SMALL_TALK = {"selamla", "veda", "teşekkür", "yardım"}
        BOOKING_FLOW = {"fiyat_sorgulama", "rezervasyon_oluşturma"}
        LINK_INTENTS = {"rezervasyon_değiştirme", "rezervasyon_iptali", "rezervasyon_durumu"}
        
        # Devam eden rezervasyon akışı kontrolü
        if st.session_state.in_booking:
            metadata['processing_steps'].append("Continuing booking flow")
            
            start_time = time.time()
            booking_state, reply, done = handle_booking(st.session_state.booking_state, user_input)
            processing_time = (time.time() - start_time) * 1000
            
            st.session_state.booking_state = booking_state
            chatbot_logger.log_booking_state(booking_state, user_input, done)
            
            if done:
                st.session_state.in_booking = False
                metadata['booking_completed'] = True
            
            metadata['processing_steps'].append(f"Booking dialog processed in {processing_time:.2f}ms")
            metadata['booking_state'] = booking_state
            
            return reply, "booking_dialog", metadata
        
        # Yeni mesajı sınıflandır
        metadata['processing_steps'].append("Classifying intent")
        start_time = time.time()
        intent, confidence = classifier.classify(user_input)
        classification_time = (time.time() - start_time) * 1000
        
        chatbot_logger.log_intent_classification(user_input, intent, confidence, classification_time)
        
        metadata['intent'] = intent
        metadata['confidence'] = confidence
        metadata['classification_time'] = classification_time
        metadata['processing_steps'].append(f"Intent classified as '{intent}' with {confidence:.2f} confidence in {classification_time:.2f}ms")
        
        # Yönlendirme
        start_time = time.time()
        
        if intent in SMALL_TALK:
            metadata['processing_steps'].append("Processing small talk")
            reply = respond_small_talk(user_input)
            response_type = "small_talk"
            
        elif intent in BOOKING_FLOW:
            metadata['processing_steps'].append("Starting booking flow")
            st.session_state.in_booking = True
            booking_state, reply, _ = handle_booking(st.session_state.booking_state, user_input)
            st.session_state.booking_state = booking_state
            chatbot_logger.log_booking_state(booking_state, user_input, False)
            response_type = "booking_dialog"
            metadata['booking_state'] = booking_state
            
        elif intent in LINK_INTENTS:
            metadata['processing_steps'].append("Processing link redirect")
            reply = redirect(intent)
            response_type = "link_redirect"
            
        else:
            metadata['processing_steps'].append("Processing RAG query")
            reply = answer_hotel(user_input, hotel_col)
            response_type = "rag_hotel"
        
        response_time = (time.time() - start_time) * 1000
        chatbot_logger.log_response(reply, response_type, response_time)
        
        metadata['response_type'] = response_type
        metadata['response_time'] = response_time
        metadata['processing_steps'].append(f"Response generated in {response_time:.2f}ms")
        
        return reply, response_type, metadata
        
    except Exception as e:
        chatbot_logger.log_error(e, "streamlit_message_processing", user_input)
        metadata['error'] = str(e)
        metadata['processing_steps'].append(f"Error occurred: {str(e)}")
        
        error_reply = "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
        return error_reply, "error", metadata

def show_quick_actions():
    """Hızlı aksiyon butonları"""
    st.markdown("### 🚀 Hızlı Aksiyonlar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏨 Rezervasyon Yap", use_container_width=True):
            st.session_state.messages.append({
                'role': 'user',
                'content': 'Rezervasyon yapmak istiyorum',
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()
            
        if st.button("💰 Fiyat Bilgisi", use_container_width=True):
            st.session_state.messages.append({
                'role': 'user', 
                'content': 'Oda fiyatları nedir?',
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()
    
    with col2:
        if st.button("🍽️ Restaurant Bilgisi", use_container_width=True):
            st.session_state.messages.append({
                'role': 'user',
                'content': 'Restaurant ve yemek hizmetleri hakkında bilgi verir misiniz?',
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()
            
        if st.button("🏊 Spa & Wellness", use_container_width=True):
            st.session_state.messages.append({
                'role': 'user',
                'content': 'Spa ve wellness hizmetlerinizi öğrenebilir miyim?',
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()

def show_booking_progress():
    """Rezervasyon ilerlemesini göster"""
    if st.session_state.in_booking and st.session_state.booking_state:
        st.markdown("### 📋 Rezervasyon İlerlemesi")
        
        required_fields = [
            ("Check-in Tarihi", "giris_tarihi"),
            ("Check-out Tarihi", "cikis_tarihi"), 
            ("Oda Sayısı", "oda_sayisi"),
            ("Yetişkin Sayısı", "yetiskin_sayisi"),
            ("Çocuk Sayısı", "cocuk_sayisi"),
            ("Çocuk Yaşları", "cocuk_yaslari")
        ]
        
        progress_html = '<div class="booking-progress">'
        completed = 0
        
        for field_name, field_key in required_fields:
            if field_key in st.session_state.booking_state:
                value = st.session_state.booking_state[field_key]
                progress_html += f'<div>✅ <strong>{field_name}:</strong> {value}</div>'
                completed += 1
            else:
                progress_html += f'<div>⏳ <strong>{field_name}:</strong> <em>Bekleniyor...</em></div>'
        
        progress_html += '</div>'
        
        st.markdown(progress_html, unsafe_allow_html=True)
        
        # Progress bar
        progress = completed / len(required_fields)
        st.progress(progress, text=f"İlerleme: {completed}/{len(required_fields)} tamamlandı")

def show_conversation_stats():
    """Konuşma istatistikleri"""
    st.markdown("### 📊 Konuşma İstatistikleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Toplam Mesaj", len(st.session_state.messages))
        st.metric("Rezervasyon Durumu", "Devam Ediyor" if st.session_state.in_booking else "Tamamlandı")
    
    with col2:
        session_duration = datetime.now() - st.session_state.session_start_time
        duration_minutes = int(session_duration.total_seconds() / 60)
        st.metric("Oturum Süresi", f"{duration_minutes} dakika")
        st.metric("Konuşma ID", st.session_state.conversation_id[:8] + "...")

def main():
    """Ana uygulama"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏨 Cullinan Hotel Akıllı Asistanı</h1>
        <p>Size nasıl yardımcı olabilirim? Rezervasyon, oda bilgileri ve daha fazlası...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Session state başlat
    init_session_state()
    
    # Chatbot'u başlat
    with st.spinner("🤖 Asistan hazırlanıyor..."):
        chatbot_components = initialize_chatbot()
    
    if chatbot_components['status'] == 'error':
        st.error(f"❌ Chatbot başlatılamadı: {chatbot_components['error']}")
        st.stop()
    
    # Ana layout
    col_main, col_sidebar = st.columns([2, 1])
    
    with col_main:
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Hoş geldin mesajı
        if not st.session_state.messages:
            st.session_state.messages.append({
                'role': 'assistant',
                'content': """Merhaba! 👋 Cullinan Hotel'e hoş geldiniz! 

Ben sizin akıllı asistanınızım. Size şu konularda yardımcı olabilirim:

🏨 **Rezervasyon işlemleri**
💰 **Oda fiyatları ve paket bilgileri** 
🍽️ **Restaurant ve yemek hizmetleri**
🏊 **Spa, wellness ve aktiviteler**
📍 **Konum ve ulaşım bilgileri**
❓ **Genel sorularınız**

Nasıl yardımcı olabilirim?""",
                'timestamp': datetime.now().isoformat()
            })
        
        # Mesajları göster
        for i, message in enumerate(st.session_state.messages):
            display_chat_message(
                message['role'], 
                message['content'],
                message.get('metadata')
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        
        # Text input
        user_input = st.chat_input(
            placeholder="Mesajınızı buraya yazın... (örn: 'Rezervasyon yapmak istiyorum')",
            key="chat_input"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Mesaj işleme
        if user_input:
            # Kullanıcı mesajını ekle
            st.session_state.messages.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            # Typing indicator
            typing_placeholder = st.empty()
            with typing_placeholder:
                show_typing_indicator()
            
            # Mesajı işle
            response, response_type, metadata = process_user_message(user_input, chatbot_components)
            
            # Typing indicator'ı kaldır
            typing_placeholder.empty()
            
            # Bot yanıtını ekle
            st.session_state.messages.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata
            })
            
            # Sayfa yenile
            st.rerun()
    
    with col_sidebar:
        # Hızlı aksiyonlar
        with st.container():
            show_quick_actions()
        
        st.divider()
        
        # Rezervasyon ilerlemesi
        if st.session_state.in_booking:
            show_booking_progress()
            st.divider()
        
        # Konuşma istatistikleri
        show_conversation_stats()
        
        st.divider()
        
        # Kontrol paneli
        st.markdown("### ⚙️ Kontrol Paneli")
        
        if st.button("🗑️ Konuşmayı Temizle", use_container_width=True):
            st.session_state.messages = []
            st.session_state.booking_state = {}
            st.session_state.in_booking = False
            st.session_state.conversation_id = str(uuid.uuid4())
            st.rerun()
        
        if st.button("📥 Konuşmayı İndir", use_container_width=True):
            conversation_data = {
                'conversation_id': st.session_state.conversation_id,
                'start_time': st.session_state.session_start_time.isoformat(),
                'messages': st.session_state.messages,
                'booking_state': st.session_state.booking_state
            }
            
            st.download_button(
                label="💾 JSON olarak indir",
                data=json.dumps(conversation_data, ensure_ascii=False, indent=2),
                file_name=f"conversation_{st.session_state.conversation_id[:8]}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            <p>🏨 <strong>Cullinan Hotel</strong></p>
            <p>Yapay Zeka Destekli Asistan</p>
            <p><em>v2.0 - 2024</em></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
