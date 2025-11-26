# Views/ConsoleView.py
"""
Vista de consola para la aplicación de transportes
Implementa la interfaz de usuario en modo texto
"""
import os
import sys

# Agregar el path del proyecto para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.EnvioController import EnvioController

class ConsoleView:
    """Clase que maneja la interfaz de usuario por consola"""
    
    def __init__(self):
        self.controller = EnvioController()
        self.ejecutando = True
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        """Pausa la ejecución hasta que el usuario presione Enter"""
        input("\nPresione Enter para continuar...")
    
    def mostrar_encabezado(self):
        """Muestra el encabezado de la aplicación"""
        print("\n" + "="*80)
        print(" " * 15 + "🚚 SISTEMA DE GESTIÓN DE TRANSPORTES Y ENVÍOS 🚚")
        print("="*80)
        print(" " * 20 + "Implementación de Patrones de Diseño")
        print("="*80 + "\n")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de opciones"""
        print("\n" + "─"*80)
        print("MENÚ PRINCIPAL")
        print("─"*80)
        print("1.  📦 Crear nuevo envío")
        print("2.  📋 Listar todos los envíos")
        print("3.  🔍 Consultar estado de envío")
        print("4.  ➡️  Avanzar estado de envío")
        print("5.  ❌ Cancelar envío")
        print("6.  ✏️  Modificar datos de envío")
        print("7.  ↩️  Deshacer último cambio")
        print("8.  ↪️  Rehacer cambio")
        print("9.  📜 Ver historial de cambios")
        print("10. ⏱️  Calcular tiempo de entrega")
        print("11. 💰 Calcular descuentos")
        print("12. 📄 Generar reporte completo")
        print("13. 🎯 Demostración completa de patrones")
        print("0.  🚪 Salir")
        print("─"*80)
    
    def solicitar_datos_envio(self) -> dict:
        """Solicita los datos necesarios para crear un envío"""
        print("\n" + "─"*80)
        print("CREAR NUEVO ENVÍO")
        print("─"*80 + "\n")
        
        print("Tipos de envío disponibles:")
        print("1. Express (Entrega en 24 horas)")
        print("2. Estándar (Entrega en 3-5 días)")
        print("3. Económico (Entrega en 7-10 días)")
        
        tipo_opcion = input("\nSeleccione tipo de envío (1-3): ").strip()
        
        tipos = {
            "1": "Express",
            "2": "Estándar",
            "3": "Económico"
        }
        
        tipo = tipos.get(tipo_opcion, "Estándar")
        
        print(f"\n📦 Tipo seleccionado: {tipo}\n")
        
        remitente = input("Nombre del remitente: ").strip()
        direccion_origen = input("Dirección de origen: ").strip()
        
        destinatario = input("Nombre del destinatario: ").strip()
        direccion_destino = input("Dirección de destino: ").strip()
        
        while True:
            try:
                peso = float(input("Peso del paquete (kg): ").strip())
                if peso <= 0:
                    print("⚠️  El peso debe ser mayor a 0")
                    continue
                break
            except ValueError:
                print("⚠️  Por favor ingrese un número válido")
        
        descripcion = input("Descripción del contenido (opcional): ").strip()
        
        es_fragil_input = input("¿El paquete es frágil? (s/n): ").strip().lower()
        es_fragil = es_fragil_input == 's'
        
        return {
            'tipo': tipo,
            'remitente': remitente,
            'destinatario': destinatario,
            'direccion_origen': direccion_origen,
            'direccion_destino': direccion_destino,
            'peso': peso,
            'descripcion': descripcion,
            'es_fragil': es_fragil
        }
    
    def crear_envio(self):
        """Opción 1: Crear un nuevo envío"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        datos = self.solicitar_datos_envio()
        
        envio = self.controller.crear_envio(
            tipo=datos['tipo'],
            remitente=datos['remitente'],
            destinatario=datos['destinatario'],
            direccion_origen=datos['direccion_origen'],
            direccion_destino=datos['direccion_destino'],
            peso=datos['peso'],
            descripcion=datos['descripcion'],
            es_fragil=datos['es_fragil']
        )
        
        if envio:
            print(f"\n✅ ¡Envío creado exitosamente!")
            print(f"ID del envío: {envio.id_envio}")
            print(f"Costo total: ${envio.costo:.2f}")
        
        self.pausar()
    
    def listar_envios(self):
        """Opción 2: Listar todos los envíos"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        self.controller.listar_envios()
        
        self.pausar()
    
    def consultar_estado(self):
        """Opción 3: Consultar estado de un envío"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.consultar_estado_envio(id_envio)
        
        self.pausar()
    
    def avanzar_estado(self):
        """Opción 4: Avanzar el estado de un envío"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.avanzar_estado_envio(id_envio)
        
        self.pausar()
    
    def cancelar_envio(self):
        """Opción 5: Cancelar un envío"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío a cancelar: ").strip()
        
        confirmacion = input(f"¿Está seguro de cancelar el envío {id_envio}? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            self.controller.cancelar_envio(id_envio)
        else:
            print("Cancelación abortada")
        
        self.pausar()
    
    def modificar_envio(self):
        """Opción 6: Modificar datos de un envío"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        print("\nCampos modificables:")
        print("1. Remitente")
        print("2. Destinatario")
        print("3. Peso")
        print("4. Dirección de destino")
        print("5. Marcar/desmarcar como frágil")
        
        opcion = input("\nSeleccione el campo a modificar (1-5): ").strip()
        
        campos = {
            "1": "remitente",
            "2": "destinatario",
            "3": "peso",
            "4": "direccion_destino",
            "5": "fragil"
        }
        
        campo = campos.get(opcion)
        
        if not campo:
            print("❌ Opción inválida")
            self.pausar()
            return
        
        if campo == "peso":
            try:
                nuevo_valor = float(input("Ingrese el nuevo peso (kg): ").strip())
            except ValueError:
                print("❌ Valor inválido")
                self.pausar()
                return
        elif campo == "fragil":
            respuesta = input("¿Marcar como frágil? (s/n): ").strip().lower()
            nuevo_valor = respuesta == 's'
        else:
            nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ").strip()
        
        self.controller.modificar_envio(id_envio, campo, nuevo_valor)
        
        self.pausar()
    
    def deshacer_cambio(self):
        """Opción 7: Deshacer último cambio"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.deshacer_cambio(id_envio)
        
        self.pausar()
    
    def rehacer_cambio(self):
        """Opción 8: Rehacer cambio"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.rehacer_cambio(id_envio)
        
        self.pausar()
    
    def ver_historial(self):
        """Opción 9: Ver historial de cambios"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.mostrar_historial_envio(id_envio)
        
        self.pausar()
    
    def calcular_tiempo_entrega(self):
        """Opción 10: Calcular tiempo de entrega"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.calcular_tiempo_entrega(id_envio)
        
        self.pausar()
    
    def calcular_descuentos(self):
        """Opción 11: Calcular descuentos"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.calcular_descuentos(id_envio)
        
        self.pausar()
    
    def generar_reporte(self):
        """Opción 12: Generar reporte completo"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        id_envio = input("Ingrese el ID del envío: ").strip()
        
        self.controller.generar_reporte_envio(id_envio)
        
        self.pausar()
    
    def demostracion_completa(self):
        """Opción 13: Demostración completa de todos los patrones"""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        
        print("🎯 DEMOSTRACIÓN COMPLETA DE PATRONES DE DISEÑO\n")
        print("Esta demostración creará un envío y mostrará todos los patrones en acción\n")
        
        self.pausar()
        
        # Crear envío de ejemplo
        print("\n" + "="*80)
        print("PASO 1: CREANDO ENVÍO DE DEMOSTRACIÓN")
        print("="*80 + "\n")
        
        envio = self.controller.crear_envio(
            tipo="Express",
            remitente="Juan Pérez",
            destinatario="María García",
            direccion_origen="Calle Principal 123, Bogotá",
            direccion_destino="Avenida Libertador 456, Medellín",
            peso=25.5,
            descripcion="Documentos importantes",
            es_fragil=True
        )
        
        if not envio:
            print("❌ No se pudo crear el envío de demostración")
            self.pausar()
            return
        
        id_envio = envio.id_envio
        
        self.pausar()
        
        # Demostrar Chain of Responsibility (ya ejecutado en la creación)
        print("\n" + "="*80)
        print("✅ PATRÓN 1: CHAIN OF RESPONSIBILITY")
        print("="*80)
        print("El envío pasó por una cadena de validadores:")
        print("  • Validador de Datos")
        print("  • Validador de Peso")
        print("  • Validador de Tipo")
        print("  • Validador de Distancia")
        print("  • Validador de Seguridad")
        
        self.pausar()
        
        # Demostrar State
        print("\n" + "="*80)
        print("✅ PATRÓN 2: STATE")
        print("="*80)
        print("\nAvanzando el envío por diferentes estados:\n")
        
        self.controller.consultar_estado_envio(id_envio)
        self.pausar()
        
        print("\nAvanzando a En Proceso...")
        self.controller.avanzar_estado_envio(id_envio)
        self.pausar()
        
        print("\nAvanzando a En Tránsito...")
        self.controller.avanzar_estado_envio(id_envio)
        self.pausar()
        
        # Demostrar Memento
        print("\n" + "="*80)
        print("✅ PATRÓN 3: MEMENTO")
        print("="*80)
        print("\nModificando el envío y guardando cambios:\n")
        
        print("Modificación 1: Cambiando peso...")
        self.controller.modificar_envio(id_envio, "peso", 30.0)
        self.pausar()
        
        print("\nModificación 2: Cambiando destinatario...")
        self.controller.modificar_envio(id_envio, "destinatario", "Carlos Rodríguez")
        self.pausar()
        
        print("\nMostrando historial completo de cambios:")
        self.controller.mostrar_historial_envio(id_envio)
        self.pausar()
        
        print("\nDeshaciendo último cambio...")
        self.controller.deshacer_cambio(id_envio)
        self.pausar()
        
        print("\nRehaciendo cambio...")
        self.controller.rehacer_cambio(id_envio)
        self.pausar()
        
        # Demostrar Visitor
        print("\n" + "="*80)
        print("✅ PATRÓN 4: VISITOR")
        print("="*80)
        print("\nAplicando diferentes visitantes al envío:\n")
        
        print("Visitor 1: Calculador de Costo")
        self.controller.calcular_descuentos(id_envio)
        self.pausar()
        
        print("\nVisitor 2: Calculador de Tiempo de Entrega")
        self.controller.calcular_tiempo_entrega(id_envio)
        self.pausar()
        
        print("\nVisitor 3: Generador de Reporte")
        self.controller.generar_reporte_envio(id_envio)
        self.pausar()
        
        print("\n" + "="*80)
        print("✅ ¡DEMOSTRACIÓN COMPLETA FINALIZADA!")
        print("="*80)
        print("\nSe han demostrado los 4 patrones de comportamiento:")
        print("  1. Chain of Responsibility - Validación de envíos")
        print("  2. State - Gestión de estados del envío")
        print("  3. Memento - Historial de cambios")
        print("  4. Visitor - Operaciones sobre envíos")
        print("\n" + "="*80 + "\n")
        
        self.pausar()
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación"""
        while self.ejecutando:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_menu_principal()
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.crear_envio()
            elif opcion == "2":
                self.listar_envios()
            elif opcion == "3":
                self.consultar_estado()
            elif opcion == "4":
                self.avanzar_estado()
            elif opcion == "5":
                self.cancelar_envio()
            elif opcion == "6":
                self.modificar_envio()
            elif opcion == "7":
                self.deshacer_cambio()
            elif opcion == "8":
                self.rehacer_cambio()
            elif opcion == "9":
                self.ver_historial()
            elif opcion == "10":
                self.calcular_tiempo_entrega()
            elif opcion == "11":
                self.calcular_descuentos()
            elif opcion == "12":
                self.generar_reporte()
            elif opcion == "13":
                self.demostracion_completa()
            elif opcion == "0":
                self.ejecutando = False
                self.limpiar_pantalla()
                print("\n" + "="*80)
                print(" " * 25 + "¡Gracias por usar el sistema!")
                print("="*80 + "\n")
            else:
                print("\n❌ Opción inválida. Por favor intente nuevamente.")
                self.pausar()


# Punto de entrada de la aplicación
if __name__ == "__main__":
    vista = ConsoleView()
    vista.ejecutar()
