# main.py
"""
Archivo principal de la aplicación de Transportes y Envíos
Proyecto: Implementación de Patrones de Comportamiento
Patrones implementados:
  1. Chain of Responsibility
  2. State
  3. Memento
  4. Visitor

Arquitectura: MVC (Model-View-Controller)
"""
import sys
import os

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Views.ConsoleView import ConsoleView

def main():
    """Función principal que inicia la aplicación"""
    try:
        vista = ConsoleView()
        vista.ejecutar()
    except KeyboardInterrupt:
        print("\n\n⚠️ Aplicación interrumpida por el usuario")
        print("¡Hasta pronto!\n")
    except Exception as e:
        print(f"\n❌ Error crítico en la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
