"""
Qdrant Cloud Koleksiyon Test Aracı
==================================
Bu betik, Qdrant Cloud'daki koleksiyonları test eder ve veri tabanı bağlantısını doğrular.
"""

import sys
import os
import logging
import traceback
from dotenv import load_dotenv

try:
    import openai
    from qdrant_client import QdrantClient
    from qdrant_client.http.models import ScoredPoint
    from qdrant_config import get_qdrant_client, get_collection_name, qdrant_config
except ImportError as e:
    print(f"❌ Gerekli kütüphane eksik: {e}")
    print("Lütfen şu komutu çalıştırın: pip install -r requirements.txt")
    sys.exit(1)

# ---------- Logging ----------
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Env & Clients ----------
def initialize_clients():
    """Ortam değişkenlerini yükler ve OpenAI/Qdrant istemcilerini başlatır."""
    load_dotenv()

    required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Eksik environment variables: {missing_vars}")
        logger.error("❌ Lütfen .env dosyanızı kontrol edin.")
        sys.exit(1)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = qdrant_config.embed_model

    client = get_qdrant_client()
    logger.info("✅ Qdrant ve OpenAI istemcileri başarıyla başlatıldı.")
    return client, model

# ---------- Test Functions ----------

def embed_query(text: str, model: str) -> list[float]:
    """Tek bir metin sorgusunu embed eder."""
    try:
        response = openai.embeddings.create(model=model, input=[text])
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Sorgu embedding hatası: {e}")
        raise

def print_point(point: ScoredPoint, index: int):
    """Bir arama sonucunu okunabilir formatta yazdırır."""
    print(f"    {index+1}. Sonuç (Skor: {point.score:.4f})")
    payload = point.payload
    if payload:
        text = payload.get('text', 'N/A')
        original_id = payload.get('original_id', 'N/A')
        intent = payload.get('intent', None)

        print(f"       - original_id: {original_id}")
        if intent:
            print(f"       - intent     : {intent}")
        print(f"       - text       : {text[:100]}...")

def test_collection(client: QdrantClient, collection_name: str, test_query: str, model: str):
    """Tek bir Qdrant koleksiyonunu test eder."""
    print("-" * 70)
    logger.info(f"🧪 '{collection_name}' koleksiyonu test ediliyor...")

    try:
        # Koleksiyon bilgilerini al
        info = client.get_collection(collection_name=collection_name)
        vector_size = info.config.params.vectors.size
        points_count = info.points_count
        
        print(f"   - Kayıt Sayısı: {points_count}, Vektör Boyutu: {vector_size}")

        if points_count == 0:
            print("   ⚠️ Koleksiyon boş!")
            return

        print(f"\n   - Arama sorgusu: '{test_query}'")
        query_vector = embed_query(test_query, model)
        
        # Arama yap
        response = client.query_points(
            collection_name=collection_name, 
            query=query_vector, 
            limit=3
        )
        search_results = response.points

        if not search_results:
            print("   ⚠️ Hiç sonuç bulunamadı!")
            return

        for i, point in enumerate(search_results):
            print_point(point, i)

    except Exception as e:
        logger.error(f"'{collection_name}' koleksiyonu test edilirken hata: {e}")
        traceback.print_exc()

def list_all_collections(client: QdrantClient):
    """Tüm koleksiyonları listele"""
    try:
        collections = client.get_collections()
        print(f"\n📁 Qdrant Cloud'da {len(collections.collections)} koleksiyon bulundu:")
        
        for collection in collections.collections:
            print(f"   - {collection.name}")
        
        return [col.name for col in collections.collections]
    except Exception as e:
        logger.error(f"Koleksiyonlar listelenirken hata: {e}")
        return []

if __name__ == "__main__":
    logger.info("🚀 Qdrant Cloud test başlıyor...")
    
    try:
        client, model = initialize_clients()
        
        # Tüm koleksiyonları listele
        all_collections = list_all_collections(client)
        
        # Belirli koleksiyonları test et
        test_cases = [
            {
                "collection": get_collection_name("intent"),
                "query": "Oda fiyatlarını öğrenebilir miyim?"
            },
            {
                "collection": get_collection_name("hotel"),
                "query": "Otelinizde evcil hayvan kabul ediliyor mu?"
            }
        ]
        
        for test_case in test_cases:
            collection_name = test_case["collection"]
            test_query = test_case["query"]
            
            if collection_name in all_collections:
                test_collection(client, collection_name, test_query, model)
            else:
                print(f"⚠️ Koleksiyon '{collection_name}' bulunamadı!")
        
        print("-" * 70)
        logger.info("✅ Testler tamamlandı.")
        
        # Özet bilgi
        print(f"\n📊 ÖZET:")
        print(f"   - Embed Model: {model}")
        print(f"   - Qdrant URL: {os.getenv('QDRANT_URL')}")
        print(f"   - Toplam Koleksiyon: {len(all_collections)}")
        
    except Exception as e:
        logger.error(f"💥 Kritik hata: {e}")
        traceback.print_exc()
        sys.exit(1)
