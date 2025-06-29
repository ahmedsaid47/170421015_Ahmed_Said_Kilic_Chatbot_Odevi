"""
Cullinan Hotel Chatbot - Merkezi Logging Konfigürasyonu
========================================================
Bu modül, uygulama genelinde tutarlı ve detaylı log takibi sağlar.

Özellikler:
- Structured logging (JSON format)
- Dosya ve konsol çıktısı
- Log seviyelerine göre filtreleme
- Performance monitoring
- Error tracking ve stack trace
- Request/Response logging
- Otomatik log rotasyonu
"""

import logging
import logging.handlers
import json
import sys
import os
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import uuid


class JSONFormatter(logging.Formatter):
    """JSON formatında log mesajları oluşturur"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread_id': record.thread,
            'process_id': record.process
        }
        
        # Extra alanları ekle
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'user_input'):
            log_data['user_input'] = record.user_input
        if hasattr(record, 'bot_response'):
            log_data['bot_response'] = record.bot_response
        if hasattr(record, 'intent'):
            log_data['intent'] = record.intent
        if hasattr(record, 'confidence'):
            log_data['confidence'] = record.confidence
        if hasattr(record, 'execution_time'):
            log_data['execution_time_ms'] = record.execution_time
        if hasattr(record, 'error_details'):
            log_data['error_details'] = record.error_details
        if hasattr(record, 'state_data'):
            log_data['state_data'] = record.state_data
        
        # Exception bilgilerini ekle
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_data, ensure_ascii=False, default=str)


class ColoredConsoleFormatter(logging.Formatter):
    """Konsol için renkli log formatı"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Temel format
        formatted = f"{color}[{record.levelname}]{reset} "
        formatted += f"{datetime.fromtimestamp(record.created).strftime('%H:%M:%S')} "
        formatted += f"{record.name}:{record.funcName}:{record.lineno} - "
        formatted += f"{record.getMessage()}"
        
        # Extra bilgileri ekle
        extras = []
        if hasattr(record, 'request_id'):
            extras.append(f"req_id={record.request_id[:8]}")
        if hasattr(record, 'intent'):
            extras.append(f"intent={record.intent}")
        if hasattr(record, 'execution_time'):
            extras.append(f"time={record.execution_time}ms")
        
        if extras:
            formatted += f" [{', '.join(extras)}]"
        
        return formatted


def setup_logging(
    app_name: str = "hotel_chatbot",
    log_level: str = "INFO",
    log_dir: str = "logs",
    enable_console: bool = True,
    enable_file: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Merkezi logging konfigürasyonu
    
    Args:
        app_name: Uygulama adı
        log_level: Minimum log seviyesi
        log_dir: Log dosyalarının kaydedileceği dizin
        enable_console: Konsol çıktısını etkinleştir
        enable_file: Dosya çıktısını etkinleştir
        max_bytes: Log dosyası maksimum boyutu
        backup_count: Saklanacak eski log dosyası sayısı
    
    Returns:
        Konfigüre edilmiş logger
    """
    
    # Log dizinini oluştur
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Root logger'ı temizle
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Log seviyesini ayarla
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)
    
    # Dosya handler'ı
    if enable_file:
        json_file_handler = logging.handlers.RotatingFileHandler(
            log_path / f"{app_name}.json.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        json_file_handler.setFormatter(JSONFormatter())
        json_file_handler.setLevel(numeric_level)
        root_logger.addHandler(json_file_handler)
        
        # Hata logları için ayrı dosya
        error_file_handler = logging.handlers.RotatingFileHandler(
            log_path / f"{app_name}_errors.log",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_file_handler.setFormatter(JSONFormatter())
        error_file_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_file_handler)
    
    # Konsol handler'ı
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredConsoleFormatter())
        console_handler.setLevel(numeric_level)
        root_logger.addHandler(console_handler)
    
    # Ana logger'ı döndür
    logger = logging.getLogger(app_name)
    logger.info("Logging system initialized", extra={
        'log_level': log_level,
        'log_dir': str(log_path),
        'console_enabled': enable_console,
        'file_enabled': enable_file
    })
    
    return logger


class ChatbotLogger:
    """Chatbot için özelleştirilmiş logging sınıfı"""
    
    def __init__(self, logger_name: str = "hotel_chatbot"):
        self.logger = logging.getLogger(logger_name)
        self.current_request_id = None
    
    def start_conversation(self, user_input: str) -> str:
        """Yeni bir konuşma başlat ve request ID oluştur"""
        self.current_request_id = str(uuid.uuid4())
        self.logger.info(
            "Conversation started",
            extra={
                'request_id': self.current_request_id,
                'user_input': user_input,
                'event_type': 'conversation_start'
            }
        )
        return self.current_request_id
    
    def log_intent_classification(self, user_input: str, intent: str, confidence: float, execution_time: float):
        """Intent sınıflandırma sonucunu logla"""
        self.logger.info(
            f"Intent classified: {intent}",
            extra={
                'request_id': self.current_request_id,
                'user_input': user_input,
                'intent': intent,
                'confidence': confidence,
                'execution_time': execution_time,
                'event_type': 'intent_classification'
            }
        )
    
    def log_rag_query(self, question: str, chunks_found: int, execution_time: float):
        """RAG sorgu sonucunu logla"""
        self.logger.info(
            f"RAG query processed, found {chunks_found} chunks",
            extra={
                'request_id': self.current_request_id,
                'user_input': question,
                'chunks_found': chunks_found,
                'execution_time': execution_time,
                'event_type': 'rag_query'
            }
        )
    
    def log_booking_state(self, state: Dict[str, Any], user_input: str, is_complete: bool):
        """Rezervasyon durumunu logla"""
        self.logger.info(
            f"Booking state updated, complete: {is_complete}",
            extra={
                'request_id': self.current_request_id,
                'user_input': user_input,
                'state_data': state,
                'booking_complete': is_complete,
                'event_type': 'booking_state_update'
            }
        )
    
    def log_response(self, response: str, response_type: str, execution_time: float):
        """Bot yanıtını logla"""
        self.logger.info(
            f"Response generated: {response_type}",
            extra={
                'request_id': self.current_request_id,
                'bot_response': response,
                'response_type': response_type,
                'execution_time': execution_time,
                'event_type': 'response_generated'
            }
        )
    
    def log_error(self, error: Exception, context: str, user_input: str = None):
        """Hata durumunu logla"""
        error_details = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context
        }
        
        self.logger.error(
            f"Error in {context}: {str(error)}",
            extra={
                'request_id': self.current_request_id,
                'user_input': user_input,
                'error_details': error_details,
                'event_type': 'error'
            },
            exc_info=True
        )
    
    def log_performance(self, operation: str, execution_time: float, **kwargs):
        """Performance metriklerini logla"""
        self.logger.info(
            f"Performance: {operation} completed in {execution_time}ms",
            extra={
                'request_id': self.current_request_id,
                'operation': operation,
                'execution_time': execution_time,
                'event_type': 'performance',
                **kwargs
            }
        )
    
    def log_external_api_call(self, api_name: str, endpoint: str, status_code: int, execution_time: float):
        """Dış API çağrılarını logla"""
        self.logger.info(
            f"External API call: {api_name}",
            extra={
                'request_id': self.current_request_id,
                'api_name': api_name,
                'endpoint': endpoint,
                'status_code': status_code,
                'execution_time': execution_time,
                'event_type': 'external_api_call'
            }
        )


# Decorator fonksiyonları
def log_execution_time(operation_name: str = None):
    """Fonksiyon yürütme süresini logla"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000  # milliseconds
                
                op_name = operation_name or f"{func.__module__}.{func.__name__}"
                logger = logging.getLogger("hotel_chatbot.performance")
                logger.info(
                    f"Function executed successfully: {op_name}",
                    extra={
                        'operation': op_name,
                        'execution_time': execution_time,
                        'event_type': 'function_execution'
                    }
                )
                return result
                
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                logger = logging.getLogger("hotel_chatbot.performance")
                logger.error(
                    f"Function failed: {op_name or func.__name__}",
                    extra={
                        'operation': op_name or func.__name__,
                        'execution_time': execution_time,
                        'error_details': {'type': type(e).__name__, 'message': str(e)},
                        'event_type': 'function_execution_error'
                    },
                    exc_info=True
                )
                raise
        return wrapper
    return decorator


def log_api_call(api_name: str):
    """API çağrılarını logla"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            
            logger = logging.getLogger("hotel_chatbot.api")
            logger.info(
                f"API call started: {api_name}",
                extra={
                    'api_name': api_name,
                    'function': func.__name__,
                    'event_type': 'api_call_start'
                }
            )
            
            try:
                result = func(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000
                
                logger.info(
                    f"API call successful: {api_name}",
                    extra={
                        'api_name': api_name,
                        'execution_time': execution_time,
                        'event_type': 'api_call_success'
                    }
                )
                return result
                
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                logger.error(
                    f"API call failed: {api_name}",
                    extra={
                        'api_name': api_name,
                        'execution_time': execution_time,
                        'error_details': {'type': type(e).__name__, 'message': str(e)},
                        'event_type': 'api_call_error'
                    },
                    exc_info=True
                )
                raise
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test kodu
    logger = setup_logging(log_level="DEBUG")
    chatbot_logger = ChatbotLogger()
    
    # Test mesajları
    request_id = chatbot_logger.start_conversation("Merhaba!")
    chatbot_logger.log_intent_classification("Merhaba!", "selamla", 0.95, 150.2)
    chatbot_logger.log_response("Merhaba! Size nasıl yardımcı olabilirim?", "small_talk", 250.5)
    
    try:
        raise ValueError("Test hatası")
    except Exception as e:
        chatbot_logger.log_error(e, "test_context", "test input")
    
    print(f"Logging test completed. Request ID: {request_id}")
