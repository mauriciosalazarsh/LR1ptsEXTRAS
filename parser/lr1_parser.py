#!/usr/bin/env python3
"""
Parser LR(1) - Implementación completa en Python
Compiladores - UTEC - Puntos Extras Examen 2
"""

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import List, Set, Dict, Tuple, Optional, Any
import json

@dataclass
class Production:
    """Representa una producción de la gramática"""
    left: str
    right: List[str]
    number: int = 0
    
    def __str__(self):
        right_str = ' '.join(self.right) if self.right else 'ε'
        return f"{self.left} -> {right_str}"

@dataclass
class LR1Item:
    """Representa un item LR(1) con lookahead"""
    production: int
    dot_position: int
    lookahead: str
    
    def __str__(self):
        return f"[{self.production}, {self.dot_position}, {self.lookahead}]"
    
    def __hash__(self):
        return hash((self.production, self.dot_position, self.lookahead))
    
    def __eq__(self, other):
        return (self.production == other.production and 
                self.dot_position == other.dot_position and 
                self.lookahead == other.lookahead)

class LR1Parser:
    """Parser LR(1) completo con generación de autómata y tabla de parsing"""
    
    def __init__(self):
        self.grammar: List[Production] = []
        self.terminals: Set[str] = set()
        self.non_terminals: Set[str] = set()
        self.start_symbol: str = ""
        self.augmented_start: str = ""
        
        # Conjuntos FIRST y FOLLOW
        self.first_sets: Dict[str, Set[str]] = defaultdict(set)
        self.follow_sets: Dict[str, Set[str]] = defaultdict(set)
        
        # Autómata LR(1)
        self.states: List[Set[LR1Item]] = []
        self.transitions: Dict[Tuple[int, str], int] = {}
        
        # Tabla de parsing
        self.action_table: Dict[Tuple[int, str], str] = {}
        self.goto_table: Dict[Tuple[int, str], int] = {}
        
        # Para visualización
        self.parsing_trace: List[str] = []
    
    def parse_grammar(self, grammar_text: str):
        """Analiza la gramática de entrada y construye el parser LR(1)"""
        self._clear_data()
        self._parse_grammar_text(grammar_text)
        self._create_augmented_grammar()
        self._compute_first_sets()
        self._compute_follow_sets()
        self._build_lr1_automaton()
        self._build_parsing_table()
    
    def _clear_data(self):
        """Limpia todos los datos del parser"""
        self.grammar.clear()
        self.terminals.clear()
        self.non_terminals.clear()
        self.start_symbol = ""
        self.augmented_start = ""
        self.first_sets.clear()
        self.follow_sets.clear()
        self.states.clear()
        self.transitions.clear()
        self.action_table.clear()
        self.goto_table.clear()
        self.parsing_trace.clear()
    
    def _parse_grammar_text(self, text: str):
        """Parsea el texto de la gramática"""
        lines = text.strip().split('\n')
        prod_number = 0

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '->' not in line:
                continue

            left, right = line.split('->', 1)
            left = left.strip()
            right = right.strip()

            # Primer símbolo es el inicial
            if not self.start_symbol:
                self.start_symbol = left

            self.non_terminals.add(left)

            # Soportar múltiples producciones separadas por |
            alternatives = right.split('|')

            for alternative in alternatives:
                alternative = alternative.strip()

                # Procesar lado derecho
                if alternative == 'ε' or alternative == 'epsilon' or alternative == '' or not alternative:
                    right_symbols = []
                else:
                    right_symbols = alternative.split()

                production = Production(left, right_symbols, prod_number)
                self.grammar.append(production)
                prod_number += 1

                # Identificar terminales
                for symbol in right_symbols:
                    if not self._is_non_terminal(symbol):
                        self.terminals.add(symbol)

        # Agregar $ como terminal
        self.terminals.add('$')
    
    def _is_non_terminal(self, symbol: str) -> bool:
        """Determina si un símbolo es no terminal"""
        return symbol[0].isupper() if symbol else False
    
    def _create_augmented_grammar(self):
        """Crea la gramática aumentada"""
        self.augmented_start = self.start_symbol + "'"
        self.non_terminals.add(self.augmented_start)
        
        # Insertar producción S' -> S al inicio
        augmented_prod = Production(self.augmented_start, [self.start_symbol], 0)
        
        # Renumerar producciones existentes
        for i, prod in enumerate(self.grammar):
            prod.number = i + 1
        
        # Insertar al inicio
        self.grammar.insert(0, augmented_prod)
    
    def _compute_first_sets(self):
        """Calcula los conjuntos FIRST"""
        # los terminales tienen como first a ellos mismos
        for terminal in self.terminals:
            self.first_sets[terminal].add(terminal)

        # inicializar first de no terminales como conjunto vacio
        for non_terminal in self.non_terminals:
            self.first_sets[non_terminal] = set()

        # algoritmo de punto fijo: iterar hasta que no haya cambios
        changed = True
        while changed:
            changed = False

            for prod in self.grammar:
                first_before = len(self.first_sets[prod.left])

                if not prod.right:  # produccion vacia: A -> epsilon
                    self.first_sets[prod.left].add('ε')
                else:
                    # para A -> X1 X2 ... Xn, calcular first del lado derecho
                    first_of_right = self._first_of_sequence(prod.right)
                    self.first_sets[prod.left].update(first_of_right)

                # detectar si hubo cambios para seguir iterando
                if len(self.first_sets[prod.left]) > first_before:
                    changed = True
    
    def _first_of_sequence(self, sequence: List[str]) -> Set[str]:
        """Calcula FIRST de una secuencia de símbolos"""
        if not sequence:
            return {'ε'}

        result = set()

        # procesar cada simbolo de la secuencia
        for i, symbol in enumerate(sequence):
            first_of_symbol = self.first_sets[symbol].copy()

            # agregar todos los terminales del first excepto epsilon
            result.update(first_of_symbol - {'ε'})

            # si epsilon no esta en first del simbolo, terminamos
            if 'ε' not in first_of_symbol:
                break

            # si todos los simbolos derivan epsilon, agregarlo al resultado
            if i == len(sequence) - 1:
                result.add('ε')

        return result
    
    def _compute_follow_sets(self):
        """Calcula los conjuntos FOLLOW"""
        # inicializar follow de todos los no terminales
        for non_terminal in self.non_terminals:
            self.follow_sets[non_terminal] = set()

        # el simbolo inicial siempre tiene $ en su follow
        self.follow_sets[self.augmented_start].add('$')

        # algoritmo de punto fijo para calcular follow
        changed = True
        while changed:
            changed = False

            for prod in self.grammar:
                # examinar cada simbolo del lado derecho
                for i, symbol in enumerate(prod.right):
                    if symbol in self.non_terminals:
                        follow_before = len(self.follow_sets[symbol])

                        # beta son los simbolos que siguen al no terminal
                        beta = prod.right[i + 1:]
                        first_of_beta = self._first_of_sequence(beta)

                        # regla 2: agregar first(beta) sin epsilon a follow(A)
                        self.follow_sets[symbol].update(first_of_beta - {'ε'})

                        # regla 3: si beta deriva epsilon, agregar follow del lado izquierdo
                        if 'ε' in first_of_beta:
                            self.follow_sets[symbol].update(self.follow_sets[prod.left])
                        
                        if len(self.follow_sets[symbol]) > follow_before:
                            changed = True
    
    def _build_lr1_automaton(self):
        """Construye el autómata LR(1)"""
        # Estado inicial
        initial_item = LR1Item(0, 0, '$')
        initial_state = self._closure({initial_item})
        
        self.states = [initial_state]
        state_queue = deque([0])
        state_map = {self._state_key(initial_state): 0}
        
        while state_queue:
            current_state_num = state_queue.popleft()
            current_state = self.states[current_state_num]
            
            # Agrupar items por símbolo después del punto
            symbol_groups = defaultdict(set)
            
            for item in current_state:
                if item.dot_position < len(self.grammar[item.production].right):
                    next_symbol = self.grammar[item.production].right[item.dot_position]
                    new_item = LR1Item(item.production, item.dot_position + 1, item.lookahead)
                    symbol_groups[next_symbol].add(new_item)
            
            # Para cada símbolo, crear nuevo estado
            for symbol, items in symbol_groups.items():
                new_state = self._closure(items)
                state_key = self._state_key(new_state)
                
                if state_key not in state_map:
                    # Nuevo estado
                    new_state_num = len(self.states)
                    self.states.append(new_state)
                    state_map[state_key] = new_state_num
                    state_queue.append(new_state_num)
                else:
                    new_state_num = state_map[state_key]
                
                # Agregar transición
                self.transitions[(current_state_num, symbol)] = new_state_num
    
    def _closure(self, items: Set[LR1Item]) -> Set[LR1Item]:
        """Calcula la clausura de un conjunto de items LR(1)"""
        result = set(items)
        changed = True
        
        while changed:
            changed = False
            new_items = set()
            
            for item in result:
                prod = self.grammar[item.production]
                
                # Si el punto no está al final
                if item.dot_position < len(prod.right):
                    next_symbol = prod.right[item.dot_position]
                    
                    # Si el siguiente símbolo es no terminal
                    if next_symbol in self.non_terminals:
                        # Beta = símbolos después del no terminal
                        beta = prod.right[item.dot_position + 1:] + [item.lookahead]
                        first_of_beta = self._first_of_sequence(beta)
                        
                        # Para cada producción A -> α
                        for prod_num, production in enumerate(self.grammar):
                            if production.left == next_symbol:
                                for lookahead in first_of_beta - {'ε'}:
                                    new_item = LR1Item(prod_num, 0, lookahead)
                                    if new_item not in result:
                                        new_items.add(new_item)
                                        changed = True
            
            result.update(new_items)
        
        return result
    
    def _state_key(self, state: Set[LR1Item]) -> str:
        """Genera una clave única para un estado"""
        items_list = sorted(list(state), key=lambda x: (x.production, x.dot_position, x.lookahead))
        return str(items_list)
    
    def _build_parsing_table(self):
        """Construye la tabla de parsing ACTION/GOTO"""
        for state_num, state in enumerate(self.states):
            for item in state:
                prod = self.grammar[item.production]
                
                # Item de shift: A -> α•aβ
                if item.dot_position < len(prod.right):
                    next_symbol = prod.right[item.dot_position]
                    
                    if (state_num, next_symbol) in self.transitions:
                        next_state = self.transitions[(state_num, next_symbol)]
                        
                        if next_symbol in self.terminals:
                            # ACTION[state, a] = shift next_state
                            self.action_table[(state_num, next_symbol)] = f's{next_state}'
                        else:
                            # GOTO[state, A] = next_state
                            self.goto_table[(state_num, next_symbol)] = next_state
                
                # Item de reduce: A -> α•
                else:
                    if item.production == 0:  # S' -> S•
                        # ACTION[state, $] = accept
                        self.action_table[(state_num, '$')] = 'acc'
                    else:
                        # ACTION[state, lookahead] = reduce production
                        self.action_table[(state_num, item.lookahead)] = f'r{item.production}'
    
    def parse_string(self, input_string: str) -> Dict[str, Any]:
        """Analiza una cadena usando el parser LR(1)"""
        tokens = input_string.strip().split() + ['$']
        stack = [0]  # Pila con estados
        symbol_stack = []  # Pila con símbolos para traza
        pointer = 0
        self.parsing_trace = []

        trace_steps = []  # Para la traza formateada

        step = 1
        while True:
            state = stack[-1]
            symbol = tokens[pointer]

            # Guardar paso para traza
            stack_str = ' '.join(str(s) for s in stack)
            input_str = ' '.join(tokens[pointer:])

            # Buscar acción
            action = self.action_table.get((state, symbol), 'error')

            if action == 'error':
                trace_steps.append({
                    'stack': stack_str,
                    'input': input_str,
                    'action': f'ERROR: símbolo inesperado "{symbol}"'
                })
                return {
                    'success': False,
                    'error': f'Error sintáctico en posición {pointer}: símbolo inesperado "{symbol}"',
                    'trace': trace_steps
                }

            elif action == 'acc' or action == 'accept':
                trace_steps.append({
                    'stack': stack_str,
                    'input': input_str,
                    'action': 'ACCEPT'
                })
                return {
                    'success': True,
                    'message': 'Cadena aceptada correctamente',
                    'trace': trace_steps
                }

            elif action.startswith('s'):  # Shift
                next_state = int(action[1:])
                stack.append(next_state)
                symbol_stack.append(symbol)

                trace_steps.append({
                    'stack': stack_str,
                    'input': input_str,
                    'action': f'shift {next_state}'
                })

                pointer += 1

            elif action.startswith('r'):  # Reduce
                prod_num = int(action[1:])
                prod = self.grammar[prod_num]

                # Hacer pop de |rhs| elementos (tanto de stack como de symbol_stack)
                pop_count = len(prod.right)
                for _ in range(pop_count):
                    if len(stack) > 1:  # No quitar el estado inicial
                        stack.pop()
                    if symbol_stack:
                        symbol_stack.pop()

                # Buscar GOTO
                current_state = stack[-1]
                goto_state = self.goto_table.get((current_state, prod.left), -1)

                if goto_state == -1:
                    trace_steps.append({
                        'stack': stack_str,
                        'input': input_str,
                        'action': f'ERROR en GOTO({current_state}, {prod.left})'
                    })
                    return {
                        'success': False,
                        'error': f'Error en GOTO({current_state}, {prod.left})',
                        'trace': trace_steps
                    }

                stack.append(goto_state)
                symbol_stack.append(prod.left)

                prod_str = f"{prod.left} -> {' '.join(prod.right) if prod.right else 'ε'}"
                trace_steps.append({
                    'stack': stack_str,
                    'input': input_str,
                    'action': f'reduce {prod_num} ({prod_str})'
                })

            step += 1
            if step > 1000:  # Prevenir bucles infinitos
                return {
                    'success': False,
                    'error': 'Parsing demasiado largo, posible bucle infinito',
                    'trace': trace_steps
                }
    
    def get_first_follow_sets(self) -> Dict[str, Any]:
        """Retorna los conjuntos FIRST y FOLLOW"""
        return {
            'first': {nt: sorted(list(self.first_sets[nt])) 
                     for nt in self.non_terminals if nt != self.augmented_start},
            'follow': {nt: sorted(list(self.follow_sets[nt])) 
                      for nt in self.non_terminals if nt != self.augmented_start}
        }
    
    def get_states_info(self) -> List[Dict[str, Any]]:
        """Retorna información de todos los estados"""
        states_info = []
        
        for i, state in enumerate(self.states):
            items_str = []
            for item in sorted(state, key=lambda x: (x.production, x.dot_position, x.lookahead)):
                prod = self.grammar[item.production]
                rhs = prod.right.copy()
                rhs.insert(item.dot_position, '•')
                items_str.append(f"{prod.left} -> {' '.join(rhs)}, {item.lookahead}")
            
            states_info.append({
                'number': i,
                'items': items_str
            })
        
        return states_info
    
    def get_parsing_table(self) -> Dict[str, Any]:
        """Retorna la tabla de parsing"""
        states = list(range(len(self.states)))
        terminals = sorted(list(self.terminals))
        non_terminals = sorted([nt for nt in self.non_terminals if nt != self.augmented_start])
        
        action_matrix = {}
        goto_matrix = {}
        
        for state in states:
            action_matrix[state] = {}
            goto_matrix[state] = {}
            
            for terminal in terminals:
                action_matrix[state][terminal] = self.action_table.get((state, terminal), '')
            
            for nt in non_terminals:
                goto_matrix[state][nt] = self.goto_table.get((state, nt), '')
        
        return {
            'states': states,
            'terminals': terminals,
            'non_terminals': non_terminals,
            'action': action_matrix,
            'goto': goto_matrix
        }
    
    def get_automaton_graph(self) -> Dict[str, Any]:
        """Retorna datos del autómata para visualización"""
        nodes = []
        edges = []
        
        # Crear nodos
        for i, state in enumerate(self.states):
            label = f"I{i}"
            items = []
            for item in sorted(state, key=lambda x: (x.production, x.dot_position, x.lookahead)):
                prod = self.grammar[item.production]
                rhs = prod.right.copy()
                rhs.insert(item.dot_position, '•')
                items.append(f"{prod.left} -> {' '.join(rhs)}, {item.lookahead}")
            
            nodes.append({
                'id': i,
                'label': label,
                'items': items,
                'is_initial': i == 0,
                'is_final': any(item.production == 0 and item.dot_position == 1 
                               for item in state)
            })
        
        # Crear aristas
        for (from_state, symbol), to_state in self.transitions.items():
            edges.append({
                'from': from_state,
                'to': to_state,
                'label': symbol
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }

def main():
    """Función principal para pruebas"""
    parser = LR1Parser()
    
    grammar = """
S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
"""
    
    print("Testeando Parser LR(1)")
    print("=" * 50)

    try:
        parser.parse_grammar(grammar)
        print("[OK] Gramática procesada exitosamente")

        # Mostrar conjuntos FIRST y FOLLOW
        ff = parser.get_first_follow_sets()
        print("\nConjuntos FIRST:")
        for nt, first_set in ff['first'].items():
            print(f"  FIRST({nt}) = {{{', '.join(first_set)}}}")

        print("\nConjuntos FOLLOW:")
        for nt, follow_set in ff['follow'].items():
            print(f"  FOLLOW({nt}) = {{{', '.join(follow_set)}}}")

        print(f"\nEstados del autómata: {len(parser.states)}")

        # Probar cadenas
        test_strings = ["id", "id + id", "id + id * id", "( id + id ) * id"]
        print("\nProbando cadenas:")

        for test_str in test_strings:
            result = parser.parse_string(test_str)
            status = "[ACEPTADA]" if result['success'] else "[RECHAZADA]"
            print(f"  '{test_str}' -> {status}")

        print("\n[OK] Todas las pruebas completadas")

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()