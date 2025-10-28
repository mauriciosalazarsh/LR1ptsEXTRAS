# Analizador LR(1) y LALR(1) - Puntos Extras Examen 2

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2-61dafb.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Descripción del Proyecto

Implementación completa de analizadores sintácticos **LR(1)** y **LALR(1)** en Python con interfaz web React y visualización gráfica interactiva del autómata.

### ✨ Características Principales

- ✅ **Parser LR(1)** completo con cálculo de conjuntos FIRST/FOLLOW
- ✅ **Parser LALR(1)** con fusión de estados (reduce 43.5% de estados)
- 🎨 Visualización profesional con **Graphviz** (ambos parsers)
- 🖥️ Interfaz React moderna con backend REST API
- 📊 Tabla de parsing ACTION/GOTO completa
- 🔄 Selector dinámico entre LR(1) y LALR(1)
- 📈 Comparación visual y estadística entre ambos parsers
- 🎯 Análisis de cadenas con traza paso a paso
- 💾 Exportación en múltiples formatos (PNG, SVG, PDF)

## 📁 Estructura del Proyecto

```
.
├── backend/
│   ├── __main__.py              # Punto de entrada del módulo
│   └── app.py                   # API REST con Flask (soporta LR1/LALR1)
│
├── frontend/
│   └── react-app/               # Aplicación React + Vite
│       ├── src/
│       │   ├── components/      # Componentes React
│       │   │   ├── GrammarEditor.jsx        # Editor con selector de parser
│       │   │   ├── VisualizationTabs.jsx    # Tabs de visualización
│       │   │   ├── AutomatonInfo.jsx        # Info del autómata
│       │   │   └── StringParser.jsx         # Analizador de cadenas
│       │   ├── App.jsx          # Componente principal
│       │   └── App.css          # Estilos globales
│       └── package.json
│
├── parser/
│   ├── lr1_parser.py            # Algoritmo LR(1) completo
│   ├── lalr1_parser.py          # Algoritmo LALR(1) con fusión de estados ⭐NEW
│   └── visualizer_graphviz.py   # Visualizador con Graphviz
│
├── test_comparison.py           # Script comparativo LR(1) vs LALR(1)
├── test_backend_complete.py     # Test completo del flujo backend
├── test_graphviz_lalr.py        # Test de visualización
├── GUIA_RAPIDA.md              # Guía de uso rápido
├── GRAFICOS_LISTOS.md          # Documentación de visualizaciones
├── requirements.txt             # Dependencias Python
└── README.md                    # Esta documentación
```

## Instalación

### Requisitos

- Python 3.9 o superior
- Node.js 18 o superior
- npm 9 o superior
- Graphviz (instalado en el sistema)

### Instalar Graphviz

```bash
# macOS
brew install graphviz

# Linux (Ubuntu/Debian)
sudo apt-get install graphviz

# Windows
# Descargar desde https://graphviz.org/download/
```

### Instalar Dependencias Python

```bash
pip3 install -r requirements.txt
```

### Instalar Dependencias de React

```bash
cd frontend/react-app
npm install
cd ../..
```

### Dependencias Python Incluidas

- Flask 3.0.0
- Flask-CORS 4.0.0
- matplotlib 3.8.2
- networkx 3.2.1
- graphviz >= 0.16

## Ejecución

### Backend (Terminal 1)

```bash
python3 -m backend.app
```

El backend estará disponible en: **http://localhost:5001**

### Frontend (Terminal 2)

```bash
cd frontend/react-app
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

> **Nota:** Debes ejecutar ambos servidores en terminales separadas para que la aplicación funcione correctamente.

## Funcionalidades de la Interfaz Web

### 1. Editor de Gramática
- Ingreso de gramáticas libres de contexto
- Carga de ejemplos predefinidos
- Construcción automática del parser

### 2. Visualizaciones del Autómata
- **Graphviz**: Muestra items LR(1) completos con lookahead
- Descarga en múltiples formatos (PNG, SVG)

### 3. Tabla de Parsing
- Tabla ACTION/GOTO completa
- Coloreado por tipo de acción (shift, reduce, accept)
- Leyenda explicativa

### 4. Detalles del Parser
- Lista de producciones
- Conjuntos FIRST
- Conjuntos FOLLOW
- Estadísticas del autómata

### 5. Análisis de Cadenas
- Validación de cadenas de entrada
- Traza paso a paso del proceso de parsing
- Mensajes de aceptación/rechazo

## Gramática de Ejemplo

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

### Conjuntos FIRST

- FIRST(S): {q}
- FIRST(A): {a, b}
- FIRST(B): {a, ε}
- FIRST(C): {b, ε}
- FIRST(D): {b, ε}

### Conjuntos FOLLOW

- FOLLOW(S): {$}
- FOLLOW(A): {*}
- FOLLOW(B): {*}
- FOLLOW(C): {$, *}
- FOLLOW(D): {*}

## 📊 Comparación LR(1) vs LALR(1)

### Gramática de Expresiones Aritméticas

| Métrica | LR(1) | LALR(1) | Reducción |
|---------|-------|---------|-----------|
| **Estados** | 23 | 13 | **43.5%** ✨ |
| **Transiciones** | 39 | 23 | 41.0% |
| **Correctitud** | ✅ | ✅ | - |

### Gramática del Proyecto

| Métrica | LR(1) | LALR(1) | Reducción |
|---------|-------|---------|-----------|
| **Estados** | 19 | 18 | 5.3% |
| **Transiciones** | 18 | 18 | 0% |
| **Correctitud** | ✅ | ✅ | - |

> 🎯 **LALR(1) reduce significativamente el número de estados** manteniendo el mismo poder de análisis que LR(1).

## Resultados

El analizador genera (con gramática del proyecto):

### LR(1)
- **19 estados** en el autómata
- **18 transiciones** entre estados
- **5 terminales**: {$, *, a, b, q}
- **6 no terminales**: {S, S', A, B, C, D}
- **10 producciones** en total

### LALR(1)
- **18 estados** en el autómata (5.3% menos)
- **18 transiciones** entre estados
- Mismos terminales y no terminales
- Mismas producciones

### Cadenas de Prueba

Cadenas aceptadas (ambos parsers):
- `q * a * a * b`
- `q * b * b * b * a * b`

Cadenas rechazadas (ambos parsers):
- `q * a * b`

## 🔌 API Endpoints

### POST /api/build_parser
Construye el parser con la gramática proporcionada.

**Body:**
```json
{
  "grammar": "S -> E\nE -> E + T\n...",
  "parser_type": "LR1"  // o "LALR1"
}
```

**Response:**
```json
{
  "success": true,
  "parser_type": "LR(1)",  // o "LALR(1)"
  "info": { ... },
  "first_sets": { ... },
  "follow_sets": { ... },
  "productions": [ ... ]
}
```

### POST /api/generate_graphviz
Genera visualización con Graphviz del autómata actual (funciona con LR(1) y LALR(1)).

### GET /api/get_parsing_table
Obtiene la tabla de parsing ACTION/GOTO.

### POST /api/parse_string
Analiza una cadena de entrada y retorna la traza.

## Módulos del Proyecto

### Backend (backend/)
Contiene la API REST Flask que maneja:
- Endpoints HTTP para todas las operaciones
- **Soporte para LR(1) y LALR(1)** mediante parámetro `parser_type`
- Configuración de CORS para React
- Comunicación con ambos tipos de parser

### Frontend (frontend/react-app/)
Contiene la interfaz de usuario en React:
- **Selector dinámico** entre LR(1) y LALR(1)
- Componentes modulares y reutilizables
- Manejo de estado con React hooks
- Interfaz responsive y moderna
- Comunicación con API mediante axios
- Visualización interactiva con zoom/pan

### Parser (parser/)
Contiene la lógica del compilador:
- **lr1_parser.py**: Algoritmo LR(1) completo con autómata canónico
- **lalr1_parser.py**: Algoritmo LALR(1) con fusión de estados por núcleo ⭐
- **visualizer_graphviz.py**: Visualización profesional (soporta ambos parsers)

## Librería de Visualización

### Graphviz
- Control total sobre la visualización
- Muestra items LR(1) completos: `A → α • β, lookahead`
- Estados coloreados (verde=inicial, rojo=aceptación, azul=normal)
- Formatos: PNG, PDF, SVG, DOT
- Alta resolución (300 DPI)

## Tabla de Parsing

La tabla ACTION/GOTO incluye:

- **ACTION**: Acciones shift (sN), reduce (rN), accept (ACC)
- **GOTO**: Transiciones para no terminales
- **Colores distintivos**: Verde (shift), Amarillo (reduce), Azul (accept/goto)
- **Leyenda explicativa** para facilitar la lectura

## Notas Técnicas

- Backend usa puerto 5001 para evitar conflictos con AirPlay en macOS
- Frontend usa puerto 5173 (Vite development server)
- La aplicación requiere Graphviz instalado en el sistema
- Las visualizaciones se generan bajo demanda
- CORS configurado para permitir comunicación entre frontend y backend
- La estructura modular permite fácil mantenimiento y escalabilidad

## Desarrollo

**Curso:** Compiladores
**Universidad:** UTEC
**Tipo:** Puntos Extras Examen 2
**Fecha:** Octubre 2024

## Autores

- Salazar Hillenbrand, Mauricio
- Alvarado Vargas, Martin Fabian
- Najarro Mancco, Christopher Eloy

Proyecto desarrollado para el curso de Compiladores - UTEC
