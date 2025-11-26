# Patterns/Visitor.py
"""
Patrón Visitor para calcular costos de diferentes tipos de envíos
Permite agregar nuevas operaciones sin modificar las clases de envío
"""
from abc import ABC, abstractmethod

class VisitorEnvio(ABC):
    """Interfaz base para visitantes de envíos"""
    
    @abstractmethod
    def visit(self, envio) -> float:
        """Visita un envío y realiza una operación"""
        pass


class CalculadorCosto(VisitorEnvio):
    """
    Visitor que calcula el costo total de un envío
    Considera: peso, distancia, tipo de envío, seguros adicionales
    """
    
    # Tarifas base por kilogramo
    TARIFA_BASE = {
        "Express": 15.0,      # $15 por kg
        "Estándar": 8.0,      # $8 por kg
        "Económico": 4.0      # $4 por kg
    }
    
    # Tarifa por kilómetro
    TARIFA_DISTANCIA = 0.5  # $0.5 por km
    
    # Recargos adicionales
    RECARGO_FRAGIL = 50.0       # Recargo fijo si es frágil
    RECARGO_SEGURO = 0.02       # 2% del costo base
    RECARGO_PESO_EXTRA = 2.0    # $2 por kg adicional después de 50kg
    
    def visit(self, envio) -> float:
        """Calcula el costo total del envío"""
        print(f"\n{'='*60}")
        print(f"CALCULANDO COSTO DEL ENVÍO: {envio.id_envio}")
        print(f"{'='*60}")
        
        # Costo base por peso
        tarifa_kg = self.TARIFA_BASE.get(envio.tipo_envio, self.TARIFA_BASE["Estándar"])
        costo_base = envio.peso * tarifa_kg
        print(f"Costo base ({envio.peso} kg × ${tarifa_kg}/kg): ${costo_base:.2f}")
        
        # Costo por distancia
        costo_distancia = envio.distancia * self.TARIFA_DISTANCIA
        print(f"Costo por distancia ({envio.distancia} km × ${self.TARIFA_DISTANCIA}/km): ${costo_distancia:.2f}")
        
        costo_total = costo_base + costo_distancia
        
        # Recargo por peso extra
        if envio.peso > 50:
            peso_extra = envio.peso - 50
            recargo_peso = peso_extra * self.RECARGO_PESO_EXTRA
            costo_total += recargo_peso
            print(f"Recargo por peso extra ({peso_extra} kg × ${self.RECARGO_PESO_EXTRA}/kg): ${recargo_peso:.2f}")
        
        # Recargo por envío frágil
        if envio.es_fragil:
            costo_total += self.RECARGO_FRAGIL
            print(f"Recargo por envío frágil: ${self.RECARGO_FRAGIL:.2f}")
        
        # Recargo por seguro
        if envio.requiere_seguro:
            recargo_seguro = costo_total * self.RECARGO_SEGURO
            costo_total += recargo_seguro
            print(f"Recargo por seguro ({self.RECARGO_SEGURO*100}%): ${recargo_seguro:.2f}")
        
        print(f"{'='*60}")
        print(f"COSTO TOTAL: ${costo_total:.2f}")
        print(f"{'='*60}\n")
        
        envio.costo = costo_total
        return costo_total


class CalculadorTiempoEntrega(VisitorEnvio):
    """
    Visitor que calcula el tiempo estimado de entrega
    Considera: distancia, tipo de envío, condiciones especiales
    """
    
    # Velocidad promedio por tipo de envío (km/día)
    VELOCIDAD = {
        "Express": 500,      # 500 km por día
        "Estándar": 300,     # 300 km por día
        "Económico": 150     # 150 km por día
    }
    
    # Días adicionales por procesamiento
    DIAS_PROCESAMIENTO = {
        "Express": 0,        # Procesamiento inmediato
        "Estándar": 1,       # 1 día de procesamiento
        "Económico": 2       # 2 días de procesamiento
    }
    
    def visit(self, envio) -> int:
        """Calcula los días estimados de entrega"""
        print(f"\n{'='*60}")
        print(f"CALCULANDO TIEMPO DE ENTREGA: {envio.id_envio}")
        print(f"{'='*60}")
        
        velocidad = self.VELOCIDAD.get(envio.tipo_envio, self.VELOCIDAD["Estándar"])
        dias_procesamiento = self.DIAS_PROCESAMIENTO.get(envio.tipo_envio, 1)
        
        # Calcular días de tránsito
        dias_transito = int(envio.distancia / velocidad) + 1  # Redondear hacia arriba
        
        print(f"Días de procesamiento: {dias_procesamiento}")
        print(f"Días de tránsito ({envio.distancia} km ÷ {velocidad} km/día): {dias_transito}")
        
        # Días adicionales si es frágil (requiere manejo especial)
        dias_adicionales = 1 if envio.es_fragil else 0
        if dias_adicionales:
            print(f"Días adicionales (envío frágil): {dias_adicionales}")
        
        dias_totales = dias_procesamiento + dias_transito + dias_adicionales
        
        print(f"{'='*60}")
        print(f"TIEMPO ESTIMADO DE ENTREGA: {dias_totales} días")
        print(f"{'='*60}\n")
        
        return dias_totales


class GeneradorReporte(VisitorEnvio):
    """
    Visitor que genera un reporte detallado del envío
    """
    
    def visit(self, envio) -> str:
        """Genera un reporte completo del envío"""
        print(f"\n{'='*60}")
        print(f"GENERANDO REPORTE DETALLADO")
        print(f"{'='*60}")
        
        reporte = []
        reporte.append(f"\n{'='*80}")
        reporte.append(f"REPORTE DE ENVÍO - {envio.id_envio}")
        reporte.append(f"{'='*80}")
        reporte.append(f"\nINFORMACIÓN GENERAL:")
        reporte.append(f"  • ID Envío: {envio.id_envio}")
        reporte.append(f"  • Tipo de servicio: {envio.tipo_envio}")
        reporte.append(f"  • Fecha de creación: {envio.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}")
        reporte.append(f"  • Estado actual: {envio.estado.get_descripcion() if envio.estado else 'Sin estado'}")
        
        reporte.append(f"\nREMITENTE:")
        reporte.append(f"  • Nombre: {envio.remitente}")
        reporte.append(f"  • Dirección: {envio.direccion_origen}")
        
        reporte.append(f"\nDESTINATARIO:")
        reporte.append(f"  • Nombre: {envio.destinatario}")
        reporte.append(f"  • Dirección: {envio.direccion_destino}")
        
        reporte.append(f"\nDETALLES DEL PAQUETE:")
        reporte.append(f"  • Peso: {envio.peso} kg")
        reporte.append(f"  • Distancia: {envio.distancia} km")
        reporte.append(f"  • Frágil: {'Sí' if envio.es_fragil else 'No'}")
        reporte.append(f"  • Requiere seguro: {'Sí' if envio.requiere_seguro else 'No'}")
        reporte.append(f"  • Descripción: {envio.descripcion if envio.descripcion else 'N/A'}")
        
        reporte.append(f"\nCOSTOS:")
        reporte.append(f"  • Costo total: ${envio.costo:.2f}")
        
        # Calcular tiempo de entrega
        calculador_tiempo = CalculadorTiempoEntrega()
        dias_entrega = calculador_tiempo.visit(envio)
        reporte.append(f"  • Tiempo estimado: {dias_entrega} días")
        
        reporte.append(f"\n{'='*80}")
        reporte.append(f"FIN DEL REPORTE")
        reporte.append(f"{'='*80}\n")
        
        reporte_completo = "\n".join(reporte)
        print(reporte_completo)
        
        return reporte_completo


class CalculadorDescuento(VisitorEnvio):
    """
    Visitor que calcula descuentos aplicables al envío
    """
    
    def visit(self, envio) -> float:
        """Calcula el descuento total aplicable"""
        print(f"\n{'='*60}")
        print(f"CALCULANDO DESCUENTOS: {envio.id_envio}")
        print(f"{'='*60}")
        
        descuento_total = 0.0
        
        # Descuento por volumen (envíos pesados)
        if envio.peso > 100:
            descuento_peso = envio.costo * 0.10  # 10% de descuento
            descuento_total += descuento_peso
            print(f"Descuento por volumen (peso > 100kg): ${descuento_peso:.2f} (10%)")
        elif envio.peso > 50:
            descuento_peso = envio.costo * 0.05  # 5% de descuento
            descuento_total += descuento_peso
            print(f"Descuento por volumen (peso > 50kg): ${descuento_peso:.2f} (5%)")
        
        # Descuento por distancia larga
        if envio.distancia > 1000:
            descuento_distancia = envio.costo * 0.08  # 8% de descuento
            descuento_total += descuento_distancia
            print(f"Descuento por distancia larga (>1000km): ${descuento_distancia:.2f} (8%)")
        
        # Descuento por servicio económico
        if envio.tipo_envio == "Económico":
            descuento_economico = envio.costo * 0.05  # 5% de descuento adicional
            descuento_total += descuento_economico
            print(f"Descuento por servicio económico: ${descuento_economico:.2f} (5%)")
        
        if descuento_total == 0:
            print("No hay descuentos aplicables")
        
        print(f"{'='*60}")
        print(f"DESCUENTO TOTAL: ${descuento_total:.2f}")
        print(f"COSTO FINAL CON DESCUENTO: ${envio.costo - descuento_total:.2f}")
        print(f"{'='*60}\n")
        
        return descuento_total
