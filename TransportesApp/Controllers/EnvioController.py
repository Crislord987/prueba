# Controllers/EnvioController.py
"""
Controlador principal que coordina todas las operaciones de envíos
Integra todos los patrones de diseño implementados
"""
import sys
import os

# Agregar el path del proyecto para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Models.Envio import Envio, EnvioExpress, EnvioEstandar, EnvioEconomico
from Patterns.ChainOfResponsibility import CadenaValidacion
from Patterns.State import GestorEstadoEnvio, EstadoPendiente
from Patterns.Memento import OriginadorEnvio
from Patterns.Visitor import CalculadorCosto, CalculadorTiempoEntrega, GeneradorReporte, CalculadorDescuento
from typing import List, Optional

class EnvioController:
    """
    Controlador que gestiona todas las operaciones relacionadas con envíos
    Implementa la lógica de negocio y coordina los patrones de diseño
    """
    
    def __init__(self):
        self.envios: List[Envio] = []
        self.originadores = {}  # Diccionario de originadores por ID de envío
        self.contador_envios = 1
    
    def crear_envio(self, tipo: str, remitente: str, destinatario: str,
                   direccion_origen: str, direccion_destino: str, 
                   peso: float, descripcion: str = "", es_fragil: bool = False) -> Optional[Envio]:
        """
        Crea un nuevo envío según el tipo especificado
        
        Args:
            tipo: "Express", "Estándar" o "Económico"
            remitente: Nombre del remitente
            destinatario: Nombre del destinatario
            direccion_origen: Dirección de origen
            direccion_destino: Dirección de destino
            peso: Peso en kilogramos
            descripcion: Descripción del paquete
            es_fragil: Si el paquete es frágil
            
        Returns:
            El envío creado o None si falla la validación
        """
        print(f"\n{'='*80}")
        print(f"CREANDO NUEVO ENVÍO")
        print(f"{'='*80}\n")
        
        # Generar ID único
        id_envio = f"ENV-{self.contador_envios:05d}"
        self.contador_envios += 1
        
        # Crear el envío según el tipo
        if tipo == "Express":
            envio = EnvioExpress(id_envio, remitente, destinatario, 
                               direccion_origen, direccion_destino, peso, descripcion)
        elif tipo == "Estándar":
            envio = EnvioEstandar(id_envio, remitente, destinatario,
                                direccion_origen, direccion_destino, peso, descripcion)
        elif tipo == "Económico":
            envio = EnvioEconomico(id_envio, remitente, destinatario,
                                 direccion_origen, direccion_destino, peso, descripcion)
        else:
            print(f"❌ Error: Tipo de envío '{tipo}' no válido")
            return None
        
        envio.es_fragil = es_fragil
        
        # PATRÓN CHAIN OF RESPONSIBILITY: Validar el envío
        es_valido, mensaje = CadenaValidacion.validar_envio(envio)
        
        if not es_valido:
            print(f"❌ No se pudo crear el envío: {mensaje}")
            return None
        
        # PATRÓN STATE: Inicializar el estado del envío
        GestorEstadoEnvio.inicializar_envio(envio)
        
        # PATRÓN VISITOR: Calcular costo inicial
        calculador = CalculadorCosto()
        envio.accept(calculador)
        
        # PATRÓN MEMENTO: Crear originador para historial
        originador = OriginadorEnvio(envio)
        self.originadores[id_envio] = originador
        
        # Agregar a la lista de envíos
        self.envios.append(envio)
        
        print(f"✅ Envío {id_envio} creado exitosamente")
        print(f"💰 Costo total: ${envio.costo:.2f}")
        
        return envio
    
    def obtener_envio(self, id_envio: str) -> Optional[Envio]:
        """Busca y retorna un envío por su ID"""
        for envio in self.envios:
            if envio.id_envio == id_envio:
                return envio
        return None
    
    def avanzar_estado_envio(self, id_envio: str) -> bool:
        """Avanza el envío al siguiente estado"""
        envio = self.obtener_envio(id_envio)
        if not envio:
            print(f"❌ Envío {id_envio} no encontrado")
            return False
        
        mensaje = GestorEstadoEnvio.avanzar_estado(envio)
        
        # Guardar cambio en el historial (Memento)
        if id_envio in self.originadores:
            estado_actual = envio.estado.get_descripcion()
            self.originadores[id_envio].crear_snapshot(f"Estado cambiado a: {estado_actual}")
        
        return True
    
    def consultar_estado_envio(self, id_envio: str) -> Optional[str]:
        """Consulta el estado actual de un envío"""
        envio = self.obtener_envio(id_envio)
        if not envio:
            print(f"❌ Envío {id_envio} no encontrado")
            return None
        
        return GestorEstadoEnvio.mostrar_estado_actual(envio)
    
    def cancelar_envio(self, id_envio: str) -> bool:
        """Cancela un envío"""
        envio = self.obtener_envio(id_envio)
        if not envio:
            print(f"❌ Envío {id_envio} no encontrado")
            return False
        
        mensaje = GestorEstadoEnvio.cancelar_envio(envio)
        print(mensaje)
        
        # Guardar cambio en el historial (Memento)
        if id_envio in self.originadores:
            self.originadores[id_envio].crear_snapshot("Envío cancelado")
        
        return True
    
    def modificar_envio(self, id_envio: str, campo: str, nuevo_valor) -> bool:
        """
        Modifica un campo del envío y guarda el cambio en el historial
        
        Args:
            id_envio: ID del envío
            campo: Campo a modificar ("remitente", "destinatario", "peso", etc.)
            nuevo_valor: Nuevo valor para el campo
        """
        if id_envio not in self.originadores:
            print(f"❌ Envío {id_envio} no encontrado")
            return False
        
        originador = self.originadores[id_envio]
        
        if campo == "remitente":
            originador.modificar_remitente(nuevo_valor)
        elif campo == "destinatario":
            originador.modificar_destinatario(nuevo_valor)
        elif campo == "peso":
            originador.modificar_peso(nuevo_valor)
        elif campo == "direccion_destino":
            originador.modificar_direccion_destino(nuevo_valor)
        elif campo == "fragil":
            originador.marcar_como_fragil(nuevo_valor)
        else:
            print(f"❌ Campo '{campo}' no reconocido")
            return False
        
        # Recalcular costo después de modificación
        envio = originador.envio
        calculador = CalculadorCosto()
        envio.accept(calculador)
        
        print(f"✅ Envío {id_envio} modificado exitosamente")
        return True
    
    def deshacer_cambio(self, id_envio: str) -> bool:
        """Deshace el último cambio realizado en un envío"""
        if id_envio not in self.originadores:
            print(f"❌ Envío {id_envio} no encontrado")
            return False
        
        resultado = self.originadores[id_envio].deshacer()
        
        if resultado:
            # Recalcular costo después de deshacer
            envio = self.originadores[id_envio].envio
            calculador = CalculadorCosto()
            envio.accept(calculador)
        
        return resultado
    
    def rehacer_cambio(self, id_envio: str) -> bool:
        """Rehace el último cambio deshecho en un envío"""
        if id_envio not in self.originadores:
            print(f"❌ Envío {id_envio} no encontrado")
            return False
        
        resultado = self.originadores[id_envio].rehacer()
        
        if resultado:
            # Recalcular costo después de rehacer
            envio = self.originadores[id_envio].envio
            calculador = CalculadorCosto()
            envio.accept(calculador)
        
        return resultado
    
    def mostrar_historial_envio(self, id_envio: str):
        """Muestra el historial de cambios de un envío"""
        if id_envio not in self.originadores:
            print(f"❌ Envío {id_envio} no encontrado")
            return
        
        self.originadores[id_envio].mostrar_historial()
    
    def calcular_tiempo_entrega(self, id_envio: str) -> Optional[int]:
        """Calcula el tiempo estimado de entrega de un envío"""
        envio = self.obtener_envio(id_envio)
        if not envio:
            print(f"❌ Envío {id_envio} no encontrado")
            return None
        
        calculador = CalculadorTiempoEntrega()
        dias = envio.accept(calculador)
        return dias
    
    def generar_reporte_envio(self, id_envio: str) -> Optional[str]:
        """Genera un reporte detallado de un envío"""
        envio = self.obtener_envio(id_envio)
        if not envio:
            print(f"❌ Envío {id_envio} no encontrado")
            return None
        
        generador = GeneradorReporte()
        reporte = envio.accept(generador)
        return reporte
    
    def calcular_descuentos(self, id_envio: str) -> Optional[float]:
        """Calcula los descuentos aplicables a un envío"""
        envio = self.obtener_envio(id_envio)
        if not envio:
            print(f"❌ Envío {id_envio} no encontrado")
            return None
        
        calculador = CalculadorDescuento()
        descuento = envio.accept(calculador)
        return descuento
    
    def listar_envios(self):
        """Lista todos los envíos registrados"""
        print(f"\n{'='*80}")
        print(f"LISTA DE ENVÍOS REGISTRADOS ({len(self.envios)} total)")
        print(f"{'='*80}\n")
        
        if not self.envios:
            print("No hay envíos registrados")
        else:
            for i, envio in enumerate(self.envios, 1):
                estado = envio.estado.get_descripcion() if envio.estado else "Sin estado"
                print(f"{i}. {envio.id_envio} | {envio.remitente} → {envio.destinatario}")
                print(f"   Tipo: {envio.tipo_envio} | Estado: {estado} | Costo: ${envio.costo:.2f}")
                print()
        
        print(f"{'='*80}\n")
    
    def get_total_envios(self) -> int:
        """Retorna el total de envíos registrados"""
        return len(self.envios)
