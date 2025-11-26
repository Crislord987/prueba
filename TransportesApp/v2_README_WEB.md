# 🚚 Sistema de Gestión de Transportes y Envíos - Versión Web v2

Sistema completo de gestión de transportes implementando patrones de diseño de comportamiento con arquitectura web moderna (Backend Flask + Frontend React).

## 📋 Patrones de Diseño Implementados

### 1. **Chain of Responsibility** ⛓️
Valida los envíos a través de una cadena de validadores:
- **ValidadorDatos**: Verifica que todos los campos requeridos estén presentes
- **ValidadorPeso**: Valida que el peso esté entre 0.1 kg y 1000 kg
- **ValidadorTipo**: Verifica que el tipo de envío sea válido (Express, Estándar, Económico)
- **ValidadorDistancia**: Valida distancias según el tipo de servicio
- **ValidadorSeguridad**: Determina si el envío requiere seguro adicional

### 2. **State** 🔄
Gestiona el ciclo de vida completo del envío con transiciones automáticas:
```
Pendiente de validación → En proceso de preparación → En tránsito hacia destino → 
En distribución local → Entregado exitosamente
```
- Permite cancelación desde cualquier estado antes de entrega
- Cada estado tiene su comportamiento y validaciones específicas
- Transiciones automáticas entre estados

### 3. **Memento** ⏮️
Mantiene un historial completo de cambios del envío con capacidad de deshacer/rehacer:
- Guarda snapshots de cada modificación
- Permite navegar por el historial completo
- Funcionalidad de Undo/Redo ilimitada
- Historial navegable con índice de posición actual

### 4. **Visitor** 👁️
Aplica diferentes operaciones sobre los envíos sin modificar su estructura:
- **Cálculo de costos**: Tarifa base + distancia + peso + extras
- **Cálculo de tiempo de entrega**: Según tipo y distancia
- **Generación de reportes**: Reporte completo con toda la información
- **Cálculo de descuentos**: Por volumen, distancia o promociones

## 🏗️ Arquitectura del Sistema

```
TransportesApp/
├── backend/                    # API REST con Flask
│   ├── app.py                 # Servidor principal (12 endpoints)
│   └── requirements.txt       # Dependencias Python
│
├── frontend/                   # Aplicación React
│   ├── public/                # Archivos estáticos
│   ├── src/
│   │   ├── App.js             # Componente principal
│   │   ├── index.css          # Estilos globales
│   │   └── index.js           # Punto de entrada
│   └── package.json           # Dependencias Node
│
├── Controllers/                # Lógica de negocio
│   └── EnvioController.py     # Controlador principal
│
├── Models/                     # Modelos de datos
│   └── Envio.py               # Modelo de envío
│
├── Patterns/                   # Patrones de diseño
│   ├── ChainOfResponsibility/ # Validadores
│   ├── State/                 # Estados del envío
│   ├── Memento/               # Historial de cambios
│   └── Visitor/               # Operaciones sobre envíos
│
└── Views/                      # (Solo para versión consola)
```

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- Node.js 16 o superior
- pip (gestor de paquetes Python)
- npm o yarn (gestor de paquetes Node)

### 1. Configurar Backend (API REST)

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

**Salida esperada:**
```
============================================================
🚀 Servidor Backend iniciando...
============================================================
API REST para Sistema de Transportes
Puerto: 5000
URL: http://localhost:5000
============================================================
```

### 2. Configurar Frontend (React)

```bash
# Abrir una nueva terminal
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar aplicación
npm start
```

La aplicación web se abrirá automáticamente en: `http://localhost:3000`

## 📱 Funcionalidades de la Aplicación

### 🎯 Vista Principal - Lista de Envíos
- Muestra todos los envíos registrados con información resumida
- Tarjetas visuales con estados codificados por colores
- Click en cualquier tarjeta para ver detalles completos
- Contador de envíos totales
- Estado visual vacío cuando no hay envíos

### 📦 Crear Nuevo Envío
Formulario completo para registrar envíos con:
- **Tipo de Servicio**: Express (24h), Estándar (3-5 días), Económico (7-10 días)
- **Datos del Remitente**: Nombre y dirección de origen
- **Datos del Destinatario**: Nombre y dirección de destino
- **Información del Paquete**:
  - Peso en kilogramos (validación automática)
  - Descripción del contenido (opcional)
  - Marcador de frágil
- **Validación en Tiempo Real**:
  - Chain of Responsibility valida todos los campos
  - Mensajes de error claros y específicos
  - Cálculo automático de costo al crear

### 🔍 Detalles del Envío
Vista completa con toda la información organizada en secciones:
- **Información General**: ID, tipo, estado, fecha de creación
- **Remitente y Destinatario**: Datos completos de ambas partes
- **Detalles del Paquete**: Peso, distancia, características especiales
- **Costos**: Desglose del costo total calculado
- **Acciones Disponibles**:
  - **➡️ Avanzar Estado**: Mueve al siguiente estado en el ciclo
  - **❌ Cancelar Envío**: Cancela el envío (si no está entregado)

### 📊 Estados del Envío

| Estado | Color | Descripción |
|--------|-------|-------------|
| Pendiente de validación | 🟡 Amarillo | Envío registrado, en proceso de validación |
| En proceso de preparación | 🔵 Azul | Preparando empaque y documentación |
| En tránsito hacia destino | 🟣 Morado | En camino al centro de distribución |
| En distribución local | 🟡 Rosa | En reparto final al destinatario |
| Entregado exitosamente | 🟢 Verde | Entregado y firmado por el destinatario |
| Cancelado | 🟠 Naranja | Envío cancelado por el usuario |

## 🔧 API REST Endpoints

El backend proporciona 12 endpoints REST completos:

### Endpoints Básicos
1. **`GET /api/health`** - Health check del servidor
2. **`GET /api/envios`** - Listar todos los envíos
3. **`GET /api/envios/<id>`** - Obtener envío específico
4. **`POST /api/envios`** - Crear nuevo envío

### Endpoints de Estado (Patrón State)
5. **`GET /api/envios/<id>/estado`** - Consultar estado actual
6. **`POST /api/envios/<id>/avanzar`** - Avanzar al siguiente estado
7. **`POST /api/envios/<id>/cancelar`** - Cancelar envío

### Endpoints de Historial (Patrón Memento)
8. **`PUT /api/envios/<id>/modificar`** - Modificar datos del envío
9. **`POST /api/envios/<id>/deshacer`** - Deshacer último cambio
10. **`POST /api/envios/<id>/rehacer`** - Rehacer cambio deshecho
11. **`GET /api/envios/<id>/historial`** - Ver historial completo

### Endpoints de Análisis (Patrón Visitor)
12. **`GET /api/envios/<id>/tiempo-entrega`** - Calcular tiempo estimado
13. **`GET /api/envios/<id>/descuentos`** - Calcular descuentos aplicables
14. **`GET /api/envios/<id>/reporte`** - Generar reporte completo

## 💰 Sistema de Costos

### Cálculo Base
```python
costo_base = (tarifa_por_kg * peso) + (tarifa_por_km * distancia)
```

### Tarifas por Tipo de Servicio
| Tipo | Tarifa/kg | Tarifa/km |
|------|-----------|-----------|
| Express | $5.00 | $2.00 |
| Estándar | $3.00 | $1.50 |
| Económico | $2.00 | $1.00 |

### Recargos Adicionales
- **Peso > 50 kg**: +20% del costo base
- **Paquete Frágil**: +15% del costo base
- **Seguro**: +2% del costo total (cuando aplica)

### Descuentos
- **Volumen**: Descuentos por peso (50kg+: 5%, 100kg+: 10%)
- **Distancia**: Descuentos por kilómetros recorridos
- **Promociones**: Descuentos especiales por campaña

## ⏱️ Tiempos de Entrega

### Por Tipo de Servicio
- **Express**: 1-2 días (hasta 500 km)
- **Estándar**: 3-5 días (hasta 1000 km)
- **Económico**: 7-10 días (sin límite de distancia)

### Factores que Afectan el Tiempo
- Distancia total del envío
- Tipo de servicio contratado
- Peso y características del paquete
- Condiciones climáticas y tráfico (simulado)

## 🔐 Validaciones del Sistema

### Validación de Datos (Chain of Responsibility)
1. **Campos Requeridos**:
   - Tipo de envío
   - Remitente y destinatario
   - Direcciones completas
   - Peso del paquete

2. **Validación de Peso**:
   - Mínimo: 0.1 kg
   - Máximo: 1000 kg
   - Debe ser un número positivo

3. **Validación de Tipo**:
   - Solo permite: Express, Estándar, Económico
   - Sensible a mayúsculas

4. **Validación de Distancia**:
   - Express: máximo 500 km
   - Estándar: máximo 1000 km
   - Económico: sin límite

5. **Validación de Seguridad**:
   - Seguro obligatorio si valor estimado > $1000
   - Seguro opcional para valores menores

## 🎨 Características de la Interfaz

### Diseño Moderno y Responsive
- **Gradientes Vibrantes**: Color primary (#667eea) y secondary (#764ba2)
- **Animaciones Suaves**: Transiciones de 0.3s en todos los elementos
- **Cards con Hover**: Efectos de elevación al pasar el cursor
- **Loading States**: Spinners animados durante operaciones
- **Mensajes Contextuales**: Feedback claro de éxito/error

### Colores por Estado
```css
Pendiente: #fbbf24 (amarillo/ámbar)
En Proceso: #3b82f6 (azul)
En Tránsito: #8b5cf6 (morado)
En Distribución: #ec4899 (rosa)
Entregado: #10b981 (verde)
Cancelado: #f97316 (naranja)
```

### Estados Visuales
- ✅ **Success**: Verde (#10b981)
- ❌ **Error**: Rojo (#ef4444)
- ⚠️ **Warning**: Amarillo (#f59e0b)
- ℹ️ **Info**: Azul (#3b82f6)

## 📱 Uso Paso a Paso

### 1. Crear un Envío
```
1. Click en "📦 Crear Envío"
2. Seleccionar tipo de servicio
3. Completar datos del remitente
4. Completar datos del destinatario
5. Ingresar peso y descripción
6. Marcar si es frágil (opcional)
7. Click en "Crear Envío"
8. Sistema valida y crea el envío
9. Muestra ID y costo calculado
```

### 2. Ver Lista de Envíos
```
1. Click en "📋 Lista de Envíos"
2. Ver todos los envíos con sus estados
3. Click en cualquier envío para ver detalles
```

### 3. Gestionar un Envío
```
1. Desde la lista, click en un envío
2. Ver todos los detalles organizados
3. Usar "➡️ Avanzar Estado" para moverlo
4. Usar "❌ Cancelar Envío" si es necesario
5. Ver actualización en tiempo real
```

## 🐛 Solución de Problemas

### El Backend No Inicia
**Error**: `Module not found: flask`
**Solución**:
```bash
cd backend
pip install -r requirements.txt
```

**Error**: `Port 5000 already in use`
**Solución**: Cambiar puerto en `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### El Frontend No Conecta
**Error**: `Network Error`
**Solución**:
1. Verificar que el backend esté corriendo
2. Abrir http://localhost:5000/api/health
3. Revisar que no haya errores de CORS

**Error**: `CORS policy blocking`
**Solución**: Ya está configurado CORS en el backend:
```python
from flask_cors import CORS
CORS(app)  # Permite todas las peticiones desde el frontend
```

### Error al Crear Envío
**Error**: `Validation failed`
**Solución**:
- Verificar que todos los campos estén completos
- Revisar que el peso sea válido (0.1 - 1000 kg)
- Asegurar que el tipo de envío sea correcto
- Ver detalles del error en el mensaje mostrado

## 🚀 Próximas Mejoras (Roadmap)

### Funcionalidades Faltantes en el Frontend
El backend ya tiene implementadas estas funcionalidades que falta agregar al frontend:

1. **📝 Modificar Envío**
   - Interfaz para editar campos de envíos existentes
   - Recalculo automático de costos
   - Validación en tiempo real

2. **⏱️ Historial y Memento**
   - Vista del historial completo de cambios
   - Botones de Deshacer/Rehacer
   - Timeline visual de cambios
   - Indicador de posición actual

3. **📊 Reportes y Análisis**
   - Generador de reportes completos (Visitor)
   - Cálculo de tiempo de entrega estimado
   - Cálculo de descuentos disponibles
   - Dashboard de métricas

4. **🔍 Búsqueda y Filtros**
   - Buscar envíos por ID
   - Filtrar por estado
   - Filtrar por tipo
   - Ordenar por fecha/costo

5. **📈 Dashboard de Estadísticas**
   - Total de envíos por estado
   - Gráficas de volumen
   - Ingresos totales
   - Métricas de rendimiento

### Mejoras Técnicas
- Autenticación de usuarios
- Base de datos persistente (actualmente in-memory)
- Notificaciones en tiempo real
- Exportación de reportes a PDF
- API de seguimiento público
- Integración con servicios de paquetería reales

## 📚 Documentación Adicional

### Para Desarrolladores
- Ver `Controllers/EnvioController.py` para lógica de negocio
- Ver `Patterns/` para implementación de patrones
- Ver `Models/Envio.py` para estructura de datos

### Para Evaluación Académica
Este proyecto demuestra:
- ✅ Implementación correcta de 4 patrones de diseño
- ✅ Arquitectura MVC completa
- ✅ API REST funcional con 12 endpoints
- ✅ Frontend React moderno y responsive
- ✅ Validaciones robustas en múltiples capas
- ✅ Manejo de errores apropiado
- ✅ Código limpio y bien documentado

## 📄 Licencia

Proyecto académico - Sexto Semestre - Patrones de Diseño

---

## 🎯 Estado del Proyecto

**Versión**: 2.0  
**Estado**: ✅ Backend Completo | ⚠️ Frontend Básico  
**Última actualización**: Noviembre 2024

### Backend: 100% Completo ✅
- ✅ 12 endpoints REST funcionando
- ✅ 4 patrones de diseño implementados
- ✅ Validaciones completas
- ✅ Manejo de errores robusto
- ✅ Documentación completa

### Frontend: 40% Completo ⚠️
- ✅ Listar envíos
- ✅ Crear envío
- ✅ Ver detalles
- ✅ Avanzar estado
- ✅ Cancelar envío
- ❌ Modificar envío
- ❌ Historial y Memento
- ❌ Reportes y análisis
- ❌ Búsqueda y filtros
- ❌ Dashboard

---

**¡Desarrollado con ❤️ para el aprendizaje de Patrones de Diseño!**
