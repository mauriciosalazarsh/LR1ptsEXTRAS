#!/usr/bin/env python3
"""
Visualizador de Autómata LR(1) usando Graphviz directo
Compiladores - UTEC - Puntos Extras Examen 2
"""

import graphviz
from typing import Set, Dict
import subprocess
import os


class LR1GraphvizVisualizer:
    """Visualizador profesional del autómata LR(1) usando Graphviz directo"""

    def __init__(self, parser):
        """
        Inicializa el visualizador

        Args:
            parser: Instancia de LR1Parser con el autómata construido
        """
        self.parser = parser
        self.dot = None

    def _format_item(self, item) -> str:
        """Formatea un item LR(1) para visualización"""
        prod = self.parser.grammar[item.production]
        right = list(prod.right)

        # Insertar el punto en la posición correcta
        right.insert(item.dot_position, '•')
        right_str = ' '.join(right)

        return f"{prod.left} → {right_str}, {item.lookahead}"

    def _format_state_label(self, state_idx: int, state_items: Set) -> str:
        """Formatea la etiqueta de un estado con sus items"""
        items_list = []

        # Ordenar items para presentación consistente
        sorted_items = sorted(
            state_items,
            key=lambda x: (x.production, x.dot_position, x.lookahead)
        )

        for item in sorted_items:
            item_str = self._format_item(item)
            items_list.append(item_str)

        # Construir etiqueta HTML-like para mejor formato
        header = f"<B>I{state_idx}</B>"
        items_text = '<BR/>'.join(items_list)

        return f"<{header}<BR/><BR/>{items_text}>"

    def _get_state_color(self, state_idx: int, state_items: Set) -> str:
        """Determina el color del estado según su tipo"""
        # Estado inicial (I0)
        if state_idx == 0:
            return 'lightgreen'

        # Estados de aceptación (tienen S' -> S •, $)
        for item in state_items:
            prod = self.parser.grammar[item.production]
            if (prod.left == self.parser.augmented_start and
                item.dot_position == len(prod.right) and
                item.lookahead == '$'):
                return 'lightcoral'

        # Estados normales
        return 'lightblue'

    def create_automaton(self):
        """Crea el grafo del autómata LR(1) usando Graphviz"""
        # Crear grafo dirigido
        self.dot = graphviz.Digraph(
            'LR1_Automaton',
            comment='Autómata LR(1)',
            format='png'
        )

        # Configuración global del grafo
        self.dot.attr(rankdir='LR')  # Izquierda a derecha
        self.dot.attr(dpi='300')  # Mayor resolución
        self.dot.attr('node', shape='rectangle', style='rounded,filled',
                     fontname='Courier', fontsize='14', margin='0.3,0.2')
        self.dot.attr('edge', fontname='Arial Bold', fontsize='14')

        # Título del autómata
        self.dot.attr(label='\\n\\nAutómata LR(1)\\n',
                     fontsize='20', fontname='Arial Bold')

        # Nodo invisible para la flecha de inicio
        self.dot.node('start', '', shape='point', width='0')

        # Agregar estados
        for idx, state in enumerate(self.parser.states):
            label = self._format_state_label(idx, state)
            color = self._get_state_color(idx, state)

            # Configurar nodo
            node_attrs = {
                'fillcolor': color,
                'width': '4.5',
                'height': '2.0'
            }

            # Doble círculo para estados de aceptación
            if color == 'lightcoral':
                node_attrs['peripheries'] = '2'

            self.dot.node(str(idx), label, **node_attrs)

        # Flecha de inicio apuntando a I0
        self.dot.edge('start', '0', style='bold', color='green4')

        # Agregar transiciones
        for (from_state, symbol), to_state in sorted(self.parser.transitions.items()):
            self.dot.edge(
                str(from_state),
                str(to_state),
                label=f' {symbol} ',
                fontcolor='blue'
            )

        return self.dot

    def visualize(self, filename: str = "automata_lr1_graphviz",
                  view_file: bool = False, output_format: str = 'png'):
        """
        Genera visualización del autómata LR(1)

        Args:
            filename: Nombre del archivo de salida (sin extensión)
            view_file: Si True, abre automáticamente el archivo generado
            output_format: Formato de salida ('png', 'pdf', 'svg')
        """
        if self.dot is None:
            self.create_automaton()

        # Cambiar formato si se especifica
        self.dot.format = output_format

        # Renderizar
        output_path = self.dot.render(filename, cleanup=True)

        print(f"✅ Autómata LR(1) generado: {output_path}")

        # Abrir archivo si se solicita
        if view_file and os.path.exists(output_path):
            try:
                if os.name == 'darwin':  # macOS
                    subprocess.run(['open', output_path])
                elif os.name == 'nt':  # Windows
                    os.startfile(output_path)
                else:  # Linux
                    subprocess.run(['xdg-open', output_path])
            except Exception as e:
                print(f"⚠️ No se pudo abrir el archivo automáticamente: {e}")

        return output_path

    def save_dot_file(self, filename: str = "automata_lr1.dot"):
        """Guarda el código DOT del grafo"""
        if self.dot is None:
            self.create_automaton()

        with open(filename, 'w') as f:
            f.write(self.dot.source)

        print(f"✅ Archivo DOT guardado: {filename}")
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
        """Imprime un resumen detallado del autómata"""
        info = self.get_automaton_info()

        print("\n" + "="*70)
        print("📊 RESUMEN DEL AUTÓMATA LR(1)")
        print("="*70)
        print(f"📍 Estados: {info['num_states']}")
        print(f"🔀 Transiciones: {info['num_transitions']}")
        print(f"🔤 Terminales: {{{', '.join(info['terminals'])}}}")
        print(f"🔠 No terminales: {{{', '.join(info['non_terminals'])}}}")
        print(f"📝 Producciones: {info['num_productions']}")
        print("="*70 + "\n")


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

    print("🎨 Creando visualización mejorada con Graphviz...")
    visualizer = LR1GraphvizVisualizer(parser)

    # Mostrar resumen
    visualizer.print_automaton_summary()

    # Generar visualizaciones en múltiples formatos
    print("📊 Generando visualizaciones...")
    visualizer.visualize("AUTOMATA_LR1_FINAL", output_format='png')
    visualizer.visualize("AUTOMATA_LR1_FINAL_PDF", output_format='pdf', view_file=False)
    visualizer.save_dot_file("AUTOMATA_LR1_FINAL.dot")

    print("\n✅ ¡Visualización completada exitosamente!")
    print("\nArchivos generados:")
    print("  • AUTOMATA_LR1_FINAL.png - Imagen del autómata")
    print("  • AUTOMATA_LR1_FINAL_PDF.pdf - Versión en PDF")
    print("  • AUTOMATA_LR1_FINAL.dot - Código fuente Graphviz")


if __name__ == "__main__":
    main()
