@echo off
echo.
echo ======================================
echo  Cullinan Hotel Chatbot - Logging
echo ======================================
echo.

echo [1] Chatbot'u normal modda baslat
echo [2] Chatbot'u debug modda baslat  
echo [3] Logging sistemini test et
echo [4] Log analiz raporu olustur
echo [5] Real-time log monitoring baslat
echo [6] Log dosyalarini temizle
echo [0] Cikis
echo.

set /p choice="Seciminizi yapin (0-6): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Chatbot normal modda baslatiliyor...
    python router.py
) else if "%choice%"=="2" (
    echo.
    echo 🐛 Chatbot debug modda baslatiliyor...
    set PYTHONPATH=%CD%
    python -c "from logging_config import setup_logging; setup_logging(log_level='DEBUG'); exec(open('router.py').read())"
) else if "%choice%"=="3" (
    echo.
    echo 🧪 Logging sistemi test ediliyor...
    python test_logging.py
) else if "%choice%"=="4" (
    echo.
    echo 📊 Log analiz raporu olusturuluyor...
    python log_analyzer.py --mode analyze --hours 24
) else if "%choice%"=="5" (
    echo.
    echo 📺 Real-time log monitoring baslatiliyor...
    echo Press Ctrl+C to stop monitoring
    python log_analyzer.py --mode monitor --refresh 3
) else if "%choice%"=="6" (
    echo.
    echo 🧹 Log dosyalari temizleniyor...
    if exist logs (
        del /q logs\*.log
        echo ✅ Log dosyalari temizlendi
    ) else (
        echo ⚠️ Log dizini bulunamadi
    )
) else if "%choice%"=="0" (
    echo.
    echo 👋 Gorusmek uzere!
    exit /b
) else (
    echo.
    echo ❌ Gecersiz secim!
    pause
    goto :start
)

echo.
pause
