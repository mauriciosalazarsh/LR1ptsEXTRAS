#!/usr/bin/env python3
"""
Script para probar tu gramática específica
"""

import os
import matplotlib
matplotlib.use('Agg')

from lr1_parser import LR1Parser
from graph_visualizer import LR1GraphVisualizer

def main():
    print('🧪 Probando tu gramática específica...')

    parser = LR1Parser()
    visualizer = LR1GraphVisualizer()

    # Tu gramática
    grammar = """S -> q * A * B * C
A -> a
A -> b * b * D
B -> a
B -> ε
C -> b
C -> ε
D -> C
D -> ε"""

    print('📝 Procesando gramática...')
    parser.parse_grammar(grammar)

    print(f'✅ Gramática procesada exitosamente')
    print(f'🏗️  Estados generados: {len(parser.states)}')
    print(f'📊 Terminales: {sorted(list(parser.terminals))}')
    
    # Mostrar no terminales sin el aumentado
    non_terms = [nt for nt in parser.non_terminals if nt != parser.augmented_start]
    print(f'📊 No terminales: {sorted(non_terms)}')

    # Mostrar conjuntos FIRST y FOLLOW
    ff = parser.get_first_follow_sets()
    print('\n📋 Conjuntos FIRST:')
    for nt, first_set in ff['first'].items():
        first_str = ', '.join(sorted(first_set))
        print(f'  FIRST({nt}) = {{{first_str}}}')

    print('\n📋 Conjuntos FOLLOW:')  
    for nt, follow_set in ff['follow'].items():
        follow_str = ', '.join(sorted(follow_set))
        print(f'  FOLLOW({nt}) = {{{follow_str}}}')

    # Mostrar algunos estados del autómata
    print(f'\n🏗️  Primeros 5 estados del autómata:')
    states_info = parser.get_states_info()
    for i in range(min(5, len(states_info))):
        state = states_info[i]
        print(f'  Estado I{state["number"]}:')
        for item in state['items'][:3]:  # Mostrar primeros 3 items
            print(f'    {item}')
        if len(state['items']) > 3:
            print(f'    ... y {len(state["items"]) - 3} items más')

    # Probar algunas cadenas
    test_strings = [
        'q * a * a * b',
        'q * b * b * b * a * b', 
        'q * a * b',
        'q * a',
        'q * b * b * b'
    ]
    
    print('\n🧪 Probando cadenas:')
    for test_str in test_strings:
        result = parser.parse_string(test_str)
        status = '✅ ACEPTADA' if result['success'] else '❌ RECHAZADA'
        print(f'  "{test_str}" -> {status}')

    print('\n🎨 Generando gráfico del autómata...')
    automaton_data = parser.get_automaton_graph()
    
    # Generar gráfico del autómata
    visualizer.create_automaton_graph(automaton_data, output_file='tu_automata.png')
    print('✅ Gráfico del autómata guardado como: tu_automata.png')
    
    # Generar tabla de parsing
    table_data = parser.get_parsing_table()
    visualizer.create_parsing_table_image(table_data, output_file='tu_tabla.png')
    print('✅ Tabla de parsing guardada como: tu_tabla.png')

    print('\n📊 Estadísticas finales:')
    print(f'  • Estados: {len(parser.states)}')
    print(f'  • Terminales: {len(parser.terminals)}')
    print(f'  • No terminales: {len([nt for nt in parser.non_terminals if nt != parser.augmented_start])}')
    print(f'  • Producciones: {len(parser.grammar)}')
    
    table_size = len(parser.states) * (len(parser.terminals) + len(non_terms))
    print(f'  • Entradas en tabla: {table_size}')

    print('\n🎉 ¡Todo completado exitosamente!')
    print('📁 Archivos generados:')
    print('  • tu_automata.png - Gráfico del autómata')
    print('  • tu_tabla.png - Tabla de parsing')

if __name__ == '__main__':
    main()