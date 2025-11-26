# Patterns/ChainOfResponsibility.py
"""
Patrón Chain of Responsibility para validación de envíos
Valida diferentes aspectos del envío antes de ser procesado
"""
from abc import ABC, abstractmethod
from typing import Optional

class ValidadorEnvio(ABC):
    """Clase base abstracta para validadores de envío"""
    
    def __init__(self):
        self._siguiente: Optional[ValidadorEnvio] = None
    
    def set_siguiente(self, validador: 'ValidadorEnvio') -> 'ValidadorEnvio':
        """Establece el siguiente validador en la cadena"""
        self._siguiente = validador
        return validador
    
    @abstractmethod
    def validar(self, envio) -> tuple[bool, str]:
        """
        Valida el envío y pasa al siguiente validador si es necesario
        Retorna: (es_valido, mensaje)
        """
        pass


class ValidadorDatos(ValidadorEnvio):
    """Valida que los datos básicos del envío estén completos"""
    
    def validar(self, envio) -> tuple[bool, str]:
        if not envio.remitente or not envio.destinatario:
            return False, "❌ Error: Remitente o destinatario vacío"
        
        if not envio.direccion_origen or not envio.direccion_destino:
            return False, "❌ Error: Direcciones incompletas"
        
        print("✓ Validador de Datos: Información básica completa")
        
        if self._siguiente:
            return self._siguiente.validar(envio)
        
        return True, "✓ Validación de datos exitosa"


class ValidadorPeso(ValidadorEnvio):
    """Valida que el peso del envío esté dentro de los límites permitidos"""
    
    PESO_MINIMO = 0.1  # kg
    PESO_MAXIMO = 1000  # kg
    
    def validar(self, envio) -> tuple[bool, str]:
        if envio.peso < self.PESO_MINIMO:
            return False, f"❌ Error: Peso mínimo {self.PESO_MINIMO} kg"
        
        if envio.peso > self.PESO_MAXIMO:
            return False, f"❌ Error: Peso máximo {self.PESO_MAXIMO} kg. Requiere transporte especial"
        
        print(f"✓ Validador de Peso: {envio.peso} kg dentro del rango permitido")
        
        if self._siguiente:
            return self._siguiente.validar(envio)
        
        return True, "✓ Validación de peso exitosa"


class ValidadorTipoEnvio(ValidadorEnvio):
    """Valida que el tipo de envío sea válido"""
    
    TIPOS_VALIDOS = ["Express", "Estándar", "Económico"]
    
    def validar(self, envio) -> tuple[bool, str]:
        if envio.tipo_envio not in self.TIPOS_VALIDOS:
            return False, f"❌ Error: Tipo de envío inválido. Tipos válidos: {', '.join(self.TIPOS_VALIDOS)}"
        
        print(f"✓ Validador de Tipo: {envio.tipo_envio} es válido")
        
        if self._siguiente:
            return self._siguiente.validar(envio)
        
        return True, "✓ Validación de tipo exitosa"


class ValidadorDistancia(ValidadorEnvio):
    """Valida restricciones según la distancia del envío"""
    
    def validar(self, envio) -> tuple[bool, str]:
        # Simulamos cálculo de distancia (en app real sería con API de mapas)
        distancia = len(envio.direccion_destino) * 10  # Simulación simple
        envio.distancia = distancia
        
        if envio.tipo_envio == "Express" and distancia > 500:
            return False, f"❌ Error: Envío Express limitado a 500 km (distancia: {distancia} km)"
        
        if distancia > 2000:
            print(f"⚠ Advertencia: Distancia larga ({distancia} km) - puede requerir tiempo adicional")
        
        print(f"✓ Validador de Distancia: {distancia} km calculados")
        
        if self._siguiente:
            return self._siguiente.validar(envio)
        
        return True, "✓ Validación de distancia exitosa"


class ValidadorSeguridad(ValidadorEnvio):
    """Valida aspectos de seguridad del envío"""
    
    def validar(self, envio) -> tuple[bool, str]:
        # Validar si requiere seguro
        if envio.peso > 50 or envio.es_fragil:
            envio.requiere_seguro = True
            print(f"⚠ Validador de Seguridad: Se requiere seguro adicional")
        
        print("✓ Validador de Seguridad: Verificación completada")
        
        if self._siguiente:
            return self._siguiente.validar(envio)
        
        return True, "✓ Validación de seguridad exitosa"


class CadenaValidacion:
    """Clase para configurar y ejecutar la cadena de validación"""
    
    @staticmethod
    def crear_cadena() -> ValidadorEnvio:
        """Crea y retorna la cadena de validadores configurada"""
        validador_datos = ValidadorDatos()
        validador_peso = ValidadorPeso()
        validador_tipo = ValidadorTipoEnvio()
        validador_distancia = ValidadorDistancia()
        validador_seguridad = ValidadorSeguridad()
        
        # Configurar la cadena
        validador_datos.set_siguiente(validador_peso)\
                      .set_siguiente(validador_tipo)\
                      .set_siguiente(validador_distancia)\
                      .set_siguiente(validador_seguridad)
        
        return validador_datos
    
    @staticmethod
    def validar_envio(envio) -> tuple[bool, str]:
        """Ejecuta la validación completa del envío"""
        print(f"\n{'='*60}")
        print(f"INICIANDO VALIDACIÓN DE ENVÍO: {envio.id_envio}")
        print(f"{'='*60}")
        
        cadena = CadenaValidacion.crear_cadena()
        resultado, mensaje = cadena.validar(envio)
        
        print(f"{'='*60}")
        if resultado:
            print(f"✅ VALIDACIÓN COMPLETADA EXITOSAMENTE")
        else:
            print(f"❌ VALIDACIÓN FALLIDA")
        print(f"Mensaje: {mensaje}")
        print(f"{'='*60}\n")
        
        return resultado, mensaje
