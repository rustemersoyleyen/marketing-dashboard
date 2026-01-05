"""
Database Connection Manager
===========================
MSSQL Server bağlantı yönetimi
"""

import pyodbc
from contextlib import contextmanager
from config.database import get_connection_string


class DatabaseConnection:
    """MSSQL veritabanı bağlantı yöneticisi"""
    
    _connection = None
    
    @classmethod
    def get_connection(cls):
        """Veritabanı bağlantısı döner (singleton pattern)"""
        if cls._connection is None or cls._connection.closed:
            try:
                connection_string = get_connection_string()
                cls._connection = pyodbc.connect(connection_string)
                print("✅ Veritabanı bağlantısı başarılı")
            except pyodbc.Error as e:
                print(f"❌ Veritabanı bağlantı hatası: {e}")
                raise
        return cls._connection
    
    @classmethod
    def close(cls):
        """Bağlantıyı kapatır"""
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
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
