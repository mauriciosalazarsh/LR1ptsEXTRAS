# 🌐 DEPLOYMENT WEB - GUÍA COMPLETA

## 🎯 OBJETIVO

Deployar tu proyecto para que sea accesible con un link público (sin localhost).

**Resultado final:**
- ✅ Backend accesible: `https://tu-app.onrender.com`
- ✅ Frontend accesible: `https://tu-app.vercel.app`
- ✅ Gratis 100%

---

## 📋 REQUISITOS PREVIOS

1. ✅ Código ya está en GitHub: https://github.com/mauriciosalazarsh/LR1ptsEXTRAS
2. ⚠️ Necesitas crear cuentas (gratis) en:
   - [Render.com](https://render.com) - Para el backend
   - [Vercel.com](https://vercel.com) - Para el frontend

---

# 🔧 PARTE 1: DEPLOYAR BACKEND (Render)

## Paso 1.1: Crear cuenta en Render

1. Ve a: https://render.com
2. Click **"Get Started"**
3. Regístrate con GitHub (usa tu cuenta de GitHub)
4. Autoriza a Render para acceder a tus repositorios

## Paso 1.2: Crear Web Service

1. En el dashboard de Render, click **"New +"**
2. Selecciona **"Web Service"**
3. Busca el repositorio: `LR1ptsEXTRAS`
4. Click **"Connect"**

## Paso 1.3: Configurar el servicio

Llena los campos:

| Campo | Valor |
|-------|-------|
| **Name** | `lr1-parser-backend` (o el que quieras) |
| **Region** | Oregon (US West) |
| **Branch** | `main` |
| **Root Directory** | (dejar vacío) |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn backend.app:app --bind 0.0.0.0:$PORT` |

**Importante:**
- En **Environment Variables**, añade:
  - `PYTHON_VERSION` = `3.9.0`

- Selecciona el plan **Free**

## Paso 1.4: Deploy

1. Click **"Create Web Service"**
2. ⏳ Espera 5-10 minutos mientras se construye
3. ✅ Cuando termine verás: "Your service is live 🎉"
4. 📝 **Copia la URL** que te dan (algo como: `https://lr1-parser-backend.onrender.com`)

---

# 🎨 PARTE 2: DEPLOYAR FRONTEND (Vercel)

## Paso 2.1: Crear cuenta en Vercel

1. Ve a: https://vercel.com
2. Click **"Sign Up"**
3. Regístrate con GitHub
4. Autoriza a Vercel para acceder a tus repositorios

## Paso 2.2: Importar proyecto

1. En el dashboard, click **"Add New..."** → **"Project"**
2. Busca: `LR1ptsEXTRAS`
3. Click **"Import"**

## Paso 2.3: Configurar el proyecto

Llena los campos:

| Campo | Valor |
|-------|-------|
| **Project Name** | `lr1-parser` (o el que quieras) |
| **Framework Preset** | Vite |
| **Root Directory** | `frontend/react-app` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

**MUY IMPORTANTE - Variables de entorno:**

Click en **"Environment Variables"** y añade:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://lr1-parser-backend.onrender.com/api` |

⚠️ **Reemplaza** `lr1-parser-backend` con el nombre de TU backend de Render del Paso 1.4

## Paso 2.4: Deploy

1. Click **"Deploy"**
2. ⏳ Espera 2-3 minutos
3. ✅ Verás: "Congratulations! 🎉"
4. 📝 **Copia la URL** (algo como: `https://lr1-parser.vercel.app`)

---

# ✅ VERIFICACIÓN

## Probar que funciona

1. **Abre la URL de Vercel** en tu navegador
2. Deberías ver la interfaz del parser
3. **Prueba construir un parser:**
   - Selecciona LR(1) o LALR(1)
   - Click "Construir Parser"
   - Si funciona, ¡éxito! 🎉

## Si hay errores

### Error: "Failed to fetch" o "Network Error"

**Causa:** El frontend no puede conectarse al backend

**Solución:**
1. Verifica que la URL del backend esté correcta en Vercel
2. Ve a: Vercel Dashboard → Tu proyecto → Settings → Environment Variables
3. Verifica que `VITE_API_URL` tenga la URL correcta de Render
4. Si la cambiaste, ve a Deployments → Click en los 3 puntos → **"Redeploy"**

### Error: "Application error" en Render

**Causa:** El backend no arrancó correctamente

**Solución:**
1. Ve a Render Dashboard → Tu servicio → Logs
2. Revisa los errores
3. Comunes:
   - Falta `graphviz`: Render necesita instalarlo (contactar soporte o usar otra plataforma)
   - Puerto incorrecto: Asegúrate que el Start Command tenga `--bind 0.0.0.0:$PORT`

---

# 🎉 RESULTADO FINAL

Si todo salió bien, tendrás:

```
✅ Backend deployado: https://lr1-parser-backend.onrender.com
✅ Frontend deployado: https://lr1-parser.vercel.app
✅ Funcionando 100% en la nube
```

**Comparte tu link:** `https://lr1-parser.vercel.app`

---

# 📊 LIMITACIONES DEL PLAN GRATUITO

### Render (Backend):
- ⏰ El servidor "duerme" después de 15 min de inactividad
- 🐌 Primera request después de dormir toma ~30 segundos
- 🔄 Despierta automáticamente con cualquier request
- ⚠️ **Graphviz**: Puede no estar disponible en plan gratuito

### Vercel (Frontend):
- ✅ Sin limitaciones importantes para este proyecto
- 🚀 Rápido y confiable

---

# 🔧 TROUBLESHOOTING

## Graphviz no funciona en Render

**Problema:** Render Free no incluye `graphviz` binario

**Soluciones alternativas:**

### Opción A: Usar Railway en vez de Render
1. Ve a: https://railway.app
2. Signup con GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repo
5. Configura:
   - Start Command: `gunicorn backend.app:app --bind 0.0.0.0:$PORT`
   - Variables: `PORT=5001`
6. Railway SÍ incluye graphviz

### Opción B: Usar Replit (todo en uno)
1. Ve a: https://replit.com
2. Import from GitHub
3. Run automáticamente

### Opción C: Solo mostrar tablas (sin gráficos)
- El resto de funcionalidades seguirán funcionando
- Solo la visualización Graphviz fallará

---

# 🔄 ACTUALIZAR EL DEPLOYMENT

Cuando hagas cambios al código:

## Backend (Render):
1. Push a GitHub: `git push origin main`
2. Render detecta automáticamente y redeploya ✅

## Frontend (Vercel):
1. Push a GitHub: `git push origin main`
2. Vercel detecta automáticamente y redeploya ✅

---

# 📱 COMPARTIR TU PROYECTO

Envía este link a quien quieras:
```
https://lr1-parser.vercel.app
```

O crea un README badge:
```markdown
[![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://lr1-parser.vercel.app)
```

---

# 💡 TIPS

1. **Primera carga lenta:** Normal por el "cold start" de Render
2. **Mantener despierto:** Usa [UptimeRobot](https://uptimerobot.com) para ping cada 5 min
3. **Dominios custom:** Tanto Vercel como Render permiten dominios propios (gratis)

---

# ✅ CHECKLIST FINAL

Antes de compartir tu app:

- [ ] Backend responde en `/` (debería dar info del API)
- [ ] Frontend carga correctamente
- [ ] Puedes construir un parser LR(1)
- [ ] Puedes construir un parser LALR(1)
- [ ] La tabla de parsing carga
- [ ] El análisis de cadenas funciona
- [ ] (Opcional) Graphviz genera gráficos

---

¡Listo! Tu proyecto está en la nube 🚀
