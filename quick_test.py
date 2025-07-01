"""
Hızlı Qdrant Test
================
En basit Qdrant bağlantı testi ve intent classification testi.
"""
import os
from dotenv import load_dotenv

# Environment yükle
load_dotenv()

def main():
    print("🔍 Qdrant Quick Test...")
    
    try:
        # 1. Environment kontrol
        required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
        for var in required_vars:
            if not os.getenv(var):
                print(f"❌ {var} eksik!")
                return
        print("✅ Environment variables OK")
        
        # 2. Qdrant bağlantı
        from qdrant_config import get_qdrant_client
        client = get_qdrant_client()
        collections = client.get_collections()
        print(f"✅ Qdrant bağlantısı OK - {len(collections.collections)} koleksiyon")
        
        # 3. Intent classifier test
        from chains.intent_classifier_qdrant import IntentClassifier
        classifier = IntentClassifier()
        
        test_text = "Oda fiyatları nedir?"
        intent, confidence = classifier.classify(test_text)
        print(f"✅ Intent test OK: '{test_text}' -> {intent} (%.2f)" % confidence)
        
        # 4. RAG test
        from chains.rag_hotel_qdrant import answer_hotel_qdrant
        question = "Havuz var mı?"
        answer = answer_hotel_qdrant(question)
        print(f"✅ RAG test OK: '{question}' -> {answer[:50]}...")
        
        print("\n🎉 Tüm testler başarılı! Sistem hazır.")
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    main()
