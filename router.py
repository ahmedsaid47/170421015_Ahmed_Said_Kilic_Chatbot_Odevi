from chains.intent_classifier import IntentClassifier
from chains.rag_hotel import answer_hotel
from chains.booking_dialog import handle_booking
from chains.small_talk import respond_small_talk
from chains.link_redirect import redirect
from config import load_api_key
from logging_config import ChatbotLogger, log_execution_time
import time
import logging

import chromadb, openai, readline  # noqa: F401

# Logging sistemi
chatbot_logger = ChatbotLogger()
logger = logging.getLogger("hotel_chatbot.router")

logger.info("Router initialization started")

try:
    openai.api_key = load_api_key()
    logger.info("OpenAI API key configured successfully")
except Exception as e:
    logger.error(f"Failed to configure OpenAI API key: {str(e)}", exc_info=True)
    raise

# Chroma bağlantıları
try:
    logger.info("Initializing database connections")
    intent_db = chromadb.PersistentClient(path="db/intent_db")
    hotel_db  = chromadb.PersistentClient(path="db/hotel_db")

    intent_col = intent_db.get_or_create_collection("user_intents")
    hotel_col  = hotel_db.get_or_create_collection("hotel_facts")
    
    logger.info("Database connections established successfully", extra={
        'intent_db_path': 'db/intent_db',
        'hotel_db_path': 'db/hotel_db'
    })
except Exception as e:
    logger.error(f"Failed to initialize database connections: {str(e)}", exc_info=True)
    raise

try:
    classifier = IntentClassifier(intent_col)
    logger.info("Intent classifier initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize intent classifier: {str(e)}", exc_info=True)
    raise

# Niyet kümeleri
SMALL_TALK   = {"selamla", "veda", "teşekkür", "yardım"}
BOOKING_FLOW = {"fiyat_sorgulama", "rezervasyon_oluşturma"}
LINK_INTENTS = {"rezervasyon_değiştirme", "rezervasyon_iptali", "rezervasyon_durumu"}

logger.info("Intent categories configured", extra={
    'small_talk_intents': list(SMALL_TALK),
    'booking_intents': list(BOOKING_FLOW),
    'link_intents': list(LINK_INTENTS)
})

# Oturum değişkenleri
booking_state = {}
in_booking    = False  # akış takipçisi

logger.info("Router initialized successfully, starting chat interface")
print("👋 Cullinan Hotel Asistanına hoş geldiniz! (Çıkmak için Ctrl+C)")

try:
    while True:
        user = input("👤> ").strip()
        if not user:
            continue

        # Her yeni konuşma için request ID oluştur
        request_id = chatbot_logger.start_conversation(user)
        conversation_start_time = time.time()
        
        logger.info(f"Processing user input", extra={
            'request_id': request_id,
            'user_input': user,
            'in_booking_flow': in_booking
        })

        try:
            # 1) Devam eden rezervasyon akışı varsa sınıflandırma atlanır
            if in_booking:
                logger.info("Continuing booking flow", extra={'request_id': request_id})
                booking_start_time = time.time()
                
                booking_state, reply, done = handle_booking(booking_state, user)
                booking_time = (time.time() - booking_start_time) * 1000
                
                chatbot_logger.log_booking_state(booking_state, user, done)
                
                if done:
                    in_booking = False
                    logger.info("Booking flow completed", extra={
                        'request_id': request_id,
                        'final_state': booking_state
                    })
                
                chatbot_logger.log_response(reply, "booking_dialog", booking_time)
                print(f"🤖> {reply}\n")
                continue

            # 2) Yeni mesajı sınıflandır
            classification_start_time = time.time()
            intent, confidence = classifier.classify(user)
            classification_time = (time.time() - classification_start_time) * 1000
            
            chatbot_logger.log_intent_classification(user, intent, confidence, classification_time)

            # 3) Yönlendirme
            response_start_time = time.time()
            response_type = ""
            
            if intent in SMALL_TALK:
                logger.info(f"Processing small talk intent: {intent}", extra={'request_id': request_id})
                reply = respond_small_talk(user)
                response_type = "small_talk"

            elif intent in BOOKING_FLOW:
                logger.info(f"Starting booking flow for intent: {intent}", extra={'request_id': request_id})
                in_booking = True
                booking_state, reply, _ = handle_booking(booking_state, user)
                chatbot_logger.log_booking_state(booking_state, user, False)
                response_type = "booking_dialog"

            elif intent in LINK_INTENTS:
                logger.info(f"Processing link redirect for intent: {intent}", extra={'request_id': request_id})
                reply = redirect(intent)
                response_type = "link_redirect"

            else:  # RAG
                logger.info(f"Processing RAG query for intent: {intent}", extra={'request_id': request_id})
                rag_start_time = time.time()
                reply = answer_hotel(user, hotel_col)
                rag_time = (time.time() - rag_start_time) * 1000
                chatbot_logger.log_rag_query(user, 10, rag_time)  # Assuming 10 chunks as default
                response_type = "rag_hotel"

            response_time = (time.time() - response_start_time) * 1000
            total_time = (time.time() - conversation_start_time) * 1000
            
            chatbot_logger.log_response(reply, response_type, response_time)
            chatbot_logger.log_performance("full_conversation", total_time, 
                                         intent=intent, 
                                         confidence=confidence,
                                         response_type=response_type)

            print(f"🤖> {reply}\n")

        except Exception as e:
            error_time = (time.time() - conversation_start_time) * 1000
            chatbot_logger.log_error(e, "message_processing", user)
            
            error_reply = "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
            chatbot_logger.log_response(error_reply, "error_response", error_time)
            print(f"🤖> {error_reply}\n")
            
            logger.error(f"Error processing user input: {str(e)}", extra={
                'request_id': request_id,
                'user_input': user,
                'execution_time': error_time
            }, exc_info=True)

except KeyboardInterrupt:
    logger.info("Chat session ended by user (Ctrl+C)")
    print("\n👋 Görüşmek üzere!")
except Exception as e:
    logger.critical(f"Critical error in main chat loop: {str(e)}", exc_info=True)
    print("\n💥 Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.")
