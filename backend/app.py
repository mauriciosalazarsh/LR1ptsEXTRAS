#!/usr/bin/env python3
"""
Aplicación Web Flask para visualización de Autómata LR(1)
Compiladores - UTEC - Puntos Extras Examen 2
"""

import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from parser.lr1_parser import LR1Parser
from parser.lalr1_parser import LALR1Parser
from parser.visualizer_graphviz import LR1GraphvizVisualizer
import base64
from io import BytesIO

# Configurar rutas para static (almacenar imágenes generadas)
static_dir = os.path.join(os.path.dirname(__file__), '../frontend/static')

app = Flask(__name__, static_folder=static_dir)
app.config['SECRET_KEY'] = 'lr1-parser-utec-2024'

# Configurar CORS para permitir peticiones desde React (Vite usa puerto 5173)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Parser global
parser = None
graphviz_viz = None

# Gramática por defecto
DEFAULT_GRAMMAR = """S -> q * A * B * C
A -> a
A -> b * b * D
B -> a
B -> ε
C -> b
C -> ε
D -> C
D -> ε"""


def init_parser(grammar_text, parser_type='LR1'):
    """Inicializa el parser con una gramática"""
    global parser, graphviz_viz

    if parser_type.upper() == 'LALR1' or parser_type.upper() == 'LALR(1)':
        parser = LALR1Parser()
    else:
        parser = LR1Parser()

    parser.parse_grammar(grammar_text)

    graphviz_viz = LR1GraphvizVisualizer(parser)

    return parser


@app.route('/')
def index():
    """Endpoint raíz - información de la API"""
    return jsonify({
        'message': 'LR(1) Parser API - Backend para visualizador React',
        'version': '1.0',
        'endpoints': {
            'build_parser': '/api/build_parser',
            'generate_graphviz': '/api/generate_graphviz',
            'parse_string': '/api/parse_string',
            'get_states': '/api/get_states',
            'get_parsing_table': '/api/get_parsing_table'
        }
    })


@app.route('/api/build_parser', methods=['POST'])
def build_parser():
    """Construye el parser LR(1) o LALR(1) con la gramática dada"""
    try:
        data = request.json
        grammar = data.get('grammar', DEFAULT_GRAMMAR)
        parser_type = data.get('parser_type', 'LR1')

        # Construir parser
        init_parser(grammar, parser_type)

        # Obtener información
        info = graphviz_viz.get_automaton_info()

        # Obtener conjuntos FIRST y FOLLOW
        first_sets = {}
        follow_sets = {}

        for nt in sorted(parser.non_terminals):
            first_sets[nt] = sorted(list(parser.first_sets.get(nt, set())))
            follow_sets[nt] = sorted(list(parser.follow_sets.get(nt, set())))

        # Obtener producciones
        productions = []
        for i, prod in enumerate(parser.grammar):
            productions.append({
                'number': i,
                'text': str(prod)
            })

        # Determinar tipo de parser usado
        parser_type_str = 'LALR(1)' if isinstance(parser, LALR1Parser) else 'LR(1)'

        return jsonify({
            'success': True,
            'parser_type': parser_type_str,
            'info': info,
            'first_sets': first_sets,
            'follow_sets': follow_sets,
            'productions': productions
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/generate_graphviz', methods=['POST'])
def generate_graphviz():
    """Genera visualización con Graphviz"""
    try:
        if parser is None:
            return jsonify({
                'success': False,
                'error': 'Parser no inicializado. Primero construya el parser.'
            }), 400

        # Generar visualización
        static_path = os.path.join(os.path.dirname(__file__), '../frontend/static')
        filename = os.path.join(static_path, 'automata_graphviz')
        os.makedirs(static_path, exist_ok=True)

        graphviz_viz.visualize(filename, output_format='svg', view_file=False)

        # Leer el archivo SVG
        with open(f'{filename}.svg', 'r') as f:
            svg_content = f.read()

        return jsonify({
            'success': True,
            'svg': svg_content,
            'png_url': f'/static/automata_graphviz.png'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/parse_string', methods=['POST'])
def parse_string():
    """Analiza una cadena con el parser LR(1)"""
    try:
        if parser is None:
            return jsonify({
                'success': False,
                'error': 'Parser no inicializado. Primero construya el parser.'
            }), 400

        data = request.json
        input_string = data.get('string', '')

        # Analizar cadena
        result = parser.parse_string(input_string)

        # El método parse_string retorna 'success' (True/False) y 'trace'
        return jsonify({
            'success': True,
            'accepted': result.get('success', False),
            'trace': result.get('trace', []),
            'error': result.get('error', '')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/get_states', methods=['GET'])
def get_states():
    """Obtiene información de todos los estados"""
    try:
        if parser is None:
            return jsonify({
                'success': False,
                'error': 'Parser no inicializado'
            }), 400

        states_info = []

        for idx, state in enumerate(parser.states):
            items = []
            for item in sorted(state, key=lambda x: (x.production, x.dot_position, x.lookahead)):
                prod = parser.grammar[item.production]
                right = list(prod.right)
                right.insert(item.dot_position, '•')

                items.append({
                    'production': item.production,
                    'left': prod.left,
                    'right': ' '.join(right),
                    'lookahead': item.lookahead
                })

            states_info.append({
                'id': idx,
                'items': items
            })

        return jsonify({
            'success': True,
            'states': states_info
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/get_parsing_table', methods=['GET'])
def get_parsing_table():
    """Obtiene la tabla de parsing ACTION/GOTO"""
    try:
        if parser is None:
            return jsonify({
                'success': False,
                'error': 'Parser no inicializado'
            }), 400

        # Obtener terminales y no terminales
        terminals = sorted(list(parser.terminals))
        non_terminals = sorted(list(parser.non_terminals))

        # Construir tabla ACTION
        action_table = {}
        for state_idx in range(len(parser.states)):
            action_table[state_idx] = {}
            for terminal in terminals:
                key = (state_idx, terminal)
                if key in parser.action_table:
                    action_table[state_idx][terminal] = parser.action_table[key]
                else:
                    action_table[state_idx][terminal] = ''

        # Construir tabla GOTO
        goto_table = {}
        for state_idx in range(len(parser.states)):
            goto_table[state_idx] = {}
            for non_terminal in non_terminals:
                # Excluir S' de la tabla GOTO (es símbolo aumentado)
                if non_terminal == parser.augmented_start:
                    continue
                key = (state_idx, non_terminal)
                if key in parser.goto_table:
                    goto_table[state_idx][non_terminal] = parser.goto_table[key]
                else:
                    goto_table[state_idx][non_terminal] = ''

        # Filtrar no terminales para no mostrar S'
        non_terminals_filtered = [nt for nt in non_terminals if nt != parser.augmented_start]

        return jsonify({
            'success': True,
            'terminals': terminals,
            'non_terminals': non_terminals_filtered,
            'action': action_table,
            'goto': goto_table,
            'num_states': len(parser.states)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/download/<viz_type>')
def download(viz_type):
    """Descarga archivos generados"""
    try:
        static_path = os.path.join(os.path.dirname(__file__), '../frontend/static')

        if viz_type == 'graphviz-png':
            file_path = os.path.join(static_path, 'automata_graphviz.png')
            return send_file(file_path,
                           as_attachment=True,
                           download_name='automata_lr1_graphviz.png')
        elif viz_type == 'graphviz-svg':
            file_path = os.path.join(static_path, 'automata_graphviz.svg')
            return send_file(file_path,
                           as_attachment=True,
                           download_name='automata_lr1_graphviz.svg')
        else:
            return "Tipo de archivo no válido", 400

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    # Inicializar con gramática por defecto
    init_parser(DEFAULT_GRAMMAR)

    print("\n" + "="*70)
    print(" " * 15 + "VISUALIZADOR WEB DE AUTOMATA LR(1)")
    print(" " * 10 + "Compiladores - UTEC - Puntos Extras")
    print("="*70)
    print("\nServidor iniciado en: http://127.0.0.1:5001")
    print("Presiona Ctrl+C para detener el servidor\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
