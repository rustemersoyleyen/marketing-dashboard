"""
Marketing Dashboard - Main App
==============================
Reklam harcamaları vs Lead/Ciro dashboard'u
"""

import streamlit as st
import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta
from dashboard.components.filters import render_all_filters
from dashboard.components.kpi_cards import render_kpi_cards, render_source_kpi_cards
from dashboard.components.charts import (
    render_spend_vs_revenue_chart,
    render_platform_pie_chart,
    render_daily_trend_chart,
    render_content_performance_table,
    render_roas_comparison_chart
)
from services.metrics_service import (
    calculate_overall_metrics,
    calculate_metrics_by_source,
    calculate_metrics_by_content
)
from services.ad_spend_service import get_daily_spend
from services.lead_service import get_lead_daily_trend
from services.revenue_service import get_revenue_daily_trend


# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Marketing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stMetric {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Ana dashboard fonksiyonu"""
    
    # Header
    st.markdown('<p class="main-header">📊 Marketing Performance Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Reklam Harcamaları vs Lead ve Ciro Analizi</p>', unsafe_allow_html=True)
    
    # Sidebar filtreleri
    filters = render_all_filters()
    start_date = filters["start_date"]
    end_date = filters["end_date"]
    platforms = filters["platforms"]
    
    # Tarih bilgisi
    st.caption(f"📅 Veri aralığı: {start_date} - {end_date}")
    
    st.divider()
    
    # Veri yükleme durumu
    with st.spinner("📊 Veriler yükleniyor..."):
        try:
            # Metrikleri hesapla
            overall_metrics = calculate_overall_metrics(start_date, end_date)
            metrics_by_source = calculate_metrics_by_source(start_date, end_date)
            content_metrics = calculate_metrics_by_content(start_date, end_date)
            
            # Sadece seçili platformları filtrele
            filtered_by_source = {
                k: v for k, v in metrics_by_source.items() 
                if k in platforms
            }
            
        except Exception as e:
            st.error(f"❌ Veri yüklenirken hata oluştu: {e}")
            st.info("⚠️ Lütfen veritabanı ve API bağlantılarını kontrol edin")
            st.stop()
    
    # =====================
    # ANA KPI KARTLARI
    # =====================
    st.subheader("🎯 Genel Performans")
    render_kpi_cards(overall_metrics)
    
    st.divider()
    
    # =====================
    # PLATFORM KARŞILAŞTIRMASI
    # =====================
    st.subheader("📱 Platform Bazlı Performans")
    render_source_kpi_cards(filtered_by_source)
    
    st.divider()
    
    # =====================
    # GRAFİKLER
    # =====================
    col1, col2 = st.columns(2)
    
    with col1:
        render_spend_vs_revenue_chart(filtered_by_source)
    
    with col2:
        render_roas_comparison_chart(filtered_by_source)
    
    st.divider()
    
    # =====================
    # DAĞILIM GRAFİKLERİ
    # =====================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_platform_pie_chart(filtered_by_source, "spend")
    
    with col2:
        render_platform_pie_chart(filtered_by_source, "leads")
    
    with col3:
        render_platform_pie_chart(filtered_by_source, "revenue")
    
    st.divider()
    
    # =====================
    # TREND GRAFİKLERİ
    # =====================
    st.subheader("📈 Trend Analizi")
    
    tab1, tab2, tab3 = st.tabs(["💰 Harcama Trendi", "👥 Lead Trendi", "💵 Ciro Trendi"])
    
    with tab1:
        daily_spend = get_daily_spend(start_date, end_date)
        render_daily_trend_chart(daily_spend, "spend")
    
    with tab2:
        daily_leads = get_lead_daily_trend(start_date, end_date, platforms)
        render_daily_trend_chart(daily_leads, "LeadCount")
    
    with tab3:
        daily_revenue = get_revenue_daily_trend(start_date, end_date, platforms)
        render_daily_trend_chart(daily_revenue, "TotalRevenue")
    
    st.divider()
    
    # =====================
    # KAMPANYA DETAY TABLOSU
    # =====================
    render_content_performance_table(content_metrics)
    
    # Footer
    st.divider()
    st.caption("📊 Marketing Dashboard v1.0 | Veriler: Google Ads, Facebook Ads")


if __name__ == "__main__":
    main()
