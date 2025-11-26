# Patterns/State.py
"""
Patrón State para gestionar los diferentes estados de un envío
Estados: Pendiente -> En Proceso -> En Tránsito -> En Distribución -> Entregado
También puede pasar a Cancelado desde cualquier estado antes de Entregado
"""
from abc import ABC, abstractmethod
from datetime import datetime

class EstadoEnvio(ABC):
    """Clase base abstracta para los estados del envío"""
    
    @abstractmethod
    def procesar(self, envio):
        """Procesa el envío en el estado actual"""
        pass
    
    @abstractmethod
    def siguiente(self, envio):
        """Avanza al siguiente estado"""
        pass
    
    @abstractmethod
    def cancelar(self, envio):
        """Cancela el envío"""
        pass
    
    @abstractmethod
    def get_descripcion(self) -> str:
        """Retorna la descripción del estado"""
        pass


class EstadoPendiente(EstadoEnvio):
    """Estado inicial: el envío ha sido registrado pero no procesado"""
    
    def procesar(self, envio):
        print(f"📋 Envío {envio.id_envio} está PENDIENTE de validación")
        return "El envío ha sido registrado y está pendiente de validación"
    
    def siguiente(self, envio):
        print(f"🔄 Cambiando estado: Pendiente → En Proceso")
        envio.estado = EstadoEnProceso()
        return "Envío pasado a procesamiento"
    
    def cancelar(self, envio):
        print(f"❌ Cancelando envío desde estado Pendiente")
        envio.estado = EstadoCancelado()
        return "Envío cancelado desde estado Pendiente"
    
    def get_descripcion(self) -> str:
        return "Pendiente de validación"


class EstadoEnProceso(EstadoEnvio):
    """El envío está siendo procesado y preparado"""
    
    def procesar(self, envio):
        print(f"⚙️ Envío {envio.id_envio} está EN PROCESO")
        print(f"   - Verificando documentación")
        print(f"   - Preparando empaque")
        print(f"   - Asignando ruta de entrega")
        return "El envío está siendo procesado y preparado para transporte"
    
    def siguiente(self, envio):
        print(f"🔄 Cambiando estado: En Proceso → En Tránsito")
        envio.estado = EstadoEnTransito()
        return "Envío despachado y en tránsito"
    
    def cancelar(self, envio):
        print(f"❌ Cancelando envío desde estado En Proceso")
        envio.estado = EstadoCancelado()
        return "Envío cancelado durante el procesamiento"
    
    def get_descripcion(self) -> str:
        return "En proceso de preparación"


class EstadoEnTransito(EstadoEnvio):
    """El envío está en camino al destino"""
    
    def procesar(self, envio):
        print(f"🚚 Envío {envio.id_envio} está EN TRÁNSITO")
        print(f"   - Ubicación actual: En ruta")
        print(f"   - Distancia aproximada: {envio.distancia} km")
        print(f"   - Tipo de servicio: {envio.tipo_envio}")
        return "El envío está en camino al centro de distribución de destino"
    
    def siguiente(self, envio):
        print(f"🔄 Cambiando estado: En Tránsito → En Distribución")
        envio.estado = EstadoEnDistribucion()
        return "Envío llegó al centro de distribución"
    
    def cancelar(self, envio):
        print(f"⚠️ Envío en tránsito - se requiere coordinación especial para cancelar")
        envio.estado = EstadoCancelado()
        return "Envío cancelado - se realizará devolución al origen"
    
    def get_descripcion(self) -> str:
        return "En tránsito hacia destino"


class EstadoEnDistribucion(EstadoEnvio):
    """El envío está en el centro de distribución local para entrega final"""
    
    def procesar(self, envio):
        print(f"📦 Envío {envio.id_envio} está EN DISTRIBUCIÓN LOCAL")
        print(f"   - Centro de distribución: Ciudad de destino")
        print(f"   - Preparando ruta de reparto")
        print(f"   - Destinatario: {envio.destinatario}")
        return "El envío está en el centro de distribución local, listo para entrega"
    
    def siguiente(self, envio):
        print(f"🔄 Cambiando estado: En Distribución → Entregado")
        envio.estado = EstadoEntregado()
        return "¡Envío entregado exitosamente!"
    
    def cancelar(self, envio):
        print(f"⚠️ Cancelación en última etapa - se contactará al destinatario")
        envio.estado = EstadoCancelado()
        return "Envío cancelado - disponible para devolución o recogida"
    
    def get_descripcion(self) -> str:
        return "En distribución local"


class EstadoEntregado(EstadoEnvio):
    """Estado final: el envío ha sido entregado al destinatario"""
    
    def procesar(self, envio):
        print(f"✅ Envío {envio.id_envio} fue ENTREGADO")
        print(f"   - Destinatario: {envio.destinatario}")
        print(f"   - Dirección: {envio.direccion_destino}")
        print(f"   - Fecha de entrega: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "El envío ha sido entregado satisfactoriamente al destinatario"
    
    def siguiente(self, envio):
        return "El envío ya fue entregado. No hay más estados"
    
    def cancelar(self, envio):
        return "No se puede cancelar un envío ya entregado"
    
    def get_descripcion(self) -> str:
        return "Entregado exitosamente"


class EstadoCancelado(EstadoEnvio):
    """Estado terminal: el envío ha sido cancelado"""
    
    def procesar(self, envio):
        print(f"🚫 Envío {envio.id_envio} ha sido CANCELADO")
        print(f"   - Fecha de cancelación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   - Se procederá según políticas de devolución")
        return "El envío ha sido cancelado"
    
    def siguiente(self, envio):
        return "Un envío cancelado no puede avanzar a otros estados"
    
    def cancelar(self, envio):
        return "El envío ya está cancelado"
    
    def get_descripcion(self) -> str:
        return "Cancelado"


class GestorEstadoEnvio:
    """Clase auxiliar para gestionar los estados del envío"""
    
    @staticmethod
    def inicializar_envio(envio):
        """Inicializa un envío en estado Pendiente"""
        envio.estado = EstadoPendiente()
        print(f"🆕 Envío {envio.id_envio} inicializado en estado: {envio.estado.get_descripcion()}")
    
    @staticmethod
    def mostrar_estado_actual(envio):
        """Muestra el estado actual del envío"""
        print(f"\n{'='*60}")
        print(f"ESTADO ACTUAL DEL ENVÍO: {envio.id_envio}")
        print(f"{'='*60}")
        mensaje = envio.estado.procesar(envio)
        print(f"{'='*60}\n")
        return mensaje
    
    @staticmethod
    def avanzar_estado(envio):
        """Avanza el envío al siguiente estado"""
        estado_anterior = envio.estado.get_descripcion()
        mensaje = envio.estado.siguiente(envio)
        estado_nuevo = envio.estado.get_descripcion()
        print(f"📊 Estado actualizado: {estado_anterior} → {estado_nuevo}")
        return mensaje
    
    @staticmethod
    def cancelar_envio(envio):
        """Cancela el envío"""
        return envio.estado.cancelar(envio)
