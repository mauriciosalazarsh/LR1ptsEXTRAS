#!/usr/bin/env python3
"""
Script de prueba para verificar que Graphviz funciona con LALR(1)
"""

from parser.lalr1_parser import LALR1Parser
from parser.lr1_parser import LR1Parser
from parser.visualizer_graphviz import LR1GraphvizVisualizer

def test_visualization():
    grammar = """
S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
"""

    print("="*70)
    print("PRUEBA DE VISUALIZACIÓN - LR(1) vs LALR(1)")
    print("="*70)

    # Test LR(1)
    print("\n[1] Construyendo LR(1)...")
    lr1 = LR1Parser()
    lr1.parse_grammar(grammar)
    print(f"    Estados: {len(lr1.states)}")

    print("[2] Generando visualización LR(1)...")
    viz_lr1 = LR1GraphvizVisualizer(lr1)
    viz_lr1.visualize("TEST_LR1", output_format='svg', view_file=False)
    print("    ✅ Visualización LR(1) generada: TEST_LR1.svg")

    # Test LALR(1)
    print("\n[3] Construyendo LALR(1)...")
    lalr1 = LALR1Parser()
    lalr1.parse_grammar(grammar)
    print(f"    Estados: {len(lalr1.states)}")

    print("[4] Generando visualización LALR(1)...")
    viz_lalr1 = LR1GraphvizVisualizer(lalr1)
    viz_lalr1.visualize("TEST_LALR1", output_format='svg', view_file=False)
    print("    ✅ Visualización LALR(1) generada: TEST_LALR1.svg")

    print("\n" + "="*70)
    print("RESULTADO")
    print("="*70)
    print(f"✅ Ambas visualizaciones generadas exitosamente")
    print(f"   LR(1): TEST_LR1.svg ({len(lr1.states)} estados)")
    print(f"   LALR(1): TEST_LALR1.svg ({len(lalr1.states)} estados)")
    print("="*70)

if __name__ == "__main__":
    test_visualization()
