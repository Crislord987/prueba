# INSTRUCCIONES DE EJECUCIÓN

## 🚀 Cómo Ejecutar el Proyecto

### Requisitos Previos
- Python 3.8 o superior instalado
- Terminal o línea de comandos

### Pasos para Ejecutar

#### 1. Navegar al directorio del proyecto
```bash
cd "D:\Trabajos u\Sexto semestre\Patrones de diseño\Parcial 3\TransportesApp"
```

#### 2. Ejecutar la aplicación principal
```bash
python main.py
```

#### 3. Ejecutar el script de pruebas (opcional)
```bash
python test_patrones.py
```

---

## 📱 Uso de la Aplicación

### Aplicación Principal (main.py)

Al ejecutar `main.py`, verás un menú con 13 opciones:

1. **📦 Crear nuevo envío**
   - Ingresar tipo de servicio (Express/Estándar/Económico)
   - Proporcionar datos del remitente y destinatario
   - Especificar peso y características
   - El sistema valida automáticamente

2. **📋 Listar todos los envíos**
   - Muestra todos los envíos creados
   - Información resumida de cada uno

3. **🔍 Consultar estado de envío**
   - Ingresa el ID del envío (ejemplo: ENV-00001)
   - Muestra el estado actual detallado

4. **➡️ Avanzar estado de envío**
   - Ingresa el ID del envío
   - Avanza al siguiente estado en el ciclo de vida

5. **❌ Cancelar envío**
   - Ingresa el ID del envío
   - Confirma la cancelación
   - El envío pasa a estado "Cancelado"

6. **✏️ Modificar datos de envío**
   - Selecciona el campo a modificar
   - Ingresa el nuevo valor
   - El cambio se guarda en el historial

7. **↩️ Deshacer último cambio**
   - Revierte la última modificación
   - Usa el patrón Memento

8. **↪️ Rehacer cambio**
   - Recupera un cambio previamente deshecho

9. **📜 Ver historial de cambios**
   - Muestra todos los cambios realizados al envío
   - Navegación completa por el historial

10. **⏱️ Calcular tiempo de entrega**
    - Estima los días de entrega según tipo y distancia

11. **💰 Calcular descuentos**
    - Verifica descuentos aplicables por volumen o distancia

12. **📄 Generar reporte completo**
    - Crea un reporte detallado con toda la información

13. **🎯 Demostración completa de patrones**
    - Tutorial interactivo que muestra todos los patrones en acción
    - **¡RECOMENDADO PARA PRIMERA EJECUCIÓN!**

0. **🚪 Salir**
   - Cierra la aplicación

---

## 🧪 Script de Pruebas (test_patrones.py)

Este script ofrece pruebas individuales o completas de cada patrón:

### Menú de Pruebas

1. **Chain of Responsibility**: Prueba la validación de envíos
2. **State**: Prueba los cambios de estado
3. **Memento**: Prueba el historial y undo/redo
4. **Visitor**: Prueba los cálculos y reportes
5. **Integración Completa**: Prueba todos los patrones juntos
6. **Casos Borde**: Prueba validaciones límite
7. **Ejecutar TODAS**: Ejecuta todas las pruebas secuencialmente

---

## 💡 Ejemplos de Uso Rápido

### Ejemplo 1: Crear y Procesar un Envío Completo

1. Ejecutar: `python main.py`
2. Seleccionar opción `13` (Demostración completa)
3. Seguir las instrucciones interactivas
4. Observar cómo cada patrón se ejecuta

### Ejemplo 2: Crear un Envío Personalizado

1. Ejecutar: `python main.py`
2. Seleccionar opción `1` (Crear nuevo envío)
3. Elegir tipo: `1` (Express)
4. Ingresar datos:
   ```
   Remitente: Juan Pérez
   Dirección origen: Calle 100 #45-67, Bogotá
   Destinatario: María García
   Dirección destino: Carrera 50 #23-45, Medellín
   Peso: 25.5
   Descripción: Documentos importantes
   ¿Frágil?: s
   ```
5. El sistema mostrará el ID y costo del envío

### Ejemplo 3: Modificar y Ver Historial

1. Crear un envío (obtener el ID, ej: ENV-00001)
2. Seleccionar opción `6` (Modificar)
3. Ingresar ID: ENV-00001
4. Seleccionar campo: `3` (Peso)
5. Ingresar nuevo peso: 30
6. Seleccionar opción `9` (Ver historial)
7. Ingresar ID: ENV-00001
8. Ver todos los cambios realizados

### Ejemplo 4: Deshacer Cambios

1. Después de modificar un envío
2. Seleccionar opción `7` (Deshacer)
3. Ingresar ID del envío
4. El cambio se revierte automáticamente

---

## 🎓 Demostración Académica

Para presentar el proyecto en clase o evaluación:

### Opción A: Demostración Automática (Recomendada)
```bash
python main.py
# Seleccionar opción 13
# Seguir el tutorial interactivo
```

Esta opción muestra:
- Creación de envío con validación (Chain of Responsibility)
- Avance por todos los estados (State)
- Modificaciones con historial (Memento)
- Cálculos y reportes (Visitor)

### Opción B: Pruebas Individuales
```bash
python test_patrones.py
# Seleccionar prueba específica
```

### Opción C: Todas las Pruebas
```bash
python test_patrones.py
# Seleccionar opción 7
```

---

## 🔧 Solución de Problemas

### Error: "No se puede encontrar el módulo X"
**Solución**: Asegúrate de estar en el directorio correcto:
```bash
cd "D:\Trabajos u\Sexto semestre\Patrones de diseño\Parcial 3\TransportesApp"
```

### Error: "Python no se reconoce como comando"
**Solución**: Verifica la instalación de Python:
```bash
python --version
```
Si no funciona, intenta:
```bash
py main.py
```

### La aplicación se cierra inmediatamente
**Solución**: Ejecuta desde la terminal/CMD directamente, no haciendo doble clic al archivo.

---

## 📊 Flujo Recomendado de Demostración

1. **Inicio** (2 min)
   - Ejecutar main.py
   - Mostrar menú principal
   - Explicar arquitectura MVC

2. **Patrón Chain of Responsibility** (3 min)
   - Crear envío válido
   - Intentar crear envío inválido
   - Explicar la cadena de validadores

3. **Patrón State** (4 min)
   - Avanzar envío por estados
   - Mostrar transiciones
   - Demostrar cancelación

4. **Patrón Memento** (4 min)
   - Modificar envío varias veces
   - Mostrar historial
   - Hacer undo/redo

5. **Patrón Visitor** (4 min)
   - Calcular tiempo de entrega
   - Calcular descuentos
   - Generar reporte completo

6. **Cierre** (3 min)
   - Ejecutar demostración completa (opción 13)
   - Responder preguntas

**Tiempo total**: ~20 minutos

---

## 📝 Notas Importantes

1. **IDs de Envío**: Se generan automáticamente con formato ENV-XXXXX
2. **Estados**: Siguen secuencia predefinida (no se puede saltar estados)
3. **Historial**: Máximo 50 cambios guardados por envío
4. **Costos**: Se recalculan automáticamente tras modificaciones

---

## 🎯 Atajos y Tips

- Para salir rápido de cualquier menú: opción `0`
- Para ver todos los envíos: opción `2` desde menú principal
- Para prueba rápida completa: ejecutar `python test_patrones.py` → opción `7`
- Para demostración visual: `python main.py` → opción `13`

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que estás en el directorio correcto
2. Confirma que Python 3.8+ está instalado
3. Revisa que todos los archivos estén presentes
4. Consulta el archivo README.md para más detalles

---

**¡Listo para ejecutar! 🚀**

Comando rápido de inicio:
```bash
cd "D:\Trabajos u\Sexto semestre\Patrones de diseño\Parcial 3\TransportesApp" && python main.py
```
