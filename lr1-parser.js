class LR1Parser {
    constructor() {
        this.grammar = [];
        this.terminals = new Set();
        this.nonTerminals = new Set();
        this.startSymbol = null;
        this.firstSets = new Map();
        this.followSets = new Map();
        this.items = [];
        this.parsingTable = new Map();
        this.augmentedGrammar = [];
    }

    parseGrammar(grammarText) {
        this.grammar = [];
        this.terminals = new Set();
        this.nonTerminals = new Set();
        
        const lines = grammarText.trim().split('\n');
        
        for (let line of lines) {
            line = line.trim();
            if (!line || line.startsWith('//')) continue;
            
            const parts = line.split('->');
            if (parts.length !== 2) continue;
            
            const left = parts[0].trim();
            const right = parts[1].trim();
            
            this.nonTerminals.add(left);
            
            if (!this.startSymbol) {
                this.startSymbol = left;
            }
            
            const production = {
                left: left,
                right: right === 'ε' || right === 'epsilon' ? [] : right.split(/\s+/)
            };
            
            this.grammar.push(production);
            
            for (let symbol of production.right) {
                if (!this.isNonTerminal(symbol)) {
                    this.terminals.add(symbol);
                }
            }
        }
        
        this.terminals.add('$');
        this.createAugmentedGrammar();
        this.computeFirstSets();
        this.computeFollowSets();
        this.generateLR1Items();
        this.buildParsingTable();
    }

    isNonTerminal(symbol) {
        return /^[A-Z]/.test(symbol) && symbol.length === 1;
    }

    createAugmentedGrammar() {
        const newStart = this.startSymbol + "'";
        this.augmentedGrammar = [
            { left: newStart, right: [this.startSymbol] }
        ];
        this.augmentedGrammar = this.augmentedGrammar.concat(this.grammar);
        this.nonTerminals.add(newStart);
        this.startSymbol = newStart;
    }

    computeFirstSets() {
        this.firstSets.clear();
        
        for (let terminal of this.terminals) {
            this.firstSets.set(terminal, new Set([terminal]));
        }
        
        for (let nonTerminal of this.nonTerminals) {
            this.firstSets.set(nonTerminal, new Set());
        }
        
        let changed = true;
        while (changed) {
            changed = false;
            
            for (let production of this.augmentedGrammar) {
                const firstOfRight = this.getFirstOfSequence(production.right);
                const currentFirst = this.firstSets.get(production.left);
                const sizeBefore = currentFirst.size;
                
                for (let symbol of firstOfRight) {
                    currentFirst.add(symbol);
                }
                
                if (currentFirst.size > sizeBefore) {
                    changed = true;
                }
            }
        }
    }

    getFirstOfSequence(sequence) {
        if (sequence.length === 0) {
            return new Set(['ε']);
        }
        
        const result = new Set();
        
        for (let i = 0; i < sequence.length; i++) {
            const symbol = sequence[i];
            const firstOfSymbol = this.firstSets.get(symbol) || new Set([symbol]);
            
            for (let f of firstOfSymbol) {
                if (f !== 'ε') {
                    result.add(f);
                }
            }
            
            if (!firstOfSymbol.has('ε')) {
                break;
            }
            
            if (i === sequence.length - 1) {
                result.add('ε');
            }
        }
        
        return result;
    }

    computeFollowSets() {
        this.followSets.clear();
        
        for (let nonTerminal of this.nonTerminals) {
            this.followSets.set(nonTerminal, new Set());
        }
        
        this.followSets.get(this.startSymbol).add('$');
        
        let changed = true;
        while (changed) {
            changed = false;
            
            for (let production of this.augmentedGrammar) {
                for (let i = 0; i < production.right.length; i++) {
                    const symbol = production.right[i];
                    
                    if (this.nonTerminals.has(symbol)) {
                        const beta = production.right.slice(i + 1);
                        const firstOfBeta = this.getFirstOfSequence(beta);
                        const followOfSymbol = this.followSets.get(symbol);
                        const sizeBefore = followOfSymbol.size;
                        
                        for (let f of firstOfBeta) {
                            if (f !== 'ε') {
                                followOfSymbol.add(f);
                            }
                        }
                        
                        if (firstOfBeta.has('ε')) {
                            const followOfLeft = this.followSets.get(production.left);
                            for (let f of followOfLeft) {
                                followOfSymbol.add(f);
                            }
                        }
                        
                        if (followOfSymbol.size > sizeBefore) {
                            changed = true;
                        }
                    }
                }
            }
        }
    }

    generateLR1Items() {
        this.items = [];
        const itemSets = [];
        const visited = new Set();
        
        const startItem = {
            production: 0,
            dot: 0,
            lookahead: '$'
        };
        
        const initialSet = this.closure([startItem]);
        itemSets.push(initialSet);
        this.items.push(initialSet);
        
        let i = 0;
        while (i < itemSets.length) {
            const currentSet = itemSets[i];
            const transitions = new Map();
            
            for (let item of currentSet) {
                const production = this.augmentedGrammar[item.production];
                if (item.dot < production.right.length) {
                    const nextSymbol = production.right[item.dot];
                    
                    if (!transitions.has(nextSymbol)) {
                        transitions.set(nextSymbol, []);
                    }
                    
                    transitions.get(nextSymbol).push({
                        production: item.production,
                        dot: item.dot + 1,
                        lookahead: item.lookahead
                    });
                }
            }
            
            for (let [symbol, items] of transitions) {
                const newSet = this.closure(items);
                const setKey = this.getSetKey(newSet);
                
                if (!visited.has(setKey)) {
                    visited.add(setKey);
                    itemSets.push(newSet);
                    this.items.push(newSet);
                }
            }
            
            i++;
        }
    }

    closure(items) {
        const result = [...items];
        const added = new Set();
        
        let changed = true;
        while (changed) {
            changed = false;
            
            for (let item of result) {
                const production = this.augmentedGrammar[item.production];
                
                if (item.dot < production.right.length) {
                    const nextSymbol = production.right[item.dot];
                    
                    if (this.nonTerminals.has(nextSymbol)) {
                        const beta = production.right.slice(item.dot + 1);
                        const firstOfBetaLookahead = this.getFirstOfSequence([...beta, item.lookahead]);
                        
                        for (let i = 0; i < this.augmentedGrammar.length; i++) {
                            if (this.augmentedGrammar[i].left === nextSymbol) {
                                for (let lookahead of firstOfBetaLookahead) {
                                    if (lookahead !== 'ε') {
                                        const newItem = {
                                            production: i,
                                            dot: 0,
                                            lookahead: lookahead
                                        };
                                        
                                        const itemKey = `${i}-${0}-${lookahead}`;
                                        if (!added.has(itemKey)) {
                                            added.add(itemKey);
                                            result.push(newItem);
                                            changed = true;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        return result;
    }

    getSetKey(itemSet) {
        return itemSet.map(item => `${item.production}-${item.dot}-${item.lookahead}`).sort().join('|');
    }

    buildParsingTable() {
        this.parsingTable.clear();
        
        for (let i = 0; i < this.items.length; i++) {
            const itemSet = this.items[i];
            
            for (let item of itemSet) {
                const production = this.augmentedGrammar[item.production];
                
                if (item.dot < production.right.length) {
                    const nextSymbol = production.right[item.dot];
                    const gotoState = this.findGoto(i, nextSymbol);
                    
                    if (gotoState !== -1) {
                        if (this.terminals.has(nextSymbol)) {
                            this.setAction(i, nextSymbol, `s${gotoState}`);
                        } else {
                            this.setGoto(i, nextSymbol, gotoState);
                        }
                    }
                } else {
                    if (item.production === 0) {
                        this.setAction(i, '$', 'acc');
                    } else {
                        this.setAction(i, item.lookahead, `r${item.production}`);
                    }
                }
            }
        }
    }

    findGoto(state, symbol) {
        const currentSet = this.items[state];
        const transitions = [];
        
        for (let item of currentSet) {
            const production = this.augmentedGrammar[item.production];
            if (item.dot < production.right.length && production.right[item.dot] === symbol) {
                transitions.push({
                    production: item.production,
                    dot: item.dot + 1,
                    lookahead: item.lookahead
                });
            }
        }
        
        if (transitions.length === 0) return -1;
        
        const targetSet = this.closure(transitions);
        const targetKey = this.getSetKey(targetSet);
        
        for (let i = 0; i < this.items.length; i++) {
            if (this.getSetKey(this.items[i]) === targetKey) {
                return i;
            }
        }
        
        return -1;
    }

    setAction(state, terminal, action) {
        const key = `${state},${terminal}`;
        this.parsingTable.set(key, action);
    }

    setGoto(state, nonTerminal, nextState) {
        const key = `${state},${nonTerminal}`;
        this.parsingTable.set(key, nextState.toString());
    }

    getAction(state, terminal) {
        const key = `${state},${terminal}`;
        return this.parsingTable.get(key) || 'error';
    }

    getGoto(state, nonTerminal) {
        const key = `${state},${nonTerminal}`;
        const result = this.parsingTable.get(key);
        return result ? parseInt(result) : -1;
    }

    parseString(input) {
        const tokens = input.trim().split(/\s+/);
        tokens.push('$');
        
        const stack = [0];
        const trace = [];
        let pointer = 0;
        
        trace.push(`Iniciando parsing de: ${input}`);
        trace.push(`Stack: [${stack.join(', ')}]   Input: ${tokens.slice(pointer).join(' ')}`);
        
        while (true) {
            const state = stack[stack.length - 1];
            const symbol = tokens[pointer];
            const action = this.getAction(state, symbol);
            
            trace.push(`Estado ${state}, Símbolo '${symbol}', Acción: ${action}`);
            
            if (action === 'error') {
                trace.push(`ERROR: No se encontró acción para estado ${state} y símbolo '${symbol}'`);
                return {
                    success: false,
                    trace: trace,
                    error: `Error sintáctico en posición ${pointer}: símbolo inesperado '${symbol}'`
                };
            }
            
            if (action === 'acc') {
                trace.push('ACEPTADO: La cadena pertenece al lenguaje');
                return {
                    success: true,
                    trace: trace,
                    message: 'Cadena aceptada correctamente'
                };
            }
            
            if (action.startsWith('s')) {
                const nextState = parseInt(action.substring(1));
                stack.push(nextState);
                pointer++;
                trace.push(`Shift: empujar estado ${nextState}, avanzar`);
                trace.push(`Stack: [${stack.join(', ')}]   Input: ${tokens.slice(pointer).join(' ')}`);
            }
            
            else if (action.startsWith('r')) {
                const prodNum = parseInt(action.substring(1));
                const production = this.augmentedGrammar[prodNum];
                
                for (let i = 0; i < production.right.length; i++) {
                    stack.pop();
                }
                
                const currentState = stack[stack.length - 1];
                const gotoState = this.getGoto(currentState, production.left);
                
                if (gotoState === -1) {
                    trace.push(`ERROR: No se encontró GOTO para estado ${currentState} y no terminal '${production.left}'`);
                    return {
                        success: false,
                        trace: trace,
                        error: `Error en GOTO(${currentState}, ${production.left})`
                    };
                }
                
                stack.push(gotoState);
                trace.push(`Reduce: ${production.left} -> ${production.right.join(' ') || 'ε'}`);
                trace.push(`Stack: [${stack.join(', ')}]   Input: ${tokens.slice(pointer).join(' ')}`);
            }
            
            if (trace.length > 1000) {
                trace.push('ERROR: Parsing muy largo, posible bucle infinito');
                return {
                    success: false,
                    trace: trace,
                    error: 'Parsing demasiado largo'
                };
            }
        }
    }

    getFirstFollowDisplay() {
        const result = {
            first: {},
            follow: {}
        };
        
        for (let [symbol, set] of this.firstSets) {
            if (this.nonTerminals.has(symbol)) {
                result.first[symbol] = Array.from(set).sort();
            }
        }
        
        for (let [symbol, set] of this.followSets) {
            if (this.nonTerminals.has(symbol)) {
                result.follow[symbol] = Array.from(set).sort();
            }
        }
        
        return result;
    }

    getItemsDisplay() {
        return this.items.map((itemSet, index) => {
            const items = itemSet.map(item => {
                const production = this.augmentedGrammar[item.production];
                const rightWithDot = [...production.right];
                rightWithDot.splice(item.dot, 0, '•');
                return `${production.left} -> ${rightWithDot.join(' ') || '•'}, ${item.lookahead}`;
            });
            return {
                state: index,
                items: items
            };
        });
    }

    getParsingTableDisplay() {
        const states = Array.from({length: this.items.length}, (_, i) => i);
        const terminals = Array.from(this.terminals).sort();
        const nonTerminals = Array.from(this.nonTerminals).filter(nt => nt !== this.startSymbol).sort();
        
        const table = {
            states: states,
            terminals: terminals,
            nonTerminals: nonTerminals,
            actions: {},
            gotos: {}
        };
        
        for (let state of states) {
            table.actions[state] = {};
            table.gotos[state] = {};
            
            for (let terminal of terminals) {
                table.actions[state][terminal] = this.getAction(state, terminal);
            }
            
            for (let nonTerminal of nonTerminals) {
                const gotoValue = this.getGoto(state, nonTerminal);
                table.gotos[state][nonTerminal] = gotoValue === -1 ? '' : gotoValue.toString();
            }
        }
        
        return table;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LR1Parser };
} else if (typeof window !== 'undefined') {
    window.LR1Parser = LR1Parser;
}