# Patterns/__init__.py
"""
Paquete de patrones de diseño de comportamiento
"""
from .ChainOfResponsibility import CadenaValidacion
from .State import GestorEstadoEnvio
from .Memento import OriginadorEnvio
from .Visitor import CalculadorCosto, CalculadorTiempoEntrega, GeneradorReporte, CalculadorDescuento

__all__ = [
    'CadenaValidacion',
    'GestorEstadoEnvio',
    'OriginadorEnvio',
    'CalculadorCosto',
    'CalculadorTiempoEntrega',
    'GeneradorReporte',
    'CalculadorDescuento'
]
