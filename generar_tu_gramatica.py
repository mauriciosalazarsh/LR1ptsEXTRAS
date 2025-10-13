#!/usr/bin/env python3
"""
Script final para generar TU gramática con el formato CORRECTO
"""

import os
import matplotlib
matplotlib.use('Agg')

from lr1_parser import LR1Parser
from graph_visualizer_correct import LR1GraphVisualizerCorrect
from graph_visualizer import LR1GraphVisualizer

def main():
    print("🎯 Generando tu gramática con formato CORRECTO")
    print("=" * 60)

    parser = LR1Parser()
    automaton_visualizer = LR1GraphVisualizerCorrect()
    table_visualizer = LR1GraphVisualizer()

    # Tu gramática exacta
    grammar = """S -> q * A * B * C
A -> a
A -> b * b * D
B -> a
B -> ε
C -> b
C -> ε
D -> C
D -> ε"""

    print('📝 Procesando tu gramática...')
    parser.parse_grammar(grammar)

    print(f'✅ Gramática procesada exitosamente')
    print(f'🏗️  Estados generados: {len(parser.states)}')

    # Mostrar información básica
    ff = parser.get_first_follow_sets()
    print(f'\n📊 Conjuntos FIRST/FOLLOW calculados para {len(ff["first"])} no terminales')
    
    # Probar cadenas clave
    test_strings = [
        'q * a * a * b',
        'q * b * b * b * a * b', 
        'q * a * b'
    ]
    
    print('\n🧪 Probando cadenas:')
    for test_str in test_strings:
        result = parser.parse_string(test_str)
        status = '✅ ACEPTADA' if result['success'] else '❌ RECHAZADA'
        print(f'  "{test_str}" -> {status}')

    print('\n🎨 Generando gráficos en formato CORRECTO...')
    
    # Obtener datos
    automaton_data = parser.get_automaton_graph()
    table_data = parser.get_parsing_table()
    
    # Generar autómata con formato jerárquico CORRECTO
    automaton_visualizer.create_automaton_graph(
        automaton_data, 
        output_file='AUTOMATA_FINAL_CORRECTO.png'
    )
    print('✅ Autómata CORRECTO guardado: AUTOMATA_FINAL_CORRECTO.png')
    
    # Generar tabla de parsing
    table_visualizer.create_parsing_table_image(
        table_data,
        output_file='TABLA_FINAL_CORRECTO.png'
    )
    print('✅ Tabla CORRECTA guardada: TABLA_FINAL_CORRECTO.png')

    print('\n📊 Estadísticas finales:')
    print(f'  • Estados: {len(parser.states)}')
    print(f'  • Terminales: {len(parser.terminals)}')
    non_terms = [nt for nt in parser.non_terminals if nt != parser.augmented_start]
    print(f'  • No terminales: {len(non_terms)}')
    print(f'  • Producciones: {len(parser.grammar)}')
    
    table_size = len(parser.states) * (len(parser.terminals) + len(non_terms))
    print(f'  • Entradas en tabla: {table_size}')

    print('\n🎉 ¡ARCHIVOS FINALES GENERADOS CORRECTAMENTE!')
    print('📁 Archivos:')
    print('  • AUTOMATA_FINAL_CORRECTO.png - Autómata jerárquico con items')
    print('  • TABLA_FINAL_CORRECTO.png - Tabla de parsing completa')
    
    print('\n🚀 Para la aplicación web completa:')
    print('   python3 RUN.py')
    print('   (Ahora usa el formato correcto automáticamente)')

if __name__ == '__main__':
    main()