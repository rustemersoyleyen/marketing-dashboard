"""
Google Ads API Configuration
============================
Google Ads API credentials
Streamlit Cloud'da secrets kullanır
"""

import os
import streamlit as st
import tempfile
import yaml

def get_google_ads_config():
    """Google Ads konfigürasyonunu döner"""
    # Streamlit Cloud'da secrets kullan
    if hasattr(st, 'secrets') and 'google_ads' in st.secrets:
        return {
            "developer_token": st.secrets["google_ads"]["developer_token"],
            "client_id": st.secrets["google_ads"]["client_id"],
            "client_secret": st.secrets["google_ads"]["client_secret"],
            "refresh_token": st.secrets["google_ads"]["refresh_token"],
            "login_customer_id": st.secrets["google_ads"].get("login_customer_id", ""),
            "use_proto_plus": True
        }
    
    # Lokal geliştirme - yaml dosyasına bak
    return None

def get_google_ads_yaml_path():
    """Google Ads YAML config path döner veya secrets'tan geçici dosya oluşturur"""
    config = get_google_ads_config()
    
    if config:
        # Secrets'tan geçici YAML dosyası oluştur
        yaml_content = {
            "developer_token": config["developer_token"],
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "refresh_token": config["refresh_token"],
            "login_customer_id": config["login_customer_id"],
            "use_proto_plus": True
        }
        
        # Geçici dosya oluştur
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(yaml_content, temp_file)
        temp_file.close()
        return temp_file.name
    
    # Lokal dosya
    local_path = os.path.join(os.path.dirname(__file__), "google-ads.yaml")
    if os.path.exists(local_path):
        return local_path
    
    return None

# Customer ID
CUSTOMER_ID = "7731368325"
