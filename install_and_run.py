#!/usr/bin/env python3
"""
Script para instalar dependencias y ejecutar el Parser LR(1)
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala las dependencias necesarias"""
    print("🔧 Instalando dependencias...")
    
    packages = [
        'flask',
        'matplotlib',
        'networkx',
        'numpy'
    ]
    
    for package in packages:
        print(f"Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError:
            print(f"❌ Error al instalar {package}")
            return False
    
    print("✅ Dependencias instaladas correctamente")
    return True

def test_parser():
    """Prueba el parser LR(1)"""
    print("\n🧪 Probando Parser LR(1)...")
    
    try:
        from lr1_parser import LR1Parser
        
        parser = LR1Parser()
        grammar = """
S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
"""
        
        parser.parse_grammar(grammar)
        result = parser.parse_string("id + id * id")
        
        if result['success']:
            print("✅ Parser funcionando correctamente")
            return True
        else:
            print("❌ Error en el parser")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_app():
    """Ejecuta la aplicación Flask"""
    print("\n🚀 Iniciando aplicación web...")
    print("📍 La aplicación estará disponible en: http://127.0.0.1:5000")
    print("🛑 Presiona Ctrl+C para detener")
    
    try:
        # Configurar variables de entorno
        import os
        os.environ['FLASK_ENV'] = 'development'
        
        # Importar y ejecutar app
        from app import app
        app.run(debug=False, host='127.0.0.1', port=5000, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida")
    except Exception as e:
        print(f"❌ Error al ejecutar aplicación: {e}")
        print("💡 Intenta ejecutar: python3 run_server.py")

def main():
    print("🎯 Parser LR(1) - Setup y Ejecución")
    print("=" * 50)
    
    # Verificar si las dependencias están instaladas
    try:
        import flask, matplotlib, networkx, numpy
        print("✅ Dependencias ya instaladas")
    except ImportError:
        if not install_requirements():
            return
    
    # Probar el parser
    if not test_parser():
        return
    
    print("\n" + "=" * 50)
    print("🎉 Todo listo para usar!")
    print("\nOpciones:")
    print("1. Ejecutar aplicación web (Flask)")
    print("2. Solo probar parser en consola")
    print("3. Salir")
    
    while True:
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == '1':
            run_app()
            break
        elif choice == '2':
            # Ejecutar solo pruebas
            os.system('python3 lr1_parser.py')
            break
        elif choice == '3':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()