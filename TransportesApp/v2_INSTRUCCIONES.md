# INSTRUCCIONES DE EJECUCIÓN - VERSIÓN WEB v2

## 🚀 Cómo Ejecutar el Proyecto Web

El proyecto tiene dos componentes que deben ejecutarse simultáneamente:
1. **Backend** (API REST con Flask) - Puerto 5000
2. **Frontend** (Aplicación React) - Puerto 3000

### Requisitos Previos
- Python 3.8 o superior instalado
- Node.js 16 o superior instalado
- Terminal o línea de comandos
- Navegador web moderno (Chrome, Firefox, Edge recomendados)

---

## 📋 PASOS RÁPIDOS DE EJECUCIÓN

### Opción 1: Ejecución Manual (Recomendada)

#### Terminal 1 - Backend
```bash
# Navegar al directorio del backend
cd "D:\Trabajos u\Sexto semestre\Patrones de diseño\Parcial 3\TransportesApp\backend"

# Activar entorno virtual (si lo tienes configurado)
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
# source venv/bin/activate

# Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

**Salida esperada:**
```
============================================================
🚀 Servidor Backend iniciando...
============================================================
API REST para Sistema de Transportes
Puerto: 5000
URL: http://localhost:5000
============================================================
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

#### Terminal 2 - Frontend
```bash
# Abrir UNA NUEVA terminal (dejar la anterior corriendo)
# Navegar al directorio del frontend
cd "D:\Trabajos u\Sexto semestre\Patrones de diseño\Parcial 3\TransportesApp\frontend"

# Instalar dependencias (solo la primera vez)
npm install

# Ejecutar aplicación
npm start
```

**Resultado:**
- Se abrirá automáticamente tu navegador en `http://localhost:3000`
- Si no se abre, navega manualmente a esa URL

---

## 📱 Uso de la Aplicación Web

### 1. Verificar que Todo Funciona

Al abrir http://localhost:3000 deberías ver:
- ✅ Header con título "🚚 Sistema de Gestión de Transportes"
- ✅ Navegación con dos botones: "Lista de Envíos" y "Crear Envío"
- ✅ Vista inicial mostrando la lista de envíos (vacía si es primera ejecución)

### 2. Crear un Envío de Prueba

```
1. Click en "📦 Crear Envío" (botón superior derecho)
2. Completar el formulario:
   
   Tipo de Envío: Express
   Remitente: Juan Pérez
   Dirección Origen: Calle 100 #45-67, Bogotá
   Destinatario: María García
   Dirección Destino: Carrera 50 #23-45, Medellín
   Peso: 25
   Descripción: Documentos importantes
   ¿Frágil?: ✓ (marcar checkbox)

3. Click en "Crear Envío"
4. Observar:
   - Mensaje verde de éxito
   - Envío aparece en la lista automáticamente
   - Muestra el ID generado (ej: ENV-00001)
   - Muestra el costo calculado
```

### 3. Ver Detalles del Envío

```
1. Desde la lista, click en el envío creado
2. Ver información completa organizada en secciones:
   - Información General
   - Remitente y Destinatario  
   - Detalles del Paquete
   - Costos
3. Botones disponibles:
   - "➡️ Avanzar Estado" - Mover al siguiente estado
   - "❌ Cancelar Envío" - Cancelar el envío
   - "← Volver" - Regresar a la lista
```

### 4. Avanzar el Estado del Envío

```
1. Desde la vista de detalles
2. Click en "➡️ Avanzar Estado"
3. Observar:
   - El estado cambia al siguiente en la secuencia
   - Color de la etiqueta cambia
   - Mensaje de confirmación
4. Repetir para ver todos los estados:
   Pendiente → En Proceso → En Tránsito → En Distribución → Entregado
```

### 5. Cancelar un Envío

```
1. Desde la vista de detalles
2. Click en "❌ Cancelar Envío"
3. Confirmar en el diálogo
4. Observar:
   - Estado cambia a "Cancelado"
   - Color naranja
   - Ya no se pueden hacer más cambios
```

---

## 🎯 Demostración de Patrones de Diseño

### Patrón Chain of Responsibility (Validación)

**Demostración:**
```
1. Ir a "Crear Envío"
2. Dejar campos vacíos y dar click en "Crear Envío"
   → Verás errores de validación específicos

3. Ingresar peso inválido (ej: 2000 kg)
   → Error: "Peso debe estar entre 0.1 y 1000 kg"

4. Seleccionar "Express" e ingresar peso muy alto
   → La validación calcula restricciones automáticamente
```

### Patrón State (Estados del Envío)

**Demostración:**
```
1. Crear un envío nuevo
2. Ver que inicia en "Pendiente de validación"
3. Click en "Avanzar Estado" varias veces
4. Observar la secuencia completa de estados
5. Intentar cancelar en diferentes estados
```

### Patrón Memento (NO VISIBLE EN FRONTEND ACTUAL)

**Estado:** ⚠️ Implementado en backend pero sin interfaz

**Endpoints disponibles:**
- PUT /api/envios/<id>/modificar
- POST /api/envios/<id>/deshacer
- POST /api/envios/<id>/rehacer
- GET /api/envios/<id>/historial

### Patrón Visitor (NO VISIBLE EN FRONTEND ACTUAL)

**Estado:** ⚠️ Implementado en backend pero sin interfaz

**Endpoints disponibles:**
- GET /api/envios/<id>/tiempo-entrega
- GET /api/envios/<id>/descuentos
- GET /api/envios/<id>/reporte

---

## 🔧 Pruebas de la API (Opcional)

Si quieres probar directamente la API sin el frontend:

### Usando cURL

```bash
# 1. Health Check
curl http://localhost:5000/api/health

# 2. Crear Envío
curl -X POST http://localhost:5000/api/envios \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Express",
    "remitente": "Juan Pérez",
    "destinatario": "María García",
    "direccion_origen": "Calle 100 #45-67, Bogotá",
    "direccion_destino": "Carrera 50 #23-45, Medellín",
    "peso": 25.5,
    "descripcion": "Documentos",
    "es_fragil": true
  }'

# 3. Listar Envíos
curl http://localhost:5000/api/envios

# 4. Ver Envío Específico
curl http://localhost:5000/api/envios/ENV-00001

# 5. Avanzar Estado
curl -X POST http://localhost:5000/api/envios/ENV-00001/avanzar

# 6. Calcular Tiempo de Entrega (Visitor)
curl http://localhost:5000/api/envios/ENV-00001/tiempo-entrega

# 7. Generar Reporte (Visitor)
curl http://localhost:5000/api/envios/ENV-00001/reporte

# 8. Ver Historial (Memento)
curl http://localhost:5000/api/envios/ENV-00001/historial
```

### Usando Postman o Thunder Client

1. Importar la colección de endpoints
2. Configurar base URL: `http://localhost:5000/api`
3. Probar todos los endpoints disponibles

---

## 🐛 Solución de Problemas

### Problema 1: Backend No Inicia

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solución:**
```bash
cd backend
pip install flask flask-cors
# O instalar todo:
pip install -r requirements.txt
```

**Error:** `Address already in use: Port 5000`

**Solución:**
```bash
# Opción A: Matar el proceso en el puerto 5000
# En Windows:
netstat -ano | findstr :5000
taskkill /PID <número_de_proceso> /F

# En Linux/Mac:
lsof -ti:5000 | xargs kill -9

# Opción B: Cambiar puerto en app.py
# Editar línea final de app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problema 2: Frontend No Inicia

**Error:** `npm: command not found`

**Solución:**
- Instalar Node.js desde https://nodejs.org/
- Reiniciar la terminal después de instalar
- Verificar con: `node --version` y `npm --version`

**Error:** `Port 3000 already in use`

**Solución:**
```bash
# Opción A: Usar otro puerto
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # Linux/Mac

# Opción B: Matar proceso en puerto 3000
# En Windows:
netstat -ano | findstr :3000
taskkill /PID <número_de_proceso> /F
```

**Error:** `Module not found: Can't resolve 'axios'`

**Solución:**
```bash
cd frontend
npm install axios
npm start
```

### Problema 3: Frontend No Conecta con Backend

**Error:** `Network Error` o `Failed to fetch`

**Verificar:**
1. ¿El backend está corriendo?
   - Abrir http://localhost:5000/api/health
   - Debería responder: `{"status": "ok", ...}`

2. ¿El puerto es correcto?
   - Verificar en `frontend/src/App.js`:
   ```javascript
   const API_URL = 'http://localhost:5000/api';
   ```

3. ¿CORS está configurado?
   - En `backend/app.py` debe tener:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

### Problema 4: Errores al Crear Envío

**Error:** `Validation failed`

**Causas comunes:**
- Peso fuera de rango (debe ser 0.1 - 1000 kg)
- Tipo de envío incorrecto (debe ser exactamente: Express, Estándar, Económico)
- Campos requeridos vacíos
- Caracteres especiales en direcciones

**Solución:**
- Revisar el mensaje de error específico
- Ver la consola del navegador (F12) para más detalles
- Verificar que todos los campos estén completos

---

## 📊 Flujo Completo de Demostración

### Para Presentación en Clase (10 minutos)

#### 1. Introducción (1 min)
```
"Voy a mostrar un sistema de gestión de transportes que implementa
4 patrones de diseño: Chain of Responsibility, State, Memento y Visitor"
```

#### 2. Demostrar Backend (2 min)
```
1. Mostrar que el backend está corriendo
2. Abrir http://localhost:5000/api/health
3. Explicar: "Tenemos 12 endpoints REST funcionando"
4. Mostrar rápidamente la estructura del código backend
```

#### 3. Demostrar Frontend (3 min)
```
1. Abrir http://localhost:3000
2. Crear un envío completo
3. Mostrar validaciones (intentar crear envío inválido)
4. Explicar: "Aquí vemos Chain of Responsibility en acción"
```

#### 4. Demostrar Patrón State (2 min)
```
1. Seleccionar el envío creado
2. Avanzar por todos los estados
3. Explicar cada transición
4. Mostrar que no se puede retroceder (flujo unidireccional)
5. Intentar cancelar desde un estado intermedio
```

#### 5. Demostrar API Directa (2 min)
```
1. Abrir terminal
2. Ejecutar: curl http://localhost:5000/api/envios/ENV-00001/reporte
3. Explicar Patrón Visitor
4. Ejecutar: curl http://localhost:5000/api/envios/ENV-00001/historial
5. Explicar Patrón Memento
```

### Para Evaluación Detallada (20 minutos)

#### Parte 1: Arquitectura (5 min)
- Explicar arquitectura MVC
- Mostrar separación de responsabilidades
- Explicar cómo se comunican frontend y backend
- Mostrar estructura de carpetas

#### Parte 2: Patrones de Diseño (10 min)
- Chain of Responsibility: Validadores en cadena
- State: Máquina de estados del envío
- Memento: Historial y undo/redo
- Visitor: Operaciones sobre envíos

#### Parte 3: Demostración Práctica (5 min)
- Crear varios envíos
- Avanzar estados
- Mostrar cálculos automáticos
- Mostrar validaciones

---

## 📝 Notas Importantes

### Estado Actual del Proyecto

**✅ Backend: 100% Completo**
- 12 endpoints funcionando
- 4 patrones implementados
- Validaciones robustas
- Manejo de errores completo

**⚠️ Frontend: 40% Completo**
- ✅ Listar envíos
- ✅ Crear envío
- ✅ Ver detalles
- ✅ Avanzar estado
- ✅ Cancelar envío
- ❌ Modificar envío (backend listo)
- ❌ Historial y Memento (backend listo)
- ❌ Reportes y análisis (backend listo)

### Funcionalidades Disponibles Solo en API

Para demostrar Memento y Visitor completamente, usar la API directamente:

```bash
# Memento: Modificar y ver historial
curl -X PUT http://localhost:5000/api/envios/ENV-00001/modificar \
  -H "Content-Type: application/json" \
  -d '{"campo": "peso", "valor": 30}'

curl http://localhost:5000/api/envios/ENV-00001/historial

# Visitor: Cálculos y reportes
curl http://localhost:5000/api/envios/ENV-00001/tiempo-entrega
curl http://localhost:5000/api/envios/ENV-00001/descuentos
curl http://localhost:5000/api/envios/ENV-00001/reporte
```

---

## 🎯 Checklist de Verificación

Antes de presentar/demostrar, verificar:

- [ ] Backend corriendo en puerto 5000
- [ ] Frontend corriendo en puerto 3000
- [ ] Se puede abrir http://localhost:3000
- [ ] Se puede crear un envío de prueba
- [ ] Los estados avanzan correctamente
- [ ] Las validaciones funcionan
- [ ] La API responde en http://localhost:5000/api/health
- [ ] No hay errores en consola del navegador (F12)
- [ ] No hay errores en terminal del backend

---

## 📞 Comandos Rápidos de Referencia

```bash
# Iniciar Backend
cd backend && python app.py

# Iniciar Frontend
cd frontend && npm start

# Verificar Backend
curl http://localhost:5000/api/health

# Ver todos los envíos
curl http://localhost:5000/api/envios

# Matar proceso en puerto (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Reinstalar dependencias Frontend
cd frontend && rm -rf node_modules && npm install

# Reinstalar dependencias Backend
cd backend && pip install -r requirements.txt --force-reinstall
```

---

**¡Listo para ejecutar! 🚀**

Comando para iniciar ambos (en Windows):
```bash
# En una terminal:
cd backend && python app.py

# En otra terminal:
cd frontend && npm start
```
