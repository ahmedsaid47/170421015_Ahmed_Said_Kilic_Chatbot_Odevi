"""
Streamlit Cloud için basitleştirilmiş konfigürasyon
"""
import os
import streamlit as st

def get_openai_api_key():
    """OpenAI API anahtarını al"""
    # Önce ortam değişkenini kontrol et
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        # Streamlit secrets'tan al
        try:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets["OPENAI_API_KEY"]
            else:
                raise ValueError("OpenAI API key not found")
        except Exception:
            raise ValueError("OpenAI API key not configured")
    
    return api_key

class Config:
    """Basit konfigürasyon sınıfı"""
    
    def __init__(self):
        self.openai_api_key = get_openai_api_key()
        self.app_name = "cullinan_hotel_chatbot"
        self.version = "1.0.0"
    
    def get_api_key(self):
        return self.openai_api_key
