#!/usr/bin/env python3
"""
Visualizador de autómatas LR(1) usando NetworkX y Matplotlib
"""

import os
import matplotlib
# CRUCIAL: Configurar matplotlib ANTES de importar pyplot
matplotlib.use('Agg')  # Backend sin GUI para servidor
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import numpy as np
from typing import Dict, List, Any, Tuple
import io
import base64
import warnings

# Suprimir warnings de matplotlib
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

class LR1GraphVisualizer:
    """Visualizador para autómatas LR(1)"""
    
    def __init__(self):
        self.fig_size = (16, 12)
        self.node_size = 3000
        self.font_size = 8
        self.edge_font_size = 10
        
    def create_automaton_graph(self, automaton_data: Dict[str, Any], 
                             output_file: str = None, 
                             return_base64: bool = False) -> str:
        """
        Crea una visualización del autómata LR(1)
        
        Args:
            automaton_data: Datos del autómata desde LR1Parser.get_automaton_graph()
            output_file: Archivo donde guardar la imagen (opcional)
            return_base64: Si retornar la imagen como string base64
            
        Returns:
            String base64 de la imagen si return_base64=True, sino None
        """
        
        # Crear grafo dirigido
        G = nx.DiGraph()
        
        # Agregar nodos
        for node in automaton_data['nodes']:
            G.add_node(node['id'], **node)
        
        # Agregar aristas
        for edge in automaton_data['edges']:
            G.add_edge(edge['from'], edge['to'], label=edge['label'])
        
        # Configurar figura
        fig = plt.figure(figsize=self.fig_size)
        plt.clf()
        
        # Calcular layout usando spring layout mejorado
        pos = self._calculate_layout(G, automaton_data)
        
        # Dibujar el gráfico
        self._draw_graph(G, pos, automaton_data)
        
        # Configurar el plot
        plt.title("Autómata LR(1)", fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Guardar o retornar
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
            plt.close(fig)  # CRUCIAL: Cerrar figura para liberar memoria
            return image_base64
        
        if not return_base64:
            try:
                plt.show()
            except:
                print("⚠️  No se puede mostrar gráfico en modo headless")
        
        plt.close(fig)  # CRUCIAL: Siempre cerrar figura
        return None
    
    def _calculate_layout(self, G: nx.DiGraph, automaton_data: Dict[str, Any]) -> Dict[int, Tuple[float, float]]:
        """Calcula el layout del grafo para mejor visualización"""
        
        # Intentar layout jerárquico primero
        try:
            # Usar layout circular mejorado para autómatas
            pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
            
            # Ajustar posiciones para evitar solapamiento
            pos = self._adjust_positions(pos, G)
            
        except:
            # Fallback a layout circular
            pos = nx.circular_layout(G)
            
        return pos
    
    def _adjust_positions(self, pos: Dict[int, Tuple[float, float]], 
                         G: nx.DiGraph) -> Dict[int, Tuple[float, float]]:
        """Ajusta posiciones para evitar solapamiento de nodos"""
        
        min_distance = 0.3
        adjusted_pos = pos.copy()
        
        # Separar nodos que están muy cerca
        for node1 in G.nodes():
            for node2 in G.nodes():
                if node1 >= node2:
                    continue
                    
                x1, y1 = adjusted_pos[node1]
                x2, y2 = adjusted_pos[node2]
                
                distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                if distance < min_distance and distance > 0:
                    # Separar los nodos
                    dx = (x2 - x1) / distance
                    dy = (y2 - y1) / distance
                    
                    move_distance = (min_distance - distance) / 2
                    
                    adjusted_pos[node1] = (x1 - dx * move_distance, y1 - dy * move_distance)
                    adjusted_pos[node2] = (x2 + dx * move_distance, y2 + dy * move_distance)
        
        return adjusted_pos
    
    def _draw_graph(self, G: nx.DiGraph, pos: Dict[int, Tuple[float, float]], 
                   automaton_data: Dict[str, Any]):
        """Dibuja el grafo con estilos personalizados"""
        
        # Preparar colores y estilos para nodos
        node_colors = []
        node_sizes = []
        
        for node_data in automaton_data['nodes']:
            node_id = node_data['id']
            
            if node_data.get('is_initial', False):
                node_colors.append('#90EE90')  # Verde claro para inicial
                node_sizes.append(self.node_size * 1.2)
            elif node_data.get('is_final', False):
                node_colors.append('#FFB6C1')  # Rosa claro para final
                node_sizes.append(self.node_size * 1.1)
            else:
                node_colors.append('#E6E6FA')  # Lavanda para normales
                node_sizes.append(self.node_size)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(G, pos, 
                              node_color=node_colors,
                              node_size=node_sizes,
                              edgecolors='black',
                              linewidths=2)
        
        # Dibujar etiquetas de nodos
        node_labels = {node['id']: f"I{node['id']}" for node in automaton_data['nodes']}
        nx.draw_networkx_labels(G, pos, node_labels, 
                               font_size=self.font_size + 2,
                               font_weight='bold')
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos,
                              edge_color='gray',
                              arrows=True,
                              arrowsize=20,
                              arrowstyle='->',
                              width=2,
                              connectionstyle="arc3,rad=0.1")
        
        # Dibujar etiquetas de aristas
        edge_labels = {}
        for edge in automaton_data['edges']:
            edge_labels[(edge['from'], edge['to'])] = edge['label']
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels,
                                    font_size=self.edge_font_size,
                                    font_color='red',
                                    font_weight='bold',
                                    bbox=dict(boxstyle="round,pad=0.2", 
                                            facecolor='white', 
                                            edgecolor='none',
                                            alpha=0.8))
        
        # Agregar leyenda
        self._add_legend()
    
    def _add_legend(self):
        """Agrega leyenda al gráfico"""
        
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='#90EE90', markersize=15, 
                      markeredgecolor='black', label='Estado Inicial'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='#FFB6C1', markersize=15, 
                      markeredgecolor='black', label='Estado de Aceptación'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='#E6E6FA', markersize=15, 
                      markeredgecolor='black', label='Estado Normal')
        ]
        
        plt.legend(handles=legend_elements, loc='upper left', 
                  bbox_to_anchor=(0, 1), frameon=True, 
                  fancybox=True, shadow=True)
    
    def create_parsing_table_image(self, table_data: Dict[str, Any], 
                                 output_file: str = None,
                                 return_base64: bool = False) -> str:
        """
        Crea una imagen de la tabla de parsing
        
        Args:
            table_data: Datos de la tabla desde LR1Parser.get_parsing_table()
            output_file: Archivo donde guardar la imagen
            return_base64: Si retornar como base64
            
        Returns:
            String base64 si return_base64=True
        """
        
        states = table_data['states']
        terminals = table_data['terminals']
        non_terminals = table_data['non_terminals']
        action_matrix = table_data['action']
        goto_matrix = table_data['goto']
        
        # Calcular dimensiones
        rows = len(states) + 2  # +2 para headers
        cols = 1 + len(terminals) + len(non_terminals)  # +1 para estados
        
        fig, ax = plt.subplots(figsize=(max(16, cols * 1.2), max(10, rows * 0.5)))
        ax.axis('tight')
        ax.axis('off')
        
        # Crear datos de la tabla
        table_data_matrix = []
        
        # Header principal
        header1 = ['Estado'] + ['ACTION'] * len(terminals) + ['GOTO'] * len(non_terminals)
        table_data_matrix.append(header1)
        
        # Sub-header
        header2 = [''] + terminals + non_terminals
        table_data_matrix.append(header2)
        
        # Filas de datos
        for state in states:
            row = [str(state)]
            
            # Acciones
            for terminal in terminals:
                action = action_matrix[state].get(terminal, '')
                row.append(action)
            
            # Gotos
            for nt in non_terminals:
                goto = goto_matrix[state].get(nt, '')
                row.append(str(goto) if goto else '')
            
            table_data_matrix.append(row)
        
        # Crear tabla
        table = ax.table(cellText=table_data_matrix,
                        cellLoc='center',
                        loc='center',
                        bbox=[0, 0, 1, 1])
        
        # Estilizar tabla
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2)
        
        # Colorear headers
        for i in range(cols):
            table[(0, i)].set_facecolor('#4472C4')
            table[(0, i)].set_text_props(weight='bold', color='white')
            table[(1, i)].set_facecolor('#B4C6E7')
            table[(1, i)].set_text_props(weight='bold')
        
        # Colorear columnas de estado
        for i in range(2, rows):
            table[(i, 0)].set_facecolor('#F2F2F2')
            table[(i, 0)].set_text_props(weight='bold')
        
        # Colorear acciones y gotos
        action_cols = len(terminals)
        for i in range(2, rows):
            for j in range(1, action_cols + 1):
                table[(i, j)].set_facecolor('#E2EFDA')
            for j in range(action_cols + 1, cols):
                table[(i, j)].set_facecolor('#FFF2CC')
        
        plt.title("Tabla de Parsing LR(1)", fontsize=14, fontweight='bold', pad=20)
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"✅ Tabla guardada en: {output_file}")
        
        if return_base64:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close(fig)  # Cerrar figura específica
            return image_base64
        
        try:
            plt.show()
        except:
            print("⚠️  No se puede mostrar gráfico en modo headless")
        
        plt.close(fig)  # Siempre cerrar figura
        return None

def test_visualization():
    """Función de prueba para el visualizador"""
    from lr1_parser import LR1Parser
    
    print("🎨 Testeando visualizador de autómatas LR(1)")
    print("=" * 50)
    
    # Crear parser
    parser = LR1Parser()
    
    # Gramática de prueba
    grammar = """
S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
"""
    
    try:
        # Procesar gramática
        parser.parse_grammar(grammar)
        print("✅ Gramática procesada")
        
        # Crear visualizador
        visualizer = LR1GraphVisualizer()
        
        # Obtener datos del autómata
        automaton_data = parser.get_automaton_graph()
        print(f"📊 Estados: {len(automaton_data['nodes'])}")
        print(f"📊 Transiciones: {len(automaton_data['edges'])}")
        
        # Crear gráfico del autómata
        print("🎨 Generando gráfico del autómata...")
        visualizer.create_automaton_graph(automaton_data, 
                                        output_file="automaton_lr1.png")
        
        # Crear tabla de parsing
        print("📋 Generando tabla de parsing...")
        table_data = parser.get_parsing_table()
        visualizer.create_parsing_table_image(table_data,
                                            output_file="parsing_table_lr1.png")
        
        print("🎉 ¡Visualización completada!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_visualization()