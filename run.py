"""
Marketing Dashboard - Run Script
================================
Dashboard'u başlatmak için kullanılır
"""

import subprocess
import sys
import os

def main():
    """Dashboard'u başlatır"""
    
    # Proje dizinine geç
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Streamlit uygulamasını başlat
    app_path = os.path.join(project_dir, "dashboard", "app.py")
    
    print("🚀 Marketing Dashboard başlatılıyor...")
    print(f"📁 Proje dizini: {project_dir}")
    print(f"📊 Uygulama: {app_path}")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            app_path,
            "--server.port=8501",
            "--server.headless=true"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard kapatıldı")
    except Exception as e:
        print(f"❌ Hata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
