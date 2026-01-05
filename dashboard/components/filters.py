"""
Filter Components
=================
Tarih ve platform filtre bileşenleri
"""

import streamlit as st
from datetime import date, timedelta
from config.database import DEFAULT_DATE_RANGE_DAYS, SUPPORTED_PLATFORMS, UTM_SOURCE_MAPPING


def render_date_filter():
    """
    Sidebar'da tarih filtresi render eder
    
    Returns:
        tuple: (start_date, end_date)
    """
    st.sidebar.subheader("📅 Tarih Aralığı")
    
    # Hızlı seçim butonları
    quick_select = st.sidebar.radio(
        "Hızlı Seçim",
        ["Son 7 gün", "Son 30 gün", "Son 90 gün", "Bu Ay", "Özel"],
        index=0,  # Varsayılan: Son 7 gün
        horizontal=True
    )
    
    today = date.today()
    
    if quick_select == "Son 7 gün":
        start_date = today - timedelta(days=7)
        end_date = today
    elif quick_select == "Son 30 gün":
        start_date = today - timedelta(days=30)
        end_date = today
    elif quick_select == "Son 90 gün":
        start_date = today - timedelta(days=90)
        end_date = today
    elif quick_select == "Bu Ay":
        start_date = today.replace(day=1)
        end_date = today
    else:  # Özel
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input(
                "Başlangıç",
                value=today - timedelta(days=DEFAULT_DATE_RANGE_DAYS),
                max_value=today
            )
        with col2:
            end_date = st.date_input(
                "Bitiş",
                value=today,
                min_value=start_date,
                max_value=today
            )
    
    # Seçilen aralığı göster
    days_diff = (end_date - start_date).days
    st.sidebar.caption(f"📊 {days_diff} günlük veri gösteriliyor")
    
    return start_date, end_date


def render_platform_filter():
    """
    Sidebar'da platform filtresi render eder
    
    Returns:
        list: Seçilen platform listesi
    """
    st.sidebar.subheader("📱 Platformlar")
    
    # Tüm platformları seç/kaldır
    all_selected = st.sidebar.checkbox("Tümünü Seç", value=True)
    
    if all_selected:
        selected = SUPPORTED_PLATFORMS.copy()
    else:
        selected = []
        for platform in SUPPORTED_PLATFORMS:
            display_name = UTM_SOURCE_MAPPING.get(platform, platform)
            if st.sidebar.checkbox(display_name, value=True, key=f"platform_{platform}"):
                selected.append(platform)
    
    if not selected:
        st.sidebar.warning("⚠️ En az bir platform seçin")
        selected = SUPPORTED_PLATFORMS.copy()
    
    return selected


def render_all_filters():
    """
    Tüm filtreleri render eder
    
    Returns:
        dict: {start_date, end_date, platforms}
    """
    st.sidebar.header("🔍 Filtreler")
    
    start_date, end_date = render_date_filter()
    st.sidebar.divider()
    platforms = render_platform_filter()
    
    st.sidebar.divider()
    
    # Yenile butonu
    if st.sidebar.button("🔄 Verileri Yenile", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "platforms": platforms
    }
