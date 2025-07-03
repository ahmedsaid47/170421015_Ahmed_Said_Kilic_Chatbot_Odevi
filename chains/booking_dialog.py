# chains/booking_dialog.py
# =====================================================================
# Cullinan Hotel – Akıcı Rezervasyon Diyaloğu (URL dahili)
# =====================================================================
from __future__ import annotations
import logging, re, time
from datetime import datetime, date
from typing import Dict, Any, List, Tuple
from urllib.parse import urlencode, quote_plus
from openai import OpenAI            # pip install openai>=1.0

# ---------------------------------------------------------------------
# Genel Ayarlar
# ---------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("hotel_chatbot.booking_dialog")

def timed(tag):
    def deco(fn):
        def wrap(*a, **kw):
            t0 = time.time()
            try:
                return fn(*a, **kw)
            finally:
                log.debug("%s %.0f ms", tag, (time.time() - t0) * 1000)
        return wrap
    return deco

CHAT_MODEL  = "ft:gpt-4o-mini-2024-07-18:personal::Bj1i1nW4"
client      = OpenAI()

HOTEL_ID    = 114_738
DOMAIN      = "www.cullinanhotels.com"
LANGUAGEID  = 1
ANCHOR      = "guestsandrooms"

# Zorunlu alanlar  (çocuk sayısı 0 olabilir)
REQUIRED = [
    "giris_tarihi",
    "cikis_tarihi",
    "yetiskin_sayisi",
    "cocuk_sayisi",
    "oda_sayisi"
]

# ---------------------------------------------------------------------
# Yardımcı Fonksiyonlar
# ---------------------------------------------------------------------
def _to_tc(iso: str) -> str:
    """ISO (YYYY-MM-DD) → MM/DD/YYYY (TravelClick)"""
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%m/%d/%Y")

def build_url(state: Dict[str, Any]) -> str:
    """State → TravelClick URL"""
    params = dict(
        adults     = state["yetiskin_sayisi"],
        datein     = _to_tc(state["giris_tarihi"]),
        dateout    = _to_tc(state["cikis_tarihi"]),
        rooms      = state["oda_sayisi"],
        domain     = DOMAIN,
        languageid = LANGUAGEID
    )
    if state["cocuk_sayisi"]:
        params["children"] = state["cocuk_sayisi"]
        if state.get("cocuk_yaslari"):
            params["childage"] = ",".join(f"{a:02d}" for a in state["cocuk_yaslari"])
    return (
        f"https://bookings.travelclick.com/{HOTEL_ID}"
        f"?{urlencode(params, quote_via=quote_plus)}#/{ANCHOR}"
    )

def param_summary(st: Dict[str, Any]) -> str:
    """Kullanıcıya okunabilir parametre özeti"""
    chunks = [
        f"datein={_to_tc(st['giris_tarihi'])}",
        f"dateout={_to_tc(st['cikis_tarihi'])}",
        f"adults={st['yetiskin_sayisi']}",
        f"rooms={st['oda_sayisi']}"
    ]
    if st["cocuk_sayisi"]:
        chunks.append(f"children={st['cocuk_sayisi']}")
        if st.get("cocuk_yaslari"):
            chunks.append(
                "childage=" + ",".join(f"{a:02d}" for a in st["cocuk_yaslari"])
            )
    return ", ".join(chunks)

def missing(st: Dict[str, Any]) -> List[str]:
    """Eksik zorunlu alanları döndürür."""
    m = [k for k in REQUIRED if k not in st]
    if st.get("cocuk_sayisi") and "cocuk_yaslari" not in st:
        m.append("cocuk_yaslari")
    return m

def summary(st: Dict[str, Any]) -> str:
    """Kullanıcıya onay özeti."""
    gi = datetime.strptime(st["giris_tarihi"], "%Y-%m-%d").strftime("%d %B %Y")
    co = datetime.strptime(st["cikis_tarihi"], "%Y-%m-%d").strftime("%d %B %Y")
    msg = (
        f"🔎 Bilgileriniz:\n"
        f"• {gi} → {co}\n"
        f"• Yetişkin: {st['yetiskin_sayisi']}\n"
        f"• Çocuk: {st['cocuk_sayisi']}\n"
        f"• Oda: {st['oda_sayisi']}"
    )
    if st["cocuk_sayisi"]:
        yas = ", ".join(map(str, st.get("cocuk_yaslari", []))) or "—"
        msg += f" (Yaş: {yas})"
    return msg + "\n\nOnaylıyor musunuz?"

# ---------------------------------------------------------------------
# Sistem Mesajı
# ---------------------------------------------------------------------
def system_prompt(st: Dict[str, Any]) -> str:
    today = date.today().isoformat()
    known = {k: v for k, v in st.items() if k not in {"history"}}
    miss  = missing(st)

    instr = (
        "Sen Cullinan Hotel’in Türkçe konuşan sanal rezervasyon asistanısın.\n"
        "• Kullanıcıyı biçimlere zorlamadan, **tek ve kapsayıcı sorularla** "
        "giriş/çıkış tarihleri, yetişkin & çocuk sayısı, oda sayısı ve "
        "(gerekirse) çocuk yaşlarını öğren.\n"
        "• Eksik birden çok alan varsa şu tip sor: "
        "“Hangi tarihler arasında, kaç yetişkin ve çocukla, kaç odada "
        "konaklamayı planlıyorsunuz?”\n"
        "• Gereksiz hiçbir detay isteme.\n"
        "• **Tüm** alanlar tamamlandığında özetle ve mutlaka *‘evet/hayır’* "
        "onayı iste. Kullanıcı onay verirse, aşağıdaki *ikinci bölümde* "
        "KESİNLİKLE `karar=ONAY` satırı bulunsun.\n"
        "• Cevaplarının İKİ bölümü olsun, `---` çizgisiyle ayır:\n"
        "  1) Kullanıcıya giden sohbet metni.\n"
        "  2) Çıkardığın veriler: her satır `anahtar=deger` veya `karar=ONAY/RED`.\n"
        "• Tarihleri ISO `YYYY-MM-DD` biçiminde döndür.\n"
    )

    context = ("Eksik alanlar: " + (", ".join(miss) if miss else
               "— yok, onay iste."))
    return f"{instr}\nBugün: {today}\nToplanan veriler: {known or '—'}\n{context}"

# ---------------------------------------------------------------------
# LLM Çağrısı
# ---------------------------------------------------------------------
@timed("LLM")
def llm_step(state: Dict[str, Any]) -> Tuple[str, Dict[str, str]]:
    msgs = [{"role": "system", "content": system_prompt(state)}] + state["history"]
    resp = client.chat.completions.create(
        model       = CHAT_MODEL,
        messages    = msgs,
        temperature = 0.2,
        max_tokens  = 350
    )
    raw = resp.choices[0].message.content.strip()
    part1, part2 = (raw.split("---", 1) + ["", ""])[:2]

    data: Dict[str, str] = {}
    for line in part2.strip().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return part1.strip(), data

def merge(state: Dict[str, Any], data: Dict[str, str]) -> None:
    if "giris_tarihi"   in data: state["giris_tarihi"]   = data["giris_tarihi"]
    if "cikis_tarihi"   in data: state["cikis_tarihi"]   = data["cikis_tarihi"]
    if "yetiskin_sayisi" in data:
        try: state["yetiskin_sayisi"] = int(data["yetiskin_sayisi"])
        except: pass
    if "cocuk_sayisi" in data:
        try: state["cocuk_sayisi"] = int(data["cocuk_sayisi"])
        except: pass
    if "oda_sayisi"   in data:
        try: state["oda_sayisi"]   = int(data["oda_sayisi"])
        except: pass
    if "cocuk_yaslari" in data:
        state["cocuk_yaslari"] = [int(n) for n in re.findall(r"\d+", data["cocuk_yaslari"])]

# Heuristik “evet/onay” kelimeleri
_POSITIVE_WORDS = ("onay", "evet", "kabul", "tamam", "olur", "onaylıyorum",
                   "onayladım", "peki")

def _user_confirms(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in _POSITIVE_WORDS)

# ---------------------------------------------------------------------
# Ana Fonksiyon
# ---------------------------------------------------------------------
def handle_booking(
    state: Dict[str, Any],
    user_msg: str
) -> Tuple[Dict[str, Any], str, bool]:
    """
    ► state    : Oturum belleği (ilk çağrıda {})
    ► user_msg : Kullanıcı mesajı
    ◄ returns  : (güncellenmiş state, asistan cevabı, işlem tamam mı)
    """
    if "history" not in state:
        state["history"] = []

    state["history"].append({"role": "user", "content": user_msg})

    # LLM yanıtı
    reply, parsed = llm_step(state)
    merge(state, parsed)

    # Tamamlandı mı?
    finished = False
    no_missing = not missing(state)

    # 1) LLM 'karar=ONAY' dedi → kesin
    if parsed.get("karar") == "ONAY" and no_missing:
        finished = True
    # 2) Heuristik: Kullanıcı mesajı doğrudan onay içeriyor + eksik yok
    elif no_missing and _user_confirms(user_msg):
        finished = True

    # Bağlantı oluştur ve yanıtı güncelle
    if finished:
        url  = build_url(state)
        pstr = param_summary(state)
        reply = (
            "✅ Harika! Rezervasyon bağlantınız hazır:\n"
            f"{url}\n\n"
            f"🔧 *Parametre özeti*: {pstr}"
        )
    # Eksik yok ama onay da yok → özet sor
    elif no_missing and parsed.get("karar") != "RED":
        reply = summary(state)

    state["history"].append({"role": "assistant", "content": reply})
    return state, reply, finished

# ---------------------------------------------------------------------
# Basit CLI testi
# ---------------------------------------------------------------------
if __name__ == "__main__":
    sess = {}
    while True:
        u = input("👤> ")
        sess, bot, done = handle_booking(sess, u)
        print("🤖", bot)
        if done:
            break
