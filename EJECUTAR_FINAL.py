#!/usr/bin/env python3
"""
🎯 SCRIPT FINAL - Genera tu gramática con formato EXACTO
"""

import os
import matplotlib
matplotlib.use('Agg')

from lr1_parser import LR1Parser
from graph_visualizer_exact import LR1GraphVisualizerExact
from graph_visualizer import LR1GraphVisualizer

def main():
    print("🎯 GENERANDO TU GRAMÁTICA CON FORMATO EXACTO")
    print("=" * 60)

    parser = LR1Parser()
    automaton_visualizer = LR1GraphVisualizerExact()  # Visualizador EXACTO
    table_visualizer = LR1GraphVisualizer()           # Para la tabla

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
    print(f'📊 Conjuntos FIRST/FOLLOW calculados')
    
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

    print('\n🎨 Generando gráfico en formato EXACTO...')
    
    # Obtener datos
    automaton_data = parser.get_automaton_graph()
    table_data = parser.get_parsing_table()
    
    # Generar autómata con formato EXACTO
    automaton_visualizer.create_automaton_graph(
        automaton_data, 
        output_file='TU_AUTOMATA_EXACTO.png'
    )
    print('✅ Autómata EXACTO guardado: TU_AUTOMATA_EXACTO.png')
    
    # Generar tabla de parsing
    table_visualizer.create_parsing_table_image(
        table_data,
        output_file='TU_TABLA_EXACTA.png'
    )
    print('✅ Tabla EXACTA guardada: TU_TABLA_EXACTA.png')

    print('\n📊 Estadísticas finales:')
    print(f'  • Estados: {len(parser.states)}')
    print(f'  • Terminales: {len(parser.terminals)}')
    non_terms = [nt for nt in parser.non_terminals if nt != parser.augmented_start]
    print(f'  • No terminales: {len(non_terms)}')
    print(f'  • Producciones: {len(parser.grammar)}')

    print('\n🎉 ¡GRÁFICO EXACTO GENERADO!')
    print('📁 Archivos finales:')
    print('  🎯 TU_AUTOMATA_EXACTO.png - Formato EXACTO como tu referencia')
    print('  📊 TU_TABLA_EXACTA.png - Tabla de parsing completa')
    
    print('\n✨ El gráfico ahora tiene:')
    print('  ✅ Layout tipo árbol jerárquico')
    print('  ✅ Nodos rectangulares blancos') 
    print('  ✅ Items LR(1) línea por línea')
    print('  ✅ Estado Accept mostrado')
    print('  ✅ Formato idéntico a tu referencia')

if __name__ == '__main__':
    main()