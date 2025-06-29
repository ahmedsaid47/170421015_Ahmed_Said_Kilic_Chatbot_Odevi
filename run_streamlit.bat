@echo off
title Cullinan Hotel Chatbot - Streamlit Web Arayuzu

echo.
echo ================================================
echo   🏨 CULLINAN HOTEL CHATBOT - WEB ARAYUZU 🏨
echo ================================================
echo.

:: Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadi! Lutfen Python 3.8+ yukleyin.
    echo    https://python.org/downloads
    pause
    exit /b 1
)

:: Gerekli kütüphaneleri kontrol et
echo 📦 Gerekli kutuphaneler kontrol ediliyor...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Streamlit bulunamadi. Kutuphaneler yukleniyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Kutuphaneler yuklenemedi!
        pause
        exit /b 1
    )
) else (
    echo ✅ Streamlit hazir!
)

:: Log dizini oluştur
if not exist "logs" mkdir logs

:: API key kontrolü
python -c "from config import load_api_key; load_api_key()" >nul 2>&1
if errorlevel 1 (
    echo ❌ OpenAI API key bulunamadi!
    echo.
    echo Lutfen asagidakilerden birini yapin:
    echo 1. OPENAI_API_KEY ortam degiskenini ayarlayin
    echo 2. secrets.json dosyasi olusturun: {"OPENAI_API_KEY": "sk-..."}
    echo 3. .env dosyasi olusturun: OPENAI_API_KEY=sk-...
    echo.
    pause
    exit /b 1
)

:: Veritabanı kontrolü
if not exist "db\hotel_db\chroma.sqlite3" (
    echo ⚠️ Hotel veritabani bulunamadi: db\hotel_db\chroma.sqlite3
    echo Lutfen once veritabanini olusturun.
)

if not exist "db\intent_db\chroma.sqlite3" (
    echo ⚠️ Intent veritabani bulunamadi: db\intent_db\chroma.sqlite3  
    echo Lutfen once veritabanini olusturun.
)

echo.
echo 🚀 Streamlit uygulamasi baslatiliyor...
echo.
echo 📱 Tarayici otomatik acilacak: http://localhost:8501
echo 🛑 Durdurmak icin Ctrl+C basin
echo.

:: Streamlit'i başlat
streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --theme.primaryColor "#1f4e79"

echo.
echo 👋 Uygulama kapatildi.
pause
