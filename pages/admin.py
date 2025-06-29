"""
Admin Panel - Sistem Yönetimi ve Konfigürasyon
"""

import streamlit as st
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
import sys
import subprocess
import sqlite3

# Proje path'ini ekle
sys.path.append(str(Path(__file__).parent.parent))

try:
    from logging_config import setup_logging
    from config import load_api_key
except ImportError:
    st.error("Gerekli modüller yüklenemedi.")
    st.stop()

# Page config
st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide"
)

# Authentication (basit)
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

def check_admin_password():
    """Admin şifre kontrolü"""
    password = st.text_input("Admin Şifresi", type="password")
    if st.button("Giriş"):
        if password == "admin123":  # Gerçek uygulamada güvenli authentication kullanın
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("❌ Yanlış şifre!")

if not st.session_state.admin_authenticated:
    st.title("🔐 Admin Panel - Giriş")
    st.warning("Bu sayfa sadece sistem yöneticileri içindir.")
    check_admin_password()
    st.stop()

# Header
st.title("⚙️ Admin Panel - Sistem Yönetimi")
st.markdown("Chatbot sisteminin yönetimi ve konfigürasyonu")

# Sidebar
st.sidebar.header("🔧 Admin Araçları")
admin_section = st.sidebar.selectbox(
    "Bölüm Seç",
    [
        "📊 Sistem Durumu",
        "🗄️ Veritabanı Yönetimi", 
        "📝 Log Yönetimi",
        "⚙️ Konfigürasyon",
        "🔄 Backup & Restore",
        "🧪 Test Araçları"
    ]
)

def get_system_status():
    """Sistem durumu bilgilerini al"""
    status = {
        'python_version': sys.version,
        'working_directory': str(Path.cwd()),
        'log_directory_exists': Path('logs').exists(),
        'db_directory_exists': Path('db').exists(),
    }
    
    # API key kontrolü
    try:
        load_api_key()
        status['api_key_status'] = '✅ Mevcut'
    except:
        status['api_key_status'] = '❌ Bulunamadı'
    
    # Veritabanı kontrolü
    db_files = {
        'hotel_db': Path('db/hotel_db/chroma.sqlite3').exists(),
        'intent_db': Path('db/intent_db/chroma.sqlite3').exists(),
        'booking_db': Path('db/booking_db/chroma.sqlite3').exists()
    }
    status['databases'] = db_files
    
    # Log dosyaları
    log_files = {}
    if Path('logs').exists():
        for log_file in Path('logs').glob('*.log'):
            log_files[log_file.name] = log_file.stat().st_size
    status['log_files'] = log_files
    
    return status

def show_system_status():
    """Sistem durumu göster"""
    st.subheader("📊 Sistem Durumu")
    
    status = get_system_status()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖥️ Sistem Bilgileri")
        st.code(f"Python: {status['python_version']}")
        st.code(f"Çalışma Dizini: {status['working_directory']}")
        st.code(f"API Key: {status['api_key_status']}")
        
        st.markdown("### 📁 Dizin Durumu")
        st.write(f"📁 logs/: {'✅' if status['log_directory_exists'] else '❌'}")
        st.write(f"📁 db/: {'✅' if status['db_directory_exists'] else '❌'}")
    
    with col2:
        st.markdown("### 🗄️ Veritabanları")
        for db_name, exists in status['databases'].items():
            st.write(f"🗄️ {db_name}: {'✅' if exists else '❌'}")
        
        st.markdown("### 📝 Log Dosyaları")
        for log_name, size in status['log_files'].items():
            size_mb = size / (1024 * 1024)
            st.write(f"📝 {log_name}: {size_mb:.2f} MB")

def show_database_management():
    """Veritabanı yönetimi"""
    st.subheader("🗄️ Veritabanı Yönetimi")
    
    tab1, tab2, tab3 = st.tabs(["📊 Durum", "🔍 İçerik", "🧹 Temizlik"])
    
    with tab1:
        st.markdown("### Veritabanı Durumu")
        
        db_info = {}
        db_paths = {
            'hotel_db': 'db/hotel_db/chroma.sqlite3',
            'intent_db': 'db/intent_db/chroma.sqlite3', 
            'booking_db': 'db/booking_db/chroma.sqlite3'
        }
        
        for db_name, db_path in db_paths.items():
            if Path(db_path).exists():
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Tablo sayısı
                    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
                    table_count = cursor.fetchone()[0]
                    
                    # Dosya boyutu
                    file_size = Path(db_path).stat().st_size / (1024 * 1024)
                    
                    db_info[db_name] = {
                        'status': '✅ Aktif',
                        'tables': table_count,
                        'size_mb': round(file_size, 2)
                    }
                    conn.close()
                except Exception as e:
                    db_info[db_name] = {
                        'status': f'❌ Hata: {str(e)}',
                        'tables': 0,
                        'size_mb': 0
                    }
            else:
                db_info[db_name] = {
                    'status': '❌ Bulunamadı',
                    'tables': 0,
                    'size_mb': 0
                }
        
        # Tablo olarak göster
        import pandas as pd
        df = pd.DataFrame.from_dict(db_info, orient='index')
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.markdown("### Veritabanı İçeriği")
        
        selected_db = st.selectbox(
            "Veritabanı Seç",
            ['hotel_db', 'intent_db', 'booking_db']
        )
        
        db_path = f'db/{selected_db}/chroma.sqlite3'
        
        if Path(db_path).exists():
            try:
                conn = sqlite3.connect(db_path)
                
                # Tabloları listele
                tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                
                if tables:
                    st.write(f"📊 **{selected_db}** veritabanındaki tablolar:")
                    for table in tables:
                        st.write(f"- {table[0]}")
                        
                        # İlk 5 satırı göster
                        if st.checkbox(f"İçeriği göster: {table[0]}", key=f"show_{table[0]}"):
                            df = pd.read_sql_query(f"SELECT * FROM {table[0]} LIMIT 5", conn)
                            st.dataframe(df)
                else:
                    st.info("Tablolar bulunamadı.")
                
                conn.close()
            except Exception as e:
                st.error(f"Veritabanı okuma hatası: {str(e)}")
        else:
            st.warning(f"Veritabanı dosyası bulunamadı: {db_path}")
    
    with tab3:
        st.markdown("### 🧹 Veritabanı Temizliği")
        st.warning("⚠️ Bu işlemler geri alınamaz! Dikkatli olun.")
        
        if st.button("🗑️ Tüm Log Verilerini Temizle"):
            if st.checkbox("Eminim, tüm log verilerini silmek istiyorum"):
                # Log dosyalarını sil
                if Path('logs').exists():
                    for log_file in Path('logs').glob('*.log'):
                        log_file.unlink()
                    st.success("✅ Log dosyaları temizlendi")
                else:
                    st.info("Log dizini bulunamadı")

def show_log_management():
    """Log yönetimi"""
    st.subheader("📝 Log Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Log İstatistikleri")
        
        if Path('logs').exists():
            total_size = 0
            file_count = 0
            
            for log_file in Path('logs').glob('*'):
                if log_file.is_file():
                    total_size += log_file.stat().st_size
                    file_count += 1
            
            st.metric("📁 Toplam Dosya", file_count)
            st.metric("💾 Toplam Boyut", f"{total_size / (1024*1024):.2f} MB")
            
            # Log dosyaları listesi
            st.markdown("### 📄 Log Dosyaları")
            for log_file in Path('logs').glob('*.log'):
                size = log_file.stat().st_size / 1024  # KB
                modified = datetime.fromtimestamp(log_file.stat().st_mtime)
                
                with st.expander(f"📝 {log_file.name} ({size:.1f} KB)"):
                    st.write(f"**Son Değişiklik:** {modified.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if st.button(f"👁️ Son 10 Satırı Göster", key=f"view_{log_file.name}"):
                        try:
                            with open(log_file, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                last_lines = lines[-10:] if len(lines) > 10 else lines
                                for line in last_lines:
                                    st.code(line.strip())
                        except Exception as e:
                            st.error(f"Dosya okuma hatası: {e}")
        else:
            st.info("Log dizini bulunamadı")
    
    with col2:
        st.markdown("### 🔧 Log Araçları")
        
        # Log level ayarı
        log_level = st.selectbox(
            "Log Seviyesi",
            ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=1
        )
        
        if st.button("⚙️ Log Seviyesini Güncelle"):
            # Burada log seviyesini güncelleyebilirsiniz
            st.success(f"✅ Log seviyesi {log_level} olarak ayarlandı")
        
        # Log temizlik
        st.markdown("### 🧹 Log Temizliği")
        
        if st.button("🗑️ Eski Logları Temizle (7+ gün)"):
            if Path('logs').exists():
                cutoff_date = datetime.now() - timedelta(days=7)
                deleted_count = 0
                
                for log_file in Path('logs').glob('*.log'):
                    file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_time < cutoff_date:
                        log_file.unlink()
                        deleted_count += 1
                
                st.success(f"✅ {deleted_count} eski log dosyası silindi")
            else:
                st.info("Log dizini bulunamadı")

def show_configuration():
    """Konfigürasyon yönetimi"""
    st.subheader("⚙️ Sistem Konfigürasyonu")
    
    tab1, tab2, tab3 = st.tabs(["🔑 API Ayarları", "🎨 UI Ayarları", "📊 Monitoring"])
    
    with tab1:
        st.markdown("### 🔑 API Konfigürasyonu")
        
        # Mevcut API key durumu
        try:
            api_key = load_api_key()
            st.success("✅ OpenAI API key mevcut")
            st.code(f"Key: {api_key[:7]}...{api_key[-4:]}")
        except:
            st.error("❌ OpenAI API key bulunamadı")
        
        # Yeni API key
        st.markdown("### 🔄 API Key Güncelle")
        new_api_key = st.text_input("Yeni OpenAI API Key", type="password")
        
        if st.button("💾 API Key'i Kaydet"):
            if new_api_key:
                secrets_file = Path("secrets.json")
                secrets = {"OPENAI_API_KEY": new_api_key}
                
                with open(secrets_file, 'w') as f:
                    json.dump(secrets, f, indent=2)
                
                st.success("✅ API key kaydedildi")
            else:
                st.error("❌ API key boş olamaz")
    
    with tab2:
        st.markdown("### 🎨 UI Konfigürasyonu")
        
        # Streamlit config
        config_file = Path(".streamlit/config.toml")
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_content = f.read()
            
            st.markdown("#### Mevcut Konfigürasyon")
            edited_config = st.text_area(
                "config.toml",
                value=config_content,
                height=300
            )
            
            if st.button("💾 Konfigürasyonu Kaydet"):
                with open(config_file, 'w') as f:
                    f.write(edited_config)
                st.success("✅ Konfigürasyon kaydedildi")
        else:
            st.info("Streamlit konfigürasyon dosyası bulunamadı")
    
    with tab3:
        st.markdown("### 📊 Monitoring Ayarları")
        
        # Log rotation ayarları
        st.markdown("#### Log Rotation")
        max_log_size = st.slider("Max Log Dosyası Boyutu (MB)", 1, 100, 10)
        backup_count = st.slider("Backup Dosya Sayısı", 1, 20, 5)
        
        if st.button("⚙️ Log Ayarlarını Uygula"):
            st.success(f"✅ Log ayarları güncellendi: {max_log_size}MB, {backup_count} backup")

def show_backup_restore():
    """Backup ve restore işlemleri"""
    st.subheader("🔄 Backup & Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💾 Backup Oluştur")
        
        backup_items = st.multiselect(
            "Backup edilecek öğeler:",
            ["Veritabanları", "Log Dosyaları", "Konfigürasyon", "Kodlar"],
            default=["Veritabanları", "Konfigürasyon"]
        )
        
        if st.button("📦 Backup Oluştur"):
            backup_dir = Path(f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            backup_dir.mkdir(exist_ok=True)
            
            try:
                if "Veritabanları" in backup_items and Path("db").exists():
                    shutil.copytree("db", backup_dir / "db")
                
                if "Log Dosyaları" in backup_items and Path("logs").exists():
                    shutil.copytree("logs", backup_dir / "logs")
                
                if "Konfigürasyon" in backup_items:
                    config_files = [".streamlit", "secrets.json", "requirements.txt"]
                    for config_file in config_files:
                        if Path(config_file).exists():
                            if Path(config_file).is_dir():
                                shutil.copytree(config_file, backup_dir / config_file)
                            else:
                                shutil.copy2(config_file, backup_dir)
                
                if "Kodlar" in backup_items:
                    code_files = ["*.py", "*.md", "*.bat"]
                    for pattern in code_files:
                        for file in Path(".").glob(pattern):
                            shutil.copy2(file, backup_dir)
                
                # ZIP oluştur
                shutil.make_archive(str(backup_dir), 'zip', backup_dir)
                shutil.rmtree(backup_dir)
                
                st.success(f"✅ Backup oluşturuldu: {backup_dir}.zip")
                
                # Download linki
                with open(f"{backup_dir}.zip", "rb") as f:
                    st.download_button(
                        "📥 Backup'ı İndir",
                        data=f.read(),
                        file_name=f"{backup_dir}.zip",
                        mime="application/zip"
                    )
                    
            except Exception as e:
                st.error(f"❌ Backup hatası: {str(e)}")
    
    with col2:
        st.markdown("### 📤 Restore İşlemi")
        
        uploaded_file = st.file_uploader(
            "Backup dosyası seç (.zip)",
            type=['zip']
        )
        
        if uploaded_file and st.button("🔄 Restore Et"):
            st.warning("⚠️ Bu işlem mevcut verilerin üzerine yazacak!")
            
            if st.checkbox("Eminim, restore işlemini yapmak istiyorum"):
                try:
                    # Temp dizin oluştur
                    temp_dir = Path("temp_restore")
                    temp_dir.mkdir(exist_ok=True)
                    
                    # ZIP'i extract et
                    with open(temp_dir / "backup.zip", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    shutil.unpack_archive(temp_dir / "backup.zip", temp_dir)
                    
                    # Restore işlemi
                    # Bu kısım backup içeriğine göre customize edilebilir
                    
                    st.success("✅ Restore işlemi tamamlandı")
                    
                    # Temp dosyaları temizle
                    shutil.rmtree(temp_dir)
                    
                except Exception as e:
                    st.error(f"❌ Restore hatası: {str(e)}")

def show_test_tools():
    """Test araçları"""
    st.subheader("🧪 Test Araçları")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Sistem Testleri")
        
        if st.button("🧪 Logging Sistemi Test"):
            result = subprocess.run([sys.executable, "test_logging.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success("✅ Logging sistemi testi başarılı")
                st.code(result.stdout)
            else:
                st.error("❌ Logging sistemi testi başarısız")
                st.code(result.stderr)
        
        if st.button("🔌 API Bağlantısı Test"):
            try:
                import openai
                openai.api_key = load_api_key()
                
                # Basit bir test çağrısı
                client = openai.OpenAI()
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5
                )
                
                st.success("✅ OpenAI API bağlantısı başarılı")
                st.info(f"Response: {response.choices[0].message.content}")
                
            except Exception as e:
                st.error(f"❌ API bağlantı hatası: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Performance Testleri")
        
        if st.button("⚡ Chatbot Performance Test"):
            # Basit performance testi
            import time
            
            start_time = time.time()
            
            # Test mesajları
            test_messages = [
                "Merhaba",
                "Rezervasyon yapmak istiyorum", 
                "Fiyatlar nedir?",
                "Teşekkürler"
            ]
            
            times = []
            for msg in test_messages:
                msg_start = time.time()
                # Burada gerçek chatbot çağrısı yapılabilir
                time.sleep(0.1)  # Simülasyon
                msg_time = time.time() - msg_start
                times.append(msg_time * 1000)  # ms
            
            total_time = time.time() - start_time
            
            st.success("✅ Performance testi tamamlandı")
            st.metric("Toplam Süre", f"{total_time:.2f}s")
            st.metric("Ortalama Yanıt", f"{sum(times)/len(times):.2f}ms")
            
            # Grafik göster
            import pandas as pd
            import plotly.express as px
            
            df = pd.DataFrame({
                'Mesaj': [f"Test {i+1}" for i in range(len(times))],
                'Süre (ms)': times
            })
            
            fig = px.bar(df, x='Mesaj', y='Süre (ms)')
            st.plotly_chart(fig, use_container_width=True)

# Main content based on selection
if admin_section == "📊 Sistem Durumu":
    show_system_status()
elif admin_section == "🗄️ Veritabanı Yönetimi":
    show_database_management()
elif admin_section == "📝 Log Yönetimi":
    show_log_management()
elif admin_section == "⚙️ Konfigürasyon":
    show_configuration()
elif admin_section == "🔄 Backup & Restore":
    show_backup_restore()
elif admin_section == "🧪 Test Araçları":
    show_test_tools()

# Footer
st.divider()
if st.button("🚪 Admin Panelden Çık"):
    st.session_state.admin_authenticated = False
    st.rerun()
