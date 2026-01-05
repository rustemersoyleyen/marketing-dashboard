"""
Facebook Ads API Connector
==========================
Facebook Ads API'den kampanya verilerini çeker
"""

import pandas as pd
from datetime import date
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from config.facebook_ads import get_config


def get_account():
    """Facebook Ads hesabına bağlanır"""
    try:
        config = get_config()
        FacebookAdsApi.init(
            config["app_id"],
            config["app_secret"],
            config["access_token"]
        )
        account = AdAccount(config["ad_account_id"])
        
        # Hesap testi
        account_info = account.api_get(fields=['name', 'currency', 'account_status'])
        print(f"✅ Facebook Ads bağlantısı başarılı: {account_info.get('name', 'N/A')}")
        
        return account
    except Exception as e:
        print(f"❌ Facebook Ads bağlantı hatası: {e}")
        raise


def fetch_campaign_data(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Facebook Ads'den kampanya verilerini çeker
    
    Args:
        start_date: Başlangıç tarihi
        end_date: Bitiş tarihi
    
    Returns:
        DataFrame: Kampanya verileri (source, content, spend, clicks, conversions, impressions)
    """
    try:
        account = get_account()
        
        params = {
            'time_range': {
                'since': str(start_date),
                'until': str(end_date)
            },
            'time_increment': 1,  # Günlük
            'level': 'campaign',  # Kampanya bazlı
        }
        
        fields = [
            AdsInsights.Field.date_start,
            AdsInsights.Field.campaign_id,
            AdsInsights.Field.campaign_name,
            AdsInsights.Field.spend,
            AdsInsights.Field.impressions,
            AdsInsights.Field.clicks,
            AdsInsights.Field.actions,
        ]
        
        insights = account.get_insights(fields=fields, params=params)
        
        data = []
        for insight in insights:
            campaign_name = insight.get('campaign_name', '')
            
            # Dönüşümleri hesapla
            conversions = 0
            if insight.get('actions'):
                for action in insight.get('actions'):
                    if action.get('action_type') in ['purchase', 'lead', 'complete_registration', 'omni_purchase']:
                        conversions += int(action.get('value', 0))
            
            # Kampanya adından UTM content çıkar
            utm_content = extract_utm_content(campaign_name)
            
            data.append({
                "date": insight.get('date_start'),
                "source": "facebook",
                "campaign_id": insight.get('campaign_id'),
                "campaign_name": campaign_name,
                "utm_content": utm_content,
                "spend": float(insight.get('spend', 0)),
                "impressions": int(insight.get('impressions', 0)),
                "clicks": int(insight.get('clicks', 0)),
                "conversions": conversions
            })
        
        df = pd.DataFrame(data)
        
        if df.empty:
            print("⚠️ Facebook Ads'den veri alınamadı")
            return pd.DataFrame(columns=[
                "date", "source", "campaign_id", "campaign_name",
                "utm_content", "spend", "impressions", "clicks", "conversions"
            ])
        
        print(f"✅ Facebook Ads: {len(df)} satır veri alındı")
        return df
        
    except Exception as e:
        print(f"❌ Facebook Ads veri çekme hatası: {e}")
        return pd.DataFrame()


def extract_utm_content(campaign_name: str) -> str:
    """
    Kampanya adından UTM content değerini çıkarır
    
    Kampanya isimlendirme kurallarınıza göre bu fonksiyonu özelleştirin.
    """
    if not campaign_name:
        return ""
    
    return campaign_name


def get_spend_summary(start_date: date, end_date: date) -> dict:
    """
    Belirli tarih aralığı için harcama özeti döner
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
