"""
Analytics ve Log Monitoring Sayfası
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Proje path'ini ekle
sys.path.append(str(Path(__file__).parent.parent))

try:
    from log_analyzer import LogAnalyzer, LogMonitor
except ImportError:
    st.error("Log analyzer modülü yüklenemedi. log_analyzer.py dosyasının mevcut olduğundan emin olun.")
    st.stop()

# Page config
st.set_page_config(
    page_title="Analytics & Monitoring",
    page_icon="📊",
    layout="wide"
)

# Header
st.markdown("""
# 📊 Analytics & Log Monitoring

Bu sayfada chatbot'unuzun performance metriklerini, hata analizini ve kullanıcı etkileşim verilerini görüntüleyebilirsiniz.
""")

# Sidebar controls
st.sidebar.header("🔧 Kontrol Paneli")

log_file = st.sidebar.selectbox(
    "Log Dosyası Seç",
    ["logs/hotel_chatbot.json.log", "logs/streamlit_chatbot.json.log"],
    help="Analiz edilecek log dosyasını seçin"
)

time_range = st.sidebar.selectbox(
    "Zaman Aralığı",
    [1, 6, 12, 24, 48, 72, 168],  # hours
    index=3,  # default 24 hours
    format_func=lambda x: f"Son {x} saat" if x < 24 else f"Son {x//24} gün"
)

auto_refresh = st.sidebar.checkbox("Otomatik Yenileme (30s)", value=False)

if auto_refresh:
    st.sidebar.info("🔄 Sayfa her 30 saniyede otomatik yenileniyor")
    
# Log file kontrolü
log_path = Path(log_file)
if not log_path.exists():
    st.error(f"❌ Log dosyası bulunamadı: {log_path}")
    st.info("💡 Önce chatbot'u çalıştırarak log dosyası oluşturun.")
    st.stop()

# Analytics loading
@st.cache_data(ttl=30 if auto_refresh else 300)
def load_analytics_data(log_file_path, hours_back):
    """Analytics verilerini yükle"""
    analyzer = LogAnalyzer(Path(log_file_path))
    
    return {
        'error_summary': analyzer.get_error_summary(hours_back),
        'performance_summary': analyzer.get_performance_summary(hours_back),
        'intent_analysis': analyzer.get_intent_analysis(hours_back),
        'api_usage': analyzer.get_api_usage_summary(hours_back),
        'user_interactions': analyzer.get_user_interaction_summary(hours_back),
        'raw_logs': analyzer.get_logs_by_timerange(hours_back)
    }

# Load data
with st.spinner("📈 Analytics verileri yükleniyor..."):
    analytics_data = load_analytics_data(log_file, time_range)

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

# KPI Metrics
with col1:
    total_logs = len(analytics_data['raw_logs'])
    st.metric("📝 Toplam Log", f"{total_logs:,}")

with col2:
    error_rate = analytics_data['error_summary']['error_rate']
    st.metric(
        "🚨 Hata Oranı", 
        f"{error_rate:.2f}%",
        delta=f"{error_rate-5:.1f}%" if error_rate > 5 else None,
        delta_color="inverse"
    )

with col3:
    if 'avg_execution_time' in analytics_data['performance_summary']:
        avg_time = analytics_data['performance_summary']['avg_execution_time']
        st.metric("⚡ Ortalama Süre", f"{avg_time:.0f}ms")
    else:
        st.metric("⚡ Ortalama Süre", "N/A")

with col4:
    if 'total_conversations' in analytics_data['user_interactions']:
        conversations = analytics_data['user_interactions']['total_conversations']
        st.metric("👥 Konuşma Sayısı", f"{conversations}")
    else:
        st.metric("👥 Konuşma Sayısı", "0")

st.divider()

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["🚨 Hata Analizi", "⚡ Performance", "🎯 Intent Analizi", "💰 API Kullanımı"])

with tab1:
    st.subheader("🚨 Hata Analizi")
    
    error_data = analytics_data['error_summary']
    
    if error_data['total_errors'] > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### En Sık Hata Tipleri")
            error_types_df = pd.DataFrame(
                list(error_data['error_types'].items()),
                columns=['Hata Tipi', 'Sayı']
            )
            fig = px.bar(error_types_df, x='Sayı', y='Hata Tipi', orientation='h')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Hata Kontekstleri")
            contexts_df = pd.DataFrame(
                list(error_data['error_contexts'].items()),
                columns=['Kontekst', 'Sayı']
            )
            fig = px.pie(contexts_df, values='Sayı', names='Kontekst')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # Son hatalar
        st.markdown("### 🕐 Son Hatalar")
        for error in error_data['recent_errors'][-3:]:
            with st.expander(f"❌ {error.get('timestamp', 'N/A')[:19]} - {error.get('message', 'No message')[:50]}..."):
                st.json(error)
    else:
        st.success("🎉 Seçilen zaman aralığında hata bulunamadı!")

with tab2:
    st.subheader("⚡ Performance Analizi")
    
    perf_data = analytics_data['performance_summary']
    
    if 'operation_stats' in perf_data and perf_data['operation_stats']:
        # Performance metrics table
        st.markdown("### 📊 İşlem Bazında Performance")
        
        perf_df = pd.DataFrame.from_dict(perf_data['operation_stats'], orient='index')
        perf_df = perf_df.round(2)
        perf_df = perf_df.sort_values('avg', ascending=False)
        
        st.dataframe(
            perf_df,
            column_config={
                "count": st.column_config.NumberColumn("İşlem Sayısı"),
                "avg": st.column_config.NumberColumn("Ortalama (ms)"),
                "min": st.column_config.NumberColumn("Minimum (ms)"),
                "max": st.column_config.NumberColumn("Maximum (ms)"),
                "p50": st.column_config.NumberColumn("P50 (ms)"),
                "p95": st.column_config.NumberColumn("P95 (ms)"),
                "p99": st.column_config.NumberColumn("P99 (ms)")
            },
            use_container_width=True
        )
        
        # Performance chart
        st.markdown("### 📈 Ortalama Execution Time")
        fig = px.bar(
            x=perf_df.index,
            y=perf_df['avg'],
            title="İşlem Bazında Ortalama Süre (ms)"
        )
        fig.update_xaxes(title="İşlem Tipi")
        fig.update_yaxes(title="Süre (ms)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 Performance verisi bulunamadı.")

with tab3:
    st.subheader("🎯 Intent Sınıflandırma Analizi")
    
    intent_data = analytics_data['intent_analysis']
    
    if 'intent_distribution' in intent_data and intent_data['intent_distribution']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Intent Dağılımı")
            intent_df = pd.DataFrame(
                list(intent_data['intent_distribution'].items()),
                columns=['Intent', 'Sayı']
            )
            fig = px.pie(intent_df, values='Sayı', names='Intent')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Güven Skorları")
            confidence_data = intent_data['average_confidence_by_intent']
            conf_df = pd.DataFrame(
                list(confidence_data.items()),
                columns=['Intent', 'Ortalama Güven']
            )
            conf_df['Ortalama Güven'] = conf_df['Ortalama Güven'].round(3)
            
            fig = px.bar(conf_df, x='Intent', y='Ortalama Güven')
            fig.update_yaxes(range=[0, 1])
            st.plotly_chart(fig, use_container_width=True)
        
        # Düşük güven skorları
        if intent_data['low_confidence_count'] > 0:
            st.markdown("### ⚠️ Düşük Güven Skorlu Örnekler")
            st.warning(f"{intent_data['low_confidence_count']} adet düşük güven skorlu sınıflandırma bulundu.")
            
            for example in intent_data['low_confidence_examples'][-5:]:
                with st.expander(f"⚠️ {example['intent']} (güven: {example['confidence']:.2f})"):
                    st.write(f"**Kullanıcı Girişi:** {example['user_input']}")
                    st.write(f"**Zaman:** {example['timestamp'][:19]}")
    else:
        st.info("🎯 Intent analiz verisi bulunamadı.")

with tab4:
    st.subheader("💰 API Kullanımı ve Maliyet")
    
    api_data = analytics_data['api_usage']
    
    if 'total_api_calls' in api_data:
        # API usage metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📞 Toplam API Çağrısı", f"{api_data['total_api_calls']:,}")
        
        with col2:
            st.metric("🎫 Toplam Token", f"{api_data['total_tokens_used']:,}")
        
        with col3:
            st.metric("💵 Tahmini Maliyet", f"${api_data['estimated_cost_usd']:.4f}")
        
        # API distribution
        if api_data['api_distribution']:
            st.markdown("### 📊 API Dağılımı")
            api_df = pd.DataFrame(
                list(api_data['api_distribution'].items()),
                columns=['API', 'Çağrı Sayısı']
            )
            
            fig = px.bar(api_df, x='API', y='Çağrı Sayısı')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💰 API kullanım verisi bulunamadı.")

# Real-time monitoring section
st.divider()
st.subheader("📺 Real-time Monitoring")

if st.button("🔄 Verileri Yenile"):
    st.cache_data.clear()
    st.rerun()

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Detaylı Rapor Oluştur", use_container_width=True):
        analyzer = LogAnalyzer(Path(log_file))
        report = analyzer.generate_full_report(time_range)
        
        st.text_area(
            "📋 Detaylı Analiz Raporu",
            value=report,
            height=400
        )
        
        # Download button
        st.download_button(
            label="💾 Raporu İndir",
            data=report,
            file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

with col2:
    st.markdown("### 🔧 Export Seçenekleri")
    
    export_format = st.radio(
        "Format seçin:",
        ["JSON", "CSV", "Excel"],
        horizontal=True
    )
    
    if st.button("📥 Verileri Export Et", use_container_width=True):
        if export_format == "JSON":
            export_data = json.dumps(analytics_data, indent=2, default=str)
            st.download_button(
                "💾 JSON İndir",
                data=export_data,
                file_name=f"analytics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        elif export_format == "CSV":
            # Convert to DataFrame for CSV
            if analytics_data['raw_logs']:
                df = pd.json_normalize(analytics_data['raw_logs'])
                csv_data = df.to_csv(index=False)
                st.download_button(
                    "💾 CSV İndir",
                    data=csv_data,
                    file_name=f"logs_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

# Auto-refresh logic
if auto_refresh:
    time.sleep(30)
    st.rerun()
