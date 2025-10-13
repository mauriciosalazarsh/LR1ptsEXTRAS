#!/usr/bin/env python3
"""
Visualizador EXACTO para autómatas LR(1) - Replica el formato de referencia
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import networkx as nx
import numpy as np
from typing import Dict, List, Any, Tuple
import io
import base64

class LR1GraphVisualizerExact:
    """Visualizador que replica exactamente el formato de referencia"""
    
    def __init__(self):
        self.fig_size = (14, 16)
        self.node_width = 2.5
        self.node_height = 1.2
        self.level_spacing = 2.0
        self.node_spacing = 3.0
        
    def create_automaton_graph(self, automaton_data: Dict[str, Any], 
                             output_file: str = None, 
                             return_base64: bool = False) -> str:
        """Crea visualización EXACTA del autómata LR(1)"""
        
        # Crear figura con fondo blanco
        fig, ax = plt.subplots(figsize=self.fig_size, facecolor='white')
        ax.set_facecolor('white')
        
        # Obtener datos
        nodes = automaton_data['nodes']
        edges = automaton_data['edges']
        
        # Calcular layout exacto como en la referencia
        positions = self._calculate_exact_layout(nodes, edges)
        
        # Limpiar ejes
        ax.set_xlim(-1, 15)
        ax.set_ylim(-1, 16)
        ax.axis('off')
        
        # Agregar título "Autómata LR(1)"
        ax.text(7, 15, 'Autómata LR(1)', fontsize=16, fontweight='bold', 
               ha='center', va='center')
        
        # Dibujar nodos exactamente como en la referencia
        self._draw_exact_nodes(ax, nodes, positions)
        
        # Dibujar aristas exactamente como en la referencia
        self._draw_exact_edges(ax, edges, positions)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none', pad_inches=0.2)
            print(f"✅ Gráfico EXACTO guardado en: {output_file}")
        
        if return_base64:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none', pad_inches=0.2)
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close(fig)
            return image_base64
        
        plt.close(fig)
        return None
    
    def _calculate_exact_layout(self, nodes: List[Dict], edges: List[Dict]) -> Dict[int, Tuple[float, float]]:
        """Calcula layout exacto como en la imagen de referencia"""
        
        # Layout exacto basado en la imagen de referencia
        positions = {}
        
        # Nivel 0: I0 (estado inicial, verde)
        positions[0] = (7, 13.5)
        
        # Nivel 1: I1 (izquierda) e I2 (derecha, rojo/accept)
        positions[1] = (3.5, 11.5)
        positions[2] = (10.5, 11.5)
        
        # Nivel 2: I3 (centro, bajo I1)
        positions[3] = (7, 9.5)
        
        # Nivel 3: I4, I5, I6 (fila horizontal)
        positions[4] = (2, 7.5)
        positions[5] = (7, 7.5)
        positions[6] = (12, 7.5)
        
        # Nivel 4: I7, I8 (bajo I4 e I6)
        positions[7] = (3.5, 5.5)
        positions[8] = (10.5, 5.5)
        
        # Nivel 5: I9, I10, I11 (fila horizontal)
        positions[9] = (2, 3.5)
        positions[10] = (7, 3.5)
        positions[11] = (12, 3.5)
        
        # Nivel 6: I12, I13 (penúltimo nivel)
        positions[12] = (4.5, 1.5)
        positions[13] = (9.5, 1.5)
        
        # Nivel 7: I14, I15, I16, I17, I18 (nivel inferior)
        bottom_y = 0
        positions[14] = (1, bottom_y)
        positions[15] = (4, bottom_y)
        positions[16] = (7, bottom_y)
        positions[17] = (10, bottom_y)
        positions[18] = (13, bottom_y)
        
        # Para nodos adicionales que no están en el layout fijo
        positioned_ids = set(positions.keys())
        remaining_nodes = [n for n in nodes if n['id'] not in positioned_ids]
        
        # Colocar nodos restantes en niveles adicionales
        if remaining_nodes:
            extra_y = -2
            for i, node in enumerate(remaining_nodes):
                x = 2 + (i % 5) * 3
                y = extra_y - (i // 5) * 2
                positions[node['id']] = (x, y)
        
        return positions
    
    def _draw_exact_nodes(self, ax, nodes: List[Dict], positions: Dict):
        """Dibuja nodos exactamente como en la imagen de referencia"""
        
        for node in nodes:
            node_id = node['id']
            items = node['items']
            
            if node_id not in positions:
                continue
                
            x, y = positions[node_id]
            
            # Determinar color del nodo según la referencia
            if node_id == 0:  # I0 - verde
                face_color = '#90EE90'  # Light green
                edge_color = '#228B22'  # Forest green
                linewidth = 2
            elif node.get('is_final', False) or node_id == 2:  # I2 - rojo (Accept)
                face_color = '#FFB6C1'  # Light pink
                edge_color = '#DC143C'  # Crimson
                linewidth = 2
            else:  # Resto - gris
                face_color = '#F5F5F5'  # Whitesmoke
                edge_color = '#696969'  # Dim gray
                linewidth = 1.5
            
            # Calcular tamaño del nodo basado en contenido
            max_lines = min(len(items), 4)
            node_height = max(1.0, 0.4 + max_lines * 0.15)
            node_width = 2.5
            
            # Dibujar rectángulo con colores apropiados
            rect = Rectangle(
                (x - node_width/2, y - node_height/2),
                node_width, node_height,
                facecolor=face_color,
                edgecolor=edge_color,
                linewidth=linewidth
            )
            ax.add_patch(rect)
            
            # Título del nodo (I0, I1, etc.)
            ax.text(x, y + node_height/2 - 0.15, f'I{node_id}',
                   fontsize=11, fontweight='bold', ha='center', va='top')
            
            # Items LR(1) línea por línea
            line_height = 0.14
            start_y = y + node_height/2 - 0.35
            
            for i, item in enumerate(items[:4]):  # Mostrar máximo 4 items
                item_y = start_y - i * line_height
                # Limpiar y formatear item
                clean_item = self._format_item_for_display(item)
                ax.text(x, item_y, clean_item,
                       fontsize=8, ha='center', va='center',
                       fontfamily='monospace')
            
            if len(items) > 4:
                ax.text(x, start_y - 4 * line_height, '...',
                       fontsize=8, ha='center', va='center', 
                       fontweight='bold')
    
    def _format_item_for_display(self, item: str) -> str:
        """Formatea un item LR(1) para mostrar correctamente"""
        # Limpiar el item
        clean = item.strip()
        
        # Reemplazar símbolos especiales exactamente como en la referencia
        clean = clean.replace("S' ->", "S' ->")
        clean = clean.replace('•', '•')
        clean = clean.replace(' • ', ' • ')
        clean = clean.replace(', $', ', $')
        
        # Manejar epsilon correctamente
        clean = clean.replace('ε', 'ε')
        clean = clean.replace('epsilon', 'ε')
        
        # Truncar si es muy largo pero mantener formato
        if len(clean) > 22:
            clean = clean[:19] + "..."
        
        return clean
    
    def _draw_exact_edges(self, ax, edges: List[Dict], positions: Dict):
        """Dibuja aristas exactamente como en la imagen de referencia"""
        
        for edge in edges:
            from_id = edge['from']
            to_id = edge['to']
            label = edge['label']
            
            if from_id not in positions or to_id not in positions:
                continue
            
            x1, y1 = positions[from_id]
            x2, y2 = positions[to_id]
            
            # Calcular puntos de conexión
            dx = x2 - x1
            dy = y2 - y1
            length = np.sqrt(dx*dx + dy*dy)
            
            if length == 0:
                continue
            
            # Normalizar
            dx_norm = dx / length
            dy_norm = dy / length
            
            # Márgenes de los nodos
            margin = 1.1
            start_x = x1 + dx_norm * margin
            start_y = y1 + dy_norm * margin
            end_x = x2 - dx_norm * margin
            end_y = y2 - dy_norm * margin
            
            # Dibujar flecha simple y limpia
            ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
            
            # Etiqueta de la transición
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            
            # Posicionar etiqueta
            offset = 0.2
            if abs(dx) > abs(dy):  # Más horizontal
                label_x = mid_x
                label_y = mid_y + offset if dy >= 0 else mid_y - offset
            else:  # Más vertical
                label_x = mid_x + offset if dx >= 0 else mid_x - offset
                label_y = mid_y
            
            ax.text(label_x, label_y, label, fontsize=9, fontweight='bold',
                   ha='center', va='center', color='black')
    
    def _add_accept_indication(self, ax, nodes: List[Dict], positions: Dict):
        """Agrega indicación de Accept si hay estado final"""
        
        for node in nodes:
            if node.get('is_final', False) and node['id'] in positions:
                x, y = positions[node['id']]
                # Agregar "Accept" cerca del estado final
                ax.text(x + 1.5, y, 'Accept', fontsize=10, fontweight='bold',
                       ha='left', va='center',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray',
                               edgecolor='black'))
                break

def test_exact_visualization():
    """Prueba el visualizador exacto"""
    from lr1_parser import LR1Parser
    
    print("🎯 Probando visualizador EXACTO...")
    
    parser = LR1Parser()
    
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
    
    parser.parse_grammar(grammar)
    print(f"✅ Gramática procesada: {len(parser.states)} estados")
    
    automaton_data = parser.get_automaton_graph()
    visualizer = LR1GraphVisualizerExact()
    
    # Generar gráfico exacto
    visualizer.create_automaton_graph(automaton_data, output_file='automata_EXACTO.png')
    print("✅ Gráfico EXACTO guardado como: automata_EXACTO.png")

if __name__ == "__main__":
    test_exact_visualization()