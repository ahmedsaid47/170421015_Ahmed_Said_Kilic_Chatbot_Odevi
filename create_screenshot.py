from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image():
    # 1200x800 boyutunda resim oluştur
    width, height = 1200, 800
    
    # Gradient background oluştur
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Gradient effect için üstten alta renkler
    for y in range(height):
        ratio = y / height
        r = int(102 + (255 - 102) * ratio)  # 102 -> 255
        g = int(126 + (255 - 126) * ratio)  # 126 -> 255
        b = int(234 + (255 - 234) * ratio)  # 234 -> 255
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    try:
        # Büyük title font
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        text_font = ImageFont.truetype("arial.ttf", 16)
    except:
        # Eğer arial.ttf yoksa default font kullan
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Chatbot interface mockup
    # Header area
    draw.rectangle([(50, 50), (width-50, 120)], fill=(103, 126, 234), outline=(70, 90, 200), width=2)
    draw.text((width//2 - 200, 75), "🏨 Cullinan Hotel Chatbot", font=title_font, fill='white', anchor="mm")
    
    # Chat area mockup
    chat_area = [(70, 140), (width-330, height-100)]
    draw.rectangle(chat_area, fill='white', outline=(200, 200, 200), width=1)
    
    # Sample chat messages
    messages = [
        ("👤 Merhaba! Otel hakkında bilgi alabilir miyim?", 170, (240, 240, 255)),
        ("🤖 Merhaba! Cullinan Hotel'e hoş geldiniz. Size nasıl yardımcı olabilirim?", 220, (245, 255, 245)),
        ("👤 Rezervasyon yapmak istiyorum.", 270, (240, 240, 255)),
        ("🤖 Tabii ki! Hangi tarihler arasında konaklama planlıyorsunuz?", 320, (245, 255, 245)),
    ]
    
    for msg, y_pos, bg_color in messages:
        msg_rect = [(90, y_pos), (width-350, y_pos+35)]
        draw.rectangle(msg_rect, fill=bg_color, outline=(220, 220, 220), width=1)
        draw.text((100, y_pos + 10), msg, font=text_font, fill=(50, 50, 50))
    
    # Sidebar mockup
    sidebar = [(width-300, 140), (width-50, height-100)]
    draw.rectangle(sidebar, fill=(248, 250, 252), outline=(200, 200, 200), width=1)
    
    # Sidebar content
    draw.text((width-290, 160), "Hızlı Aksiyonlar", font=subtitle_font, fill=(70, 90, 200))
    
    quick_actions = [
        "📍 Konum Bilgisi",
        "💰 Fiyat Listesi", 
        "🏊 Otel Olanakları",
        "📞 İletişim",
        "🎯 Rezervasyon"
    ]
    
    for i, action in enumerate(quick_actions):
        y_pos = 200 + i * 40
        action_rect = [(width-290, y_pos), (width-70, y_pos+30)]
        draw.rectangle(action_rect, fill=(103, 126, 234), outline=(70, 90, 200), width=1)
        draw.text((width-280, y_pos + 8), action, font=text_font, fill='white')
    
    # Input area
    input_area = [(70, height-90), (width-330, height-50)]
    draw.rectangle(input_area, fill='white', outline=(103, 126, 234), width=2)
    draw.text((80, height-78), "Mesajınızı yazın...", font=text_font, fill=(150, 150, 150))
    
    # Send button
    send_btn = [(width-320, height-90), (width-270, height-50)]
    draw.rectangle(send_btn, fill=(103, 126, 234), outline=(70, 90, 200), width=1)
    draw.text((width-305, height-75), "Gönder", font=text_font, fill='white')
    
    # Statistics panel
    stats_area = [(width-290, 420), (width-70, 600)]
    draw.rectangle(stats_area, fill='white', outline=(200, 200, 200), width=1)
    draw.text((width-280, 430), "📊 İstatistikler", font=subtitle_font, fill=(70, 90, 200))
    
    stats = [
        "Toplam Sohbet: 1,247",
        "Rezervasyon: 156",
        "Memnuniyet: %94",
        "Yanıt Süresi: 0.8s"
    ]
    
    for i, stat in enumerate(stats):
        draw.text((width-280, 470 + i * 25), stat, font=text_font, fill=(100, 100, 100))
    
    # Footer
    draw.text((width//2, height-20), "Modern AI-Powered Hotel Assistant", font=text_font, fill=(100, 100, 100), anchor="mm")
    
    return img

# Resim oluştur ve kaydet
if __name__ == "__main__":
    img = create_placeholder_image()
    img.save("resim.png", "PNG", quality=95)
    print("Resim başarıyla oluşturuldu: resim.png")
