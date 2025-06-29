"""
chains/booking_dialog.py
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
(⇽ önceki sürümden fark: _llm_enrich_state içinde 'reply' inşası)
"""
from __future__ import annotations
from typing import Dict, Any, Tuple, List
from datetime import datetime
from urllib.parse import urlencode, quote_plus
import re
import time
import logging
from openai import OpenAI
from logging_config import log_api_call

# Logger
logger = logging.getLogger("hotel_chatbot.booking_dialog")

CHAT_MODEL = "gpt-4o-mini"
client = OpenAI()

HOTEL_ID   = 114738
DOMAIN     = "www.cullinanhotels.com"
LANGUAGEID = 1
ANCHOR     = "guestsandrooms"

REQ = [
    "giris_tarihi",
    "cikis_tarihi",
    "oda_sayisi",
    "yetiskin_sayisi",
    "cocuk_sayisi",
    "cocuk_yaslari",
]

SYSTEM_PROMPT = """
Sen Cullinan Hotel'in rezervasyon asistanısın.
Aşağıda "state" sözlüğünde eksik alanları sırayla ve net sorularla tamamla.
• Gereken alanlar → giris_tarihi, cikis_tarihi (YYYY-MM-DD),
  oda_sayisi, yetiskin_sayisi, cocuk_sayisi, cocuk_yaslari (örn: 8,5)
• İlk satır her zaman KULLANICIYA GÖRÜNECEK mesajdır.
• Mesajın alt satırlarında bulduğun bilgileri `alan=deger` biçiminde ekle.
• Tarihleri mutlaka `YYYY-MM-DD` formatında döndür. 
"""

MONTHS_TR_EN = {
    "Ocak": "January",   "Şubat": "February", "Mart": "March",
    "Nisan": "April",    "Mayıs": "May",      "Haziran": "June",
    "Temmuz": "July",    "Ağustos": "August", "Eylül": "September",
    "Ekim": "October",   "Kasım": "November", "Aralık": "December",
}

_date_num_pat = re.compile(r"\d+")

# —————————————————— Yardımcı fonksiyonlar ——————————————————
def _tr_to_en_month(text: str) -> str:
    for tr, en in MONTHS_TR_EN.items():
        text = re.sub(rf"\b{tr}\b", en, text, flags=re.IGNORECASE)
    return text

def _normalize_date(text: str) -> str | None:
    """Tarih string'ini YYYY-MM-DD formatına dönüştürür"""
    text = text.strip()
    logger.debug(f"Normalizing date: {text}")
    
    try:
        if "-" in text:
            normalized = datetime.strptime(text, "%Y-%m-%d").date().isoformat()
            logger.debug(f"Date normalized from ISO format: {text} -> {normalized}")
            return normalized
        if "/" in text:
            normalized = datetime.strptime(text, "%d/%m/%Y").date().isoformat()
            logger.debug(f"Date normalized from dd/mm/yyyy format: {text} -> {normalized}")
            return normalized
        eng = _tr_to_en_month(text)
        normalized = datetime.strptime(eng, "%d %B %Y").date().isoformat()
        logger.debug(f"Date normalized from Turkish format: {text} -> {normalized}")
        return normalized
    except ValueError as e:
        logger.warning(f"Failed to normalize date '{text}': {str(e)}")
        return None

def _ints_in(t: str) -> List[int]:
    """String içindeki tüm sayıları bulur"""
    numbers = list(map(int, _date_num_pat.findall(t)))
    logger.debug(f"Extracted numbers from '{t}': {numbers}")
    return numbers

def build_url(
    hotel_id: int,
    date_in: str,
    date_out: str,
    adults: int,
    child_ages: list[int],
    rooms: int = 1,
    domain: str = DOMAIN,
    languageid: int = LANGUAGEID,
    anchor: str = ANCHOR,
    extra: dict | None = None,
) -> str:
    """Rezervasyon URL'si oluşturur"""
    def _fmt(d: str) -> str:
        if "/" in d:
            return d
        return datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d/%Y")

    params = {
        "adults": adults,
        "datein": _fmt(date_in),
        "dateout": _fmt(date_out),
        "rooms": rooms,
        "domain": domain,
        "languageid": languageid,
    }
    if child_ages:
        params.update({"children": len(child_ages),
                       "childage": ",".join(f"{a:02d}" for a in child_ages)})
    if extra:
        params.update(extra)

    url = f"https://bookings.travelclick.com/{hotel_id}?{urlencode(params, quote_via=quote_plus)}#/{anchor}"
    
    logger.info(f"Booking URL generated", extra={
        'hotel_id': hotel_id,
        'check_in': date_in,
        'check_out': date_out,
        'adults': adults,
        'children': len(child_ages),
        'child_ages': child_ages,
        'rooms': rooms,
        'url_length': len(url)
    })
    
    return url

# —————————————————— State güncelleme ——————————————————
def _update_state_regex(state: Dict[str, Any], user_msg: str) -> Dict[str, Any]:
    """Regex kullanarak state'i günceller"""
    logger.debug(f"Updating state with regex for message: {user_msg}")
    initial_state = state.copy()
    
    if "giris_tarihi" not in state:
        if d := _normalize_date(user_msg):
            state["giris_tarihi"] = d
            logger.info(f"Check-in date extracted: {d}")
    elif "cikis_tarihi" not in state:
        if d := _normalize_date(user_msg):
            state["cikis_tarihi"] = d
            logger.info(f"Check-out date extracted: {d}")

    nums = _ints_in(user_msg)
    if nums:
        if "oda_sayisi" not in state:
            state["oda_sayisi"] = nums.pop(0)
            logger.info(f"Room count extracted: {state['oda_sayisi']}")
        if nums and "yetiskin_sayisi" not in state:
            state["yetiskin_sayisi"] = nums.pop(0)
            logger.info(f"Adult count extracted: {state['yetiskin_sayisi']}")
        if nums and "cocuk_sayisi" not in state:
            state["cocuk_sayisi"] = nums.pop(0)
            logger.info(f"Child count extracted: {state['cocuk_sayisi']}")

    ages = [int(a) for a in user_msg.split(",") if a.strip().isdigit()]
    if ages and "cocuk_yaslari" not in state:
        state["cocuk_yaslari"] = ages
        logger.info(f"Child ages extracted: {ages}")

    # State değişikliklerini logla
    changes = {}
    for key, value in state.items():
        if key not in initial_state or initial_state[key] != value:
            changes[key] = value
    
    if changes:
        logger.info(f"State updated via regex", extra={'changes': changes})

    return state

# —————————————————— LLM enrich ——————————————————
@log_api_call("OpenAI Chat Completion")
def _llm_enrich_state(state: Dict[str, Any], user_msg: str) -> Tuple[Dict[str, Any], str]:
    """LLM kullanarak state'i zenginleştirir"""
    logger.info(f"Enriching state with LLM", extra={
        'current_state': state,
        'user_message': user_msg
    })
    
    start_time = time.time()
    
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"state={state}"},
            {"role": "user",   "content": user_msg},
        ]
        
        completion = client.chat.completions.create(
            model=CHAT_MODEL, 
            messages=messages,
            temperature=0.1,
            max_tokens=300
        )
        
        raw = completion.choices[0].message.content.strip()
        execution_time = (time.time() - start_time) * 1000
        
        logger.debug(f"LLM raw response: {raw}")

        lines = [ln.rstrip() for ln in raw.splitlines() if ln.strip()]
        # Kullanıcıya gösterilecek satırlar: "=" içermeyenler
        visible = [ln for ln in lines if "=" not in ln]
        reply   = "\n".join(visible) if visible else lines[0]

        # State güncelle
        initial_state = state.copy()
        extracted_fields = {}
        
        for ln in lines:
            if "=" not in ln:
                continue
            k, v = map(str.strip, ln.split("=", 1))
            match k:
                case "giris_tarihi" | "cikis_tarihi":
                    if norm := _normalize_date(v):
                        state[k] = norm
                        extracted_fields[k] = norm
                case "oda_sayisi" | "yetiskin_sayisi" | "cocuk_sayisi":
                    if v.isdigit():
                        state[k] = int(v)
                        extracted_fields[k] = int(v)
                case "cocuk_yaslari":
                    ages = [int(a) for a in _ints_in(v)]
                    state[k] = ages
                    extracted_fields[k] = ages

        # Token kullanımı
        usage = completion.usage
        
        logger.info(f"LLM state enrichment completed", extra={
            'execution_time': execution_time,
            'extracted_fields': extracted_fields,
            'reply_length': len(reply),
            'prompt_tokens': usage.prompt_tokens if usage else None,
            'completion_tokens': usage.completion_tokens if usage else None,
            'total_tokens': usage.total_tokens if usage else None
        })
        
        return state, reply
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        logger.error(f"LLM state enrichment failed: {str(e)}", extra={
            'execution_time': execution_time,
            'user_message': user_msg,
            'current_state': state
        }, exc_info=True)
        
        # Fallback reply
        fallback_reply = "Üzgünüm, bilgilerinizi işlerken bir sorun yaşadım. Lütfen tekrar deneyin."
        return state, fallback_reply

# —————————————————— Dışa açık fonksiyon ——————————————————
def handle_booking(
    state: Dict[str, Any],
    user_msg: str,
) -> Tuple[Dict[str, Any], str, bool]:
    """
    Rezervasyon diyaloğunu yönetir
    """
    logger.info(f"Handling booking dialog", extra={
        'current_state_keys': list(state.keys()),
        'user_message': user_msg,
        'missing_fields': [k for k in REQ if k not in state]
    })
    
    start_time = time.time()
    
    try:
        # Regex ile state güncelle
        state = _update_state_regex(state, user_msg)
        missing = [k for k in REQ if k not in state]

        logger.debug(f"After regex update, missing fields: {missing}")

        if missing:
            # LLM ile zenginleştir
            state, reply = _llm_enrich_state(state, user_msg)
            execution_time = (time.time() - start_time) * 1000
            
            logger.info(f"Booking dialog incomplete", extra={
                'execution_time': execution_time,
                'remaining_fields': [k for k in REQ if k not in state],
                'response_type': 'continue_dialog'
            })
            
            return state, reply, False

        # Tüm alanlar tamamlandı - URL oluştur
        child_ages = (
            state["cocuk_yaslari"]
            if isinstance(state["cocuk_yaslari"], list)
            else [int(a) for a in _ints_in(str(state["cocuk_yaslari"]))]
        )

        url = build_url(
            hotel_id   = HOTEL_ID,
            date_in    = state["giris_tarihi"],
            date_out   = state["cikis_tarihi"],
            adults     = state["yetiskin_sayisi"],
            child_ages = child_ages,
            rooms      = state["oda_sayisi"],
        )

        reply = (
            "Rezervasyon bilgileriniz hazır! Aşağıdaki bağlantıdan güvenle "
            f"işlemi tamamlayabilirsiniz:\n{url}"
        )
        
        execution_time = (time.time() - start_time) * 1000
        
        logger.info(f"Booking dialog completed successfully", extra={
            'execution_time': execution_time,
            'final_state': state,
            'booking_url_generated': True,
            'response_type': 'booking_complete'
        })
        
        return state, reply, True
        
    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        logger.error(f"Booking dialog handling failed: {str(e)}", extra={
            'execution_time': execution_time,
            'user_message': user_msg,
            'current_state': state
        }, exc_info=True)
        
        # Error fallback
        error_reply = "Üzgünüm, rezervasyon işleminizi tamamlarken bir sorun yaşadım. Lütfen tekrar deneyin."
        return state, error_reply, False
