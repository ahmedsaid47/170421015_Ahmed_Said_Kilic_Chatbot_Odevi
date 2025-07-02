"""
Qdrant Tabanlı RAG Sistemi - Otel bilgisi için RAG zinciri
========================================================
Bu modül Qdrant Cloud vektör veritabanını kullanarak otel hakkındaki soruları yanıtlar.
"""
import time
import logging
import os

# Global client'ları cache için
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

SYSTEM_BASE = """Sen Cullinan Hotel'in akıllı asistanısın. 
Aşağıdaki döküman parçalarından yararlanarak soruları kesin ve doğru biçimde yanıtla.
Yanıtın dostça, kısa ve net olsun. Yalnızca emin olduğun bilgileri paylaş."""

def answer_hotel_qdrant(question: str, qdrant_client=None) -> str:
    """
    Qdrant Cloud kullanarak otel hakkındaki soruları RAG ile yanıtlar
    """
    if qdrant_client is None:
        qdrant_client = get_qdrant_client()
    
    collection_name = "knowledge_collection_2"  # Sabit koleksiyon adı
    
    try:
        # 1. Embedding oluştur
        q_emb = embed_single(question)
        
        # 2. Qdrant'tan relevantı dokümanları getir
        search_result = qdrant_client.query_points(
            collection_name=collection_name,
            query=q_emb,
            limit=10
        )
        
        # 3. Sonuçları işle
        chunks = []
        for point in search_result.points:
            if point.payload and 'text' in point.payload:
                chunks.append(point.payload['text'])
        
        if not chunks:
            return "Üzgünüm, bu konuda yeterli bilgim bulunmuyor. Lütfen farklı bir soru sorabilir misiniz?"
        
        # 4. Context oluştur
        context = "\n\n".join(chunks)
        
        # 5. Chat completion
        client = get_openai_client()
        messages = [
            {"role": "system", "content": SYSTEM_BASE},
            {"role": "system", "content": f"<KONTEKS>\n{context}\n</KONTEKS>"},
            {"role": "user", "content": question},
        ]
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18:personal::Bj1i1nW4", 
            messages=messages,
            temperature=0.1,
            max_tokens=500
        )
        
        answer = completion.choices[0].message.content.strip()
        return answer
        
    except Exception as e:
        logging.error(f"RAG hatası: {e}")
        return "Üzgünüm, şu anda sorunuzu yanıtlayamıyorum. Lütfen daha sonra tekrar deneyin."

# Backward compatibility için alias
answer_hotel = answer_hotel_qdrant
