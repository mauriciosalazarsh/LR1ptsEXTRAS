# Analizador LR(1) - Puntos Extras Examen 2

## Descripción del Proyecto

Implementación completa de un analizador LR(1) en Python con interfaz React y visualización gráfica del autómata.

### Características

- Parser LR(1) completo con cálculo de conjuntos FIRST/FOLLOW
- Autómata LR(1) con visualización profesional
- Interfaz React moderna con backend REST API
- Tabla de parsing ACTION/GOTO completa
- Múltiples formatos de exportación (PNG, SVG, PDF)

## Estructura del Proyecto

```
.
├── backend/
│   ├── __main__.py           # Punto de entrada del módulo
│   └── app.py                # API REST con Flask
│
├── frontend/
│   └── react-app/            # Aplicación React + Vite
│       ├── src/
│       │   ├── components/   # Componentes React
│       │   ├── App.jsx       # Componente principal
│       │   └── App.css       # Estilos globales
│       └── package.json
│
├── parser/
│   ├── lr1_parser.py         # Algoritmo LR(1) principal
│   ├── visualizer_graphviz.py    # Visualizador con Graphviz
│   └── visualizer_automathon.py  # Visualizador con automathon
│
├── requirements.txt          # Dependencias Python
└── README.md                 # Esta documentación
```

## Instalación

### Opción A: Con Docker (Recomendado)

**Requisitos:**
- Docker 20.10 o superior
- Docker Compose 2.0 o superior

No necesitas instalar Python, Node.js ni Graphviz manualmente. Docker se encarga de todo.

### Opción B: Sin Docker

**Requisitos:**
- Python 3.9 o superior
- Node.js 18 o superior
- npm 9 o superior
- Graphviz (instalado en el sistema)

#### Instalar Graphviz (Solo si no usas Docker)

```bash
# macOS
brew install graphviz

# Linux (Ubuntu/Debian)
sudo apt-get install graphviz

# Windows
# Descargar desde https://graphviz.org/download/
```

#### Instalar Dependencias Python (Solo si no usas Docker)

```bash
pip3 install -r requirements.txt
```

#### Instalar Dependencias de React (Solo si no usas Docker)

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
- automathon >= 0.0.15
- graphviz >= 0.16

## Ejecución

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# O en modo detached (segundo plano)
docker-compose up -d

# Para detener los servicios
docker-compose down
```

La aplicación estará disponible en:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5001

### Opción 2: Manual (Sin Docker)

#### Backend (Terminal 1)

```bash
cd backend
python3 -m backend.app
```

El backend estará disponible en: **http://localhost:5001**

#### Frontend (Terminal 2)

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
- **automathon**: Visualización simplificada tipo DFA
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

## Resultados

El analizador genera:

- **19 estados** en el autómata LR(1)
- **18 transiciones** entre estados
- **5 terminales**: {$, *, a, b, q}
- **6 no terminales**: {S, S', A, B, C, D}
- **10 producciones** en total

### Cadenas de Prueba

Cadenas aceptadas:
- `q * a * a * b`
- `q * b * b * b * a * b`

Cadenas rechazadas:
- `q * a * b`

## API Endpoints

### POST /api/build_parser
Construye el parser con la gramática proporcionada.

### POST /api/generate_graphviz
Genera visualización con Graphviz (items LR(1) completos).

### POST /api/generate_automathon
Genera visualización simplificada con automathon.

### GET /api/get_parsing_table
Obtiene la tabla de parsing ACTION/GOTO.

### POST /api/parse_string
Analiza una cadena de entrada y retorna la traza.

## Módulos del Proyecto

### Backend (backend/)
Contiene la API REST Flask que maneja:
- Endpoints HTTP para todas las operaciones
- Configuración de CORS para React
- Comunicación con el parser

### Frontend (frontend/react-app/)
Contiene la interfaz de usuario en React:
- Componentes modulares y reutilizables
- Manejo de estado con React hooks
- Interfaz responsive y moderna
- Comunicación con API mediante axios

### Parser (parser/)
Contiene la lógica del compilador:
- **lr1_parser.py**: Algoritmo LR(1) completo
- **visualizer_graphviz.py**: Visualización con items completos
- **visualizer_automathon.py**: Visualización simplificada

## Librerías de Visualización

### Graphviz (Recomendado para LR(1))
- Control total sobre la visualización
- Muestra items LR(1) completos: `A → α • β, lookahead`
- Estados coloreados (verde=inicial, rojo=aceptación, azul=normal)
- Formatos: PNG, PDF, SVG, DOT
- Alta resolución (300 DPI)

### automathon
- Visualización simplificada tipo DFA
- Solo muestra números de estados
- Bueno para vista general rápida
- Formatos: PNG, SVG

## Tabla de Parsing

La tabla ACTION/GOTO incluye:

- **ACTION**: Acciones shift (sN), reduce (rN), accept (ACC)
- **GOTO**: Transiciones para no terminales
- **Colores distintivos**: Verde (shift), Amarillo (reduce), Azul (accept/goto)
- **Leyenda explicativa** para facilitar la lectura

## Comandos Útiles de Docker

### Ver logs de los contenedores
```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs solo del backend
docker-compose logs -f backend

# Ver logs solo del frontend
docker-compose logs -f frontend
```

### Reconstruir contenedores
```bash
# Reconstruir todo desde cero
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Detener y limpiar
```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Detener y eliminar imágenes
docker-compose down --rmi all
```

### Acceder a un contenedor
```bash
# Acceder al backend
docker exec -it lr1-backend /bin/bash

# Acceder al frontend
docker exec -it lr1-frontend /bin/sh
```

## Notas Técnicas

- Backend usa puerto 5001 para evitar conflictos con AirPlay en macOS
- Frontend usa puerto 5173 (Vite development server)
- La aplicación requiere Graphviz (incluido en el contenedor Docker)
- Las visualizaciones se generan bajo demanda
- CORS configurado para permitir comunicación entre frontend y backend
- La estructura modular permite fácil mantenimiento y escalabilidad
- Con Docker, los cambios en el código se reflejan automáticamente (hot reload)

## Desarrollo

**Curso:** Compiladores
**Universidad:** UTEC
**Tipo:** Puntos Extras Examen 2
**Fecha:** Octubre 2024

## Autores

Proyecto desarrollado para el curso de Compiladores - UTEC
