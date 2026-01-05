"""
KPI Card Components
===================
Ana metrik kartları
"""

import streamlit as st


def render_kpi_cards(metrics: dict):
    """
    5 ana KPI kartını render eder
    
    Args:
        metrics: {total_spend, total_leads, total_revenue, cpa, roas}
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="💰 Toplam Harcama",
            value=f"₺{metrics['total_spend']:,.0f}",
            help="Tüm reklam platformlarındaki toplam harcama"
        )
    
    with col2:
        st.metric(
            label="👥 Toplam Lead",
            value=f"{metrics['total_leads']:,}",
            help="Reklam kaynaklı toplam lead sayısı"
        )
    
    with col3:
        st.metric(
            label="💵 Toplam Ciro",
            value=f"₺{metrics['total_revenue']:,.0f}",
            help="Reklam kaynaklı toplam satış geliri"
        )
    
    with col4:
        cpa_color = "normal"
        st.metric(
            label="📊 CPA (Lead Başı Maliyet)",
            value=f"₺{metrics['cpa']:,.0f}",
            help="Cost per Acquisition - Bir lead edinme maliyeti"
        )
    
    with col5:
        roas_value = metrics['roas']
        roas_delta = f"{metrics['roas_percentage']:.0f}%" if roas_value > 0 else None
        st.metric(
            label="📈 ROAS",
            value=f"{roas_value:.2f}x",
            delta=roas_delta,
            help="Return on Ad Spend - Harcama başına getiri"
        )


def render_source_kpi_cards(metrics_by_source: dict):
    """
    Platform bazlı KPI kartlarını render eder
    
    Args:
        metrics_by_source: {"google": {...}, "facebook": {...}}
    """
    platform_icons = {
        "google": "🔍",
        "facebook": "📘",
        "apple": "🍎"
    }
    
    platform_names = {
        "google": "Google Ads",
        "facebook": "Facebook Ads",
        "apple": "Apple Ads"
    }
    
    cols = st.columns(len(metrics_by_source))
    
    for i, (source, metrics) in enumerate(metrics_by_source.items()):
        icon = platform_icons.get(source, "📊")
        name = platform_names.get(source, source)
        
        with cols[i]:
            st.subheader(f"{icon} {name}")
            
            subcol1, subcol2 = st.columns(2)
            
            with subcol1:
                st.metric("Harcama", f"₺{metrics['spend']:,.0f}")
                st.metric("Lead", f"{metrics['leads']:,}")
            
            with subcol2:
                st.metric("Ciro", f"₺{metrics['revenue']:,.0f}")
                st.metric("ROAS", f"{metrics['roas']:.2f}x")


def render_comparison_cards(current: dict, previous: dict = None):
    """
    Karşılaştırmalı KPI kartları (gelecekte dönem karşılaştırması için)
    
    Args:
        current: Mevcut dönem metrikleri
        previous: Önceki dönem metrikleri (opsiyonel)
    """
    # Basit versiyon - sadece mevcut değerleri göster
    render_kpi_cards(current)
    
    if previous:
        # Delta hesaplama
        st.caption("📈 Önceki döneme göre değişim")
        
        spend_delta = ((current['total_spend'] - previous['total_spend']) / previous['total_spend'] * 100) if previous['total_spend'] > 0 else 0
        leads_delta = ((current['total_leads'] - previous['total_leads']) / previous['total_leads'] * 100) if previous['total_leads'] > 0 else 0
        revenue_delta = ((current['total_revenue'] - previous['total_revenue']) / previous['total_revenue'] * 100) if previous['total_revenue'] > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Harcama Değişimi", f"{spend_delta:+.1f}%")
        col2.metric("Lead Değişimi", f"{leads_delta:+.1f}%")
        col3.metric("Ciro Değişimi", f"{revenue_delta:+.1f}%")
