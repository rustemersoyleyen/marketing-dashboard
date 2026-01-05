"""
Revenue Service
===============
Ciro (satış) verilerini çeker
"""

import pandas as pd
from datetime import date
from database.connection import execute_query
from database.queries import (
    REVENUE_QUERY,
    REVENUE_SUMMARY_BY_SOURCE_CONTENT,
    REVENUE_DAILY_TREND,
    format_sources
)
from config.database import SUPPORTED_PLATFORMS


def get_revenue(start_date: date, end_date: date, sources: list = None) -> pd.DataFrame:
    """
    Belirli tarih aralığındaki satış/ciro verilerini döner
    
    Args:
        start_date: Başlangıç tarihi
        end_date: Bitiş tarihi
        sources: UTM source listesi
    
    Returns:
        DataFrame: Ciro verileri
    """
    if sources is None:
        sources = SUPPORTED_PLATFORMS
    
    query = REVENUE_QUERY.format(sources=format_sources(sources))
    
    try:
        results = execute_query(query, (start_date, end_date))
        df = pd.DataFrame(results)
        
        if df.empty:
            return pd.DataFrame(columns=[
                "MemberId", "UtmSource", "UtmMedium", "UtmContent",
                "StudentName", "Product", "TotalPrice", "NetPrice", "OrderDate"
            ])
        
        print(f"✅ Revenue Service: {len(df)} satış kaydı bulundu")
        return df
        
    except Exception as e:
        print(f"❌ Ciro verisi çekme hatası: {e}")
        return pd.DataFrame()


def get_revenue_summary_by_source_content(start_date: date, end_date: date, sources: list = None) -> pd.DataFrame:
    """
    UTM Source ve Content bazlı ciro özeti döner
    
    Returns:
        DataFrame: UtmSource, UtmContent, OrderCount, TotalRevenue, NetRevenue, AvgOrderValue
    """
    if sources is None:
        sources = SUPPORTED_PLATFORMS
    
    query = REVENUE_SUMMARY_BY_SOURCE_CONTENT.format(sources=format_sources(sources))
    
    try:
        results = execute_query(query, (start_date, end_date))
        df = pd.DataFrame(results)
        
        if df.empty:
            return pd.DataFrame(columns=[
                "UtmSource", "UtmContent", "OrderCount", 
                "TotalRevenue", "NetRevenue", "AvgOrderValue"
            ])
        
        return df
        
    except Exception as e:
        print(f"❌ Ciro özeti çekme hatası: {e}")
        return pd.DataFrame()


def get_revenue_daily_trend(start_date: date, end_date: date, sources: list = None) -> pd.DataFrame:
    """
    Günlük ciro trendi döner
    
    Returns:
        DataFrame: Date, UtmSource, TotalRevenue, OrderCount
    """
    if sources is None:
        sources = SUPPORTED_PLATFORMS
    
    query = REVENUE_DAILY_TREND.format(sources=format_sources(sources))
    
    try:
        results = execute_query(query, (start_date, end_date))
        df = pd.DataFrame(results)
        
        if df.empty:
            return pd.DataFrame(columns=["Date", "UtmSource", "TotalRevenue", "OrderCount"])
        
        return df
        
    except Exception as e:
        print(f"❌ Ciro trend verisi çekme hatası: {e}")
        return pd.DataFrame()


def get_total_revenue(start_date: date, end_date: date, sources: list = None) -> float:
    """Toplam ciro döner"""
    df = get_revenue_summary_by_source_content(start_date, end_date, sources)
    return float(df["TotalRevenue"].sum()) if not df.empty else 0.0


def get_revenue_by_source(start_date: date, end_date: date) -> dict:
    """
    Platform bazlı ciro döner
    
    Returns:
        dict: {"google": 12500.00, "facebook": 8900.00}
    """
    df = get_revenue_summary_by_source_content(start_date, end_date)
    
    if df.empty:
        return {source: 0.0 for source in SUPPORTED_PLATFORMS}
    
    summary = df.groupby("UtmSource")["TotalRevenue"].sum().to_dict()
    
    # Decimal'i float'a çevir ve eksik platformları 0 ile doldur
    result = {}
    for source in SUPPORTED_PLATFORMS:
        if source in summary:
            result[source] = float(summary[source])
        else:
            result[source] = 0.0
    
    return result


def get_order_count_by_source(start_date: date, end_date: date) -> dict:
    """
    Platform bazlı sipariş sayısı döner
    
    Returns:
        dict: {"google": 45, "facebook": 32}
    """
    df = get_revenue_summary_by_source_content(start_date, end_date)
    
    if df.empty:
        return {source: 0 for source in SUPPORTED_PLATFORMS}
    
    summary = df.groupby("UtmSource")["OrderCount"].sum().to_dict()
    
    for source in SUPPORTED_PLATFORMS:
        if source not in summary:
            summary[source] = 0
    
    return summary
