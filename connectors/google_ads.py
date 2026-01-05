"""
Google Ads API Connector
========================
Google Ads API'den kampanya verilerini çeker
"""

import os
import pandas as pd
from datetime import date, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# Google Ads Customer ID
CUSTOMER_ID = "7731368325"

# Config dosyası yolu
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "google-ads.yaml")


def get_client():
    """Google Ads API client döner"""
    try:
        client = GoogleAdsClient.load_from_storage(CONFIG_PATH)
        return client
    except Exception as e:
        print(f"❌ Google Ads bağlantı hatası: {e}")
        raise


def fetch_campaign_data(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Google Ads'den kampanya verilerini çeker
    
    Args:
        start_date: Başlangıç tarihi
        end_date: Bitiş tarihi
    
    Returns:
        DataFrame: Kampanya verileri (source, content, spend, clicks, conversions, impressions)
    """
    try:
        client = get_client()
        ga_service = client.get_service("GoogleAdsService")
        
        # GAQL sorgusu - Reklam bazlı veriler (final_urls dahil)
        query = f"""
            SELECT
                segments.date,
                campaign.name,
                campaign.id,
                ad_group.name,
                ad_group_ad.ad.final_urls,
                metrics.cost_micros,
                metrics.impressions,
                metrics.clicks,
                metrics.conversions
            FROM ad_group_ad
            WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
              AND campaign.status != 'REMOVED'
              AND ad_group.status != 'REMOVED'
              AND ad_group_ad.status != 'REMOVED'
            ORDER BY segments.date ASC
        """
        
        response = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        
        data = []
        for batch in response:
            for row in batch.results:
                campaign_name = row.campaign.name
                ad_group_name = row.ad_group.name if row.ad_group else ""
                
                # Final URL'lerden utm_content çıkar
                final_urls = list(row.ad_group_ad.ad.final_urls) if row.ad_group_ad.ad.final_urls else []
                utm_content = extract_utm_content_from_url(final_urls[0] if final_urls else "")
                
                # URL'den bulunamadıysa kampanya adını kullan
                if not utm_content:
                    utm_content = campaign_name
                
                data.append({
                    "date": row.segments.date,
                    "source": "google",
                    "campaign_id": row.campaign.id,
                    "campaign_name": campaign_name,
                    "ad_group_name": ad_group_name,
                    "final_url": final_urls[0] if final_urls else "",
                    "utm_content": utm_content,
                    "spend": row.metrics.cost_micros / 1_000_000,
                    "impressions": row.metrics.impressions,
                    "clicks": row.metrics.clicks,
                    "conversions": row.metrics.conversions
                })
        
        df = pd.DataFrame(data)
        
        if df.empty:
            print("⚠️ Google Ads'den veri alınamadı")
            return pd.DataFrame(columns=[
                "date", "source", "campaign_id", "campaign_name", 
                "utm_content", "spend", "impressions", "clicks", "conversions"
            ])
        
        print(f"✅ Google Ads: {len(df)} satır veri alındı")
        return df
        
    except GoogleAdsException as ex:
        print(f"❌ Google Ads API Hatası!")
        print(f"   Request ID: {ex.request_id}")
        for error in ex.failure.errors:
            print(f"   Hata: {error.message}")
        return pd.DataFrame()
    
    except Exception as e:
        print(f"❌ Google Ads veri çekme hatası: {e}")
        return pd.DataFrame()


def extract_utm_content_from_url(url: str) -> str:
    """
    URL'den utm_content parametresini çıkarır
    
    Args:
        url: Reklam final URL'si
        
    Returns:
        str: utm_content değeri veya boş string
    """
    if not url:
        return ""
    
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # utm_content parametresini al
        if 'utm_content' in params:
            return params['utm_content'][0]
        
        # Alternatif olarak content parametresini dene
        if 'content' in params:
            return params['content'][0]
            
        return ""
    except Exception:
        return ""


def extract_utm_content(campaign_name: str) -> str:
    """
    Kampanya adından UTM content değerini çıkarır (fallback)
    
    Kampanya isimlendirme kurallarınıza göre bu fonksiyonu özelleştirin.
    """
    if not campaign_name:
        return ""
    
    return campaign_name


def get_spend_summary(start_date: date, end_date: date) -> dict:
    """
    Belirli tarih aralığı için harcama özeti döner
    
    Returns:
        dict: {total_spend, total_clicks, total_impressions, total_conversions}
    """
    df = fetch_campaign_data(start_date, end_date)
    
    if df.empty:
        return {
            "total_spend": 0,
            "total_clicks": 0,
            "total_impressions": 0,
            "total_conversions": 0
        }
    
    return {
        "total_spend": df["spend"].sum(),
        "total_clicks": df["clicks"].sum(),
        "total_impressions": df["impressions"].sum(),
        "total_conversions": df["conversions"].sum()
    }


def get_daily_spend(start_date: date, end_date: date) -> pd.DataFrame:
    """Günlük harcama verisi döner"""
    df = fetch_campaign_data(start_date, end_date)
    
    if df.empty:
        return pd.DataFrame(columns=["date", "spend", "clicks", "impressions", "conversions"])
    
    daily = df.groupby("date").agg({
        "spend": "sum",
        "clicks": "sum",
        "impressions": "sum",
        "conversions": "sum"
    }).reset_index()
    
    return daily


def get_campaign_spend(start_date: date, end_date: date) -> pd.DataFrame:
    """Kampanya bazlı harcama verisi döner"""
    df = fetch_campaign_data(start_date, end_date)
    
    if df.empty:
        return pd.DataFrame(columns=[
            "campaign_name", "utm_content", "spend", "clicks", "impressions", "conversions"
        ])
    
    campaign = df.groupby(["campaign_name", "utm_content"]).agg({
        "spend": "sum",
        "clicks": "sum",
        "impressions": "sum",
        "conversions": "sum"
    }).reset_index()
    
    return campaign.sort_values("spend", ascending=False)
