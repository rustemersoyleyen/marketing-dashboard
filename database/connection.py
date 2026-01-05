"""
Database Connection Manager
===========================
MSSQL Server bağlantı yönetimi
Streamlit Cloud için pymssql, lokal için pyodbc destekler
"""

import streamlit as st
from contextlib import contextmanager


class DatabaseConnection:
    """MSSQL veritabanı bağlantı yöneticisi"""
    
    _connection = None
    _driver = None  # 'pymssql' veya 'pyodbc'
    
    @classmethod
    def _get_config(cls):
        """Secrets'dan database config alır"""
        if hasattr(st, 'secrets') and 'database' in st.secrets:
            return {
                'server': st.secrets["database"]["server"],
                'database': st.secrets["database"]["database"],
                'username': st.secrets["database"]["username"],
                'password': st.secrets["database"]["password"],
                'driver': st.secrets["database"].get("driver", "ODBC Driver 17 for SQL Server")
            }
        # Fallback
        return {
            'server': 'deep.konusarakogren.com',
            'database': 'MemberPrime',
            'username': 'sa',
            'password': '',
            'driver': 'ODBC Driver 17 for SQL Server'
        }
    
    @classmethod
    def get_connection(cls):
        """Veritabanı bağlantısı döner (singleton pattern)"""
        if cls._connection is not None:
            try:
                # Bağlantının hala açık olup olmadığını kontrol et
                if cls._driver == 'pymssql':
                    cursor = cls._connection.cursor()
                    cursor.execute("SELECT 1")
                    cursor.close()
                else:
                    if not cls._connection.closed:
                        return cls._connection
                return cls._connection
            except:
                cls._connection = None
        
        config = cls._get_config()
        
        # Önce pymssql dene (Streamlit Cloud için ideal)
        try:
            import pymssql
            cls._connection = pymssql.connect(
                server=config['server'],
                user=config['username'],
                password=config['password'],
                database=config['database'],
                charset='utf8'
            )
            cls._driver = 'pymssql'
            print("✅ Veritabanı bağlantısı başarılı (pymssql)")
            return cls._connection
        except Exception as e1:
            print(f"⚠️ pymssql bağlantısı başarısız: {e1}")
        
        # pymssql başarısız olursa pyodbc dene
        try:
            import pyodbc
            connection_string = (
                f"DRIVER={{{config['driver']}}};"
                f"SERVER={config['server']};"
                f"DATABASE={config['database']};"
                f"UID={config['username']};"
                f"PWD={config['password']};"
                f"TrustServerCertificate=yes;"
            )
            cls._connection = pyodbc.connect(connection_string)
            cls._driver = 'pyodbc'
            print("✅ Veritabanı bağlantısı başarılı (pyodbc)")
            return cls._connection
        except Exception as e2:
            print(f"❌ pyodbc bağlantısı da başarısız: {e2}")
            raise Exception(f"Veritabanı bağlantısı kurulamadı. pymssql hatası: {e1}, pyodbc hatası: {e2}")
    
    @classmethod
    def close(cls):
        """Bağlantıyı kapatır"""
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
            cls._driver = None
            print("Veritabanı bağlantısı kapatıldı")


@contextmanager
def get_db_cursor():
    """Context manager ile cursor kullanımı"""
    connection = DatabaseConnection.get_connection()
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()


def execute_query(query, params=None):
    """SQL sorgusu çalıştırır ve sonuçları döner"""
    with get_db_cursor() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results


def test_connection():
    """Bağlantı testi yapar"""
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        return result[0] == 1
    except Exception as e:
        print(f"Bağlantı testi başarısız: {e}")
        return False
