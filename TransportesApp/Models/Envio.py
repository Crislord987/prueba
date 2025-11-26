# Models/Envio.py
"""
Modelo principal de Envío para la empresa de transportes
"""
from datetime import datetime
from typing import List, Optional

class Envio:
    """Clase que representa un envío en la empresa de transportes"""
    
    def __init__(self, id_envio: str, remitente: str, destinatario: str, 
                 direccion_origen: str, direccion_destino: str, peso: float, 
                 tipo_envio: str, descripcion: str = ""):
        self.id_envio = id_envio
        self.remitente = remitente
        self.destinatario = destinatario
        self.direccion_origen = direccion_origen
        self.direccion_destino = direccion_destino
        self.peso = peso  # en kg
        self.tipo_envio = tipo_envio  # "express", "estandar", "economico"
        self.descripcion = descripcion
        self.fecha_creacion = datetime.now()
        self.estado = None  # Se asignará por el patrón State
        self.costo = 0.0
        self.distancia = 0.0  # en km
        self.es_fragil = False
        self.requiere_seguro = False
        
    def __str__(self):
        return f"Envío {self.id_envio}: {self.remitente} -> {self.destinatario} ({self.tipo_envio})"
    
    def get_info(self) -> dict:
        """Retorna información completa del envío"""
        return {
            'id': self.id_envio,
            'remitente': self.remitente,
            'destinatario': self.destinatario,
            'origen': self.direccion_origen,
            'destino': self.direccion_destino,
            'peso': self.peso,
            'tipo': self.tipo_envio,
            'estado': self.estado.__class__.__name__ if self.estado else "Sin estado",
            'costo': self.costo,
            'fecha': self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def accept(self, visitor):
        """Método para el patrón Visitor"""
        return visitor.visit(self)


class EnvioExpress(Envio):
    """Envío express - entrega en 24 horas"""
    def __init__(self, id_envio: str, remitente: str, destinatario: str, 
                 direccion_origen: str, direccion_destino: str, peso: float, descripcion: str = ""):
        super().__init__(id_envio, remitente, destinatario, direccion_origen, 
                        direccion_destino, peso, "Express", descripcion)


class EnvioEstandar(Envio):
    """Envío estándar - entrega en 3-5 días"""
    def __init__(self, id_envio: str, remitente: str, destinatario: str, 
                 direccion_origen: str, direccion_destino: str, peso: float, descripcion: str = ""):
        super().__init__(id_envio, remitente, destinatario, direccion_origen, 
                        direccion_destino, peso, "Estándar", descripcion)


class EnvioEconomico(Envio):
    """Envío económico - entrega en 7-10 días"""
    def __init__(self, id_envio: str, remitente: str, destinatario: str, 
                 direccion_origen: str, direccion_destino: str, peso: float, descripcion: str = ""):
        super().__init__(id_envio, remitente, destinatario, direccion_origen, 
                        direccion_destino, peso, "Económico", descripcion)
