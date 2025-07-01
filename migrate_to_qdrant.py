"""
ChromaDB'den Qdrant Cloud'a Veri Aktarım Aracı
============================================
Bu script mevcut ChromaDB verilerini Qdrant Cloud'a aktarır.
"""
import sys
import os
import logging
import traceback
import time
from typing import List, Dict, Any
from pathlib import Path

# Gerekli kütüphaneleri import et
try:
    import chromadb
    from qdrant_client import QdrantClient
    from qdrant_client.http.models import VectorParams, Distance, PointStruct
    from openai import OpenAI
    from dotenv import load_dotenv
    from qdrant_config import get_qdrant_client, get_collection_name, qdrant_config
except ImportError as e:
    print(f"❌ Gerekli kütüphane eksik: {e}")
    print("Lütfen şu komutu çalıştırın: pip install -r requirements.txt")
    sys.exit(1)

# Logging
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_clients():
    """OpenAI ve Qdrant istemcilerini başlat"""
    load_dotenv()
    
    # OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY environment variable required")
    
    openai_client = OpenAI(api_key=openai_key)
    
    # Qdrant
    qdrant_client = get_qdrant_client()
    
    logger.info("✅ OpenAI ve Qdrant istemcileri başlatıldı")
    return openai_client, qdrant_client

def create_embeddings(texts: List[str], openai_client: OpenAI) -> List[List[float]]:
    """Metinleri embedding'e çevir"""
    model = qdrant_config.embed_model
    
    try:
        response = openai_client.embeddings.create(
            model=model,
            input=texts
        )
        return [record.embedding for record in response.data]
    except Exception as e:
        logger.error(f"Embedding oluşturma hatası: {e}")
        raise

def migrate_collection(
    chroma_db_path: str,
    chroma_collection_name: str,
    qdrant_client: QdrantClient,
    qdrant_collection_name: str,
    openai_client: OpenAI
):
    """Tek bir koleksiyonu ChromaDB'den Qdrant'a aktarır"""
    
    logger.info(f"🔄 '{chroma_collection_name}' -> '{qdrant_collection_name}' aktarımı başlıyor...")
    
    try:
        # ChromaDB'den veri oku
        chroma_client = chromadb.PersistentClient(path=chroma_db_path)
        chroma_collection = chroma_client.get_collection(chroma_collection_name)
        
        # Tüm verileri al
        all_data = chroma_collection.get()
        documents = all_data.get('documents', [])
        metadatas = all_data.get('metadatas', [])
        ids = all_data.get('ids', [])
        
        if not documents:
            logger.warning(f"'{chroma_collection_name}' koleksiyonu boş")
            return
        
        logger.info(f"📖 {len(documents)} döküman bulundu")
        
        # Qdrant koleksiyonu oluştur veya kontrol et
        try:
            collection_info = qdrant_client.get_collection(qdrant_collection_name)
            logger.info(f"✅ Qdrant koleksiyonu '{qdrant_collection_name}' mevcut")
        except Exception:
            # Koleksiyon yoksa oluştur
            logger.info(f"🆕 Qdrant koleksiyonu '{qdrant_collection_name}' oluşturuluyor...")
            qdrant_client.create_collection(
                collection_name=qdrant_collection_name,
                vectors_config=qdrant_config.get_vector_params()
            )
        
        # Embedding'leri oluştur (batch halinde)
        batch_size = 100
        total_migrated = 0
        
        for i in range(0, len(documents), batch_size):
            batch_end = min(i + batch_size, len(documents))
            batch_documents = documents[i:batch_end]
            batch_metadatas = metadatas[i:batch_end] if metadatas else [{}] * len(batch_documents)
            batch_ids = ids[i:batch_end]
            
            logger.info(f"📤 Batch {i//batch_size + 1}: {len(batch_documents)} döküman işleniyor...")
            
            # Embedding'leri oluştur
            embeddings = create_embeddings(batch_documents, openai_client)
            
            # Qdrant noktalarını hazırla
            points = []
            for j, (doc, metadata, doc_id, embedding) in enumerate(zip(
                batch_documents, batch_metadatas, batch_ids, embeddings
            )):
                # Payload oluştur
                payload = {
                    "text": doc,
                    "original_id": doc_id
                }
                
                # Metadata'yı ekle
                if metadata:
                    payload.update(metadata)
                
                point = PointStruct(
                    id=hash(doc_id) % (2**63),  # String ID'yi integer'a çevir
                    vector=embedding,
                    payload=payload
                )
                points.append(point)
            
            # Qdrant'a yükle
            qdrant_client.upsert(
                collection_name=qdrant_collection_name,
                points=points
            )
            
            total_migrated += len(points)
            logger.info(f"✅ {total_migrated}/{len(documents)} döküman aktarıldı")
            
            # Kısa bekleme
            time.sleep(0.5)
        
        logger.info(f"🎉 '{chroma_collection_name}' aktarımı tamamlandı! ({total_migrated} döküman)")
        
    except Exception as e:
        logger.error(f"❌ '{chroma_collection_name}' aktarımında hata: {e}")
        traceback.print_exc()

def verify_migration(qdrant_client: QdrantClient, collection_name: str, test_query: str = "test"):
    """Aktarımı doğrula"""
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        point_count = collection_info.points_count
        
        logger.info(f"🔍 '{collection_name}' doğrulaması:")
        logger.info(f"   - Toplam nokta sayısı: {point_count}")
        
        if point_count > 0:
            # Basit arama testi
            from chains.rag_hotel_qdrant import embed_single
            test_vector = embed_single(test_query)
            
            search_result = qdrant_client.query_points(
                collection_name=collection_name,
                query=test_vector,
                limit=3
            )
            
            logger.info(f"   - Arama testi: {len(search_result.points)} sonuç bulundu")
            
            if search_result.points:
                top_result = search_result.points[0]
                logger.info(f"   - En yüksek skor: {top_result.score:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Doğrulama hatası: {e}")
        return False

def main():
    """Ana aktarım işlemi"""
    logger.info("🚀 ChromaDB -> Qdrant Cloud aktarımı başlıyor...")
    
    try:
        # İstemcileri başlat
        openai_client, qdrant_client = initialize_clients()
        
        # Aktarım planı
        migrations = [
            {
                "chroma_db": "./db/intent_db",
                "chroma_collection": "user_intents",
                "qdrant_collection": get_collection_name("intent")
            },
            {
                "chroma_db": "./db/hotel_db", 
                "chroma_collection": "hotel_facts",
                "qdrant_collection": get_collection_name("hotel")
            }
        ]
        
        # Her koleksiyonu aktarır
        for migration in migrations:
            chroma_path = Path(migration["chroma_db"])
            
            if not chroma_path.exists():
                logger.warning(f"⚠️ ChromaDB klasörü bulunamadı: {chroma_path}")
                continue
            
            migrate_collection(
                str(chroma_path),
                migration["chroma_collection"],
                qdrant_client,
                migration["qdrant_collection"],
                openai_client
            )
        
        # Doğrulama
        logger.info("\n🔍 Aktarım doğrulaması yapılıyor...")
        
        for migration in migrations:
            verify_migration(
                qdrant_client,
                migration["qdrant_collection"],
                "test sorgu"
            )
        
        logger.info("\n🎉 Tüm aktarım işlemleri tamamlandı!")
        logger.info("Artık Qdrant Cloud ile test edebilirsiniz:")
        logger.info("  python test_collections.py")
        
    except Exception as e:
        logger.error(f"💥 Kritik hata: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
