"""
Selamlama, veda, teşekkür, yardım mesajlarını 4o-mini ile üretir.
"""
from openai import OpenAI
import time
import logging
from logging_config import log_api_call

# Logger
logger = logging.getLogger("hotel_chatbot.small_talk")

CHAT_MODEL = "gpt-4o-mini-2024-07-18:personal::Bj1i1nW4"
client = OpenAI()

TEMPLATE = """Sen Cullinan Hotel'in nazik sohbet asistanısın. 
Kullanıcının mesajına kısa, sıcak ve samimi bir cevap ver."""

@log_api_call("OpenAI Chat Completion")
def respond_small_talk(user_msg: str) -> str:
    """
    Küçük sohbet mesajlarına yanıt üretir
    """
    logger.info(f"Processing small talk message", extra={
        'message_length': len(user_msg)
    })
    
    start_time = time.time()
    
    try:
        messages = [
            {"role": "system", "content": TEMPLATE},
            {"role": "user", "content": user_msg},
        ]
        
        completion = client.chat.completions.create(
            model=CHAT_MODEL, 
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        response = completion.choices[0].message.content.strip()
        execution_time = (time.time() - start_time) * 1000
        
        # Token kullanımı
        usage = completion.usage
        
        logger.info(f"Small talk response generated", extra={
            'user_message': user_msg,
            'response_length': len(response),
            'execution_time': execution_time,
            'model': CHAT_MODEL,
            'prompt_tokens': usage.prompt_tokens if usage else None,
            'completion_tokens': usage.completion_tokens if usage else None,
            'total_tokens': usage.total_tokens if usage else None
        })
        
        return response
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        logger.error(f"Small talk response generation failed: {str(e)}", extra={
            'user_message': user_msg,
            'execution_time': execution_time
        }, exc_info=True)
        
        # Fallback yanıt
        fallback_responses = [
            "Teşekkür ederim! Size nasıl yardımcı olabilirim?",
            "Merhaba! Cullinan Hotel'e hoş geldiniz.",
            "Size nasıl yardımcı olabilirim?",
            "İyi günler! Sorularınızı bekliyorum."
        ]
        
        import random
        fallback = random.choice(fallback_responses)
        logger.info(f"Returning fallback response: {fallback}")
        return fallback
