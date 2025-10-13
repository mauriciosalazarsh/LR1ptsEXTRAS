/* 
 * JavaScript para la aplicación Parser LR(1)
 * Compiladores - UTEC
 */

// Configuración global
const CONFIG = {
    API_BASE_URL: '',
    ANIMATION_DURATION: 300,
    MAX_TRACE_LINES: 1000
};

// Estado de la aplicación
let appState = {
    grammarProcessed: false,
    currentGrammarData: null,
    isProcessing: false
};

// Utilidades
const Utils = {
    /**
     * Escapa caracteres HTML
     */
    escapeHtml: function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Formatea números con separadores
     */
    formatNumber: function(num) {
        return num.toLocaleString();
    },

    /**
     * Copia texto al portapapeles
     */
    copyToClipboard: async function(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback para navegadores más antiguos
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return true;
        }
    },

    /**
     * Descarga contenido como archivo
     */
    downloadFile: function(content, filename, mimeType = 'text/plain') {
        const blob = new Blob([content], { type: mimeType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
    },

    /**
     * Scroll suave a un elemento
     */
    smoothScrollTo: function(selector, offset = 80) {
        const element = document.querySelector(selector);
        if (element) {
            const top = element.offsetTop - offset;
            window.scrollTo({
                top: top,
                behavior: 'smooth'
            });
        }
    },

    /**
     * Debounce para funciones
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Manejo de notificaciones
const Notifications = {
    show: function(type, message, duration = 5000) {
        const alertClass = `alert-${type === 'error' ? 'danger' : type}`;
        const icon = this.getIcon(type);
        
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                <i class="fas fa-${icon} me-2"></i>
                ${Utils.escapeHtml(message)}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const container = document.getElementById('status-alert');
        container.innerHTML = alertHtml;
        container.style.display = 'block';
        
        // Auto-dismiss después del tiempo especificado
        if (duration > 0) {
            setTimeout(() => {
                const alert = container.querySelector('.alert');
                if (alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, duration);
        }
    },

    getIcon: function(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'warning': 'exclamation-circle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    },

    hide: function() {
        const container = document.getElementById('status-alert');
        container.style.display = 'none';
    }
};

// Manejo de estado de carga
const LoadingManager = {
    show: function(message = 'Procesando...') {
        const indicator = document.getElementById('loading-indicator');
        const button = document.getElementById('btn-parse-grammar');
        
        indicator.style.display = 'block';
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
        
        appState.isProcessing = true;
    },

    hide: function() {
        const indicator = document.getElementById('loading-indicator');
        const button = document.getElementById('btn-parse-grammar');
        
        indicator.style.display = 'none';
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-cogs me-2"></i>Generar Parser LR(1)';
        
        appState.isProcessing = false;
    }
};

// API Client
const ApiClient = {
    async request(endpoint, options = {}) {
        try {
            const response = await fetch(CONFIG.API_BASE_URL + endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    },

    async parseGrammar(grammar) {
        return this.request('/api/parse_grammar', {
            method: 'POST',
            body: JSON.stringify({ grammar })
        });
    },

    async parseString(string) {
        return this.request('/api/parse_string', {
            method: 'POST',
            body: JSON.stringify({ string })
        });
    },

    async getExamples() {
        return this.request('/api/examples');
    }
};

// Validación de entrada
const Validator = {
    validateGrammar: function(grammar) {
        if (!grammar || grammar.trim().length === 0) {
            return { valid: false, message: 'La gramática no puede estar vacía' };
        }

        const lines = grammar.trim().split('\n');
        const validLines = lines.filter(line => {
            const trimmed = line.trim();
            return trimmed.length > 0 && !trimmed.startsWith('#');
        });

        if (validLines.length === 0) {
            return { valid: false, message: 'La gramática debe tener al menos una producción' };
        }

        // Validar formato básico
        for (let i = 0; i < validLines.length; i++) {
            const line = validLines[i];
            if (!line.includes('->')) {
                return { 
                    valid: false, 
                    message: `Línea ${i + 1}: Formato inválido. Use "A -> α"` 
                };
            }
        }

        return { valid: true };
    },

    validateString: function(string) {
        if (!string || string.trim().length === 0) {
            return { valid: false, message: 'La cadena no puede estar vacía' };
        }

        return { valid: true };
    }
};

// Exportadores
const Exporters = {
    async exportGrammarData() {
        if (!appState.currentGrammarData) {
            Notifications.show('warning', 'No hay datos para exportar');
            return;
        }

        const data = {
            grammar: document.getElementById('grammar-input').value,
            timestamp: new Date().toISOString(),
            data: appState.currentGrammarData
        };

        const json = JSON.stringify(data, null, 2);
        Utils.downloadFile(json, `lr1_grammar_${Date.now()}.json`, 'application/json');
        
        Notifications.show('success', 'Datos exportados exitosamente');
    },

    async exportParsingTable() {
        if (!appState.currentGrammarData) {
            Notifications.show('warning', 'No hay tabla para exportar');
            return;
        }

        try {
            const response = await fetch('/api/export_table');
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `parsing_table_${Date.now()}.png`;
                a.click();
                window.URL.revokeObjectURL(url);
                
                Notifications.show('success', 'Tabla exportada exitosamente');
            } else {
                throw new Error('Error al exportar tabla');
            }
        } catch (error) {
            Notifications.show('error', 'Error al exportar tabla');
        }
    },

    async exportAutomaton() {
        if (!appState.currentGrammarData) {
            Notifications.show('warning', 'No hay autómata para exportar');
            return;
        }

        try {
            const response = await fetch('/api/export_graph');
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `automaton_${Date.now()}.png`;
                a.click();
                window.URL.revokeObjectURL(url);
                
                Notifications.show('success', 'Autómata exportado exitosamente');
            } else {
                throw new Error('Error al exportar autómata');
            }
        } catch (error) {
            Notifications.show('error', 'Error al exportar autómata');
        }
    }
};

// Gestión de ejemplos
const ExampleManager = {
    examples: {},

    async loadExamples() {
        try {
            this.examples = await ApiClient.getExamples();
        } catch (error) {
            console.error('Error loading examples:', error);
            Notifications.show('warning', 'No se pudieron cargar los ejemplos');
        }
    },

    loadExample(exampleType) {
        const example = this.examples[exampleType];
        if (!example) {
            Notifications.show('error', 'Ejemplo no encontrado');
            return;
        }

        document.getElementById('grammar-input').value = example.grammar;
        document.getElementById('input-string').value = example.test_strings[0] || '';
        
        Notifications.show('success', `Ejemplo cargado: ${example.name}`);
    }
};

// Event handlers
const EventHandlers = {
    init() {
        // Botones principales
        document.getElementById('btn-parse-grammar').addEventListener('click', this.handleParseGrammar);
        document.getElementById('btn-parse-string').addEventListener('click', this.handleParseString);
        document.getElementById('btn-clear').addEventListener('click', this.handleClear);

        // Hotkeys
        document.getElementById('grammar-input').addEventListener('keydown', this.handleGrammarKeydown);
        document.getElementById('input-string').addEventListener('keydown', this.handleStringKeydown);

        // Auto-resize textarea
        const grammarInput = document.getElementById('grammar-input');
        grammarInput.addEventListener('input', this.handleGrammarInput);

        // Copiar al portapapeles
        document.addEventListener('click', this.handleCopyClick);
    },

    handleParseGrammar: async function() {
        if (appState.isProcessing) return;

        const grammar = document.getElementById('grammar-input').value.trim();
        const validation = Validator.validateGrammar(grammar);
        
        if (!validation.valid) {
            Notifications.show('error', validation.message);
            return;
        }

        LoadingManager.show();

        try {
            const result = await ApiClient.parseGrammar(grammar);
            
            if (result.success) {
                appState.currentGrammarData = result.data;
                appState.grammarProcessed = true;
                
                UI.displayResults(result.data);
                Notifications.show('success', result.message);
                
                document.getElementById('btn-parse-string').disabled = false;
                Utils.smoothScrollTo('#results-section');
            } else {
                Notifications.show('error', result.error);
            }
        } catch (error) {
            Notifications.show('error', 'Error de conexión al servidor');
        } finally {
            LoadingManager.hide();
        }
    },

    handleParseString: async function() {
        const inputString = document.getElementById('input-string').value.trim();
        const validation = Validator.validateString(inputString);
        
        if (!validation.valid) {
            Notifications.show('error', validation.message);
            return;
        }

        if (!appState.grammarProcessed) {
            Notifications.show('error', 'Primero debe generar el parser LR(1)');
            return;
        }

        try {
            const result = await ApiClient.parseString(inputString);
            
            if (result.success) {
                UI.displayParsingResult(result.parsing_result);
                
                // Cambiar a la pestaña de parsing
                const parsingTab = new bootstrap.Tab(document.getElementById('parsing-tab'));
                parsingTab.show();
            } else {
                Notifications.show('error', result.error);
            }
        } catch (error) {
            Notifications.show('error', 'Error al analizar cadena');
        }
    },

    handleClear: function() {
        document.getElementById('grammar-input').value = '';
        document.getElementById('input-string').value = '';
        
        document.getElementById('results-section').style.display = 'none';
        document.getElementById('graph-section').style.display = 'none';
        document.getElementById('btn-parse-string').disabled = true;
        
        appState.grammarProcessed = false;
        appState.currentGrammarData = null;
        
        Notifications.hide();
        Notifications.show('info', 'Datos limpiados');
    },

    handleGrammarKeydown: function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            EventHandlers.handleParseGrammar();
        }
    },

    handleStringKeydown: function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            EventHandlers.handleParseString();
        }
    },

    handleGrammarInput: Utils.debounce(function(e) {
        const textarea = e.target;
        textarea.style.height = 'auto';
        textarea.style.height = Math.max(200, textarea.scrollHeight) + 'px';
    }, 100),

    handleCopyClick: function(e) {
        if (e.target.matches('[data-copy]')) {
            const text = e.target.getAttribute('data-copy');
            Utils.copyToClipboard(text).then(() => {
                Notifications.show('success', 'Copiado al portapapeles', 2000);
            });
        }
    }
};

// UI Management
const UI = {
    displayResults(data) {
        // Mostrar secciones
        document.getElementById('results-section').style.display = 'block';
        document.getElementById('graph-section').style.display = 'block';
        
        // Actualizar contadores
        this.updateCounters(data);
        
        // Mostrar contenido
        this.displayFirstFollow(data.first_follow);
        this.displayStates(data.states);
        this.displayParsingTable(data.parsing_table);
        this.displayGraphs(data);
    },

    updateCounters(data) {
        document.getElementById('states-count').textContent = Utils.formatNumber(data.num_states);
        document.getElementById('terminals-count').textContent = Utils.formatNumber(data.num_terminals);
        document.getElementById('nonterminals-count').textContent = Utils.formatNumber(data.num_nonterminals);
        
        const tableSize = data.num_states * (data.num_terminals + data.num_nonterminals);
        document.getElementById('table-size').textContent = Utils.formatNumber(tableSize);
    },

    displayFirstFollow(firstFollow) {
        const firstHtml = Object.entries(firstFollow.first)
            .map(([symbol, set]) => `
                <div class="mb-2 p-2 border-start border-primary border-3">
                    <strong>FIRST(${Utils.escapeHtml(symbol)}):</strong> 
                    <span class="text-muted">{${set.join(', ')}}</span>
                </div>
            `).join('');
        
        const followHtml = Object.entries(firstFollow.follow)
            .map(([symbol, set]) => `
                <div class="mb-2 p-2 border-start border-success border-3">
                    <strong>FOLLOW(${Utils.escapeHtml(symbol)}):</strong> 
                    <span class="text-muted">{${set.join(', ')}}</span>
                </div>
            `).join('');
        
        document.getElementById('first-sets-display').innerHTML = firstHtml;
        document.getElementById('follow-sets-display').innerHTML = followHtml;
    },

    displayStates(states) {
        const html = states.map(state => `
            <div class="col-lg-6 col-xl-4 mb-3">
                <div class="card h-100">
                    <div class="card-header bg-light d-flex justify-content-between align-items-center">
                        <h6 class="card-title mb-0">Estado I${state.number}</h6>
                        <button class="btn btn-sm btn-outline-secondary" 
                                data-copy="${state.items.join('\\n')}"
                                title="Copiar estado">
                            <i class="fas fa-copy"></i>
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="font-monospace small">
                            ${state.items.map(item => 
                                `<div class="mb-1 p-1 bg-light rounded">${Utils.escapeHtml(item)}</div>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
        
        document.getElementById('states-display').innerHTML = html;
    },

    displayParsingTable(tableData) {
        // Implementación de la tabla de parsing (similar a la versión anterior)
        // ... código de la tabla ...
    },

    displayParsingResult(result) {
        const resultClass = result.success ? 'alert-success' : 'alert-danger';
        const icon = result.success ? 'check-circle' : 'times-circle';
        const status = result.success ? '✅ CADENA ACEPTADA' : '❌ CADENA RECHAZADA';
        const message = result.success ? result.message : result.error;

        const resultHtml = `
            <div class="alert ${resultClass}">
                <h5><i class="fas fa-${icon} me-2"></i>${status}</h5>
                <p class="mb-0">${Utils.escapeHtml(message)}</p>
            </div>
        `;

        document.getElementById('parsing-result-display').innerHTML = resultHtml;
        document.getElementById('parsing-trace-display').textContent = result.trace.join('\n');
    },

    displayGraphs(data) {
        const automatonImg = document.getElementById('automaton-image');
        const tableImg = document.getElementById('table-image');
        
        automatonImg.src = 'data:image/png;base64,' + data.automaton_image;
        tableImg.src = 'data:image/png;base64,' + data.table_image;
        
        // Agregar funcionalidad de zoom
        [automatonImg, tableImg].forEach(img => {
            img.addEventListener('click', () => this.showImageModal(img.src));
        });
    },

    showImageModal(src) {
        // Crear modal para mostrar imagen en grande
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Vista Ampliada</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <img src="${src}" class="img-fluid">
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }
};

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', async function() {
    console.log('🚀 Iniciando aplicación Parser LR(1)');
    
    // Inicializar components
    EventHandlers.init();
    await ExampleManager.loadExamples();
    
    // Cargar ejemplo por defecto
    ExampleManager.loadExample('arithmetic');
    
    // Configurar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    console.log('✅ Aplicación inicializada correctamente');
});

// Exponer funciones globales para uso en templates
window.loadExample = (type) => ExampleManager.loadExample(type);
window.exportAutomaton = () => Exporters.exportAutomaton();
window.exportTable = () => Exporters.exportParsingTable();
window.exportData = () => Exporters.exportGrammarData();
window.scrollToSection = (selector) => Utils.smoothScrollTo(selector);