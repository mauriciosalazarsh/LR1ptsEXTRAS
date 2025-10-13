#!/usr/bin/env python3
"""
Aplicación Web Flask para el Parser LR(1)
Compiladores - UTEC - Puntos Extras Examen 2
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from lr1_parser import LR1Parser
from graph_visualizer import LR1GraphVisualizer
import tempfile
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lr1-parser-utec-2024'

# Instancias globales
parser = LR1Parser()
visualizer = LR1GraphVisualizer()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/parse_grammar', methods=['POST'])
def parse_grammar():
    """API para procesar gramática"""
    try:
        data = request.get_json()
        grammar_text = data.get('grammar', '').strip()
        
        if not grammar_text:
            return jsonify({
                'success': False,
                'error': 'Por favor ingrese una gramática'
            })
        
        # Procesar gramática
        parser.parse_grammar(grammar_text)
        
        # Obtener datos
        first_follow = parser.get_first_follow_sets()
        states_info = parser.get_states_info()
        parsing_table = parser.get_parsing_table()
        automaton_data = parser.get_automaton_graph()
        
        # Generar gráficos
        automaton_image = visualizer.create_automaton_graph(
            automaton_data, return_base64=True
        )
        
        table_image = visualizer.create_parsing_table_image(
            parsing_table, return_base64=True
        )
        
        return jsonify({
            'success': True,
            'message': 'Gramática procesada exitosamente',
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
        
        # Analizar cadena
        result = parser.parse_string(input_string)
        
        return jsonify({
            'success': True,
            'parsing_result': result
        })
        
    except Exception as e:
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
        
        # Generar tabla
        table_data = parser.get_parsing_table()
        visualizer.create_parsing_table_image(table_data, output_file=temp_file.name)
        
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

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Iniciando aplicación Parser LR(1)")
    print("📍 URL: http://127.0.0.1:5000")
    print("📍 URL alternativa: http://localhost:5000")
    print("=" * 50)
    
    # Configuración más permisiva para desarrollo
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)