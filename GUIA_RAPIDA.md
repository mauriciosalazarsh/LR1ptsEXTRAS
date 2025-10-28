# 🚀 GUÍA RÁPIDA - CÓMO CORRER LR(1) Y LALR(1)

## 📋 Pasos para Iniciar la Aplicación

### 1️⃣ INICIAR EL BACKEND

Abre una terminal y ejecuta:

```bash
cd /Users/msalazarh/Documents/utec/Compiladores/PRPTSEXTRAS
python3 -m backend.app
```

**Verás algo como:**
```
======================================================================
               VISUALIZADOR WEB DE AUTOMATA LR(1)
          Compiladores - UTEC - Puntos Extras
======================================================================

Servidor iniciado en: http://127.0.0.1:5001
Presiona Ctrl+C para detener el servidor
```

✅ **El backend está corriendo en: http://localhost:5001**

---

### 2️⃣ INICIAR EL FRONTEND

Abre **OTRA TERMINAL** (deja la primera corriendo) y ejecuta:

```bash
cd /Users/msalazarh/Documents/utec/Compiladores/PRPTSEXTRAS/frontend/react-app
npm run dev
```

**Verás algo como:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ **El frontend está corriendo en: http://localhost:5173**

---

## 🎯 USAR LA APLICACIÓN

### 3️⃣ ABRIR EN EL NAVEGADOR

Abre tu navegador y ve a: **http://localhost:5173**

---

## 🔄 CAMBIAR ENTRE LR(1) Y LALR(1)

### En la Interfaz Web:

1. **Verás un selector dropdown** debajo del campo de gramática:
   ```
   Tipo de Parser: [Seleccionar ▼]
   ```

2. **Opciones disponibles:**
   - **LR(1)** → Parser LR(1) completo (más estados)
   - **LALR(1)** → Parser LALR(1) optimizado (menos estados)

3. **Pasos para probar:**

   **a) Probar con LR(1):**
   - Selecciona **"LR(1)"** en el dropdown
   - Clic en **"Construir Parser LR(1)"**
   - Observa el número de estados generados

   **b) Probar con LALR(1):**
   - Selecciona **"LALR(1)"** en el dropdown
   - Clic en **"Construir Parser LALR(1)"**
   - Compara: verás menos estados

---

## 📊 COMPARACIÓN VISUAL

### Gramática de Ejemplo (por defecto):
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

### Resultados Esperados:

| Parser   | Estados | Transiciones | Reducción |
|----------|---------|--------------|-----------|
| LR(1)    | 19      | 18           | -         |
| LALR(1)  | 18      | 18           | 5.3%      |

### Para Gramática de Expresiones Aritméticas:
```
S -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
```

| Parser   | Estados | Transiciones | Reducción |
|----------|---------|--------------|-----------|
| LR(1)    | 23      | 39           | -         |
| LALR(1)  | 13      | 23           | 43.5%     |

---

## 🧪 PROBAR CADENAS

Después de construir el parser (LR1 o LALR1):

1. **Desplázate hacia abajo** hasta "Análisis de Cadenas"
2. **Ingresa una cadena**, ejemplo:
   - Para la gramática por defecto: `q * a * a * b`
   - Para expresiones: `id + id * id`
3. **Clic en "Analizar"**
4. **Verás:**
   - ✅ "Cadena aceptada" o ❌ "Cadena rechazada"
   - Traza paso a paso del proceso de parsing

---

## 📈 VER VISUALIZACIONES

Una vez construido el parser:

### 1. **Autómata (Graphviz)** ⭐ INCLUYE LR(1) Y LALR(1)
   - Click en pestaña **"Autómata (Graphviz)"**
   - Click en **"Generar con Graphviz"**
   - ✅ **Funciona con ambos parsers: LR(1) y LALR(1)**
   - Verás el autómata con todos los items completos
   - **Estados coloreados:**
     - 🟢 Verde = Estado inicial
     - 🔴 Rojo = Estado de aceptación
     - 🔵 Azul = Estados normales
   - **Controles:**
     - 🖱️ Scroll para zoom in/out
     - 🖱️ Arrastrar para mover el gráfico
     - 🔄 Botón "Resetear Zoom" para volver a la vista original

### 2. **Tabla ACTION/GOTO**
   - Click en pestaña **"Tabla de Parsing"**
   - Verás la tabla completa
   - **Colores:**
     - 🟢 Verde = shift
     - 🟡 Amarillo = reduce
     - 🔵 Azul = goto
     - 🟣 Morado = accept

### 3. **Detalles del Parser**
   - Click en pestaña **"Detalles"**
   - Verás:
     - Producciones de la gramática
     - Conjuntos FIRST
     - Conjuntos FOLLOW
     - Estadísticas del autómata

---

## 🔧 COMPARACIÓN DESDE TERMINAL

Si prefieres ver la comparación desde la terminal:

```bash
python3 test_comparison.py
```

Esto ejecutará ambos parsers y mostrará una tabla comparativa.

---

## ❓ TROUBLESHOOTING

### Backend no inicia:
```bash
pip3 install -r requirements.txt
```

### Frontend no inicia:
```bash
cd frontend/react-app
npm install
npm run dev
```

### Puerto 5001 ocupado:
Edita `backend/app.py` línea 323:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambiar 5001 por otro puerto
```

---

## 📊 COMPARAR GRÁFICAMENTE LR(1) vs LALR(1)

### Proceso paso a paso:

**Paso 1: Generar gráfico LR(1)**
1. Selecciona **"LR(1)"** en el dropdown
2. Click **"Construir Parser LR(1)"**
3. Ve a pestaña **"Autómata (Graphviz)"**
4. Click **"Generar con Graphviz"**
5. 📸 **Toma captura** o observa: 23 estados con la gramática de expresiones

**Paso 2: Generar gráfico LALR(1)**
1. Selecciona **"LALR(1)"** en el dropdown
2. Click **"Construir Parser LALR(1)"**
3. Ve a pestaña **"Autómata (Graphviz)"**
4. Click **"Generar con Graphviz"** nuevamente
5. 📸 **Compara**: Solo 13 estados (43.5% menos!)

**Diferencias visuales:**
- 🔢 **Número de nodos**: LR(1) tiene más estados
- 🔗 **Transiciones**: LR(1) tiene más aristas
- 📦 **Items**: En LALR(1) verás estados con múltiples lookaheads fusionados
- ✅ **Ambos funcionan igual**: Aceptan/rechazan las mismas cadenas

---

## 🎓 PARA LA DEMO

### Flujo recomendado:

1. **Mostrar LR(1)**
   - Construir con LR(1)
   - **Generar y mostrar gráfico Graphviz** (23 estados para expresiones)
   - Analizar una cadena

2. **Cambiar a LALR(1)**
   - Cambiar selector a LALR(1)
   - Reconstruir parser
   - **Generar y mostrar gráfico Graphviz** (13 estados para expresiones)
   - Analizar la misma cadena

3. **Comparar visualmente**
   - Mostrar ambos gráficos lado a lado
   - Explicar: LALR(1) reduce 43.5% de estados
   - Ambos parsers aceptan/rechazan las mismas cadenas
   - LALR(1) es más eficiente en memoria

---

## 🎯 RESUMEN RÁPIDO

```
Terminal 1:  python3 -m backend.app
Terminal 2:  cd frontend/react-app && npm run dev
Navegador:   http://localhost:5173

Selector:    Cambiar entre LR(1) y LALR(1)
Construir:   Click "Construir Parser"
Visualizar:  Pestañas de Autómata, Tabla, Detalles
Analizar:    Ingresar cadena y click "Analizar"
```

---

## ✅ TODO LISTO

Ahora puedes demostrar ambos parsers y comparar sus resultados en tiempo real! 🚀
