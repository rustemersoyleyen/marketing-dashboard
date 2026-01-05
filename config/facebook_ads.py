"""
Facebook Ads API Configuration
==============================
Facebook Ads API credentials
Streamlit Cloud'da secrets kullanır
"""

import os
import streamlit as st

def get_facebook_config():
    """Facebook Ads konfigürasyonunu döner"""
    # Streamlit Cloud'da secrets kullan
    if hasattr(st, 'secrets') and 'facebook_ads' in st.secrets:
        return {
            "app_id": st.secrets["facebook_ads"]["app_id"],
            "app_secret": st.secrets["facebook_ads"]["app_secret"],
            "access_token": st.secrets["facebook_ads"]["access_token"],
            "ad_account_id": st.secrets["facebook_ads"]["ad_account_id"]
        }
    
    # Lokal geliştirme için environment variable veya varsayılan
    return {
        "app_id": os.getenv("FB_APP_ID", "813584908341021"),
        "app_secret": os.getenv("FB_APP_SECRET", "77758fa9b6d9e6be5516470d0608ee19"),
        "access_token": os.getenv("FB_ACCESS_TOKEN", "EAALj8390zx0BQIOamy1Ii3UWnjeMgHFFHPnTFnm8drQ3iXgJfwi82oBakM9uyf429Uu5fAKUUZBMZBAMw7EqVRyKx5RkXbGKNXVqzIcdTQkJhZB9VCjudsdH9ZBjzIiFtQkSYY1zep7yVDLAuZCvOog4703Cnvca3xQUMeZC8YGY4ZBHZBmj3a8lW7fIIjycmtIRDUwgnz4GMYWNFQQQ6Cty"),
        "ad_account_id": os.getenv("FB_AD_ACCOUNT_ID", "act_76604119")
    }

# Lazy loading
_fb_config = None

def get_config():
    global _fb_config
    if _fb_config is None:
        _fb_config = get_facebook_config()
    return _fb_config

# Backward compatibility
FACEBOOK_ADS_CONFIG = None

def init_config():
    global FACEBOOK_ADS_CONFIG
    FACEBOOK_ADS_CONFIG = get_config()
    return FACEBOOK_ADS_CONFIG
