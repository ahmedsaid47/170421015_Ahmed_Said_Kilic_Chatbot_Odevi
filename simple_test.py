"""
Basit Qdrant Bağlantı Testi
===========================
"""
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Gerekli değişkenleri kontrol et
print("🔍 Environment variables kontrol ediliyor...")

required_vars = ["OPENAI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✅ {var}: {'*' * 10}")
    else:
        print(f"❌ {var}: Bulunamadı!")

# Qdrant bağlantısını test et
try:
    from qdrant_client import QdrantClient
    
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    
    print(f"\n🌐 Qdrant bağlantısı test ediliyor...")
    print(f"URL: {url}")
    
    client = QdrantClient(
        url=url,
        api_key=api_key,
        timeout=30
    )
    
    # Koleksiyonları listele
    collections = client.get_collections()
    print(f"✅ Bağlantı başarılı!")
    print(f"📁 {len(collections.collections)} koleksiyon bulundu:")
    
    for collection in collections.collections:
        info = client.get_collection(collection.name)
        print(f"   - {collection.name}: {info.points_count} nokta")
    
except Exception as e:
    print(f"❌ Bağlantı hatası: {e}")

print("\n🎯 Test tamamlandı!")
