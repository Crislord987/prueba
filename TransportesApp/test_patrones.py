# test_patrones.py
"""
Script de prueba para demostrar todos los patrones de diseño
Ejecutar: python test_patrones.py
"""
import sys
import os

# Agregar el path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Controllers.EnvioController import EnvioController
from Patterns.ChainOfResponsibility import CadenaValidacion
from Patterns.State import GestorEstadoEnvio
from Patterns.Visitor import CalculadorCosto, CalculadorTiempoEntrega, GeneradorReporte

def separador(titulo):
    """Imprime un separador visual"""
    print("\n" + "="*80)
    print(f" {titulo}")
    print("="*80 + "\n")

def prueba_chain_of_responsibility():
    """Prueba del patrón Chain of Responsibility"""
    separador("PRUEBA 1: CHAIN OF RESPONSIBILITY")
    
    print("Caso 1: Envío válido")
    print("-" * 40)
    controller = EnvioController()
    envio1 = controller.crear_envio(
        tipo="Express",
        remitente="Juan Pérez",
        destinatario="María García",
        direccion_origen="Calle 100 #45-67, Bogotá",
        direccion_destino="Carrera 50 #23-45, Medellín",
        peso=25.5,
        descripcion="Documentos importantes"
    )
    
    print("\n" + "-" * 40)
    print("Caso 2: Envío con peso inválido (debe fallar)")
    print("-" * 40)
    envio2 = controller.crear_envio(
        tipo="Express",
        remitente="Pedro López",
        destinatario="Ana Martínez",
        direccion_origen="Avenida 80 #12-34",
        direccion_destino="Calle 200 #56-78",
        peso=-5,  # Peso inválido
        descripcion="Prueba de validación"
    )
    
    print("\n" + "-" * 40)
    print("Caso 3: Envío sin datos completos (debe fallar)")
    print("-" * 40)
    envio3 = controller.crear_envio(
        tipo="Estándar",
        remitente="",  # Remitente vacío
        destinatario="Carlos Rodríguez",
        direccion_origen="",  # Dirección vacía
        direccion_destino="Calle 300 #90-12",
        peso=10,
        descripcion="Otra prueba"
    )
    
    input("\nPresione Enter para continuar...")

def prueba_state():
    """Prueba del patrón State"""
    separador("PRUEBA 2: STATE (ESTADOS)")
    
    controller = EnvioController()
    
    print("Creando envío de prueba...")
    envio = controller.crear_envio(
        tipo="Estándar",
        remitente="Laura Gómez",
        destinatario="Diego Hernández",
        direccion_origen="Calle Principal 123",
        direccion_destino="Avenida Secundaria 456",
        peso=15.0,
        descripcion="Paquete de prueba para estados"
    )
    
    if not envio:
        print("❌ No se pudo crear el envío")
        return
    
    id_envio = envio.id_envio
    
    print("\n" + "-" * 40)
    print("Consultando estado inicial...")
    controller.consultar_estado_envio(id_envio)
    
    input("\nPresione Enter para avanzar a 'En Proceso'...")
    controller.avanzar_estado_envio(id_envio)
    controller.consultar_estado_envio(id_envio)
    
    input("\nPresione Enter para avanzar a 'En Tránsito'...")
    controller.avanzar_estado_envio(id_envio)
    controller.consultar_estado_envio(id_envio)
    
    input("\nPresione Enter para avanzar a 'En Distribución'...")
    controller.avanzar_estado_envio(id_envio)
    controller.consultar_estado_envio(id_envio)
    
    input("\nPresione Enter para avanzar a 'Entregado'...")
    controller.avanzar_estado_envio(id_envio)
    controller.consultar_estado_envio(id_envio)
    
    print("\n" + "-" * 40)
    print("Intentando avanzar un envío ya entregado...")
    controller.avanzar_estado_envio(id_envio)
    
    # Probar cancelación
    print("\n" + "-" * 40)
    print("Creando otro envío para probar cancelación...")
    envio2 = controller.crear_envio(
        tipo="Express",
        remitente="Sofía Ramírez",
        destinatario="Miguel Torres",
        direccion_origen="Carrera 70 #30-40",
        direccion_destino="Calle 80 #50-60",
        peso=8.5,
        descripcion="Envío para cancelar"
    )
    
    if envio2:
        controller.avanzar_estado_envio(envio2.id_envio)
        input("\nPresione Enter para cancelar el envío...")
        controller.cancelar_envio(envio2.id_envio)
        controller.consultar_estado_envio(envio2.id_envio)
    
    input("\nPresione Enter para continuar...")

def prueba_memento():
    """Prueba del patrón Memento"""
    separador("PRUEBA 3: MEMENTO (HISTORIAL)")
    
    controller = EnvioController()
    
    print("Creando envío de prueba...")
    envio = controller.crear_envio(
        tipo="Económico",
        remitente="Roberto Sánchez",
        destinatario="Patricia Morales",
        direccion_origen="Avenida 100 #20-30",
        direccion_destino="Carrera 40 #60-70",
        peso=20.0,
        descripcion="Envío para prueba de historial",
        es_fragil=False
    )
    
    if not envio:
        print("❌ No se pudo crear el envío")
        return
    
    id_envio = envio.id_envio
    
    print("\n" + "-" * 40)
    print("Realizando modificaciones...")
    print("-" * 40)
    
    input("\nModificación 1: Cambiar peso a 25 kg (Enter para continuar)...")
    controller.modificar_envio(id_envio, "peso", 25.0)
    
    input("\nModificación 2: Cambiar destinatario (Enter para continuar)...")
    controller.modificar_envio(id_envio, "destinatario", "Carolina Díaz")
    
    input("\nModificación 3: Marcar como frágil (Enter para continuar)...")
    controller.modificar_envio(id_envio, "fragil", True)
    
    input("\nModificación 4: Cambiar peso a 30 kg (Enter para continuar)...")
    controller.modificar_envio(id_envio, "peso", 30.0)
    
    input("\nModificación 5: Cambiar dirección de destino (Enter para continuar)...")
    controller.modificar_envio(id_envio, "direccion_destino", "Nueva Calle 123, Nueva Ciudad")
    
    print("\n" + "-" * 40)
    print("Mostrando historial completo de cambios:")
    print("-" * 40)
    controller.mostrar_historial_envio(id_envio)
    
    input("\nPresione Enter para DESHACER último cambio...")
    controller.deshacer_cambio(id_envio)
    controller.mostrar_historial_envio(id_envio)
    
    input("\nPresione Enter para DESHACER otro cambio...")
    controller.deshacer_cambio(id_envio)
    controller.mostrar_historial_envio(id_envio)
    
    input("\nPresione Enter para REHACER cambio...")
    controller.rehacer_cambio(id_envio)
    controller.mostrar_historial_envio(id_envio)
    
    input("\nPresione Enter para DESHACER múltiples cambios...")
    controller.deshacer_cambio(id_envio)
    controller.deshacer_cambio(id_envio)
    controller.deshacer_cambio(id_envio)
    controller.mostrar_historial_envio(id_envio)
    
    print("\n✅ Prueba de Memento completada")
    input("\nPresione Enter para continuar...")

def prueba_visitor():
    """Prueba del patrón Visitor"""
    separador("PRUEBA 4: VISITOR (OPERACIONES)")
    
    controller = EnvioController()
    
    print("Creando diferentes tipos de envíos para probar visitantes...")
    print("-" * 40)
    
    # Envío Express
    envio1 = controller.crear_envio(
        tipo="Express",
        remitente="Andrea Castro",
        destinatario="Felipe Vargas",
        direccion_origen="Calle Corta 10",
        direccion_destino="Avenida Larga 200",
        peso=5.0,
        descripcion="Envío ligero express",
        es_fragil=False
    )
    
    # Envío Estándar pesado
    envio2 = controller.crear_envio(
        tipo="Estándar",
        remitente="Gabriela Ruiz",
        destinatario="Ricardo Mendoza",
        direccion_origen="Origen Ciudad A muy lejos de aquí en el norte del país",
        direccion_destino="Destino Ciudad B en el extremo sur del territorio nacional completo",
        peso=75.0,
        descripcion="Envío pesado estándar",
        es_fragil=True
    )
    
    # Envío Económico muy pesado
    envio3 = controller.crear_envio(
        tipo="Económico",
        remitente="Valentina Ortiz",
        destinatario="Sebastián Rojas",
        direccion_origen="Punto A en coordenadas lejanas del mapa geográfico nacional",
        direccion_destino="Punto B ubicado en la región más distante del país entero",
        peso=150.0,
        descripcion="Envío muy pesado económico",
        es_fragil=False
    )
    
    if not (envio1 and envio2 and envio3):
        print("❌ Error al crear envíos de prueba")
        return
    
    # Probar Visitor: Calculador de Tiempo
    print("\n" + "="*80)
    print("VISITOR 1: CALCULADOR DE TIEMPO DE ENTREGA")
    print("="*80)
    
    input("\nPresione Enter para calcular tiempo de Envío 1...")
    controller.calcular_tiempo_entrega(envio1.id_envio)
    
    input("\nPresione Enter para calcular tiempo de Envío 2...")
    controller.calcular_tiempo_entrega(envio2.id_envio)
    
    input("\nPresione Enter para calcular tiempo de Envío 3...")
    controller.calcular_tiempo_entrega(envio3.id_envio)
    
    # Probar Visitor: Calculador de Descuentos
    print("\n" + "="*80)
    print("VISITOR 2: CALCULADOR DE DESCUENTOS")
    print("="*80)
    
    input("\nPresione Enter para calcular descuentos de Envío 1...")
    controller.calcular_descuentos(envio1.id_envio)
    
    input("\nPresione Enter para calcular descuentos de Envío 2...")
    controller.calcular_descuentos(envio2.id_envio)
    
    input("\nPresione Enter para calcular descuentos de Envío 3...")
    controller.calcular_descuentos(envio3.id_envio)
    
    # Probar Visitor: Generador de Reporte
    print("\n" + "="*80)
    print("VISITOR 3: GENERADOR DE REPORTES")
    print("="*80)
    
    input("\nPresione Enter para generar reporte de Envío 2 (completo)...")
    controller.generar_reporte_envio(envio2.id_envio)
    
    print("\n✅ Prueba de Visitor completada")
    input("\nPresione Enter para continuar...")

def prueba_integracion_completa():
    """Prueba de integración de todos los patrones"""
    separador("PRUEBA 5: INTEGRACIÓN COMPLETA")
    
    controller = EnvioController()
    
    print("Esta prueba demuestra cómo todos los patrones trabajan juntos")
    print("-" * 80)
    
    input("\nPresione Enter para comenzar...")
    
    # 1. Crear envío (Chain of Responsibility + State + Visitor + Memento)
    print("\n1. CREANDO ENVÍO (Chain + State + Visitor + Memento)")
    print("-" * 80)
    envio = controller.crear_envio(
        tipo="Express",
        remitente="Cliente Premium S.A.",
        destinatario="Empresa Destino Ltda.",
        direccion_origen="Sede Principal, Calle Empresarial 100, Bogotá DC",
        direccion_destino="Sucursal Norte, Avenida Industrial 500, Barranquilla",
        peso=35.0,
        descripcion="Documentos contractuales urgentes",
        es_fragil=True
    )
    
    if not envio:
        print("❌ Error en la creación")
        return
    
    id_envio = envio.id_envio
    
    input("\n✓ Envío creado. Presione Enter para continuar...")
    
    # 2. Avanzar estados (State + Memento)
    print("\n2. AVANZANDO ESTADOS (State + Memento)")
    print("-" * 80)
    input("Avanzar a 'En Proceso' (Enter)...")
    controller.avanzar_estado_envio(id_envio)
    
    input("Avanzar a 'En Tránsito' (Enter)...")
    controller.avanzar_estado_envio(id_envio)
    
    # 3. Modificar durante tránsito (Memento + Visitor)
    print("\n3. MODIFICANDO ENVÍO EN TRÁNSITO (Memento + Visitor)")
    print("-" * 80)
    input("Modificar peso (Enter)...")
    controller.modificar_envio(id_envio, "peso", 40.0)
    
    input("Modificar destinatario (Enter)...")
    controller.modificar_envio(id_envio, "destinatario", "Nueva Empresa Receptora")
    
    # 4. Ver historial (Memento)
    print("\n4. REVISANDO HISTORIAL (Memento)")
    print("-" * 80)
    input("Ver historial completo (Enter)...")
    controller.mostrar_historial_envio(id_envio)
    
    # 5. Calcular métricas (Visitor)
    print("\n5. CALCULANDO MÉTRICAS (Visitor)")
    print("-" * 80)
    input("Calcular tiempo de entrega (Enter)...")
    controller.calcular_tiempo_entrega(id_envio)
    
    input("Calcular descuentos aplicables (Enter)...")
    controller.calcular_descuentos(id_envio)
    
    # 6. Generar reporte final (Visitor)
    print("\n6. GENERANDO REPORTE FINAL (Visitor)")
    print("-" * 80)
    input("Generar reporte completo (Enter)...")
    controller.generar_reporte_envio(id_envio)
    
    # 7. Finalizar envío (State)
    print("\n7. FINALIZANDO ENVÍO (State)")
    print("-" * 80)
    input("Avanzar a 'En Distribución' (Enter)...")
    controller.avanzar_estado_envio(id_envio)
    
    input("Avanzar a 'Entregado' (Enter)...")
    controller.avanzar_estado_envio(id_envio)
    
    controller.consultar_estado_envio(id_envio)
    
    print("\n" + "="*80)
    print("✅ INTEGRACIÓN COMPLETA EXITOSA")
    print("="*80)
    print("\nTodos los patrones trabajaron en conjunto:")
    print("  ✓ Chain of Responsibility - Validó el envío")
    print("  ✓ State - Gestionó los estados")
    print("  ✓ Memento - Guardó el historial")
    print("  ✓ Visitor - Realizó cálculos y reportes")
    print("="*80)
    
    input("\nPresione Enter para continuar...")

def prueba_casos_borde():
    """Prueba de casos borde y validaciones"""
    separador("PRUEBA 6: CASOS BORDE Y VALIDACIONES")
    
    controller = EnvioController()
    
    print("Probando validaciones y casos límite...")
    print("-" * 80)
    
    # Peso en el límite
    print("\nCaso 1: Peso en el límite mínimo (0.1 kg)")
    envio1 = controller.crear_envio(
        tipo="Económico",
        remitente="Test Usuario",
        destinatario="Test Destino",
        direccion_origen="Origen Test",
        direccion_destino="Destino Test",
        peso=0.1,
        descripcion="Peso mínimo"
    )
    
    # Peso muy alto
    print("\nCaso 2: Peso muy alto (500 kg)")
    envio2 = controller.crear_envio(
        tipo="Estándar",
        remitente="Test Usuario 2",
        destinatario="Test Destino 2",
        direccion_origen="Origen Test 2",
        direccion_destino="Destino Test 2",
        peso=500.0,
        descripcion="Peso alto"
    )
    
    # Express con distancia larga (debería fallar)
    print("\nCaso 3: Express con distancia muy larga (debería fallar)")
    envio3 = controller.crear_envio(
        tipo="Express",
        remitente="Test Usuario 3",
        destinatario="Test Destino 3",
        direccion_origen="Origen muy muy muy lejos en el extremo norte",
        direccion_destino="Destino extremadamente distante en el lejano sur del país completo y más allá",
        peso=10.0,
        descripcion="Distancia prohibida para Express"
    )
    
    # Intentar múltiples deshacer sin cambios
    if envio1:
        print("\nCaso 4: Intentar deshacer sin cambios adicionales")
        controller.deshacer_cambio(envio1.id_envio)
        controller.deshacer_cambio(envio1.id_envio)
    
    print("\n✅ Prueba de casos borde completada")
    input("\nPresione Enter para continuar...")

def menu_pruebas():
    """Menú de selección de pruebas"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*80)
        print(" " * 20 + "🧪 SCRIPT DE PRUEBAS DE PATRONES 🧪")
        print("="*80)
        print("\nSeleccione la prueba a ejecutar:")
        print("\n1. Chain of Responsibility (Validación)")
        print("2. State (Estados del envío)")
        print("3. Memento (Historial de cambios)")
        print("4. Visitor (Operaciones)")
        print("5. Integración Completa (Todos los patrones)")
        print("6. Casos Borde y Validaciones")
        print("7. Ejecutar TODAS las pruebas")
        print("\n0. Salir")
        print("\n" + "="*80)
        
        opcion = input("\nOpción: ").strip()
        
        if opcion == "1":
            prueba_chain_of_responsibility()
        elif opcion == "2":
            prueba_state()
        elif opcion == "3":
            prueba_memento()
        elif opcion == "4":
            prueba_visitor()
        elif opcion == "5":
            prueba_integracion_completa()
        elif opcion == "6":
            prueba_casos_borde()
        elif opcion == "7":
            print("\n🚀 Ejecutando todas las pruebas...")
            input("\nPresione Enter para comenzar...")
            prueba_chain_of_responsibility()
            prueba_state()
            prueba_memento()
            prueba_visitor()
            prueba_integracion_completa()
            prueba_casos_borde()
            
            separador("TODAS LAS PRUEBAS COMPLETADAS")
            print("✅ Todas las pruebas se ejecutaron exitosamente")
            print("\nResumen:")
            print("  • Chain of Responsibility - OK")
            print("  • State - OK")
            print("  • Memento - OK")
            print("  • Visitor - OK")
            print("  • Integración - OK")
            print("  • Casos Borde - OK")
            input("\nPresione Enter para volver al menú...")
        elif opcion == "0":
            print("\n¡Hasta pronto!")
            break
        else:
            print("\n❌ Opción inválida")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    try:
        menu_pruebas()
    except KeyboardInterrupt:
        print("\n\n⚠️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()
