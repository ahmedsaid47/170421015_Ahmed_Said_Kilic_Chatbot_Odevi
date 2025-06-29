# intent → link eşlemesi tek yerde
import logging

# Logger
logger = logging.getLogger("hotel_chatbot.link_redirect")

LINKS = {
    "rezervasyon_değiştirme": "https://cullinan.com.tr/rezervasyon/değiştir",
    "rezervasyon_iptali":     "https://cullinan.com.tr/rezervasyon/iptal",
    "rezervasyon_durumu":     "https://cullinan.com.tr/rezervasyon/durum",
}

def redirect(intent: str) -> str:
    """
    Belirtilen intent için redirect mesajı oluşturur
    """
    logger.info(f"Processing redirect request", extra={
        'intent': intent,
        'available_intents': list(LINKS.keys())
    })
    
    try:
        if intent not in LINKS:
            logger.warning(f"Unknown redirect intent: {intent}")
            return "Üzgünüm, bu işlem için uygun bir bağlantı bulunamadı. Lütfen müşteri hizmetlerimizle iletişime geçin."
        
        url = LINKS[intent]
        response = f"İlgili işlemi aşağıdaki bağlantıdan yapabilirsiniz:\n{url}"
        
        logger.info(f"Redirect response generated", extra={
            'intent': intent,
            'redirect_url': url,
            'response_length': len(response)
        })
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating redirect response: {str(e)}", extra={
            'intent': intent
        }, exc_info=True)
        
        # Fallback response
        fallback = "Üzgünüm, bu işlem için size yardımcı olamıyorum. Lütfen müşteri hizmetlerimizle iletişime geçin."
        logger.info(f"Returning fallback redirect response")
        return fallback
