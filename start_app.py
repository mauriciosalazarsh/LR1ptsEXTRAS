#!/usr/bin/env python3
"""
Script simple para iniciar la aplicación Flask
"""

import os
import sys
import webbrowser
import threading
import time

def start_flask_app():
    """Inicia la aplicación Flask"""
    try:
        # Configurar entorno
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = '0'  # Deshabilitar debug para evitar problemas
        
        print("🚀 Iniciando Parser LR(1)...")
        print("📍 URL: http://127.0.0.1:5000")
        print("🔄 Abriendo navegador automáticamente...")
        print("🛑 Presiona Ctrl+C para detener")
        print("=" * 50)
        
        # Importar la aplicación
        from app import app
        
        # Abrir navegador después de 2 segundos
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open('http://127.0.0.1:5000')
                print("🌐 Navegador abierto")
            except:
                print("⚠️  No se pudo abrir el navegador automáticamente")
                print("📍 Abre manualmente: http://127.0.0.1:5000")
        
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Ejecutar Flask
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            threaded=True,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Instala las dependencias: pip install flask matplotlib networkx numpy")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("💡 Verifica que estés en el directorio correcto")

if __name__ == "__main__":
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    start_flask_app()