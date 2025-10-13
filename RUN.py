#!/usr/bin/env python3
"""
🚀 SCRIPT DE EJECUCIÓN ÚNICO PARA PARSER LR(1)
TODO EN UNO - Instalación automática + Ejecución completa
"""

import subprocess
import sys
import os
import time

def check_python():
    """Verifica la versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instala todas las dependencias automáticamente"""
    print("🔧 Instalando dependencias...")
    
    dependencies = [
        'flask==3.0.0',
        'matplotlib==3.8.2', 
        'networkx==3.2.1',
        'numpy==1.26.2'
    ]
    
    for dep in dependencies:
        print(f"   📦 {dep.split('==')[0]}...", end=' ')
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', dep, '--quiet'],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                print("✅")
            else:
                print("⚠️  (ya instalado)")
        except subprocess.TimeoutExpired:
            print("⏱️  (timeout - continuar)")
        except Exception:
            print("❌")
    
    print("✅ Dependencias listas")

def verify_installation():
    """Verifica que todo esté instalado correctamente"""
    print("🔍 Verificando instalación...")
    
    modules = ['flask', 'matplotlib', 'networkx', 'numpy']
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - FALTA")
            return False
    
    return True

def setup_environment():
    """Configura el entorno para evitar problemas"""
    os.environ['MPLBACKEND'] = 'Agg'
    os.environ['FLASK_ENV'] = 'production'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # Crear directorios necesarios
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("✅ Entorno configurado")

def test_parser():
    """Prueba rápida del parser"""
    print("🧪 Probando parser LR(1)...")
    
    try:
        # Test básico
        from lr1_parser import LR1Parser
        parser = LR1Parser()
        
        grammar = "S -> E\nE -> E + T\nE -> T\nT -> id"
        parser.parse_grammar(grammar)
        
        result = parser.parse_string("id + id")
        if result['success']:
            print("✅ Parser funcionando correctamente")
            return True
        else:
            print("❌ Error en parsing")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_graphics():
    """Prueba la generación de gráficos"""
    print("🎨 Probando generación de gráficos...")
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        
        from lr1_parser import LR1Parser
        from graph_visualizer import LR1GraphVisualizer
        
        parser = LR1Parser()
        visualizer = LR1GraphVisualizer()
        
        grammar = "S -> E\nE -> id"
        parser.parse_grammar(grammar)
        
        automaton_data = parser.get_automaton_graph()
        image_b64 = visualizer.create_automaton_graph(automaton_data, return_base64=True)
        
        if len(image_b64) > 1000:  # Imagen válida
            print("✅ Gráficos funcionando correctamente")
            return True
        else:
            print("❌ Gráfico muy pequeño")
            return False
            
    except Exception as e:
        print(f"❌ Error en gráficos: {e}")
        return False

def run_application():
    """Ejecuta la aplicación completa"""
    print("🚀 Iniciando aplicación completa...")
    print("=" * 60)
    
    try:
        # Importar y ejecutar aplicación
        from app_complete import main
        main()
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida")
    except Exception as e:
        print(f"❌ Error al ejecutar: {e}")
        print("\n💡 Alternativa - ejecutar solo el parser:")
        print("   python3 lr1_parser.py")

def main():
    """Función principal que hace TODO"""
    print("🎯 PARSER LR(1) - EJECUCIÓN COMPLETA")
    print("=" * 60)
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verificaciones
    if not check_python():
        return
    
    # Instalación automática
    install_dependencies()
    
    if not verify_installation():
        print("❌ Falló la instalación de dependencias")
        return
    
    # Configuración
    setup_environment()
    
    # Pruebas
    if not test_parser():
        print("❌ Parser no funciona")
        return
    
    if not test_graphics():
        print("❌ Gráficos no funcionan")
        return
    
    print("🎉 TODO LISTO - Ejecutando aplicación completa...")
    print()
    
    # Ejecutar aplicación
    run_application()

if __name__ == "__main__":
    main()