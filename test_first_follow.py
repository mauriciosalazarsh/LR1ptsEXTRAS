#!/usr/bin/env python3
"""
Test para verificar conjuntos FIRST y FOLLOW
"""

import matplotlib
matplotlib.use('Agg')

from lr1_parser import LR1Parser

def test_first_follow():
    print("🧪 PROBANDO CONJUNTOS FIRST Y FOLLOW")
    print("=" * 50)
    
    parser = LR1Parser()
    
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
    
    print("📝 Gramática:")
    for line in grammar.split('\n'):
        print(f"  {line}")
    print()
    
    parser.parse_grammar(grammar)
    
    print("🎯 CONJUNTOS FIRST (mi implementación):")
    for nt in sorted(parser.non_terminals):
        if nt != parser.augmented_start:
            first_set = parser.first_sets[nt]
            # Reemplazar '' con ε para mostrar
            display_set = {s if s != '' else 'ε' for s in first_set}
            print(f"FIRST({nt}): {sorted(list(display_set))}")
    
    print("\n🎯 CONJUNTOS FOLLOW (mi implementación):")
    for nt in sorted(parser.non_terminals):
        if nt != parser.augmented_start:
            follow_set = parser.follow_sets[nt]
            # Reemplazar '' con ε para mostrar
            display_set = {s if s != '' else 'ε' for s in follow_set}
            print(f"FOLLOW({nt}): {sorted(list(display_set))}")
    
    print("\n📊 CONJUNTOS ESPERADOS:")
    expected = {
        'FIRST': {
            'S': ['{q}'],
            'A': ['{a,b}'],
            'B': ['{a,ε}'],
            'C': ['{b,ε}'],
            'D': ['{b,ε}']
        },
        'FOLLOW': {
            'S': ['{$}'],
            'A': ['{*}'],
            'B': ['{*}'],
            'C': ['{$,*}'],
            'D': ['{*}']
        }
    }
    
    print("FIRST esperados:")
    for nt, expected_first in expected['FIRST'].items():
        print(f"FIRST({nt}): {expected_first[0]}")
    
    print("\nFOLLOW esperados:")
    for nt, expected_follow in expected['FOLLOW'].items():
        print(f"FOLLOW({nt}): {expected_follow[0]}")

if __name__ == "__main__":
    test_first_follow()