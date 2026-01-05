"""
Lead Service
============
MemberForm tablosundan lead verilerini çeker
"""

import pandas as pd
from datetime import date
from database.connection import execute_query
from database.queries import (
    LEAD_QUERY,
    LEAD_COUNT_BY_SOURCE_CONTENT,
    LEAD_DAILY_TREND,
    format_sources
)
from config.database import SUPPORTED_PLATFORMS


def get_leads(start_date: date, end_date: date, sources: list = None) -> pd.DataFrame:
    """
    Belirli tarih aralığındaki lead'leri döner
    
    Args:
        start_date: Başlangıç tarihi
        end_date: Bitiş tarihi
        sources: UTM source listesi (varsayılan: tüm desteklenen platformlar)
    
    Returns:
        DataFrame: Lead verileri
    """
    if sources is None:
        sources = SUPPORTED_PLATFORMS
    
    query = LEAD_QUERY.format(sources=format_sources(sources))
    
    try:
        results = execute_query(query, (start_date, end_date))
        df = pd.DataFrame(results)
        
        if df.empty:
            return pd.DataFrame(columns=[
                "MemberId", "UtmSource", "UtmMedium", "UtmTerm", 
                "UtmContent", "CreateDate"
            ])
        
        print(f"✅ Lead Service: {len(df)} lead bulundu")
        return df
        
    except Exception as e:
        print(f"❌ Lead verisi çekme hatası: {e}")
        return pd.DataFrame(columns=[
            "MemberId", "UtmSource", "UtmMedium", "UtmTerm", 
            "UtmContent", "CreateDate"
        ])


def get_lead_count_by_source_content(start_date: date, end_date: date, sources: list = None) -> pd.DataFrame:
    """
    UTM Source ve Content bazlı lead sayılarını döner
    
    Returns:
        DataFrame: UtmSource, UtmContent, LeadCount, FirstLeadDate, LastLeadDate
    """
    if sources is None:
        sources = SUPPORTED_PLATFORMS
    
    query = LEAD_COUNT_BY_SOURCE_CONTENT.format(sources=format_sources(sources))
    
    try:
        results = execute_query(query, (start_date, end_date))
        df = pd.DataFrame(results)
        
        if df.empty:
            return pd.DataFrame(columns=[
                "UtmSource", "UtmContent", "LeadCount", 
                "FirstLeadDate", "LastLeadDate"
            ])
        
        return df
        
    except Exception as e:
        print(f"❌ Lead sayısı çekme hatası: {e}")
        return pd.DataFrame(columns=[
            "UtmSource", "UtmContent", "LeadCount", 
            "FirstLeadDate", "LastLeadDate"
        ])


def get_lead_daily_trend(start_date: date, end_date: date, sources: list = None) -> pd.DataFrame:
    """
    Günlük lead trendi döner
    
    Returns:
        DataFrame: Date, UtmSource, LeadCount
    """
    if sources is None:
        sources = SUPPORTED_PLATFORMS
    
    query = LEAD_DAILY_TREND.format(sources=format_sources(sources))
    
    try:
        results = execute_query(query, (start_date, end_date))
        df = pd.DataFrame(results)
        
        if df.empty:
            return pd.DataFrame(columns=["Date", "UtmSource", "LeadCount"])
        
        return df
        
    except Exception as e:
        print(f"❌ Lead trend verisi çekme hatası: {e}")
        return pd.DataFrame(columns=["Date", "UtmSource", "LeadCount"])


def get_total_leads(start_date: date, end_date: date, sources: list = None) -> int:
    """Toplam lead sayısı döner"""
    df = get_lead_count_by_source_content(start_date, end_date, sources)
    return int(df["LeadCount"].sum()) if not df.empty else 0


def get_leads_by_source(start_date: date, end_date: date) -> dict:
    """
    Platform bazlı lead sayıları döner
    
    Returns:
        dict: {"google": 123, "facebook": 456}
    """
    df = get_lead_count_by_source_content(start_date, end_date)
    
    if df.empty:
        return {source: 0 for source in SUPPORTED_PLATFORMS}
    
    summary = df.groupby("UtmSource")["LeadCount"].sum().to_dict()
    
    # int'e çevir ve eksik platformları 0 ile doldur
    result = {}
    for source in SUPPORTED_PLATFORMS:
        if source in summary:
            result[source] = int(summary[source])
        else:
            result[source] = 0
    
    return result
