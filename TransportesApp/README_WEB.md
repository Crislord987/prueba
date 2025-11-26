# 🚚 Sistema de Gestión de Transportes y Envíos - Versión Web

Sistema completo de gestión de transportes implementando patrones de diseño de comportamiento con arquitectura web moderna (Backend Flask + Frontend React).

## 📋 Patrones de Diseño Implementados

### 1. **Chain of Responsibility**
Valida los envíos a través de una cadena de validadores:
- Validador de Datos
- Validador de Peso
- Validador de Tipo
- Validador de Distancia
- Validador de Seguridad

### 2. **State**
Gestiona los estados del envío:
- Pendiente → En Proceso → En Tránsito → En Distribución → Entregado
- Permite cancelación desde cualquier estado antes de entrega

### 3. **Memento**
Mantiene un historial completo de cambios del envío:
- Guarda snapshots de cada modificación
- Permite deshacer/rehacer cambios
- Historial navegable

### 4. **Visitor**
Aplica diferentes operaciones sobre los envíos:
- Cálculo de costos
- Cálculo de tiempo de entrega
- Generación de reportes
- Cálculo de descuentos

## 🏗️ Arquitectura

```
TransportesApp/
├── backend/              # API REST con Flask
│   ├── app.py           # Servidor principal
│   └── requirements.txt # Dependencias Python
├── frontend/            # Aplicación React
│   ├── public/         # Archivos estáticos
│   ├── src/            # Código fuente React
│   └── package.json    # Dependencias Node
├── Controllers/        # Lógica de negocio
├── Models/             # Modelos de datos
├── Patterns/           # Patrones de diseño
└── README.md
```

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- Node.js 16 o superior
- pip (gestor de paquetes Python)
- npm o yarn (gestor de paquetes Node)

### 1. Configurar Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual (opcional pero recomendado)
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

### 2. Configurar Frontend

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

## 📱 Uso de la Aplicación

### Crear un Envío
1. Click en "📦 Crear Envío"
2. Completar el formulario:
   - Tipo de envío (Express, Estándar, Económico)
   - Datos del remitente y destinatario
   - Direcciones de origen y destino
   - Peso del paquete
   - Descripción (opcional)
   - Marcar si es frágil
3. Click en "Crear Envío"

### Ver Lista de Envíos
1. Click en "📋 Lista de Envíos"
2. Ver todos los envíos con sus estados
3. Click en cualquier envío para ver detalles

### Gestionar Envío
Desde los detalles de un envío puedes:
- **Avanzar Estado**: Mover el envío al siguiente estado
- **Cancelar Envío**: Cancelar el envío (si no está entregado)
- Ver información completa del envío

## 🔧 API REST Endpoints

### Envíos
- `GET /api/envios` - Listar todos los envíos
- `POST /api/envios` - Crear nuevo envío
- `GET /api/envios/<id>` - Obtener envío específico
- `GET /api/envios/<id>/estado` - Consultar estado
- `POST /api/envios/<id>/avanzar` - Avanzar estado
- `POST /api/envios/<id>/cancelar` - Cancelar envío
- `PUT /api/envios/<id>/modificar` - Modificar envío
- `GET /api/envios/<id>/historial` - Ver historial
- `POST /api/envios/<id>/deshacer` - Deshacer cambio
- `POST /api/envios/<id>/rehacer` - Rehacer cambio
- `GET /api/envios/<id>/tiempo-entrega` - Calcular tiempo
- `GET /api/envios/<id>/descuentos` - Calcular descuentos
- `GET /api/envios/<id>/reporte` - Generar reporte

### Health Check
- `GET /api/health` - Verificar estado del servidor

## 🎨 Características de la Interfaz

- **Diseño Moderno**: Interfaz atractiva con gradientes y animaciones
- **Responsive**: Adaptable a móviles, tablets y desktop
- **Feedback Visual**: Mensajes claros de éxito/error
- **Estados con Colores**: Cada estado tiene su propio color distintivo
- **Carga Dinámica**: Spinners de carga para mejor UX
- **Validación de Formularios**: Validación en tiempo real

## 📊 Estados de Envío

| Estado | Color | Descripción |
|--------|-------|-------------|
| Pendiente de validación | Amarillo | Envío registrado, en validación |
| En proceso de preparación | Azul | Preparando empaque y documentación |
| En tránsito hacia destino | Morado | En camino al centro de distribución |
| En distribución local | Rosa | En reparto final |
| Entregado exitosamente | Verde | Entregado al destinatario |
| Cancelado | Naranja | Envío cancelado |

## 🔒 Validaciones

El sistema valida automáticamente:
- Peso: entre 0.1 kg y 1000 kg
- Datos completos de remitente y destinatario
- Direcciones válidas
- Tipo de envío correcto
- Distancia según tipo de envío
- Requisitos de seguro

## 💰 Cálculo de Costos

El costo se calcula considerando:
- **Tarifa base** por kg según tipo de envío
- **Distancia** del envío
- **Recargo por peso** si supera 50 kg
- **Recargo por frágil** si aplica
- **Recargo por seguro** (2% del costo)
- **Descuentos** por volumen o distancia

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask**: Framework web ligero de Python
- **Flask-CORS**: Manejo de CORS para API REST
- **Python 3**: Lenguaje de programación

### Frontend
- **React 18**: Framework de JavaScript
- **Axios**: Cliente HTTP para peticiones
- **CSS3**: Estilos personalizados con animaciones
- **JavaScript ES6+**: Programación moderna

## 📝 Diferencias con la Versión de Consola

### Eliminado
- ❌ `main.py` - Punto de entrada de consola
- ❌ `test_patrones.py` - Tests de consola
- ❌ `Views/ConsoleView.py` - Vista de consola
- ❌ Todos los archivos `__pycache__`

### Agregado
- ✅ `backend/app.py` - API REST
- ✅ `frontend/` - Aplicación React completa
- ✅ Interfaz web moderna y responsive
- ✅ Sistema de mensajes en tiempo real
- ✅ Carga dinámica sin refrescar página

## 🐛 Solución de Problemas

### El backend no inicia
- Verificar que Python 3.8+ está instalado
- Asegurarse de que el puerto 5000 no está en uso
- Verificar que las dependencias están instaladas

### El frontend no conecta con el backend
- Verificar que el backend está corriendo en puerto 5000
- Revisar la consola del navegador para errores CORS
- Asegurarse de que ambos servidores están corriendo

### Error al crear envío
- Verificar que todos los campos requeridos están completos
- Comprobar que el peso es un número válido
- Ver la consola del navegador para más detalles

## 👨‍💻 Desarrollo

Para desarrollo, ambos servidores deben estar corriendo simultáneamente:
1. Terminal 1: Backend (puerto 5000)
2. Terminal 2: Frontend (puerto 3000)

Los cambios en el frontend se reflejan automáticamente (Hot Reload).
Los cambios en el backend requieren reiniciar el servidor.

## 📄 Licencia

Proyecto académico - Sexto Semestre - Patrones de Diseño

---

**¡Desarrollado con ❤️ para el aprendizaje de Patrones de Diseño!**
