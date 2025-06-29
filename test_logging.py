"""
Cullinan Hotel Chatbot - Logging Sistemi Test Script'i
======================================================
Bu script logging sisteminin doğru çalışıp çalışmadığını test eder.
"""

import sys
import time
import random
from pathlib import Path

# Proje kök dizinini path'e ekle
sys.path.append(str(Path(__file__).parent))

try:
    from logging_config import setup_logging, ChatbotLogger, log_execution_time, log_api_call
    print("✅ Logging modülleri başarıyla import edildi")
except ImportError as e:
    print(f"❌ Import hatası: {e}")
    sys.exit(1)


class MockAPIResponse:
    """API response'u taklit eden mock sınıf"""
    def __init__(self):
        self.usage = type('Usage', (), {
            'prompt_tokens': random.randint(50, 200),
            'completion_tokens': random.randint(20, 100),
            'total_tokens': lambda: self.prompt_tokens + self.completion_tokens
        })()
        self.choices = [type('Choice', (), {
            'message': type('Message', (), {
                'content': "Bu bir test yanıtıdır."
            })()
        })()]


@log_execution_time("test_function")
def test_function_with_timing():
    """Execution time test edilecek fonksiyon"""
    time.sleep(random.uniform(0.1, 0.5))  # Random delay
    return "Test completed successfully"


@log_api_call("Mock API")
def mock_api_call():
    """Mock API çağrısı"""
    time.sleep(random.uniform(0.05, 0.2))
    return MockAPIResponse()


def test_logging_system():
    """Ana test fonksiyonu"""
    print("🧪 Logging Sistemi Test Başlıyor...\n")
    
    # 1. Logging sistemini başlat
    print("1️⃣ Logging sistemi başlatılıyor...")
    try:
        logger = setup_logging(
            app_name="test_chatbot",
            log_level="DEBUG",
            log_dir="logs",
            enable_console=True,
            enable_file=True
        )
        print("✅ Logging sistemi başarıyla başlatıldı")
    except Exception as e:
        print(f"❌ Logging başlatma hatası: {e}")
        return False
    
    # 2. ChatbotLogger test
    print("\n2️⃣ ChatbotLogger test ediliyor...")
    try:
        chatbot_logger = ChatbotLogger("test_logger")
        
        # Test conversation başlat
        request_id = chatbot_logger.start_conversation("Test mesajı")
        print(f"✅ Conversation başlatıldı, Request ID: {request_id[:8]}...")
        
        # Intent classification test
        chatbot_logger.log_intent_classification(
            user_input="Rezervasyon yapmak istiyorum",
            intent="rezervasyon_oluşturma",
            confidence=0.95,
            execution_time=123.45
        )
        print("✅ Intent classification log'u oluşturuldu")
        
        # Booking state test
        chatbot_logger.log_booking_state(
            state={"giris_tarihi": "2024-01-15", "oda_sayisi": 2},
            user_input="2 oda istiyorum",
            is_complete=False
        )
        print("✅ Booking state log'u oluşturuldu")
        
        # Response test
        chatbot_logger.log_response(
            response="Test yanıtı",
            response_type="test_response",
            execution_time=89.12
        )
        print("✅ Response log'u oluşturuldu")
        
        # Error test
        try:
            raise ValueError("Bu bir test hatasıdır")
        except Exception as e:
            chatbot_logger.log_error(e, "test_context", "test input")
            print("✅ Error log'u oluşturuldu")
        
    except Exception as e:
        print(f"❌ ChatbotLogger test hatası: {e}")
        return False
    
    # 3. Decorator test
    print("\n3️⃣ Decorator'lar test ediliyor...")
    try:
        # Execution time decorator test
        result = test_function_with_timing()
        print(f"✅ Execution time decorator test: {result}")
        
        # API call decorator test
        api_result = mock_api_call()
        print("✅ API call decorator test tamamlandı")
        
    except Exception as e:
        print(f"❌ Decorator test hatası: {e}")
        return False
    
    # 4. Log levels test
    print("\n4️⃣ Log level'ları test ediliyor...")
    try:
        logger.debug("Bu bir DEBUG mesajıdır")
        logger.info("Bu bir INFO mesajıdır")
        logger.warning("Bu bir WARNING mesajıdır")
        logger.error("Bu bir ERROR mesajıdır")
        print("✅ Tüm log level'ları test edildi")
    except Exception as e:
        print(f"❌ Log level test hatası: {e}")
        return False
    
    # 5. Performance test
    print("\n5️⃣ Performance test yapılıyor...")
    try:
        for i in range(10):
            chatbot_logger.log_performance(
                operation=f"test_operation_{i}",
                execution_time=random.uniform(50, 500),
                test_metric=random.randint(1, 100)
            )
        print("✅ Performance log'ları oluşturuldu")
    except Exception as e:
        print(f"❌ Performance test hatası: {e}")
        return False
    
    # 6. Log dosyası kontrolü
    print("\n6️⃣ Log dosyaları kontrol ediliyor...")
    try:
        log_dir = Path("logs")
        json_log = log_dir / "test_chatbot.json.log"
        error_log = log_dir / "test_chatbot_errors.log"
        
        if json_log.exists():
            print(f"✅ JSON log dosyası oluşturuldu: {json_log}")
            
            # Dosya içeriğini kontrol et
            with open(json_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"✅ JSON log dosyasında {len(lines)} satır bulundu")
        else:
            print("❌ JSON log dosyası bulunamadı")
            return False
        
        if error_log.exists():
            print(f"✅ Error log dosyası oluşturuldu: {error_log}")
        else:
            print("⚠️ Error log dosyası bulunamadı (normal, hata yoksa oluşmayabilir)")
        
    except Exception as e:
        print(f"❌ Log dosyası kontrol hatası: {e}")
        return False
    
    print("\n🎉 Tüm testler başarıyla tamamlandı!")
    print("\n📊 Test Özeti:")
    print("- Logging sistemi kurulumu: ✅")
    print("- ChatbotLogger functionality: ✅") 
    print("- Decorator'lar: ✅")
    print("- Log level'ları: ✅")
    print("- Performance logging: ✅")
    print("- Log dosyası oluşturma: ✅")
    
    return True


def demo_conversation():
    """Örnek bir chatbot konuşması simüle eder"""
    print("\n🎭 Demo Konuşma Simülasyonu Başlıyor...\n")
    
    chatbot_logger = ChatbotLogger("demo_chatbot")
    
    # Simulated conversation
    conversations = [
        {
            "user_input": "Merhaba!",
            "intent": "selamla",
            "confidence": 0.98,
            "response": "Merhaba! Cullinan Hotel'e hoş geldiniz. Size nasıl yardımcı olabilirim?",
            "response_type": "small_talk"
        },
        {
            "user_input": "Rezervasyon yapmak istiyorum",
            "intent": "rezervasyon_oluşturma", 
            "confidence": 0.95,
            "response": "Tabii ki! Hangi tarihler için rezervasyon yapmak istiyorsunuz?",
            "response_type": "booking_dialog"
        },
        {
            "user_input": "15-20 Ocak arası",
            "intent": "rezervasyon_oluşturma",
            "confidence": 0.87,
            "response": "15-20 Ocak tarihleri not edildi. Kaç kişi için rezervasyon yapacaksınız?",
            "response_type": "booking_dialog"
        }
    ]
    
    for i, conv in enumerate(conversations, 1):
        print(f"👤 {conv['user_input']}")
        
        # Start conversation
        request_id = chatbot_logger.start_conversation(conv['user_input'])
        
        # Log intent classification
        intent_time = random.uniform(100, 300)
        chatbot_logger.log_intent_classification(
            user_input=conv['user_input'],
            intent=conv['intent'],
            confidence=conv['confidence'],
            execution_time=intent_time
        )
        
        # Log response
        response_time = random.uniform(200, 600)
        chatbot_logger.log_response(
            response=conv['response'],
            response_type=conv['response_type'],
            execution_time=response_time
        )
        
        print(f"🤖 {conv['response']}\n")
        time.sleep(1)  # Realistic delay
    
    print("✅ Demo konuşma tamamlandı!")


if __name__ == "__main__":
    print("🏨 Cullinan Hotel Chatbot - Logging System Test")
    print("=" * 60)
    
    # Ana test
    success = test_logging_system()
    
    if success:
        print(f"\n📁 Log dosyalarını kontrol edin: {Path('logs').absolute()}")
        
        # Demo konuşma sorusu
        demo_choice = input("\n🎭 Demo konuşma simülasyonu yapmak ister misiniz? (y/n): ")
        if demo_choice.lower() in ['y', 'yes', 'evet']:
            demo_conversation()
        
        print("\n🔍 Log analizi için şu komutu kullanabilirsiniz:")
        print("python log_analyzer.py --mode analyze --hours 1")
        
    else:
        print("\n❌ Testler başarısız oldu. Lütfen hataları kontrol edin.")
        sys.exit(1)
