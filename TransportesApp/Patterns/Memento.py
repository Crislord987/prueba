# Patterns/Memento.py
"""
Patrón Memento para guardar y restaurar el historial de cambios del envío
Permite deshacer cambios y mantener un registro de todas las modificaciones
"""
from datetime import datetime
from typing import List, Optional
import copy

class MementoEnvio:
    """
    Memento que guarda el estado de un envío en un momento específico
    """
    
    def __init__(self, envio):
        """Crea un snapshot del envío"""
        self._id_envio = envio.id_envio
        self._remitente = envio.remitente
        self._destinatario = envio.destinatario
        self._direccion_origen = envio.direccion_origen
        self._direccion_destino = envio.direccion_destino
        self._peso = envio.peso
        self._tipo_envio = envio.tipo_envio
        self._descripcion = envio.descripcion
        self._costo = envio.costo
        self._distancia = envio.distancia
        self._es_fragil = envio.es_fragil
        self._requiere_seguro = envio.requiere_seguro
        
        # Guardar el nombre del estado actual
        self._estado_nombre = envio.estado.__class__.__name__ if envio.estado else "Sin estado"
        
        self._timestamp = datetime.now()
        self._descripcion_cambio = ""
    
    def get_timestamp(self) -> datetime:
        """Retorna la fecha y hora del snapshot"""
        return self._timestamp
    
    def set_descripcion_cambio(self, descripcion: str):
        """Establece una descripción del cambio realizado"""
        self._descripcion_cambio = descripcion
    
    def get_descripcion_cambio(self) -> str:
        """Retorna la descripción del cambio"""
        return self._descripcion_cambio
    
    def get_estado_nombre(self) -> str:
        """Retorna el nombre del estado guardado"""
        return self._estado_nombre
    
    def restaurar_en(self, envio):
        """Restaura el estado guardado en el envío proporcionado"""
        envio.remitente = self._remitente
        envio.destinatario = self._destinatario
        envio.direccion_origen = self._direccion_origen
        envio.direccion_destino = self._direccion_destino
        envio.peso = self._peso
        envio.tipo_envio = self._tipo_envio
        envio.descripcion = self._descripcion
        envio.costo = self._costo
        envio.distancia = self._distancia
        envio.es_fragil = self._es_fragil
        envio.requiere_seguro = self._requiere_seguro
        
        # Nota: El estado no se restaura automáticamente para evitar inconsistencias
        # Debe ser manejado manualmente si es necesario
    
    def get_resumen(self) -> dict:
        """Retorna un resumen del memento"""
        return {
            'timestamp': self._timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'id_envio': self._id_envio,
            'remitente': self._remitente,
            'destinatario': self._destinatario,
            'peso': self._peso,
            'tipo': self._tipo_envio,
            'costo': self._costo,
            'estado': self._estado_nombre,
            'descripcion_cambio': self._descripcion_cambio
        }
    
    def __str__(self):
        return (f"Snapshot [{self._timestamp.strftime('%H:%M:%S')}]: "
                f"{self._id_envio} - {self._estado_nombre} - "
                f"{self._descripcion_cambio}")


class CaretakerEnvio:
    """
    Caretaker que gestiona el historial de mementos de un envío
    """
    
    def __init__(self):
        self._historial: List[MementoEnvio] = []
        self._indice_actual: int = -1
        self._max_historial: int = 50  # Límite de snapshots guardados
    
    def guardar(self, memento: MementoEnvio):
        """Guarda un nuevo memento en el historial"""
        # Si estamos en medio del historial (después de deshacer), 
        # eliminamos los estados futuros
        if self._indice_actual < len(self._historial) - 1:
            self._historial = self._historial[:self._indice_actual + 1]
        
        self._historial.append(memento)
        
        # Limitar el tamaño del historial
        if len(self._historial) > self._max_historial:
            self._historial.pop(0)
        else:
            self._indice_actual += 1
        
        print(f"💾 Snapshot guardado: {memento.get_descripcion_cambio()}")
    
    def deshacer(self) -> Optional[MementoEnvio]:
        """Retorna el memento anterior en el historial"""
        if self._indice_actual > 0:
            self._indice_actual -= 1
            memento = self._historial[self._indice_actual]
            print(f"↩️ Deshaciendo al estado: {memento.get_descripcion_cambio()}")
            return memento
        else:
            print("⚠️ No hay más cambios que deshacer")
            return None
    
    def rehacer(self) -> Optional[MementoEnvio]:
        """Retorna el memento siguiente en el historial"""
        if self._indice_actual < len(self._historial) - 1:
            self._indice_actual += 1
            memento = self._historial[self._indice_actual]
            print(f"↪️ Rehaciendo al estado: {memento.get_descripcion_cambio()}")
            return memento
        else:
            print("⚠️ No hay más cambios que rehacer")
            return None
    
    def get_historial_completo(self) -> List[dict]:
        """Retorna el historial completo de cambios"""
        return [memento.get_resumen() for memento in self._historial]
    
    def mostrar_historial(self):
        """Muestra el historial de cambios de forma legible"""
        print(f"\n{'='*80}")
        print(f"HISTORIAL DE CAMBIOS DEL ENVÍO")
        print(f"{'='*80}")
        
        if not self._historial:
            print("No hay cambios registrados")
        else:
            for i, memento in enumerate(self._historial):
                marcador = "→ " if i == self._indice_actual else "  "
                print(f"{marcador}{i+1}. {memento}")
        
        print(f"{'='*80}")
        print(f"Posición actual: {self._indice_actual + 1}/{len(self._historial)}")
        print(f"{'='*80}\n")
    
    def puede_deshacer(self) -> bool:
        """Verifica si se puede deshacer"""
        return self._indice_actual > 0
    
    def puede_rehacer(self) -> bool:
        """Verifica si se puede rehacer"""
        return self._indice_actual < len(self._historial) - 1
    
    def get_total_cambios(self) -> int:
        """Retorna el total de cambios registrados"""
        return len(self._historial)


class OriginadorEnvio:
    """
    Originador que crea y restaura mementos del envío
    """
    
    def __init__(self, envio):
        self.envio = envio
        self.caretaker = CaretakerEnvio()
        # Guardar estado inicial
        self.crear_snapshot("Estado inicial")
    
    def crear_snapshot(self, descripcion: str = "Cambio sin descripción"):
        """Crea un snapshot del estado actual"""
        memento = MementoEnvio(self.envio)
        memento.set_descripcion_cambio(descripcion)
        self.caretaker.guardar(memento)
    
    def deshacer(self) -> bool:
        """Deshace el último cambio"""
        memento = self.caretaker.deshacer()
        if memento:
            memento.restaurar_en(self.envio)
            print(f"✅ Cambios deshechos exitosamente")
            return True
        return False
    
    def rehacer(self) -> bool:
        """Rehace el último cambio deshecho"""
        memento = self.caretaker.rehacer()
        if memento:
            memento.restaurar_en(self.envio)
            print(f"✅ Cambios rehechos exitosamente")
            return True
        return False
    
    def mostrar_historial(self):
        """Muestra el historial completo de cambios"""
        self.caretaker.mostrar_historial()
    
    def modificar_remitente(self, nuevo_remitente: str):
        """Modifica el remitente y guarda el cambio"""
        self.envio.remitente = nuevo_remitente
        self.crear_snapshot(f"Remitente cambiado a: {nuevo_remitente}")
    
    def modificar_destinatario(self, nuevo_destinatario: str):
        """Modifica el destinatario y guarda el cambio"""
        self.envio.destinatario = nuevo_destinatario
        self.crear_snapshot(f"Destinatario cambiado a: {nuevo_destinatario}")
    
    def modificar_peso(self, nuevo_peso: float):
        """Modifica el peso y guarda el cambio"""
        self.envio.peso = nuevo_peso
        self.crear_snapshot(f"Peso modificado a: {nuevo_peso} kg")
    
    def modificar_direccion_destino(self, nueva_direccion: str):
        """Modifica la dirección de destino y guarda el cambio"""
        self.envio.direccion_destino = nueva_direccion
        self.crear_snapshot(f"Dirección de destino cambiada a: {nueva_direccion}")
    
    def marcar_como_fragil(self, es_fragil: bool):
        """Marca o desmarca el envío como frágil"""
        self.envio.es_fragil = es_fragil
        estado = "frágil" if es_fragil else "no frágil"
        self.crear_snapshot(f"Envío marcado como {estado}")
