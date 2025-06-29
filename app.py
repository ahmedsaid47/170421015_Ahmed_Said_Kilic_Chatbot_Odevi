"""
Cullinan Hotel Chatbot - Streamlit Web Arayüzü
==============================================
Modern ve kullanıcı dostu web arayüzü ile hotel chatbot'u
"""

import streamlit as st
import time
import json
import uuid
from datetime import datetime
from pathlib import Path
import sys
import asyncio
from typing import Dict, Any, List, Tuple

# Add project root to path
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
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Cullinan Hotel Assistant",
    page_icon="⬜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global variables */
    :root {
        --primary: #2563eb;
        --primary-light: #3b82f6;
        --secondary: #f8fafc;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border: #e2e8f0;
        --success: #059669;
        --warning: #d97706;
        --error: #dc2626;
        --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Reset default Streamlit styling */
    .main {
        padding-top: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Main header */
    .main-header {
        background: var(--gradient);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.025em;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0;
        overflow: hidden;
        height: 600px;
        display: flex;
        flex-direction: column;
    }
    
    .chat-messages {
        flex: 1;
        padding: 1.5rem;
        overflow-y: auto;
        background: #fafafa;
    }
    
    /* Chat message styling */
    .message {
        display: flex;
        margin-bottom: 1rem;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .message.user {
        flex-direction: row-reverse;
    }
    
    .message-content {
        max-width: 70%;
        padding: 0.875rem 1.125rem;
        border-radius: 1rem;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .message.user .message-content {
        background: var(--gradient);
        color: white;
        border-bottom-right-radius: 0.25rem;
    }
    
    .message.assistant .message-content {
        background: white;
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-bottom-left-radius: 0.25rem;
    }
    
    /* Input area */
    .chat-input {
        border-top: 1px solid var(--border);
        padding: 1rem 1.5rem;
        background: white;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: white;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Status indicators */
    .status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .status.active {
        background: #dcfce7;
        color: var(--success);
        border: 1px solid #bbf7d0;
    }
    
    .status.booking {
        background: #fef3c7;
        color: var(--warning);
        border: 1px solid #fde68a;
    }
    
    /* Quick actions */
    .quick-action {
        display: block;
        width: 100%;
        padding: 0.625rem;
        margin-bottom: 0.5rem;
        background: white;
        border: 1px solid var(--border);
        border-radius: 6px;
        color: var(--text-secondary);
        text-decoration: none;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .quick-action:hover {
        border-color: var(--primary-light);
        color: var(--primary);
        background: #f8fafc;
    }
    
    /* Metrics */
    .metric {
        text-align: center;
        padding: 0.75rem;
        background: #f8fafc;
        border-radius: 6px;
        border: 1px solid var(--border);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .message-content {
            max-width: 85%;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .chat-container {
            height: 500px;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_chatbot():
    """Initialize chatbot components (cached)"""
    try:
        # Setup logging
        logger = setup_logging(app_name="streamlit_chatbot", log_level="INFO")
        chatbot_logger = ChatbotLogger("streamlit_chatbot")
        
        # Configure OpenAI
        openai.api_key = load_api_key()
        
        # Initialize databases
        intent_db = chromadb.PersistentClient(path="db/intent_db")
        hotel_db = chromadb.PersistentClient(path="db/hotel_db")
        
        intent_col = intent_db.get_or_create_collection("user_intents")
        hotel_col = hotel_db.get_or_create_collection("hotel_facts")
        
        # Initialize classifier
        classifier = IntentClassifier(intent_col)
        
        return {
            'logger': logger,
            'chatbot_logger': chatbot_logger,
            'classifier': classifier,
            'hotel_col': hotel_col,
            'status': 'success'
        }
        
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def init_session_state():
    """Initialize session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'booking_state' not in st.session_state:
        st.session_state.booking_state = {}
    if 'in_booking' not in st.session_state:
        st.session_state.in_booking = False
    if 'total_messages' not in st.session_state:
        st.session_state.total_messages = 0

def process_message(user_input: str, components: dict) -> str:
    """Process user message and return response"""
    try:
        classifier = components['classifier']
        hotel_col = components['hotel_col']
        chatbot_logger = components['chatbot_logger']
        
        # Intent categories
        SMALL_TALK = {"selamla", "veda", "teşekkür", "yardım"}
        BOOKING_FLOW = {"fiyat_sorgulama", "rezervasyon_oluşturma"}
        LINK_INTENTS = {"rezervasyon_değiştirme", "rezervasyon_iptali", "rezervasyon_durumu"}
        
        # Handle ongoing booking flow
        if st.session_state.in_booking:
            booking_state, reply, done = handle_booking(st.session_state.booking_state, user_input)
            st.session_state.booking_state = booking_state
            
            if done:
                st.session_state.in_booking = False
                reply += "\n\nReservation process completed."
            
            return reply
        
        # Classify intent
        intent, confidence = classifier.classify(user_input)
        
        # Route to appropriate handler
        if intent in SMALL_TALK:
            return respond_small_talk(intent, user_input)
        elif intent in BOOKING_FLOW:
            st.session_state.in_booking = True
            booking_state, reply, done = handle_booking({}, user_input)
            st.session_state.booking_state = booking_state
            return reply
        elif intent in LINK_INTENTS:
            return redirect(intent)
        else:
            return answer_hotel(user_input, hotel_col)
            
    except Exception as e:
        return f"I apologize, but an error occurred: {str(e)}"

# Initialize components
init_session_state()
components = initialize_chatbot()

if components['status'] == 'error':
    st.error(f"Failed to initialize chatbot: {components['error']}")
    st.stop()

# Main header
st.markdown("""
<div class="main-header">
    <h1>Cullinan Hotel Assistant</h1>
    <p>Professional AI assistant for hotel services and reservations</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([4, 1])

with col1:
    # Chat interface
    st.markdown("""
    <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        role_class = "user" if message["role"] == "user" else "assistant"
        st.markdown(f"""
        <div class="message {role_class}">
            <div class="message-content">
                {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.total_messages += 1
        
        # Process and add response
        with st.spinner("Processing..."):
            response = process_message(prompt, components)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col2:
    # System status
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">System Status</div>', unsafe_allow_html=True)
    
    if st.session_state.in_booking:
        st.markdown('<div class="status booking">Booking in Progress</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status active">Ready</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Quick Actions</div>', unsafe_allow_html=True)
    
    quick_actions = [
        "Hello, can you help me?",
        "I want to make a reservation",
        "What are your room rates?",
        "Tell me about hotel amenities",
        "Check reservation status"
    ]
    
    for action in quick_actions:
        if st.button(action, key=f"action_{action[:20]}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": action})
            st.session_state.total_messages += 1
            response = process_message(action, components)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Statistics</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{len(st.session_state.messages)}</div>
            <div class="metric-label">Messages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{user_messages}</div>
            <div class="metric-label">Queries</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Controls
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Controls</div>', unsafe_allow_html=True)
    
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.booking_state = {}
        st.session_state.in_booking = False
        st.rerun()
    
    # Debug toggle
    show_debug = st.checkbox("Show Debug Info")
    
    if show_debug and st.session_state.booking_state:
        st.json(st.session_state.booking_state)
    
    st.markdown('</div>', unsafe_allow_html=True)
