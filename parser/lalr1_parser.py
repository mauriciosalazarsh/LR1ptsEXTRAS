#!/usr/bin/env python3
"""
Parser LALR(1) - Implementación basada en LR(1) con fusión de estados
Compiladores - UTEC - Puntos Extras Examen 2
"""

from collections import defaultdict, deque
from typing import List, Set, Dict, Tuple, Any

# Importar desde el mismo directorio si se ejecuta directamente
try:
    from parser.lr1_parser import LR1Parser, LR1Item, Production
except ModuleNotFoundError:
    from lr1_parser import LR1Parser, LR1Item, Production


class LALR1Parser(LR1Parser):
    """Parser LALR(1) que fusiona estados LR(1) con el mismo núcleo"""

    def __init__(self):
        super().__init__()
        self.lr1_to_lalr_map: Dict[int, int] = {}  # Mapeo de estados LR(1) a LALR(1)
        self.lalr_states: List[Set[LR1Item]] = []  # Estados LALR(1) fusionados
        self.lalr_transitions: Dict[Tuple[int, str], int] = {}

    def _build_lr1_automaton(self):
        """Construye el autómata LR(1) y luego lo convierte a LALR(1)"""
        # Primero construir autómata LR(1) completo
        super()._build_lr1_automaton()

        # Luego fusionar estados con el mismo núcleo
        self._merge_states_with_same_core()

    def _get_core(self, state: Set[LR1Item]) -> frozenset:
        """
        Obtiene el núcleo de un estado (items sin considerar lookahead)
        El núcleo es el conjunto de pares (producción, posición del punto)
        """
        core = set()
        for item in state:
            core.add((item.production, item.dot_position))
        return frozenset(core)

    def _merge_states_with_same_core(self):
        """Fusiona estados LR(1) que tienen el mismo núcleo para crear estados LALR(1)"""
        # Agrupar estados por núcleo
        core_to_lr1_states: Dict[frozenset, List[int]] = defaultdict(list)

        for state_idx, state in enumerate(self.states):
            core = self._get_core(state)
            core_to_lr1_states[core].append(state_idx)

        # Crear estados LALR(1) fusionando items con mismo núcleo
        self.lalr_states = []
        self.lr1_to_lalr_map = {}
        lalr_state_idx = 0

        for core, lr1_state_indices in core_to_lr1_states.items():
            # Fusionar todos los items de los estados con el mismo núcleo
            merged_items = set()

            for lr1_idx in lr1_state_indices:
                merged_items.update(self.states[lr1_idx])

            # Crear nuevo estado LALR(1)
            self.lalr_states.append(merged_items)

            # Mapear todos los estados LR(1) al nuevo estado LALR(1)
            for lr1_idx in lr1_state_indices:
                self.lr1_to_lalr_map[lr1_idx] = lalr_state_idx

            lalr_state_idx += 1

        # Crear transiciones LALR(1) mapeando las transiciones LR(1)
        self.lalr_transitions = {}

        for (from_lr1, symbol), to_lr1 in self.transitions.items():
            from_lalr = self.lr1_to_lalr_map[from_lr1]
            to_lalr = self.lr1_to_lalr_map[to_lr1]

            # Una transición LALR puede tener múltiples transiciones LR(1) que la generan
            # pero todas deben ir al mismo estado LALR de destino
            if (from_lalr, symbol) in self.lalr_transitions:
                # Verificar consistencia
                assert self.lalr_transitions[(from_lalr, symbol)] == to_lalr, \
                    "Conflicto en transiciones LALR(1)"
            else:
                self.lalr_transitions[(from_lalr, symbol)] = to_lalr

        # Reemplazar estados y transiciones con versiones LALR
        self.states = self.lalr_states
        self.transitions = self.lalr_transitions

        # Reconstruir tabla de parsing con estados LALR
        self._build_parsing_table()

    def _build_parsing_table(self):
        """Construye la tabla de parsing ACTION/GOTO para LALR(1)"""
        self.action_table.clear()
        self.goto_table.clear()

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
                            key = (state_num, next_symbol)
                            if key in self.action_table:
                                # Verificar conflictos shift/reduce o shift/shift
                                existing = self.action_table[key]
                                new_action = f's{next_state}'
                                if existing != new_action:
                                    # Conflicto detectado en LALR(1)
                                    # Por ahora preferir shift sobre reduce
                                    if not existing.startswith('s'):
                                        self.action_table[key] = new_action
                            else:
                                self.action_table[key] = f's{next_state}'
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
                        key = (state_num, item.lookahead)
                        if key in self.action_table:
                            # Conflicto shift/reduce o reduce/reduce
                            existing = self.action_table[key]
                            new_action = f'r{item.production}'
                            if existing != new_action:
                                # Conflicto en LALR(1)
                                # Preferir shift sobre reduce (por defecto)
                                if not existing.startswith('s'):
                                    # Si ambos son reduce, tomar el de menor número
                                    if existing.startswith('r') and new_action.startswith('r'):
                                        existing_num = int(existing[1:])
                                        new_num = int(new_action[1:])
                                        if new_num < existing_num:
                                            self.action_table[key] = new_action
                        else:
                            self.action_table[key] = f'r{item.production}'

    def get_comparison_info(self) -> Dict[str, Any]:
        """Retorna información comparativa entre LR(1) y LALR(1)"""
        return {
            'lalr_states': len(self.states),
            'lalr_transitions': len(self.transitions),
            'parser_type': 'LALR(1)'
        }


def main():
    """Función principal para pruebas"""
    parser = LALR1Parser()

    grammar = """
S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
"""

    print("Testeando Parser LALR(1)")
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

        print(f"\nEstados del autómata LALR(1): {len(parser.states)}")
        print(f"Transiciones: {len(parser.transitions)}")

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
