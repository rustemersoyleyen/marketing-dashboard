"""
Ad Spend Service
================
Tüm reklam platformlarından harcama verilerini birleştirir
"""

import pandas as pd
from datetime import date
from connectors import google_ads, facebook_ads, apple_ads
from config.database import SUPPORTED_PLATFORMS


def get_all_platform_data(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Tüm platformlardan reklam verilerini çeker ve birleştirir
    
    Returns:
        DataFrame: Birleştirilmiş platform verileri
    """
    all_data = []
    
    # Google Ads
    if "google" in SUPPORTED_PLATFORMS:
        try:
            google_df = google_ads.fetch_campaign_data(start_date, end_date)
            if not google_df.empty:
                all_data.append(google_df)
        except Exception as e:
            print(f"⚠️ Google Ads verisi alınamadı: {e}")
    
    # Facebook Ads
    if "facebook" in SUPPORTED_PLATFORMS:
        try:
            facebook_df = facebook_ads.fetch_campaign_data(start_date, end_date)
            if not facebook_df.empty:
                all_data.append(facebook_df)
        except Exception as e:
            print(f"⚠️ Facebook Ads verisi alınamadı: {e}")
    
    # Apple Ads (placeholder)
    if "apple" in SUPPORTED_PLATFORMS:
        try:
            apple_df = apple_ads.fetch_campaign_data(start_date, end_date)
            if not apple_df.empty:
                all_data.append(apple_df)
        except Exception as e:
            print(f"⚠️ Apple Ads verisi alınamadı: {e}")
    
    if not all_data:
        return pd.DataFrame(columns=[
            "date", "source", "campaign_id", "campaign_name",
            "utm_content", "spend", "impressions", "clicks", "conversions"
        ])
    
    return pd.concat(all_data, ignore_index=True)


def get_total_spend(start_date: date, end_date: date) -> float:
    """Tüm platformların toplam harcaması"""
    df = get_all_platform_data(start_date, end_date)
    return float(df["spend"].sum()) if not df.empty else 0.0


def get_spend_by_source(start_date: date, end_date: date) -> dict:
    """
    Platform bazlı harcama döner
    
    Returns:
        dict: {"google": 5000.00, "facebook": 3500.00}
    """
    df = get_all_platform_data(start_date, end_date)
    
    if df.empty:
        return {source: 0.0 for source in SUPPORTED_PLATFORMS}
    
    summary = df.groupby("source")["spend"].sum().to_dict()
    
    for source in SUPPORTED_PLATFORMS:
        if source not in summary:
            summary[source] = 0.0
    
    return summary


def get_spend_by_content(start_date: date, end_date: date) -> pd.DataFrame:
    """
    UTM Content bazlı harcama döner
    
    Returns:
        DataFrame: source, utm_content, spend, clicks, impressions, conversions
    """
    df = get_all_platform_data(start_date, end_date)
    
    if df.empty:
        return pd.DataFrame(columns=[
            "source", "utm_content", "spend", "clicks", "impressions", "conversions"
        ])
    
    summary = df.groupby(["source", "utm_content"]).agg({
        "spend": "sum",
        "clicks": "sum",
        "impressions": "sum",
        "conversions": "sum"
    }).reset_index()
    
    return summary.sort_values("spend", ascending=False)


def get_daily_spend(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Günlük harcama trendi döner
    
    Returns:
        DataFrame: date, source, spend, clicks, impressions
    """
    df = get_all_platform_data(start_date, end_date)
    
    if df.empty:
        return pd.DataFrame(columns=["date", "source", "spend", "clicks", "impressions"])
    
    daily = df.groupby(["date", "source"]).agg({
        "spend": "sum",
        "clicks": "sum",
        "impressions": "sum",
        "conversions": "sum"
    }).reset_index()
    
    return daily.sort_values("date")


def get_campaign_performance(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Kampanya performans tablosu döner
    
    Returns:
        DataFrame: source, campaign_name, utm_content, spend, clicks, impressions, conversions, ctr, cpc
    """
    df = get_all_platform_data(start_date, end_date)
    
    if df.empty:
        return pd.DataFrame(columns=[
            "source", "campaign_name", "utm_content", 
            "spend", "clicks", "impressions", "conversions", "ctr", "cpc"
        ])
    
    campaign = df.groupby(["source", "campaign_name", "utm_content"]).agg({
        "spend": "sum",
        "clicks": "sum",
        "impressions": "sum",
        "conversions": "sum"
    }).reset_index()
    
    # CTR ve CPC hesapla
    campaign["ctr"] = (campaign["clicks"] / campaign["impressions"] * 100).fillna(0).round(2)
    campaign["cpc"] = (campaign["spend"] / campaign["clicks"]).fillna(0).round(2)
    
    return campaign.sort_values("spend", ascending=False)
