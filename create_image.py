"""
Placeholder resim oluşturucu
"""
import base64
from pathlib import Path

# SVG formatında basit bir placeholder resim
svg_content = """
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Arka plan -->
  <rect width="800" height="400" fill="url(#grad1)"/>
  
  <!-- Ana başlık -->
  <text x="400" y="120" text-anchor="middle" fill="white" 
        font-family="Arial, sans-serif" font-size="48" font-weight="bold">
    🏨 Cullinan Hotel Chatbot
  </text>
  
  <!-- Alt başlık -->
  <text x="400" y="170" text-anchor="middle" fill="rgba(255,255,255,0.9)" 
        font-family="Arial, sans-serif" font-size="24">
    AI-Powered Hotel Assistant
  </text>
  
  <!-- Chat balonu mockup -->
  <rect x="50" y="220" width="300" height="120" rx="15" fill="white" opacity="0.9"/>
  <text x="70" y="250" fill="#333" font-family="Arial, sans-serif" font-size="16">
    👤 Rezervasyon yapmak istiyorum
  </text>
  <text x="70" y="280" fill="#667eea" font-family="Arial, sans-serif" font-size="16">
    🤖 Tabii ki! Hangi tarih için
  </text>
  <text x="70" y="300" fill="#667eea" font-family="Arial, sans-serif" font-size="16">
    oda rezervasyonu yapmak
  </text>
  <text x="70" y="320" fill="#667eea" font-family="Arial, sans-serif" font-size="16">
    istiyorsunuz?
  </text>
  
  <!-- Özellikler -->
  <rect x="450" y="220" width="300" height="120" rx="15" fill="rgba(255,255,255,0.1)"/>
  <text x="470" y="250" fill="white" font-family="Arial, sans-serif" font-size="18" font-weight="bold">
    Özellikler:
  </text>
  <text x="470" y="275" fill="white" font-family="Arial, sans-serif" font-size="14">
    ✓ OpenAI GPT Integration
  </text>
  <text x="470" y="295" fill="white" font-family="Arial, sans-serif" font-size="14">
    ✓ Streamlit Web Interface
  </text>
  <text x="470" y="315" fill="white" font-family="Arial, sans-serif" font-size="14">
    ✓ Real-time Conversations
  </text>
  
  <!-- Alt bilgi -->
  <text x="400" y="380" text-anchor="middle" fill="rgba(255,255,255,0.7)" 
        font-family="Arial, sans-serif" font-size="14">
    Modern Hotel Experience with AI Technology
  </text>
</svg>
"""

# SVG'yi dosyaya kaydet
with open("resim.png.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Placeholder resim oluşturuldu: resim.png.svg")
print("Bu dosyayı resim.png olarak yeniden adlandırabilir veya PNG formatına çevirebilirsiniz.")
