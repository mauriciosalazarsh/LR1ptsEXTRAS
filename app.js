class ParserApp {
    constructor() {
        this.parser = new LR1Parser();
        this.initializeElements();
        this.bindEvents();
        this.loadExampleGrammar();
    }

    initializeElements() {
        this.grammarTextarea = document.getElementById('grammar');
        this.parseGrammarBtn = document.getElementById('parse-grammar');
        this.clearGrammarBtn = document.getElementById('clear-grammar');
        this.inputStringField = document.getElementById('input-string');
        this.parseStringBtn = document.getElementById('parse-string');
        this.firstFollowDisplay = document.getElementById('first-follow-display');
        this.itemsDisplay = document.getElementById('items-display');
        this.parsingTableDisplay = document.getElementById('parsing-table-display');
        this.parsingResult = document.getElementById('parsing-result');
        this.parsingTrace = document.getElementById('parsing-trace');
    }

    bindEvents() {
        this.parseGrammarBtn.addEventListener('click', () => this.parseGrammar());
        this.clearGrammarBtn.addEventListener('click', () => this.clearGrammar());
        this.parseStringBtn.addEventListener('click', () => this.parseString());
        
        this.grammarTextarea.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.parseGrammar();
            }
        });
        
        this.inputStringField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.parseString();
            }
        });
    }

    loadExampleGrammar() {
        const exampleGrammar = `S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id`;
        this.grammarTextarea.value = exampleGrammar;
    }

    parseGrammar() {
        const grammarText = this.grammarTextarea.value.trim();
        
        if (!grammarText) {
            this.showError('Por favor ingrese una gramática');
            return;
        }

        try {
            this.showLoading('Generando tabla LR(1)...');
            
            setTimeout(() => {
                try {
                    this.parser.parseGrammar(grammarText);
                    this.displayFirstFollow();
                    this.displayItems();
                    this.displayParsingTable();
                    this.showSuccess('Tabla LR(1) generada exitosamente');
                    this.inputStringField.value = 'id + id * id';
                } catch (error) {
                    this.showError(`Error al procesar la gramática: ${error.message}`);
                    console.error('Error details:', error);
                }
            }, 100);
        } catch (error) {
            this.showError(`Error al procesar la gramática: ${error.message}`);
            console.error('Error details:', error);
        }
    }

    parseString() {
        const inputString = this.inputStringField.value.trim();
        
        if (!inputString) {
            this.showParsingError('Por favor ingrese una cadena a analizar');
            return;
        }

        if (this.parser.grammar.length === 0) {
            this.showParsingError('Primero debe generar la tabla LR(1)');
            return;
        }

        try {
            const result = this.parser.parseString(inputString);
            this.displayParsingResult(result);
            this.displayParsingTrace(result.trace);
        } catch (error) {
            this.showParsingError(`Error durante el parsing: ${error.message}`);
            console.error('Parsing error:', error);
        }
    }

    clearGrammar() {
        this.grammarTextarea.value = '';
        this.firstFollowDisplay.innerHTML = '';
        this.itemsDisplay.innerHTML = '';
        this.parsingTableDisplay.innerHTML = '';
        this.parsingResult.innerHTML = '';
        this.parsingTrace.innerHTML = '';
        this.inputStringField.value = '';
    }

    showLoading(message) {
        this.parsingResult.className = 'result-section';
        this.parsingResult.innerHTML = `<div class="loading"></div> ${message}`;
    }

    showSuccess(message) {
        this.parsingResult.className = 'result-section result-success';
        this.parsingResult.innerHTML = `✓ ${message}`;
    }

    showError(message) {
        this.parsingResult.className = 'result-section result-error';
        this.parsingResult.innerHTML = `✗ ${message}`;
    }

    showParsingError(message) {
        this.parsingResult.className = 'result-section result-error';
        this.parsingResult.innerHTML = `✗ ${message}`;
        this.parsingTrace.innerHTML = '';
    }

    displayFirstFollow() {
        const firstFollow = this.parser.getFirstFollowDisplay();
        
        let html = '<div class="first-follow-table">';
        
        html += '<div class="first-sets">';
        html += '<h3>Conjuntos FIRST</h3>';
        for (let [symbol, set] of Object.entries(firstFollow.first)) {
            html += `<div class="set-item">
                <span><strong>${symbol}:</strong></span>
                <span>{${set.join(', ')}}</span>
            </div>`;
        }
        html += '</div>';
        
        html += '<div class="follow-sets">';
        html += '<h3>Conjuntos FOLLOW</h3>';
        for (let [symbol, set] of Object.entries(firstFollow.follow)) {
            html += `<div class="set-item">
                <span><strong>${symbol}:</strong></span>
                <span>{${set.join(', ')}}</span>
            </div>`;
        }
        html += '</div>';
        
        html += '</div>';
        this.firstFollowDisplay.innerHTML = html;
    }

    displayItems() {
        const items = this.parser.getItemsDisplay();
        
        let html = '<div class="items-container">';
        
        for (let itemSet of items) {
            html += `<div class="item-set">
                <h4>I${itemSet.state}</h4>`;
            
            for (let item of itemSet.items) {
                html += `<div class="item">${this.escapeHtml(item)}</div>`;
            }
            
            html += '</div>';
        }
        
        html += '</div>';
        this.itemsDisplay.innerHTML = html;
    }

    displayParsingTable() {
        const table = this.parser.getParsingTableDisplay();
        
        let html = '<table class="parsing-table">';
        
        html += '<thead><tr>';
        html += '<th>Estado</th>';
        
        html += '<th colspan="' + table.terminals.length + '">ACTION</th>';
        html += '<th colspan="' + table.nonTerminals.length + '">GOTO</th>';
        html += '</tr>';
        
        html += '<tr>';
        html += '<th></th>';
        for (let terminal of table.terminals) {
            html += `<th>${this.escapeHtml(terminal)}</th>`;
        }
        for (let nonTerminal of table.nonTerminals) {
            html += `<th>${this.escapeHtml(nonTerminal)}</th>`;
        }
        html += '</tr></thead>';
        
        html += '<tbody>';
        for (let state of table.states) {
            html += `<tr><td><strong>${state}</strong></td>`;
            
            for (let terminal of table.terminals) {
                const action = table.actions[state][terminal];
                const cellClass = action === 'error' ? 'error-cell' : 'action-cell';
                const displayAction = action === 'error' ? '' : action;
                html += `<td class="${cellClass}">${this.escapeHtml(displayAction)}</td>`;
            }
            
            for (let nonTerminal of table.nonTerminals) {
                const gotoValue = table.gotos[state][nonTerminal];
                html += `<td class="goto-cell">${this.escapeHtml(gotoValue)}</td>`;
            }
            
            html += '</tr>';
        }
        html += '</tbody>';
        
        html += '</table>';
        this.parsingTableDisplay.innerHTML = html;
    }

    displayParsingResult(result) {
        if (result.success) {
            this.parsingResult.className = 'result-section result-success';
            this.parsingResult.innerHTML = `✓ ${result.message}`;
        } else {
            this.parsingResult.className = 'result-section result-error';
            this.parsingResult.innerHTML = `✗ ${result.error}`;
        }
    }

    displayParsingTrace(trace) {
        let html = '';
        
        for (let i = 0; i < trace.length; i++) {
            html += `<div class="trace-step">
                <strong>Paso ${i + 1}:</strong> ${this.escapeHtml(trace[i])}
            </div>`;
        }
        
        this.parsingTrace.innerHTML = html;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ParserApp();
});