"""
Qdrant Tabanlı Intent Sınıflandırıcısı
=====================================
Bu modül Qdrant Cloud'u kullanarak kullanıcı niyetlerini sınıflandırır.
"""
from typing import Tuple
import time
import logging
import os

# Global client ve cache
_qdrant_client = None
_openai_client = None

def get_openai_client():
    """OpenAI client'ı lazy loading ile al"""
    global _openai_client
    if _openai_client is None:
        try:
            from openai import OpenAI
            _openai_client = OpenAI()
        except Exception as e:
            logging.error(f"OpenAI client oluşturulamadı: {e}")
            raise
    return _openai_client

def get_qdrant_client():
    """Qdrant client'ı lazy loading ile al"""
    global _qdrant_client
    if _qdrant_client is None:
        try:
            from qdrant_client import QdrantClient
            _qdrant_client = QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY"),
                prefer_grpc=True,
                grpc_port=6334,
                timeout=30,
                check_compatibility=False
            )
        except Exception as e:
            logging.error(f"Qdrant client oluşturulamadı: {e}")
            raise
    return _qdrant_client

def embed_single(text: str) -> list[float]:
    """Tek bir metni embed eder"""
    try:
        client = get_openai_client()
        model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        
        response = client.embeddings.create(model=model, input=[text])
        return response.data[0].embedding
        
    except Exception as e:
        logging.error(f"Embedding hatası: {e}")
        raise

class IntentClassifierQdrant:
    def __init__(self, k: int = 3):
        self.k = k
        self.collection_name = "intent_collection_1"  # Sabit koleksiyon adı
        
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Kullanıcı metnini sınıflandırır ve intent + confidence döndürür
        """
        try:
            # 1. Embedding oluştur
            query_embedding = embed_single(text)
            
            # 2. Qdrant'ta arama yap
            client = get_qdrant_client()
            search_result = client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=self.k
            )
            
            # 3. En yüksek skorlu sonucu al
            if not search_result.points:
                return "unknown", 0.0
            
            best_match = search_result.points[0]
            intent = best_match.payload.get('intent', 'unknown') if best_match.payload else 'unknown'
            confidence = float(best_match.score)
            
            return intent, confidence
            
        except Exception as e:
            logging.error(f"Intent classification hatası: {e}")
            return "unknown", 0.0

# Backward compatibility için wrapper
class IntentClassifier:
    """ChromaDB'den Qdrant'a geçiş için backward compatibility wrapper"""
    
    def __init__(self, col=None, k: int = 3):
        # col parametresi artık kullanılmıyor ama backward compatibility için alıyoruz
        self.qdrant_classifier = IntentClassifierQdrant(k=k)
    
    def classify(self, text: str) -> Tuple[str, float]:
        return self.qdrant_classifier.classify(text)
