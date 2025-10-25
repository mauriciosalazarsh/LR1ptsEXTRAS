#!/usr/bin/env python3
"""
Visualizador de Autómata LR(1) usando automathon
Compiladores - UTEC - Puntos Extras Examen 2
"""

from automathon import DFA
from typing import Dict, Set, Tuple, List
import subprocess
import os

class LR1AutomatonVisualizer:
    """Visualizador del autómata LR(1) usando automathon"""

    def __init__(self, parser):
        """
        Inicializa el visualizador

        Args:
            parser: Instancia de LR1Parser con el autómata construido
        """
        self.parser = parser
        self.dfa = None

    def _format_state_label(self, state_items: Set) -> str:
        """Formatea los items de un estado para mostrarlos como etiqueta"""
        items_list = []
        for item in sorted(state_items, key=lambda x: (x.production, x.dot_position, x.lookahead)):
            prod = self.parser.grammar[item.production]
            right = list(prod.right)

            # Insertar el punto en la posición correcta
            right.insert(item.dot_position, '•')
            right_str = ' '.join(right)

            item_str = f"{prod.left} → {right_str}, {item.lookahead}"
            items_list.append(item_str)

        # Limitar a 5 items por estado para no saturar
        if len(items_list) > 5:
            items_list = items_list[:5] + ['...']

        return '\\n'.join(items_list)

    def _create_dfa_representation(self) -> Dict:
        """
        Crea una representación del autómata LR(1) compatible con automathon

        Returns:
            Dict con la configuración del DFA
        """
        # Estados
        states = set(str(i) for i in range(len(self.parser.states)))

        # Alfabeto (símbolos que causan transiciones)
        alphabet = set()
        for (_, symbol), _ in self.parser.transitions.items():
            alphabet.add(symbol)

        # Estado inicial
        initial_state = "0"

        # Estados finales (estados con items de aceptación)
        final_states = set()
        for i, state in enumerate(self.parser.states):
            for item in state:
                prod = self.parser.grammar[item.production]
                # Si es S' -> S • con lookahead $
                if (prod.left == self.parser.augmented_start and
                    item.dot_position == len(prod.right) and
                    item.lookahead == '$'):
                    final_states.add(str(i))

        if not final_states:
            final_states = {"1"}  # Estado de aceptación por defecto

        # Función de transición
        transitions = {}
        for (from_state, symbol), to_state in self.parser.transitions.items():
            if str(from_state) not in transitions:
                transitions[str(from_state)] = {}
            transitions[str(from_state)][symbol] = str(to_state)

        return {
            'states': states,
            'alphabet': alphabet,
            'initial_state': initial_state,
            'final_states': final_states,
            'transitions': transitions
        }

    def create_automaton(self):
        """Crea el autómata usando automathon"""
        config = self._create_dfa_representation()

        # Crear DFA con automathon (argumentos posicionales)
        self.dfa = DFA(
            config['states'],        # q: conjunto de estados
            config['alphabet'],      # sigma: alfabeto
            config['transitions'],   # delta: función de transición
            config['initial_state'], # estado inicial
            config['final_states']   # f: estados finales
        )

        return self.dfa

    def visualize(self, filename: str = "automata_lr1", view_pdf: bool = True):
        """
        Genera visualización del autómata LR(1)

        Args:
            filename: Nombre del archivo de salida (sin extensión)
            view_pdf: Si True, abre automáticamente el PDF generado
        """
        if self.dfa is None:
            self.create_automaton()

        # Configuración de estilo personalizado
        node_attr = {
            'fontsize': '10',
            'fontname': 'monospace',
            'shape': 'rectangle',
            'style': 'rounded,filled',
            'fillcolor': 'lightblue',
            'width': '2.5',
            'height': '1.5'
        }

        edge_attr = {
            'fontsize': '12',
            'fontname': 'Arial'
        }

        # Generar visualización
        self.dfa.view(
            file_name=filename,
            node_attr=node_attr,
            edge_attr=edge_attr
        )

        print(f"✅ Autómata LR(1) generado: {filename}.png y {filename}.svg")

        # Abrir PDF si está disponible
        if view_pdf and os.path.exists(f"{filename}.pdf"):
            try:
                if os.name == 'darwin':  # macOS
                    subprocess.run(['open', f"{filename}.pdf"])
                elif os.name == 'nt':  # Windows
                    os.startfile(f"{filename}.pdf")
                else:  # Linux
                    subprocess.run(['xdg-open', f"{filename}.pdf"])
            except Exception as e:
                print(f"⚠️ No se pudo abrir el PDF automáticamente: {e}")

        return filename

    def get_automaton_info(self) -> Dict:
        """Retorna información del autómata"""
        return {
            'num_states': len(self.parser.states),
            'num_transitions': len(self.parser.transitions),
            'terminals': sorted(self.parser.terminals),
            'non_terminals': sorted(self.parser.non_terminals),
            'num_productions': len(self.parser.grammar)
        }

    def print_automaton_summary(self):
        """Imprime un resumen del autómata"""
        info = self.get_automaton_info()

        print("\n" + "="*60)
        print("📊 RESUMEN DEL AUTÓMATA LR(1)")
        print("="*60)
        print(f"Estados: {info['num_states']}")
        print(f"Transiciones: {info['num_transitions']}")
        print(f"Terminales: {', '.join(info['terminals'])}")
        print(f"No terminales: {', '.join(info['non_terminals'])}")
        print(f"Producciones: {info['num_productions']}")
        print("="*60 + "\n")


def main():
    """Función principal de prueba"""
    from lr1_parser import LR1Parser

    # Gramática de ejemplo
    grammar = """
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

    print("🔧 Construyendo parser LR(1)...")
    parser = LR1Parser()
    parser.parse_grammar(grammar)

    print("🎨 Creando visualización con automathon...")
    visualizer = LR1AutomatonVisualizer(parser)
    visualizer.print_automaton_summary()
    visualizer.visualize("automata_lr1_automathon", view_pdf=False)

    print("\n✅ Visualización completada!")


if __name__ == "__main__":
    main()
