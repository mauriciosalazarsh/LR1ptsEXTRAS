# LR1ptsEXTRAS

## Analizador LR(1) - Puntos Extras Examen 2

Implementación completa de un analizador LR(1) en Python con interfaz web y visualización gráfica del autómata.

### 🎯 Características

- **Parser LR(1) completo** con cálculo de conjuntos FIRST/FOLLOW
- **Autómata LR(1)** con visualización jerárquica exacta
- **Interfaz web** con Flask para procesamiento en tiempo real
- **Gráficos precisos** que replican el formato de referencia académica
- **Tabla de parsing** completa con acciones SHIFT/REDUCE/ACCEPT

### 🚀 Ejecución Rápida

```bash
python3 EJECUTAR_FINAL.py
```

Este comando genera:
- `TU_AUTOMATA_EXACTO.png` - Autómata LR(1) con formato exacto
- `TU_TABLA_EXACTA.png` - Tabla de parsing completa

### 📋 Gramática de Prueba

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

### 🔧 Conjuntos FIRST y FOLLOW

**Conjuntos FIRST:**
- FIRST(S): {q}
- FIRST(A): {a, b}
- FIRST(B): {a, ε}
- FIRST(C): {b, ε}
- FIRST(D): {b, ε}

**Conjuntos FOLLOW:**
- FOLLOW(S): {$}
- FOLLOW(A): {*}
- FOLLOW(B): {*}
- FOLLOW(C): {$, *}
- FOLLOW(D): {*}

### 📁 Estructura del Proyecto

```
├── lr1_parser.py              # Algoritmo LR(1) principal
├── graph_visualizer_exact.py  # Visualización exacta del autómata
├── graph_visualizer.py        # Visualización de tablas
├── app_complete.py            # Interfaz web Flask
├── EJECUTAR_FINAL.py          # Script de ejecución principal
├── test_first_follow.py       # Pruebas de conjuntos FIRST/FOLLOW
└── README.md                  # Este archivo
```

### 🌐 Interfaz Web

```bash
python3 app_complete.py
```

Accede a `http://127.0.0.1:5000` para usar la interfaz web interactiva.

### ✅ Validación

El analizador acepta cadenas como:
- `q * a * a * b` ✅
- `q * b * b * b * a * b` ✅

Y rechaza cadenas inválidas como:
- `q * a * b` ❌

### 📊 Resultados

- **19 estados** en el autómata LR(1)
- **5 terminales**: {q, *, a, b, $}
- **5 no terminales**: {S, A, B, C, D}
- **10 producciones** en total

### 🎨 Visualización

El autómata generado incluye:
- ✅ Título "Autómata LR(1)"
- ✅ Estado inicial I0 en verde
- ✅ Estado de aceptación I2 en rojo
- ✅ Layout jerárquico tipo árbol
- ✅ Items LR(1) formateados correctamente
- ✅ Transiciones con etiquetas claras

---

**Desarrollado para:** Examen 2 - Compiladores UTEC  
**Fecha límite:** 17/10 (entrega) - 18/10 (presentación)  
**Objetivo:** 5 puntos por mejor trabajo, 3 puntos por cumplir objetivos
