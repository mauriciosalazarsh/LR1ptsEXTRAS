# INFORME: Parser LR(1) con Interfaz Web

**Curso:** Compiladores
**Universidad:** Universidad de Ingeniería y Tecnología (UTEC)
**Tipo:** Puntos Extras - Examen 2
**Fecha:** Octubre 2024

---

## 1. INTRODUCCIÓN

Este proyecto implementa un **analizador sintáctico LR(1)** completo con interfaz web moderna desarrollada en React. El parser es capaz de analizar gramáticas libres de contexto, construir el autómata LR(1) canónico, generar la tabla de parsing ACTION/GOTO, y analizar cadenas de entrada mostrando la traza completa del proceso.

### 1.1 Objetivos

- Implementar un parser LR(1) canónico desde cero
- Proporcionar una interfaz web intuitiva para interactuar con el parser
- Visualizar el autómata LR(1) de manera clara y profesional
- Permitir el análisis de cadenas con trazabilidad completa
- Exceder los requisitos del proyecto (LR(1) > LALR(1))

---

## 2. FUNDAMENTOS TEÓRICOS

### 2.1 Parser LR(1)

LR(1) significa:
- **L**: Lee la entrada de izquierda a derecha (Left-to-right)
- **R**: Construye la derivación por la derecha en reversa (Rightmost derivation)
- **(1)**: Utiliza un símbolo de lookahead

Los parsers LR(1) son más potentes que:
- **SLR(1)**: Simple LR con lookaheads simplificados
- **LALR(1)**: LR(1) con estados fusionados (requerido en el enunciado)
- **LR(0)**: Sin lookahead

### 2.2 Componentes del Parser LR(1)

1. **Conjuntos FIRST**: Primeros terminales que pueden aparecer en una derivación
2. **Conjuntos FOLLOW**: Terminales que pueden seguir a un no-terminal
3. **Items LR(1)**: `[A → α•β, a]` donde `a` es el lookahead
4. **Función CLOSURE**: Calcula la clausura de un conjunto de items
5. **Función GOTO**: Calcula transiciones entre estados
6. **Tabla ACTION**: Decide shift, reduce o accept
7. **Tabla GOTO**: Determina el siguiente estado tras una reducción

### 2.3 Algoritmo de Construcción

```
1. Calcular conjuntos FIRST para todos los símbolos
2. Calcular conjuntos FOLLOW para todos los no-terminales
3. Crear gramática aumentada S' → S
4. Construir autómata LR(1):
   - Estado inicial: CLOSURE({[S' → •S, $]})
   - Para cada estado y cada símbolo:
     * Calcular GOTO(estado, símbolo)
     * Agregar nuevo estado si no existe
5. Construir tablas ACTION y GOTO
6. Usar las tablas para analizar cadenas
```

---

## 3. ARQUITECTURA DEL PROYECTO

### 3.1 Estructura de Directorios

```
PRPTSEXTRAS/
├── backend/                    # API REST con Flask
│   ├── __main__.py            # Punto de entrada del módulo
│   └── app.py                 # Endpoints de la API
│
├── frontend/                   # Interfaz de usuario
│   ├── react-app/             # Aplicación React
│   │   ├── src/
│   │   │   ├── components/    # Componentes React modulares
│   │   │   │   ├── GrammarEditor.jsx
│   │   │   │   ├── AutomatonInfo.jsx
│   │   │   │   ├── VisualizationTabs.jsx
│   │   │   │   └── StringParser.jsx
│   │   │   ├── App.jsx        # Componente principal
│   │   │   ├── App.css        # Estilos globales
│   │   │   └── main.jsx       # Punto de entrada
│   │   ├── package.json
│   │   └── vite.config.js
│   └── static/                # Archivos generados
│
├── parser/                     # Lógica del parser LR(1)
│   ├── __init__.py
│   ├── lr1_parser.py          # Algoritmo principal
│   ├── visualizer_graphviz.py # Visualización detallada
│   └── visualizer_automathon.py # Visualización simplificada
│
├── requirements.txt            # Dependencias Python
├── .gitignore                 # Archivos ignorados
└── README.md                  # Documentación de usuario
```

### 3.2 Tecnologías Utilizadas

#### Backend
- **Python 3.11**: Lenguaje principal
- **Flask 3.0.0**: Framework web REST API
- **Flask-CORS 4.0.0**: Manejo de CORS para React
- **NetworkX 3.2.1**: Manejo de grafos
- **Graphviz 0.16**: Generación de visualizaciones
- **Automathon 0.0.15**: Visualización alternativa
- **Matplotlib 3.8.2**: Generación de gráficos

#### Frontend
- **React 18**: Framework de interfaz de usuario
- **Vite 7.1**: Build tool y dev server
- **Axios**: Cliente HTTP para API
- **JavaScript ES6+**: Lenguaje del frontend

#### DevOps
- **Docker**: Containerización
- **Docker Compose**: Orquestación de servicios

---

## 4. IMPLEMENTACIÓN DETALLADA

### 4.1 Módulo: `lr1_parser.py`

Este módulo contiene la implementación completa del parser LR(1).

#### 4.1.1 Clase `Production`

Representa una producción de la gramática:

```python
class Production:
    def __init__(self, left: str, right: List[str], number: int):
        self.left = left      # Lado izquierdo (no-terminal)
        self.right = right    # Lado derecho (lista de símbolos)
        self.number = number  # Número de producción
```

#### 4.1.2 Clase `LR1Item`

Representa un item LR(1):

```python
class LR1Item:
    def __init__(self, production: int, dot_position: int, lookahead: str):
        self.production = production      # Número de producción
        self.dot_position = dot_position  # Posición del punto
        self.lookahead = lookahead        # Símbolo de lookahead
```

#### 4.1.3 Clase `LR1Parser`

##### Atributos principales:
```python
self.grammar: List[Production]           # Producciones
self.terminals: Set[str]                 # Símbolos terminales
self.non_terminals: Set[str]             # Símbolos no-terminales
self.first_sets: Dict[str, Set[str]]     # Conjuntos FIRST
self.follow_sets: Dict[str, Set[str]]    # Conjuntos FOLLOW
self.states: List[Set[LR1Item]]          # Estados del autómata
self.transitions: Dict[Tuple, int]       # Transiciones
self.action_table: Dict[Tuple, str]      # Tabla ACTION
self.goto_table: Dict[Tuple, int]        # Tabla GOTO
```

##### Métodos principales:

**1. `_compute_first_sets()`**

Calcula los conjuntos FIRST usando un algoritmo de punto fijo:

```python
def _compute_first_sets(self):
    # Inicialización
    for terminal in self.terminals:
        self.first_sets[terminal] = {terminal}

    for non_terminal in self.non_terminals:
        self.first_sets[non_terminal] = set()

    # Punto fijo
    changed = True
    while changed:
        changed = False
        for prod in self.grammar:
            # Reglas para calcular FIRST
            # Si A → ε, agregar ε a FIRST(A)
            # Si A → X1 X2 ... Xn, agregar FIRST(X1) - {ε}
            # Si X1 deriva ε, agregar FIRST(X2), etc.
```

**2. `_compute_follow_sets()`**

Calcula los conjuntos FOLLOW:

```python
def _compute_follow_sets(self):
    # Inicialización
    self.follow_sets[self.start_symbol].add('$')

    # Punto fijo
    changed = True
    while changed:
        changed = False
        for prod in self.grammar:
            # Reglas:
            # Si A → αBβ, agregar FIRST(β) - {ε} a FOLLOW(B)
            # Si β deriva ε, agregar FOLLOW(A) a FOLLOW(B)
```

**3. `_closure(items)`**

Calcula la clausura de un conjunto de items:

```python
def _closure(self, items: Set[LR1Item]) -> Set[LR1Item]:
    result = set(items)
    changed = True

    while changed:
        changed = False
        for item in result:
            if item.dot_position < len(production.right):
                next_symbol = production.right[item.dot_position]

                if next_symbol es no-terminal:
                    # Calcular lookaheads
                    beta = symbols_after_next_symbol + [item.lookahead]
                    lookaheads = FIRST(beta) - {ε}

                    # Agregar items [B → •γ, b] para cada b en lookaheads
```

**4. `_build_lr1_automaton()`**

Construye el autómata LR(1):

```python
def _build_lr1_automaton(self):
    # Estado inicial
    initial_item = LR1Item(0, 0, '$')  # [S' → •S, $]
    initial_state = self._closure({initial_item})

    # BFS para construir estados
    queue = [0]
    while queue:
        current_state = queue.pop(0)

        # Agrupar items por símbolo después del punto
        for symbol in symbols:
            # Mover el punto: [A → α•Xβ, a] → [A → αX•β, a]
            new_items = {move_dot(item) for item in current_state
                        if next_symbol(item) == symbol}

            # Calcular clausura
            new_state = self._closure(new_items)

            # Agregar estado si es nuevo
            if new_state not in states:
                states.append(new_state)
                queue.append(len(states) - 1)
```

**5. `_build_parsing_table()`**

Construye las tablas ACTION y GOTO:

```python
def _build_parsing_table(self):
    for state_num, state in enumerate(self.states):
        for item in state:
            if item.dot_position < len(production.right):
                # Item de shift: [A → α•aβ, b]
                next_symbol = production.right[item.dot_position]
                next_state = transitions[(state_num, next_symbol)]

                if next_symbol is terminal:
                    ACTION[state_num, next_symbol] = shift next_state
                else:
                    GOTO[state_num, next_symbol] = next_state
            else:
                # Item de reduce: [A → α•, a]
                if production is S' → S:
                    ACTION[state_num, '$'] = accept
                else:
                    ACTION[state_num, item.lookahead] = reduce production
```

**6. `parse_string(input_string)`**

Analiza una cadena usando el parser LR(1):

```python
def parse_string(self, input_string: str):
    tokens = input_string.split() + ['$']
    stack = [0]  # Pila de estados
    pointer = 0  # Apuntador a la entrada

    while True:
        state = stack[-1]
        symbol = tokens[pointer]
        action = ACTION[state, symbol]

        if action == 'error':
            return {'success': False, 'error': 'Error sintáctico'}

        elif action == 'accept':
            return {'success': True, 'trace': trace}

        elif action.startswith('s'):  # Shift
            next_state = int(action[1:])
            stack.append(next_state)
            pointer += 1

        elif action.startswith('r'):  # Reduce
            prod_num = int(action[1:])
            production = grammar[prod_num]

            # Pop |rhs| elementos
            for _ in range(len(production.right)):
                stack.pop()

            # Push GOTO
            current_state = stack[-1]
            goto_state = GOTO[current_state, production.left]
            stack.append(goto_state)
```

### 4.2 Backend: `app.py`

La API REST proporciona los siguientes endpoints:

#### Endpoints Principales

**1. `GET /`**
```python
@app.route('/')
def index():
    return jsonify({
        'service': 'LR(1) Parser API',
        'version': '1.0',
        'endpoints': ['/api/build_parser', '/api/parse_string', ...]
    })
```

**2. `POST /api/build_parser`**

Construye el parser con una gramática:

```python
@app.route('/api/build_parser', methods=['POST'])
def build_parser():
    grammar_text = request.json['grammar']

    # Construir parser
    parser = LR1Parser()
    parser.parse_grammar(grammar_text)

    # Retornar información
    return jsonify({
        'success': True,
        'num_states': len(parser.states),
        'terminals': list(parser.terminals),
        'non_terminals': list(parser.non_terminals),
        'productions': [str(p) for p in parser.grammar],
        'first_sets': parser.first_sets,
        'follow_sets': parser.follow_sets
    })
```

**3. `POST /api/parse_string`**

Analiza una cadena:

```python
@app.route('/api/parse_string', methods=['POST'])
def parse_string():
    input_string = request.json['string']

    result = parser.parse_string(input_string)

    return jsonify({
        'success': True,
        'accepted': result['success'],
        'trace': result['trace'],
        'error': result.get('error', '')
    })
```

**4. `POST /api/generate_graphviz`**

Genera visualización con Graphviz:

```python
@app.route('/api/generate_graphviz', methods=['POST'])
def generate_graphviz():
    svg_content = visualizer_graphviz.generate_lr1_automaton(
        parser.states,
        parser.transitions,
        parser.grammar
    )

    return jsonify({
        'success': True,
        'svg': svg_content
    })
```

**5. `GET /api/get_parsing_table`**

Obtiene la tabla de parsing:

```python
@app.route('/api/get_parsing_table', methods=['GET'])
def get_parsing_table():
    return jsonify({
        'success': True,
        'terminals': terminals,
        'non_terminals': non_terminals,
        'action': action_table,  # {state: {symbol: action}}
        'goto': goto_table,      # {state: {symbol: state}}
        'num_states': len(parser.states)
    })
```

### 4.3 Frontend: Componentes React

#### 4.3.1 `GrammarEditor.jsx`

Editor de gramáticas con ejemplo predefinido:

```jsx
function GrammarEditor({ onBuild, loading, error }) {
  const [grammar, setGrammar] = useState(DEFAULT_GRAMMAR)

  const handleBuild = () => {
    onBuild(grammar)
  }

  return (
    <div className="section">
      <h2>Gramática</h2>
      <textarea
        value={grammar}
        onChange={(e) => setGrammar(e.target.value)}
        rows={10}
      />
      <button onClick={handleBuild} disabled={loading}>
        {loading ? 'Construyendo...' : 'Construir Parser'}
      </button>
      {error && <div className="alert alert-error">{error}</div>}
    </div>
  )
}
```

#### 4.3.2 `AutomatonInfo.jsx`

Muestra información del autómata:

```jsx
function AutomatonInfo({ info }) {
  return (
    <div className="section">
      <h2>Información del Autómata</h2>
      <div className="info-grid">
        <div className="info-card">
          <h3>Estados</h3>
          <p>{info.num_states}</p>
        </div>
        <div className="info-card">
          <h3>Transiciones</h3>
          <p>{info.num_transitions}</p>
        </div>
        <div className="info-card">
          <h3>Terminales</h3>
          <p>{info.terminals.length}</p>
        </div>
        <div className="info-card">
          <h3>No Terminales</h3>
          <p>{info.non_terminals.length}</p>
        </div>
      </div>
    </div>
  )
}
```

#### 4.3.3 `VisualizationTabs.jsx`

Tabs para diferentes visualizaciones:

```jsx
function VisualizationTabs({ details }) {
  const [activeTab, setActiveTab] = useState('graphviz')
  const [graphvizSvg, setGraphvizSvg] = useState(null)

  const generateGraphviz = async () => {
    const response = await axios.post(`${API_URL}/generate_graphviz`)
    setGraphvizSvg(response.data.svg)
  }

  return (
    <div className="section">
      <div className="tabs">
        <button onClick={() => setActiveTab('graphviz')}>
          Graphviz (Items LR(1))
        </button>
        <button onClick={() => setActiveTab('automathon')}>
          automathon (Simplificado)
        </button>
        <button onClick={() => setActiveTab('table')}>
          Tabla ACTION/GOTO
        </button>
      </div>

      {activeTab === 'graphviz' && (
        <div dangerouslySetInnerHTML={{ __html: graphvizSvg }} />
      )}

      {activeTab === 'table' && (
        <table className="parsing-table">
          {/* Renderizar tabla ACTION/GOTO */}
        </table>
      )}
    </div>
  )
}
```

#### 4.3.4 `StringParser.jsx`

Análisis de cadenas:

```jsx
function StringParser() {
  const [inputString, setInputString] = useState('')
  const [result, setResult] = useState(null)

  const handleParse = async () => {
    const response = await axios.post(`${API_URL}/parse_string`, {
      string: inputString
    })
    setResult(response.data)
  }

  return (
    <div className="section">
      <h2>Análisis de Cadenas</h2>
      <input
        type="text"
        value={inputString}
        onChange={(e) => setInputString(e.target.value)}
        placeholder="Ingrese cadena a analizar"
      />
      <button onClick={handleParse}>Analizar</button>

      {result && (
        <div className={result.accepted ? 'alert-success' : 'alert-error'}>
          {result.accepted ? 'ACEPTADA' : 'RECHAZADA'}
        </div>
      )}

      {result?.trace && (
        <table className="trace-table">
          <thead>
            <tr>
              <th>Paso</th>
              <th>Pila</th>
              <th>Entrada</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            {result.trace.map((step, i) => (
              <tr key={i}>
                <td>{i + 1}</td>
                <td>{step.stack}</td>
                <td>{step.input}</td>
                <td>{step.action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
```

---

## 5. EJEMPLOS DE USO

### 5.1 Gramática de Ejemplo

```
S -> q * A * B * C
A -> a
A -> b * b * D
B -> a
B -> ε
C -> b
C -> ε
D -> C
D -> ε
```

### 5.2 Conjuntos FIRST y FOLLOW

**FIRST:**
- FIRST(S) = {q}
- FIRST(A) = {a, b}
- FIRST(B) = {a, ε}
- FIRST(C) = {b, ε}
- FIRST(D) = {b, ε}

**FOLLOW:**
- FOLLOW(S) = {$}
- FOLLOW(A) = {*}
- FOLLOW(B) = {*}
- FOLLOW(C) = {$, *}
- FOLLOW(D) = {*}

### 5.3 Información del Autómata

- **Estados:** 19
- **Transiciones:** 28
- **Terminales:** 5 ($, *, a, b, q)
- **No terminales:** 5 (S, A, B, C, D)
- **Producciones:** 10

### 5.4 Ejemplo de Análisis de Cadena

**Entrada:** `q * a * a * b`

**Traza:**

| Paso | Pila | Entrada | Acción |
|------|------|---------|--------|
| 1 | 0 | q * a * a * b $ | shift 1 |
| 2 | 0 1 | * a * a * b $ | shift 3 |
| 3 | 0 1 3 | a * a * b $ | shift 4 |
| 4 | 0 1 3 4 | * a * b $ | reduce 2 (A → a) |
| 5 | 0 1 3 5 | * a * b $ | shift 7 |
| 6 | 0 1 3 5 7 | a * b $ | shift 10 |
| 7 | 0 1 3 5 7 10 | * b $ | reduce 4 (B → a) |
| 8 | 0 1 3 5 7 12 | * b $ | shift 13 |
| 9 | 0 1 3 5 7 12 13 | b $ | shift 14 |
| 10 | 0 1 3 5 7 12 13 14 | $ | reduce 6 (C → b) |
| 11 | 0 1 3 5 7 12 13 15 | $ | reduce 1 (S → q * A * B * C) |
| 12 | 0 2 | $ | ACCEPT |

**Resultado:** ✅ ACEPTADA

### 5.5 Cadenas de Prueba

**Cadenas Aceptadas:**
- `q * a * a * b` ✅
- `q * b * b * b * a * b` ✅

**Cadenas Rechazadas:**
- `a * a * b` ❌ (No empieza con q)
- `q * * a` ❌ (Doble asterisco)
- `q a b` ❌ (Faltan asteriscos)

---

## 6. CARACTERÍSTICAS DESTACADAS

### 6.1 Ventajas sobre LALR(1)

El proyecto implementa LR(1) canónico, que es **más potente** que LALR(1):

- **Más estados:** LR(1) puede tener más estados pero es más preciso
- **Menos conflictos:** Reduce conflictos shift/reduce y reduce/reduce
- **Mayor capacidad:** Acepta un superconjunto de gramáticas LALR(1)
- **Lookaheads precisos:** Cada item tiene su propio lookahead

### 6.2 Funcionalidades Implementadas

✅ **Parser LR(1) Completo**
- Cálculo de conjuntos FIRST y FOLLOW
- Construcción del autómata canónico LR(1)
- Generación de tablas ACTION y GOTO
- Análisis de cadenas con trazabilidad

✅ **Visualizaciones Múltiples**
- Graphviz: Muestra items LR(1) completos con lookaheads
- automathon: Visualización simplificada tipo DFA
- Tabla ACTION/GOTO interactiva con colores

✅ **Interfaz Web Moderna**
- React con componentes modulares
- Responsive design
- Feedback visual inmediato
- Manejo de errores robusto

✅ **Soporte de Producciones Epsilon**
- Manejo correcto de producciones vacías
- Cálculo preciso de FIRST y FOLLOW con ε
- Análisis correcto de cadenas con derivaciones epsilon

✅ **Docker**
- Containerización completa
- Docker Compose para orquestación
- Hot reload en desarrollo
- Fácil deployment

### 6.3 Aspectos Técnicos Destacados

**1. Algoritmo Eficiente**
- Uso de conjuntos (sets) para operaciones rápidas
- Caché de estados para evitar duplicados
- Algoritmos de punto fijo optimizados

**2. Código Limpio**
- Comentarios en español para claridad
- Separación de responsabilidades
- Type hints en Python
- Componentes React reutilizables

**3. Manejo de Errores**
- Validación de gramáticas
- Mensajes de error descriptivos
- Recuperación ante fallos
- Logging detallado

**4. Testing**
- Gramáticas de prueba incluidas
- Validación contra ejemplos conocidos
- Scripts de debugging

---

## 7. COMPARACIÓN CON REQUISITOS

### 7.1 Requisitos del Proyecto

| Requisito | Estado | Detalles |
|-----------|--------|----------|
| Parser LALR(1) | ✅ SUPERADO | Se implementó LR(1), más potente |
| Interfaz en app | ✅ CUMPLIDO | React moderna con múltiples vistas |
| Reporte pequeño | ✅ CUMPLIDO | Este documento |
| Solo Python | ✅ CUMPLIDO | Backend 100% en Python |
| Presentación | ✅ LISTO | Proyecto funcional completo |

### 7.2 Funcionalidades Adicionales (No Requeridas)

- ✅ Visualización del autómata (2 métodos)
- ✅ Análisis de cadenas con traza
- ✅ Tabla ACTION/GOTO interactiva
- ✅ Conjuntos FIRST/FOLLOW
- ✅ Docker y Docker Compose
- ✅ Frontend en React (no requerido)
- ✅ API REST completa
- ✅ Documentación extensa

---

## 8. INSTRUCCIONES DE USO

### 8.1 Instalación

#### Opción A: Con Docker (Recomendado)

```bash
# Clonar repositorio
git clone <repository-url>
cd PRPTSEXTRAS

# Levantar servicios
docker-compose up --build

# Acceder a la aplicación
# Frontend: http://localhost:5173
# Backend: http://localhost:5001
```

#### Opción B: Sin Docker

```bash
# 1. Instalar dependencias Python
pip3 install -r requirements.txt

# 2. Instalar Graphviz
# macOS: brew install graphviz
# Linux: sudo apt-get install graphviz

# 3. Instalar dependencias React
cd frontend/react-app
npm install
cd ../..

# 4. Levantar backend (Terminal 1)
python3 backend/app.py

# 5. Levantar frontend (Terminal 2)
cd frontend/react-app
npm run dev
```

### 8.2 Uso de la Aplicación

1. **Ingresar Gramática:**
   - Usar el editor de texto
   - O cargar el ejemplo predefinido

2. **Construir Parser:**
   - Click en "Construir Parser"
   - Esperar confirmación

3. **Ver Visualizaciones:**
   - Tab "Graphviz" para items completos
   - Tab "automathon" para vista simplificada
   - Tab "Tabla ACTION/GOTO" para la tabla

4. **Analizar Cadenas:**
   - Ingresar cadena en el campo
   - Click en "Analizar"
   - Ver resultado y traza

### 8.3 Formato de Gramática

```
# Comentarios con #
S -> q * A * B
A -> a
A -> b * b
B -> ε          # Producción epsilon
```

**Reglas:**
- Un no-terminal por línea
- Separar símbolos con espacios
- Usar `ε` o `epsilon` para producciones vacías
- El primer no-terminal es el símbolo inicial

---

## 9. LIMITACIONES Y TRABAJO FUTURO

### 9.1 Limitaciones Actuales

1. **Gramáticas Ambiguas:**
   - No detecta automáticamente ambigüedad
   - Toma la primera acción en caso de conflicto

2. **Optimización de Estados:**
   - No implementa minimización de estados
   - Genera más estados que LALR(1)

3. **Visualización:**
   - Graphviz puede ser lento con muchos estados
   - Tamaño de fuente fijo

### 9.2 Mejoras Futuras

1. **Funcionalidades:**
   - Detección de conflictos shift/reduce
   - Conversión a LALR(1)
   - Generación de código del parser
   - Exportar tabla en diferentes formatos

2. **Interfaz:**
   - Editor con syntax highlighting
   - Modo oscuro
   - Histórico de gramáticas
   - Compartir gramáticas por URL

3. **Optimización:**
   - Caché de autómatas
   - Paralelización de construcción
   - WebAssembly para mejor rendimiento

---

## 10. CONCLUSIONES

Este proyecto demuestra una implementación completa y funcional de un parser LR(1) canónico con las siguientes contribuciones:

### 10.1 Logros Técnicos

1. **Parser LR(1) Completo:**
   - Implementación desde cero
   - Manejo correcto de producciones epsilon
   - Generación precisa de lookaheads
   - Tablas ACTION/GOTO correctas

2. **Interfaz Moderna:**
   - React con arquitectura de componentes
   - Múltiples visualizaciones
   - Experiencia de usuario fluida
   - Responsive design

3. **Arquitectura Profesional:**
   - Separación frontend/backend
   - API REST bien diseñada
   - Código modular y mantenible
   - Documentación completa

### 10.2 Cumplimiento de Objetivos

✅ **Parser LR(1):** Implementado y probado
✅ **Interfaz Web:** React moderna y funcional
✅ **Reporte:** Este documento completo
✅ **Solo Python:** Backend 100% Python
✅ **Supera LALR(1):** LR(1) es más potente

### 10.3 Aprendizajes

- Profundización en teoría de compiladores
- Algoritmos de análisis sintáctico
- Desarrollo full-stack moderno
- Integración frontend-backend
- Containerización con Docker

### 10.4 Aplicabilidad

Este parser puede utilizarse para:
- Diseño de lenguajes de programación
- Validación de sintaxis
- Análisis de expresiones
- Educación en compiladores
- Prototipado rápido de parsers

---

## 11. REFERENCIAS

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson.

2. Cooper, K., & Torczon, L. (2011). *Engineering a Compiler* (2nd ed.). Morgan Kaufmann.

3. Appel, A. W. (2004). *Modern Compiler Implementation in ML*. Cambridge University Press.

4. Dragon Book - Capítulo 4: Análisis Sintáctico

5. Documentación oficial de Python: https://docs.python.org/3/

6. React Documentation: https://react.dev/

7. Flask Documentation: https://flask.palletsprojects.com/

8. Graphviz Documentation: https://graphviz.org/documentation/

9. Ejemplos del curso de Compiladores - UTEC

10. Páginas de referencia proporcionadas:
    - https://compiler-slr-parser.netlify.app/
    - https://jsmachines.sourceforge.net/machines/lr1.html
    - https://light0x00.github.io/parser-generator/

---

## 12. ANEXOS

### Anexo A: Ejemplo Completo de Construcción de Autómata

**Gramática:**
```
S' -> S
S -> C C
C -> c C
C -> d
```

**Estados Generados:**

```
I0:
  [S' → •S, $]
  [S → •C C, $]
  [C → •c C, c/d]
  [C → •d, c/d]

I1:
  [S → C •C, $]
  [C → •c C, $]
  [C → •d, $]

... (total 11 estados)
```

**Tabla ACTION/GOTO:**

| Estado | c | d | $ | C | S | S' |
|--------|---|---|---|---|---|-----|
| I0 | s3 | s2 | - | 1 | 5 | 4 |
| I1 | s6 | s7 | - | 8 | - | - |
| I2 | r4 | r4 | - | - | - | - |
| ... | ... | ... | ... | ... | ... | ... |

### Anexo B: Código de Ejemplo - Cálculo de FIRST

```python
def _compute_first_sets(self):
    # los terminales tienen como first a ellos mismos
    for terminal in self.terminals:
        self.first_sets[terminal] = {terminal}

    # inicializar first de no terminales como conjunto vacio
    for non_terminal in self.non_terminals:
        self.first_sets[non_terminal] = set()

    # algoritmo de punto fijo: iterar hasta que no haya cambios
    changed = True
    while changed:
        changed = False

        for prod in self.grammar:
            current_first = self.first_sets[prod.left].copy()

            if not prod.right:
                # produccion epsilon
                self.first_sets[prod.left].add('ε')
            else:
                # calcular first de la secuencia
                for symbol in prod.right:
                    first_of_symbol = self.first_sets[symbol]
                    self.first_sets[prod.left].update(
                        first_of_symbol - {'ε'}
                    )

                    if 'ε' not in first_of_symbol:
                        break
                else:
                    # todos derivan epsilon
                    self.first_sets[prod.left].add('ε')

            if self.first_sets[prod.left] != current_first:
                changed = True
```

### Anexo C: Captura de Pantalla de la Interfaz

*(En la presentación se mostrará la interfaz funcionando en vivo)*

---

**Fin del Informe**

*Desarrollado como parte del curso de Compiladores - UTEC*
*Octubre 2024*
