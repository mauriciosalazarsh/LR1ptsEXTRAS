#!/usr/bin/env python3
"""
Visualizador correcto para autómatas LR(1) - Estilo jerárquico
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import networkx as nx
import numpy as np
from typing import Dict, List, Any, Tuple
import io
import base64

class LR1GraphVisualizerCorrect:
    """Visualizador correcto para autómatas LR(1) con layout jerárquico"""
    
    def __init__(self):
        self.fig_size = (20, 14)
        self.node_width = 2.5
        self.node_height = 1.5
        self.level_spacing = 3.0
        self.node_spacing = 3.5
        
    def create_automaton_graph(self, automaton_data: Dict[str, Any], 
                             output_file: str = None, 
                             return_base64: bool = False) -> str:
        """Crea visualización jerárquica del autómata LR(1)"""
        
        # Crear figura
        fig, ax = plt.subplots(figsize=self.fig_size)
        ax.set_xlim(-2, 18)
        ax.set_ylim(-2, 16)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Título
        ax.text(8, 15, 'Autómata LR(1)', fontsize=20, fontweight='bold', 
               ha='center', va='center')
        
        # Obtener datos
        nodes = automaton_data['nodes']
        edges = automaton_data['edges']
        
        # Calcular layout jerárquico
        positions, levels = self._calculate_hierarchical_layout(nodes, edges)
        
        # Dibujar nodos con items
        self._draw_nodes_with_items(ax, nodes, positions)
        
        # Dibujar aristas
        self._draw_edges(ax, edges, positions)
        
        # Configurar y guardar
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"✅ Gráfico guardado en: {output_file}")
        
        if return_base64:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close(fig)
            return image_base64
        
        plt.close(fig)
        return None
    
    def _calculate_hierarchical_layout(self, nodes: List[Dict], edges: List[Dict]) -> Tuple[Dict, Dict]:
        """Calcula layout jerárquico basado en BFS desde el estado inicial"""
        
        # Crear grafo para BFS
        graph = {}
        for node in nodes:
            graph[node['id']] = []
        
        for edge in edges:
            graph[edge['from']].append(edge['to'])
        
        # BFS para determinar niveles
        levels = {}
        visited = set()
        queue = [(0, 0)]  # (node_id, level)
        levels[0] = 0
        visited.add(0)
        
        while queue:
            node_id, level = queue.pop(0)
            
            for neighbor in graph.get(node_id, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    levels[neighbor] = level + 1
                    queue.append((neighbor, level + 1))
        
        # Asignar niveles a nodos no visitados
        for node in nodes:
            if node['id'] not in levels:
                levels[node['id']] = max(levels.values()) + 1
        
        # Agrupar nodos por nivel
        level_groups = {}
        for node_id, level in levels.items():
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(node_id)
        
        # Calcular posiciones
        positions = {}
        max_level = max(levels.values())
        
        for level, node_ids in level_groups.items():
            y = 13 - (level * 2.2)  # De arriba hacia abajo
            node_count = len(node_ids)
            
            if node_count == 1:
                x = 8  # Centrar
            else:
                # Distribuir horizontalmente
                total_width = (node_count - 1) * self.node_spacing
                start_x = 8 - total_width / 2
                
                for i, node_id in enumerate(sorted(node_ids)):
                    x = start_x + i * self.node_spacing
                    positions[node_id] = (x, y)
                continue
            
            positions[node_ids[0]] = (x, y)
        
        return positions, levels
    
    def _draw_nodes_with_items(self, ax, nodes: List[Dict], positions: Dict):
        """Dibuja nodos con sus items LR(1)"""
        
        for node in nodes:
            node_id = node['id']
            items = node['items']
            
            if node_id not in positions:
                continue
                
            x, y = positions[node_id]
            
            # Determinar color del nodo
            if node.get('is_initial', False):
                color = '#E8F5E8'
                border_color = '#4CAF50'
                border_width = 3
            elif node.get('is_final', False):
                color = '#FFE8E8'
                border_color = '#F44336'
                border_width = 3
            else:
                color = '#F0F0F0'
                border_color = '#666666'
                border_width = 2
            
            # Calcular tamaño del nodo basado en número de items
            node_height = max(1.2, 0.3 + len(items) * 0.25)
            node_width = 2.8
            
            # Dibujar rectángulo del nodo
            rect = FancyBboxPatch(
                (x - node_width/2, y - node_height/2),
                node_width, node_height,
                boxstyle="round,pad=0.1",
                facecolor=color,
                edgecolor=border_color,
                linewidth=border_width
            )
            ax.add_patch(rect)
            
            # Título del nodo
            ax.text(x, y + node_height/2 - 0.15, f'I{node_id}',
                   fontsize=12, fontweight='bold', ha='center', va='center')
            
            # Items LR(1)
            item_y_start = y + node_height/2 - 0.4
            for i, item in enumerate(items[:6]):  # Máximo 6 items por legibilidad
                item_y = item_y_start - i * 0.2
                # Limpiar el item para mejor visualización
                clean_item = item.replace('S\' -> ', "S' -> ").replace(' • ', ' • ')
                ax.text(x, item_y, clean_item,
                       fontsize=8, ha='center', va='center',
                       fontfamily='monospace')
            
            if len(items) > 6:
                ax.text(x, item_y_start - 6 * 0.2, f'... y {len(items) - 6} más',
                       fontsize=7, ha='center', va='center', style='italic')
    
    def _draw_edges(self, ax, edges: List[Dict], positions: Dict):
        """Dibuja las aristas entre estados"""
        
        for edge in edges:
            from_id = edge['from']
            to_id = edge['to']
            label = edge['label']
            
            if from_id not in positions or to_id not in positions:
                continue
            
            x1, y1 = positions[from_id]
            x2, y2 = positions[to_id]
            
            # Calcular puntos de conexión en los bordes de los nodos
            dx = x2 - x1
            dy = y2 - y1
            length = np.sqrt(dx*dx + dy*dy)
            
            if length == 0:
                continue
                
            # Normalizar
            dx_norm = dx / length
            dy_norm = dy / length
            
            # Puntos de inicio y fin (en los bordes de los nodos)
            margin = 1.4
            start_x = x1 + dx_norm * margin
            start_y = y1 + dy_norm * margin
            end_x = x2 - dx_norm * margin
            end_y = y2 - dy_norm * margin
            
            # Dibujar flecha
            ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(arrowstyle='->', color='black', lw=1.5,
                                     shrinkA=0, shrinkB=0))
            
            # Etiqueta de la transición
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            
            # Offset para la etiqueta
            if abs(dx) > abs(dy):  # Más horizontal
                label_x = mid_x
                label_y = mid_y + 0.3
            else:  # Más vertical
                label_x = mid_x + 0.3
                label_y = mid_y
            
            ax.text(label_x, label_y, label, fontsize=10, fontweight='bold',
                   ha='center', va='center', color='red',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', 
                           edgecolor='none', alpha=0.8))

def test_correct_visualization():
    """Prueba el visualizador correcto"""
    from lr1_parser import LR1Parser
    
    print("🎨 Probando visualizador CORRECTO...")
    
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
    visualizer = LR1GraphVisualizerCorrect()
    
    # Generar gráfico correcto
    visualizer.create_automaton_graph(automaton_data, output_file='automata_correcto.png')
    print("✅ Gráfico CORRECTO guardado como: automata_correcto.png")

if __name__ == "__main__":
    test_correct_visualization()