"""
Qdrant Cloud Konfigürasyonu - Basit Sürüm
=========================================
"""
import os
import logging
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def get_qdrant_client():
    """Qdrant istemcisini oluşturur ve döndürür"""
    try:
        from qdrant_client import QdrantClient
        
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        
        if not url or not api_key:
            raise ValueError("QDRANT_URL ve QDRANT_API_KEY environment variables gerekli")
        
        client = QdrantClient(
            url=url,
            api_key=api_key,
            prefer_grpc=True,
            grpc_port=6334,
            timeout=30,
            check_compatibility=False
        )
        
        return client
        
    except Exception as e:
        logging.error(f"Qdrant client oluşturulamadı: {e}")
        raise

def get_collection_name(collection_type: str) -> str:
    """Koleksiyon tipine göre isim döndürür"""
    collections = {
        "intent": "intent_collection_1",
        "hotel": "knowledge_collection_2",
        "booking": "booking_collection_3"
    }
    return collections.get(collection_type, f"{collection_type}_collection")

# Basit config sınıfı
class QdrantConfig:
    def __init__(self):
        self.embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        
    def get_vector_size(self) -> int:
        """Embedding model için vektör boyutu"""
        sizes = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536
        }
        return sizes.get(self.embed_model, 1536)

# Global config instance
qdrant_config = QdrantConfig()
