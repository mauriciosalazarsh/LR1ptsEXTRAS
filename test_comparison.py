#!/usr/bin/env python3
"""
Script de comparación entre LR(1) y LALR(1)
Muestra las diferencias en número de estados
"""

from parser.lr1_parser import LR1Parser
from parser.lalr1_parser import LALR1Parser

def compare_parsers(grammar):
    """Compara LR(1) y LALR(1) para una gramática dada"""

    print("="*70)
    print("COMPARACIÓN LR(1) vs LALR(1)")
    print("="*70)

    # Construir parser LR(1)
    print("\n[1] Construyendo parser LR(1)...")
    lr1 = LR1Parser()
    lr1.parse_grammar(grammar)

    # Construir parser LALR(1)
    print("[2] Construyendo parser LALR(1)...")
    lalr1 = LALR1Parser()
    lalr1.parse_grammar(grammar)

    # Comparar resultados
    print("\n" + "="*70)
    print("RESULTADOS")
    print("="*70)

    print(f"\n{'Métrica':<30} {'LR(1)':<15} {'LALR(1)':<15} {'Reducción':<15}")
    print("-"*70)

    lr1_states = len(lr1.states)
    lalr1_states = len(lalr1.states)
    reduction = ((lr1_states - lalr1_states) / lr1_states) * 100 if lr1_states > 0 else 0

    print(f"{'Estados del autómata':<30} {lr1_states:<15} {lalr1_states:<15} {reduction:.1f}%")

    lr1_trans = len(lr1.transitions)
    lalr1_trans = len(lalr1.transitions)
    trans_reduction = ((lr1_trans - lalr1_trans) / lr1_trans) * 100 if lr1_trans > 0 else 0

    print(f"{'Transiciones':<30} {lr1_trans:<15} {lalr1_trans:<15} {trans_reduction:.1f}%")

    print(f"{'Terminales':<30} {len(lr1.terminals):<15} {len(lalr1.terminals):<15} {'N/A':<15}")
    print(f"{'No terminales':<30} {len(lr1.non_terminals):<15} {len(lalr1.non_terminals):<15} {'N/A':<15}")
    print(f"{'Producciones':<30} {len(lr1.grammar):<15} {len(lalr1.grammar):<15} {'N/A':<15}")

    print("\n" + "="*70)
    print("CONCLUSIÓN")
    print("="*70)
    print(f"LALR(1) reduce el número de estados en un {reduction:.1f}%")
    print(f"LR(1): {lr1_states} estados | LALR(1): {lalr1_states} estados")
    print("="*70 + "\n")

    # Probar las mismas cadenas en ambos parsers
    test_strings = ["id", "id + id", "id + id * id", "( id + id ) * id"]

    print("\nPRUEBA DE CADENAS")
    print("="*70)
    print(f"{'Cadena':<25} {'LR(1)':<15} {'LALR(1)':<15}")
    print("-"*70)

    for test_str in test_strings:
        lr1_result = lr1.parse_string(test_str)
        lalr1_result = lalr1.parse_string(test_str)

        lr1_status = "✓ Acepta" if lr1_result['success'] else "✗ Rechaza"
        lalr1_status = "✓ Acepta" if lalr1_result['success'] else "✗ Rechaza"

        print(f"{test_str:<25} {lr1_status:<15} {lalr1_status:<15}")

    print("="*70 + "\n")

if __name__ == "__main__":
    # Gramática de expresiones aritméticas
    grammar1 = """
S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
"""

    print("\n📊 GRAMÁTICA 1: Expresiones Aritméticas")
    compare_parsers(grammar1)

    # Gramática del proyecto (más compleja)
    grammar2 = """
S -> q * A * B * C
A -> a
A -> b * b * D
B -> a
B -> ε
C -> b
C -> ε
D -> C
D -> ε
"""

    print("\n📊 GRAMÁTICA 2: Gramática del Proyecto")
    compare_parsers(grammar2)
