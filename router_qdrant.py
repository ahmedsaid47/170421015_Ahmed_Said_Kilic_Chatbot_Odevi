"""
Qdrant Tabanlı Chat Router
========================
Bu modül Qdrant Cloud vektör veritabanını kullanarak chat sistemini yönetir.
"""
from chains.intent_classifier_qdrant import IntentClassifier
from chains.rag_hotel_qdrant import answer_hotel_qdrant
from chains.booking_dialog import handle_booking
from chains.small_talk import respond_small_talk
from chains.link_redirect import redirect
from config import load_api_key
from qdrant_config import get_qdrant_client, get_collection_name
from logging_config import ChatbotLogger
import time
import logging
import sys

import openai, readline  # noqa: F401

# Logging sistemi - sadece bir kez başlat
logging.basicConfig(level=logging.WARNING)  # Sadece warning ve üzeri göster
logger = logging.getLogger("hotel_chatbot.router_qdrant")
logger.setLevel(logging.INFO)

# Global değişkenler - sadece bir kez initialize et
qdrant_client = None
classifier = None
chatbot_logger = None

def initialize_system():
    """Sistemi bir kez başlat"""
    global qdrant_client, classifier, chatbot_logger
    
    if qdrant_client is not None:
        return qdrant_client, classifier, chatbot_logger
    
    print("🚀 Qdrant Chat Router başlatılıyor...")
    
    try:
        # API key
        openai.api_key = load_api_key()
        print("✅ OpenAI API key yüklendi")
        
        # Qdrant client
        qdrant_client = get_qdrant_client()
        print("✅ Qdrant bağlantısı kuruldu")
        
        # Intent classifier
        classifier = IntentClassifier()
        print("✅ Intent classifier hazır")
        
        # Logger
        chatbot_logger = ChatbotLogger()
        print("✅ Logging sistemi hazır")
        
        return qdrant_client, classifier, chatbot_logger
        
    except Exception as e:
        print(f"❌ Sistem başlatma hatası: {e}")
        sys.exit(1)

# Niyet kümeleri
SMALL_TALK   = {"selamla", "veda", "teşekkür", "yardım"}
BOOKING_FLOW = {"fiyat_sorgulama", "rezervasyon_oluşturma"}
LINK_INTENTS = {"rezervasyon_değiştirme", "rezervasyon_iptali", "rezervasyon_durumu"}

def main():
    """Ana chat döngüsü"""
    # Sistem başlat
    qdrant_client, classifier, chatbot_logger = initialize_system()
    
    # Oturum değişkenleri
    booking_state = {}
    in_booking = False
    
    print("\n👋 Cullinan Hotel Asistanına hoş geldiniz!")
    print("💡 Qdrant Cloud ile güçlendirilmiş AI asistan")
    print("📝 Çıkmak için 'quit', 'exit' veya Ctrl+C")
    print("-" * 50)
    
    try:
        while True:
            user = input("\n👤> ").strip()
            
            if not user:
                continue
                
            # Çıkış komutları
            if user.lower() in ['quit', 'exit', 'çıkış', 'bye']:
                print("👋 Görüşmek üzere!")
                break
            
            try:
                # 1) Devam eden rezervasyon akışı
                if in_booking:
                    booking_state, reply, done = handle_booking(booking_state, user)
                    if done:
                        in_booking = False
                        print("✅ Rezervasyon işlemi tamamlandı!")
                    print(f"🤖> {reply}")
                    continue

                # 2) Intent sınıflandırması
                intent, confidence = classifier.classify(user)
                print(f"🎯 Intent: {intent} (%.2f)" % confidence)
                
                # 3) Yanıt üretimi
                if intent in SMALL_TALK:
                    reply = respond_small_talk(user)
                    
                elif intent in BOOKING_FLOW:
                    in_booking = True
                    booking_state, reply, done = handle_booking(booking_state, user)
                    if done:
                        in_booking = False
                        
                elif intent in LINK_INTENTS:
                    reply = redirect(intent)
                    
                else:  # RAG
                    reply = answer_hotel_qdrant(user, qdrant_client)

                print(f"🤖> {reply}")

            except Exception as e:
                print(f"❌ Hata: {str(e)}")
                print("🔄 Lütfen tekrar deneyin.")

    except KeyboardInterrupt:
        print("\n👋 Görüşmek üzere!")
    except Exception as e:
        print(f"\n💥 Kritik hata: {e}")

if __name__ == "__main__":
    main()
