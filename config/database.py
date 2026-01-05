"""
Database Configuration
======================
MSSQL Server bağlantı ayarları
Streamlit Cloud'da secrets kullanır, lokalde environment variable
"""

import os
import streamlit as st

def get_db_config():
    """Veritabanı konfigürasyonunu döner"""
    # Streamlit Cloud'da secrets kullan
    if hasattr(st, 'secrets') and 'database' in st.secrets:
        return {
            "driver": st.secrets["database"].get("driver", "ODBC Driver 17 for SQL Server"),
            "server": st.secrets["database"]["server"],
            "database": st.secrets["database"]["database"],
            "username": st.secrets["database"]["username"],
            "password": st.secrets["database"]["password"]
        }
    
    # Lokal geliştirme için environment variable veya varsayılan
    return {
        "driver": os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
        "server": os.getenv("DB_SERVER", "deep.konusarakogren.com"),
        "database": os.getenv("DB_DATABASE", "MemberPrime"),
        "username": os.getenv("DB_USERNAME", "sa"),
        "password": os.getenv("DB_PASSWORD", "9FSmGvv!+BHY")
    }

# Lazy loading için config
_db_config = None

def get_config():
    global _db_config
    if _db_config is None:
        _db_config = get_db_config()
    return _db_config

def get_connection_string():
    """ODBC connection string oluşturur"""
    config = get_config()
    return (
        f"DRIVER={{{config['driver']}}};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['username']};"
        f"PWD={config['password']}"
    )

# UTM Source eşleştirme mapping
UTM_SOURCE_MAPPING = {
    "google": "Google Ads",
    "facebook": "Facebook Ads",
    "apple": "Apple Ads"  # Gelecekte eklenecek
}

# Desteklenen platformlar
SUPPORTED_PLATFORMS = ["google", "facebook"]

# Varsayılan tarih aralığı (gün)
DEFAULT_DATE_RANGE_DAYS = 7
