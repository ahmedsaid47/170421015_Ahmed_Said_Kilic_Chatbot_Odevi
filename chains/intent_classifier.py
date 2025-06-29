"""
Basit gömme tabanlı niyet sınıflandırıcısı.
Intent koleksiyonundaki her satır:
    {"id": "...", "metadata": {"intent": "selamla"}, "documents": ["Merhaba", "Selam", ...]}
"""
from typing import Tuple
import chromadb
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
import time
import logging
from logging_config import log_api_call

# Logger
logger = logging.getLogger("hotel_chatbot.intent_classifier")

EMBED_MODEL = "text-embedding-3-large"
client = OpenAI()

# kronik ağ hatalarına karşı tekrar dene
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(5))
@log_api_call("OpenAI Embeddings")
def embed(texts: list[str]) -> list[list[float]]:
    """
    Metinleri embedding vektörlerine dönüştürür
    """
    logger.debug(f"Creating embeddings for {len(texts)} texts")
    start_time = time.time()
    
    try:
        result = [
            record.embedding
            for record in client.embeddings.create(model=EMBED_MODEL, input=texts).data
        ]
        
        execution_time = (time.time() - start_time) * 1000
        logger.info(f"Embeddings created successfully", extra={
            'text_count': len(texts),
            'execution_time': execution_time,
            'model': EMBED_MODEL
        })
        
        return result
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        logger.error(f"Failed to create embeddings: {str(e)}", extra={
            'text_count': len(texts),
            'execution_time': execution_time,
            'model': EMBED_MODEL
        }, exc_info=True)
        raise

class IntentClassifier:
    def __init__(self, col: chromadb.Collection, k: int = 3):
        self.col = col
        self.k = k
        logger.info(f"IntentClassifier initialized", extra={
            'collection_name': col.name,
            'k_value': k
        })

    def classify(self, user_msg: str) -> Tuple[str, float]:
        """En benzer k satırı getirip oy çokluğuna göre etiket döner."""
        logger.debug(f"Classifying user message", extra={
            'message_length': len(user_msg),
            'k_value': self.k
        })
        
        start_time = time.time()
        
        try:
            # Embedding oluştur
            embed_start = time.time()
            query_emb = embed([user_msg])[0]
            embed_time = (time.time() - embed_start) * 1000
            
            # Veritabanından benzer örnekleri getir
            db_start = time.time()
            res = self.col.query(query_embeddings=[query_emb], n_results=self.k)
            db_time = (time.time() - db_start) * 1000
            
            # Sonuçları analiz et
            intents = [m["intent"] for m in res["metadatas"][0]]
            distances = res["distances"][0]
            
            if not intents:
                logger.warning("No intents found in classification results")
                return "unknown", 1.0
            
            # Oy sayma
            winners = max(set(intents), key=intents.count)
            score = distances[intents.index(winners)]
            
            total_time = (time.time() - start_time) * 1000
            
            logger.info(f"Intent classification completed", extra={
                'user_message': user_msg,
                'predicted_intent': winners,
                'confidence_score': score,
                'found_intents': intents,
                'distances': distances,
                'embedding_time': embed_time,
                'database_time': db_time,
                'total_time': total_time,
                'k_results': len(intents)
            })
            
            return winners, score
            
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            logger.error(f"Intent classification failed: {str(e)}", extra={
                'user_message': user_msg,
                'execution_time': total_time
            }, exc_info=True)
            
            # Fallback döndür
            return "unknown", 1.0
