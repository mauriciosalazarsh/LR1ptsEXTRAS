#!/usr/bin/env python3
"""
Aplicación Web Flask COMPLETA para el Parser LR(1)
VERSIÓN FINAL - Todo funciona en una sola ejecución
"""

import os
import sys
import warnings

# CRUCIAL: Configurar matplotlib ANTES de cualquier importación
os.environ['MPLBACKEND'] = 'Agg'
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI, seguro para servidores

# Suprimir warnings molestos
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

from flask import Flask, render_template, request, jsonify, send_file
import json
import tempfile
from datetime import datetime
import threading
import time
import webbrowser

# Importar nuestros módulos
from lr1_parser import LR1Parser
from graph_visualizer_correct import LR1GraphVisualizerCorrect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lr1-parser-utec-2024'

# Instancias globales
parser = LR1Parser()
visualizer = LR1GraphVisualizerCorrect()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/parse_grammar', methods=['POST'])
def parse_grammar():
    """API para procesar gramática CON gráficos"""
    try:
        data = request.get_json()
        grammar_text = data.get('grammar', '').strip()
        
        if not grammar_text:
            return jsonify({
                'success': False,
                'error': 'Por favor ingrese una gramática'
            })
        
        print(f"📝 Procesando gramática...")
        
        # Procesar gramática
        parser.parse_grammar(grammar_text)
        print(f"✅ Gramática procesada con {len(parser.states)} estados")
        
        # Obtener datos
        first_follow = parser.get_first_follow_sets()
        states_info = parser.get_states_info()
        parsing_table = parser.get_parsing_table()
        automaton_data = parser.get_automaton_graph()
        
        print(f"🎨 Generando gráficos...")
        
        # Generar gráficos de forma segura
        try:
            automaton_image = visualizer.create_automaton_graph(
                automaton_data, return_base64=True
            )
            print(f"✅ Gráfico del autómata generado")
        except Exception as e:
            print(f"⚠️  Error en gráfico autómata: {e}")
            automaton_image = None
        
        try:
            # Usar el visualizador original para la tabla
            from graph_visualizer import LR1GraphVisualizer
            table_visualizer = LR1GraphVisualizer()
            table_image = table_visualizer.create_parsing_table_image(
                parsing_table, return_base64=True
            )
            print(f"✅ Gráfico de la tabla generado")
        except Exception as e:
            print(f"⚠️  Error en gráfico tabla: {e}")
            table_image = None
        
        print(f"🎉 Todo completado exitosamente")
        
        return jsonify({
            'success': True,
            'message': 'Gramática procesada exitosamente con gráficos',
            'data': {
                'first_follow': first_follow,
                'states': states_info,
                'parsing_table': parsing_table,
                'automaton_graph': automaton_data,
                'automaton_image': automaton_image,
                'table_image': table_image,
                'num_states': len(states_info),
                'num_terminals': len(parsing_table['terminals']),
                'num_nonterminals': len(parsing_table['non_terminals'])
            }
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al procesar gramática: {str(e)}'
        })

@app.route('/api/parse_string', methods=['POST'])
def parse_string():
    """API para analizar cadena"""
    try:
        data = request.get_json()
        input_string = data.get('string', '').strip()
        
        if not input_string:
            return jsonify({
                'success': False,
                'error': 'Por favor ingrese una cadena a analizar'
            })
        
        if not parser.grammar:
            return jsonify({
                'success': False,
                'error': 'Primero debe procesar una gramática'
            })
        
        print(f"🔍 Analizando cadena: {input_string}")
        
        # Analizar cadena
        result = parser.parse_string(input_string)
        
        status = "ACEPTADA" if result['success'] else "RECHAZADA"
        print(f"📊 Resultado: {status}")
        
        return jsonify({
            'success': True,
            'parsing_result': result
        })
        
    except Exception as e:
        print(f"❌ Error en parsing: {e}")
        return jsonify({
            'success': False,
            'error': f'Error al analizar cadena: {str(e)}'
        })

@app.route('/api/export_graph')
def export_graph():
    """Exportar gráfico del autómata"""
    try:
        if not parser.grammar:
            return jsonify({
                'success': False,
                'error': 'No hay gramática procesada'
            })
        
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix='.png', prefix='automaton_lr1_'
        )
        temp_file.close()
        
        # Generar gráfico
        automaton_data = parser.get_automaton_graph()
        visualizer.create_automaton_graph(automaton_data, output_file=temp_file.name)
        
        # Enviar archivo
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'automaton_lr1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png',
            mimetype='image/png'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al exportar gráfico: {str(e)}'
        })

@app.route('/api/export_table')
def export_table():
    """Exportar tabla de parsing"""
    try:
        if not parser.grammar:
            return jsonify({
                'success': False,
                'error': 'No hay gramática procesada'
            })
        
        # Crear archivo temporal
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix='.png', prefix='parsing_table_lr1_'
        )
        temp_file.close()
        
        # Generar tabla (usar el visualizador original para la tabla)
        from graph_visualizer import LR1GraphVisualizer
        table_visualizer = LR1GraphVisualizer()
        table_data = parser.get_parsing_table()
        table_visualizer.create_parsing_table_image(table_data, output_file=temp_file.name)
        
        # Enviar archivo
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'parsing_table_lr1_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png',
            mimetype='image/png'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al exportar tabla: {str(e)}'
        })

@app.route('/api/examples')
def get_examples():
    """Obtener gramáticas de ejemplo"""
    examples = {
        'arithmetic': {
            'name': 'Expresiones Aritméticas',
            'description': 'Gramática para expresiones con +, *, paréntesis e identificadores',
            'grammar': '''S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id''',
            'test_strings': ['id', 'id + id', 'id + id * id', '( id + id ) * id']
        },
        'simple': {
            'name': 'Gramática Simple',
            'description': 'Gramática básica para pruebas',
            'grammar': '''S -> A B
A -> a
B -> b''',
            'test_strings': ['a b']
        },
        'balanced': {
            'name': 'Paréntesis Balanceados',
            'description': 'Gramática para paréntesis balanceados',
            'grammar': '''S -> ( S )
S -> S S
S -> ε''',
            'test_strings': ['( )', '( ( ) )', '( ) ( )']
        }
    }
    
    return jsonify(examples)

@app.errorhandler(404)
def page_not_found(e):
    """Página de error 404"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message='Página no encontrada'), 404

@app.errorhandler(500)
def internal_error(e):
    """Página de error 500"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message='Error interno del servidor'), 500

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

def open_browser(url):
    """Abre el navegador después de un delay"""
    time.sleep(2)
    try:
        webbrowser.open(url)
        print(f"🌐 Navegador abierto automáticamente")
    except:
        print(f"⚠️  Abre manualmente: {url}")

def main():
    """Función principal mejorada"""
    print("🚀 Parser LR(1) - APLICACIÓN COMPLETA")
    print("=" * 60)
    
    # Crear directorios necesarios
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Buscar puerto libre
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    
    print(f"📍 URL: {url}")
    print(f"🎨 Gráficos: NetworkX + Matplotlib (configurado para servidor)")
    print(f"🐍 Backend: Flask + Python")
    print(f"🌐 Frontend: Bootstrap 5 + JavaScript")
    print(f"🛑 Presiona Ctrl+C para detener")
    print("=" * 60)
    
    # Abrir navegador automáticamente
    browser_thread = threading.Thread(target=open_browser, args=(url,), daemon=True)
    browser_thread.start()
    
    try:
        # Ejecutar Flask con configuración optimizada
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,  # Sin debug para evitar problemas
            threaded=True,
            use_reloader=False  # Sin reloader para evitar problemas
        )
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica que las dependencias estén instaladas:")
        print("   pip install flask matplotlib networkx numpy")

if __name__ == '__main__':
    main()