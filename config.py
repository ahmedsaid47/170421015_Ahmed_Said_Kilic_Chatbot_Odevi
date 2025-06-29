from pathlib import Path
import os, json
import logging
from logging_config import setup_logging, ChatbotLogger

# Logging sistemini başlat
logger = setup_logging(log_level="INFO")

def load_api_key() -> str:
    """
    OPENAI_API_KEY ortam değişkeni yoksa .env ya da secrets.json dosyalarına bakar.
    """
    logger.info("API key loading started")
    
    try:
        if (key := os.getenv("OPENAI_API_KEY")):
            logger.info("API key loaded from environment variable")
            return key

        # .env dosyasından oku
        env_path = Path(__file__).with_suffix(".env")
        if env_path.exists():
            logger.info("Checking .env file for API key")
            for line in env_path.read_text().splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    logger.info("API key loaded from .env file")
                    return line.split("=", 1)[1].strip()

        # secrets.json ({"OPENAI_API_KEY": "sk-..."})
        secret_path = Path("secrets.json")
        if secret_path.exists():
            logger.info("Checking secrets.json file for API key")
            api_key = json.loads(secret_path.read_text())["OPENAI_API_KEY"]
            logger.info("API key loaded from secrets.json file")
            return api_key

        error_msg = "API anahtarı bulunamadı. OPENAI_API_KEY ortam değişkeni veya .env|secrets.json kullanın."
        logger.error(error_msg)
        raise RuntimeError(error_msg)
        
    except Exception as e:
        logger.error(f"Error loading API key: {str(e)}", exc_info=True)
        raise
