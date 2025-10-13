#!/usr/bin/env python3
"""
Servidor simple para el Parser LR(1) que evita problemas de permisos
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import flask
        import matplotlib
        import networkx
        import numpy
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("🔧 Instalando dependencias...")
        return install_dependencies()

def install_dependencies():
    """Instala las dependencias necesarias"""
    packages = ['flask', 'matplotlib', 'networkx', 'numpy']
    
    for package in packages:
        try:
            print(f"📦 Instalando {package}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package, '--user'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"❌ Error al instalar {package}")
            return False
    
    print("✅ Dependencias instaladas correctamente")
    return True

def find_free_port():
    """Encuentra un puerto libre"""
    import socket
    
    ports_to_try = [5000, 5001, 5002, 8000, 8080, 3000]
    
    for port in ports_to_try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    
    return 5000  # Fallback

def run_simple_server():
    """Ejecuta un servidor HTTP simple para desarrollo"""
    try:
        import http.server
        import socketserver
        import threading
        
        port = find_free_port()
        
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=os.getcwd(), **kwargs)
            
            def do_GET(self):
                if self.path == '/' or self.path == '/index.html':
                    self.path = '/demo.html'
                return super().do_GET()
        
        with socketserver.TCPServer(("127.0.0.1", port), CustomHandler) as httpd:
            print(f"🌐 Servidor simple iniciado en http://127.0.0.1:{port}")
            print("📝 Versión de demostración (solo frontend)")
            print("🛑 Presiona Ctrl+C para detener")
            
            # Abrir navegador automáticamente
            threading.Timer(1.5, lambda: webbrowser.open(f'http://127.0.0.1:{port}')).start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")

def run_flask_app():
    """Ejecuta la aplicación Flask principal"""
    try:
        # Configurar variables de entorno para evitar problemas
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = '1'
        
        print("🚀 Iniciando servidor Flask...")
        
        # Importar después de configurar el entorno
        from app import app
        
        port = find_free_port()
        
        print(f"📍 URL: http://127.0.0.1:{port}")
        print("🛑 Presiona Ctrl+C para detener")
        
        # Abrir navegador automáticamente
        import threading
        threading.Timer(2.0, lambda: webbrowser.open(f'http://127.0.0.1:{port}')).start()
        
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,  # Cambiar a False para evitar problemas
            threaded=True,
            use_reloader=False
        )
        
    except Exception as e:
        print(f"❌ Error al ejecutar Flask: {e}")
        print("🔄 Intentando con servidor simple...")
        return False
    
    return True

def create_demo_html():
    """Crea una página de demostración independiente"""
    demo_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parser LR(1) - Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 0;
        }
        .feature-card {
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <div class="hero-section">
        <div class="container text-center">
            <h1 class="display-4 fw-bold mb-3">
                <i class="fas fa-cogs me-3"></i>Parser LR(1)
            </h1>
            <p class="lead mb-4">
                Analizador sintáctico LR(1) completo implementado en Python
            </p>
            <div class="alert alert-warning d-inline-block">
                <i class="fas fa-info-circle me-2"></i>
                <strong>Modo Demo:</strong> Para funcionalidad completa, ejecuta <code>python3 app.py</code>
            </div>
        </div>
    </div>

    <div class="container py-5">
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-cogs fa-3x text-primary mb-3"></i>
                        <h5 class="card-title">Algoritmo LR(1)</h5>
                        <p class="card-text">Implementación completa del algoritmo LR(1) con conjuntos FIRST, FOLLOW y construcción de autómata.</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-project-diagram fa-3x text-success mb-3"></i>
                        <h5 class="card-title">Visualización</h5>
                        <p class="card-text">Gráficos del autómata generados con NetworkX y Matplotlib de alta calidad.</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <i class="fas fa-globe fa-3x text-info mb-3"></i>
                        <h5 class="card-title">Interfaz Web</h5>
                        <p class="card-text">Interfaz moderna con Flask, Bootstrap 5 y JavaScript interactivo.</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-5">
            <div class="col-lg-8 mx-auto">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h4 class="mb-0"><i class="fas fa-terminal me-2"></i>Instrucciones de Ejecución</h4>
                    </div>
                    <div class="card-body">
                        <h6><i class="fas fa-rocket me-2"></i>Opción 1: Script Automático</h6>
                        <pre class="bg-light p-3 rounded"><code>python3 install_and_run.py</code></pre>
                        
                        <h6 class="mt-4"><i class="fas fa-wrench me-2"></i>Opción 2: Manual</h6>
                        <pre class="bg-light p-3 rounded"><code># Instalar dependencias
pip install flask matplotlib networkx numpy

# Ejecutar aplicación
python3 app.py</code></pre>
                        
                        <h6 class="mt-4"><i class="fas fa-flask me-2"></i>Opción 3: Solo Testing</h6>
                        <pre class="bg-light p-3 rounded"><code># Probar algoritmo
python3 lr1_parser.py

# Probar visualización
python3 graph_visualizer.py</code></pre>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-5">
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0"><i class="fas fa-check-circle me-2"></i>Características</h5>
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">✅ Algoritmo LR(1) completo</li>
                            <li class="list-group-item">✅ Conjuntos FIRST y FOLLOW</li>
                            <li class="list-group-item">✅ Autómata visualizado</li>
                            <li class="list-group-item">✅ Tabla ACTION/GOTO</li>
                            <li class="list-group-item">✅ Análisis con traza</li>
                            <li class="list-group-item">✅ Exportación PNG</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-header bg-warning text-white">
                        <h5 class="mb-0"><i class="fas fa-code me-2"></i>Ejemplo de Gramática</h5>
                    </div>
                    <div class="card-body">
                        <pre class="bg-light p-3 rounded font-monospace"><code>S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id</code></pre>
                        <p class="mt-3"><strong>Cadenas de prueba:</strong></p>
                        <ul>
                            <li><code>id</code></li>
                            <li><code>id + id</code></li>
                            <li><code>id + id * id</code></li>
                            <li><code>( id + id ) * id</code></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container text-center">
            <h5>Parser LR(1) - Compiladores UTEC</h5>
            <p class="mb-0">Implementación completa en Python - Octubre 2024</p>
            <small class="text-muted">🐍 Flask + NetworkX + Matplotlib + Bootstrap 5</small>
        </div>
    </footer>
</body>
</html>"""
    
    with open('demo.html', 'w', encoding='utf-8') as f:
        f.write(demo_content)
    
    print("📄 Página de demostración creada: demo.html")

def main():
    print("🎯 Parser LR(1) - Servidor de Desarrollo")
    print("=" * 50)
    
    # Cambiar al directorio del script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ No se pudieron instalar las dependencias")
        return
    
    # Crear página de demo como fallback
    create_demo_html()
    
    print("\nSelecciona una opción:")
    print("1. 🚀 Ejecutar aplicación completa (Flask)")
    print("2. 🌐 Servidor simple (solo demo)")
    print("3. 🧪 Solo testing en consola")
    print("4. 🛠️ Instalar dependencias")
    
    while True:
        try:
            choice = input("\n👉 Elige una opción (1-4): ").strip()
            
            if choice == '1':
                if not run_flask_app():
                    print("🔄 Ejecutando servidor simple como alternativa...")
                    run_simple_server()
                break
            
            elif choice == '2':
                run_simple_server()
                break
            
            elif choice == '3':
                print("🧪 Ejecutando pruebas del parser...")
                os.system('python3 lr1_parser.py')
                break
            
            elif choice == '4':
                install_dependencies()
                continue
            
            else:
                print("❌ Opción inválida, intenta de nuevo")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()