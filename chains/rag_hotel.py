"""
Otel bilgisi için RAG zinciri – 10 chunk getirir, 4o-mini ile cevabı üretir.
"""
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
import chromadb
import time
import logging
from logging_config import log_api_call

# Logger
logger = logging.getLogger("hotel_chatbot.rag_hotel")

EMBED_MODEL = "text-embedding-3-large"
CHAT_MODEL = "gpt-4o-mini"
client = OpenAI()

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(5))
@log_api_call("OpenAI Embeddings")
def embed(texts: list[str]) -> list[list[float]]:
    """Metinleri embedding vektörlerine dönüştürür"""
    logger.debug(f"Creating embeddings for {len(texts)} texts")
    
    try:
        result = [
            record.embedding
            for record in client.embeddings.create(model=EMBED_MODEL, input=texts).data
        ]
        logger.debug(f"Successfully created {len(result)} embeddings")
        return result
        
    except Exception as e:
        logger.error(f"Failed to create embeddings: {str(e)}", exc_info=True)
        raise

SYSTEM_BASE = """Sen Cullinan Hotel'in akıllı asistanısın. 
Aşağıdaki döküman parçalarından yararlanarak soruları kesin ve doğru biçimde yanıtla.
Yanıtın dostça, kısa ve net olsun. Yalnızca emin olduğun bilgileri paylaş."""

@log_api_call("OpenAI Chat Completion")
def answer_hotel(question: str, hotel_col: chromadb.Collection) -> str:
    """
    Otel hakkındaki soruları RAG kullanarak yanıtlar
    """
    logger.info(f"Processing hotel question", extra={
        'question_length': len(question),
        'collection_name': hotel_col.name
    })
    
    start_time = time.time()
    
    try:
        # 1. Embedding oluştur
        embed_start = time.time()
        q_emb = embed([question])[0]
        embed_time = (time.time() - embed_start) * 1000
        
        # 2. Relevantı dokümanları getir
        retrieval_start = time.time()
        docs = hotel_col.query(query_embeddings=[q_emb], n_results=10)
        chunks = docs["documents"][0]
        retrieval_time = (time.time() - retrieval_start) * 1000
        
        logger.info(f"Retrieved {len(chunks)} document chunks", extra={
            'chunks_found': len(chunks),
            'retrieval_time': retrieval_time,
            'embedding_time': embed_time
        })
        
        # 3. Context oluştur
        context = "\n\n".join(chunks)
        context_length = len(context)
        
        # 4. Chat completion
        generation_start = time.time()
        messages = [
            {"role": "system", "content": SYSTEM_BASE},
            {"role": "system", "content": f"<KONTEKS>\n{context}\n</KONTEKS>"},
            {"role": "user", "content": question},
        ]
        
        completion = client.chat.completions.create(
            model=CHAT_MODEL, 
            messages=messages,
            temperature=0.1,
            max_tokens=500
        )
        
        answer = completion.choices[0].message.content.strip()
        generation_time = (time.time() - generation_start) * 1000
        total_time = (time.time() - start_time) * 1000
        
        # Token kullanımı bilgisi
        usage = completion.usage
        
        logger.info(f"RAG response generated successfully", extra={
            'question': question,
            'answer_length': len(answer),
            'context_length': context_length,
            'chunks_used': len(chunks),
            'embedding_time': embed_time,
            'retrieval_time': retrieval_time,
            'generation_time': generation_time,
            'total_time': total_time,
            'model': CHAT_MODEL,
            'prompt_tokens': usage.prompt_tokens if usage else None,
            'completion_tokens': usage.completion_tokens if usage else None,
            'total_tokens': usage.total_tokens if usage else None
        })
        
        return answer
        
    except Exception as e:
        total_time = (time.time() - start_time) * 1000
        logger.error(f"RAG processing failed: {str(e)}", extra={
            'question': question,
            'execution_time': total_time
        }, exc_info=True)
        
        # Fallback yanıt
        fallback_answer = "Üzgünüm, şu anda bu soruyu yanıtlayamıyorum. Lütfen daha sonra tekrar deneyin veya müşteri hizmetlerimizle iletişime geçin."
        logger.warning(f"Returning fallback answer due to error")
        return fallback_answer

