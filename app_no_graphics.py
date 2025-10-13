#!/usr/bin/env python3
"""
Aplicación Web Flask para el Parser LR(1) - Versión sin gráficos
Para evitar problemas de matplotlib en macOS
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from lr1_parser import LR1Parser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lr1-parser-utec-2024'

# Instancia global
parser = LR1Parser()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index_simple.html')

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
        
        # Obtener datos (sin gráficos)
        first_follow = parser.get_first_follow_sets()
        states_info = parser.get_states_info()
        parsing_table = parser.get_parsing_table()
        
        return jsonify({
            'success': True,
            'message': 'Gramática procesada exitosamente',
            'data': {
                'first_follow': first_follow,
                'states': states_info,
                'parsing_table': parsing_table,
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

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Iniciando Parser LR(1) (Versión sin gráficos)")
    print("📍 URL: http://127.0.0.1:5000")
    print("✅ Funcionalidad completa excepto gráficos de matplotlib")
    print("🛑 Presiona Ctrl+C para detener")
    print("=" * 60)
    
    app.run(debug=False, host='127.0.0.1', port=5000, threaded=True, use_reloader=False)