# backend/app.py
"""
Backend API REST para el sistema de transportes
Framework: Flask
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.EnvioController import EnvioController

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend

# Instancia global del controlador
controller = EnvioController()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servidor está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'API de Transportes funcionando correctamente'
    })


@app.route('/api/envios', methods=['GET'])
def listar_envios():
    """Lista todos los envíos registrados"""
    try:
        envios_data = []
        for envio in controller.envios:
            envios_data.append({
                'id': envio.id_envio,
                'remitente': envio.remitente,
                'destinatario': envio.destinatario,
                'origen': envio.direccion_origen,
                'destino': envio.direccion_destino,
                'peso': envio.peso,
                'tipo': envio.tipo_envio,
                'estado': envio.estado.get_descripcion() if envio.estado else "Sin estado",
                'costo': envio.costo,
                'distancia': envio.distancia,
                'es_fragil': envio.es_fragil,
                'requiere_seguro': envio.requiere_seguro,
                'descripcion': envio.descripcion,
                'fecha_creacion': envio.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify({
            'success': True,
            'data': envios_data,
            'total': len(envios_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>', methods=['GET'])
def obtener_envio(id_envio):
    """Obtiene un envío específico por ID"""
    try:
        envio = controller.obtener_envio(id_envio)
        
        if not envio:
            return jsonify({
                'success': False,
                'error': f'Envío {id_envio} no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': envio.id_envio,
                'remitente': envio.remitente,
                'destinatario': envio.destinatario,
                'origen': envio.direccion_origen,
                'destino': envio.direccion_destino,
                'peso': envio.peso,
                'tipo': envio.tipo_envio,
                'estado': envio.estado.get_descripcion() if envio.estado else "Sin estado",
                'costo': envio.costo,
                'distancia': envio.distancia,
                'es_fragil': envio.es_fragil,
                'requiere_seguro': envio.requiere_seguro,
                'descripcion': envio.descripcion,
                'fecha_creacion': envio.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios', methods=['POST'])
def crear_envio():
    """Crea un nuevo envío"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        campos_requeridos = ['tipo', 'remitente', 'destinatario', 'direccion_origen', 'direccion_destino', 'peso']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido faltante: {campo}'
                }), 400
        
        envio = controller.crear_envio(
            tipo=data['tipo'],
            remitente=data['remitente'],
            destinatario=data['destinatario'],
            direccion_origen=data['direccion_origen'],
            direccion_destino=data['direccion_destino'],
            peso=float(data['peso']),
            descripcion=data.get('descripcion', ''),
            es_fragil=data.get('es_fragil', False)
        )
        
        if not envio:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear el envío. Verifique los datos.'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Envío creado exitosamente',
            'data': {
                'id': envio.id_envio,
                'costo': envio.costo,
                'estado': envio.estado.get_descripcion()
            }
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Error en los datos: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/estado', methods=['GET'])
def consultar_estado(id_envio):
    """Consulta el estado actual de un envío"""
    try:
        envio = controller.obtener_envio(id_envio)
        
        if not envio:
            return jsonify({
                'success': False,
                'error': f'Envío {id_envio} no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': id_envio,
                'estado': envio.estado.get_descripcion(),
                'descripcion': envio.estado.procesar(envio) if envio.estado else 'Sin estado'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/avanzar', methods=['POST'])
def avanzar_estado(id_envio):
    """Avanza el envío al siguiente estado"""
    try:
        resultado = controller.avanzar_estado_envio(id_envio)
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'No se pudo avanzar el estado'
            }), 400
        
        envio = controller.obtener_envio(id_envio)
        
        return jsonify({
            'success': True,
            'message': 'Estado avanzado exitosamente',
            'data': {
                'id': id_envio,
                'nuevo_estado': envio.estado.get_descripcion()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/cancelar', methods=['POST'])
def cancelar_envio(id_envio):
    """Cancela un envío"""
    try:
        resultado = controller.cancelar_envio(id_envio)
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'No se pudo cancelar el envío'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Envío cancelado exitosamente'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/modificar', methods=['PUT'])
def modificar_envio(id_envio):
    """Modifica datos de un envío"""
    try:
        data = request.get_json()
        
        if 'campo' not in data or 'valor' not in data:
            return jsonify({
                'success': False,
                'error': 'Se requieren los campos "campo" y "valor"'
            }), 400
        
        resultado = controller.modificar_envio(id_envio, data['campo'], data['valor'])
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'No se pudo modificar el envío'
            }), 400
        
        envio = controller.obtener_envio(id_envio)
        
        return jsonify({
            'success': True,
            'message': 'Envío modificado exitosamente',
            'data': {
                'id': id_envio,
                'costo_actualizado': envio.costo
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/deshacer', methods=['POST'])
def deshacer_cambio(id_envio):
    """Deshace el último cambio realizado en un envío"""
    try:
        resultado = controller.deshacer_cambio(id_envio)
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'No hay cambios que deshacer'
            }), 400
        
        envio = controller.obtener_envio(id_envio)
        
        return jsonify({
            'success': True,
            'message': 'Cambio deshecho exitosamente',
            'data': {
                'id': id_envio,
                'costo_actualizado': envio.costo
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/rehacer', methods=['POST'])
def rehacer_cambio(id_envio):
    """Rehace el último cambio deshecho"""
    try:
        resultado = controller.rehacer_cambio(id_envio)
        
        if not resultado:
            return jsonify({
                'success': False,
                'error': 'No hay cambios que rehacer'
            }), 400
        
        envio = controller.obtener_envio(id_envio)
        
        return jsonify({
            'success': True,
            'message': 'Cambio rehecho exitosamente',
            'data': {
                'id': id_envio,
                'costo_actualizado': envio.costo
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/historial', methods=['GET'])
def obtener_historial(id_envio):
    """Obtiene el historial de cambios de un envío"""
    try:
        if id_envio not in controller.originadores:
            return jsonify({
                'success': False,
                'error': f'Envío {id_envio} no encontrado'
            }), 404
        
        historial = controller.originadores[id_envio].caretaker.get_historial_completo()
        
        return jsonify({
            'success': True,
            'data': historial
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/tiempo-entrega', methods=['GET'])
def calcular_tiempo_entrega(id_envio):
    """Calcula el tiempo estimado de entrega"""
    try:
        dias = controller.calcular_tiempo_entrega(id_envio)
        
        if dias is None:
            return jsonify({
                'success': False,
                'error': f'Envío {id_envio} no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': id_envio,
                'dias_estimados': dias
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/descuentos', methods=['GET'])
def calcular_descuentos(id_envio):
    """Calcula los descuentos aplicables"""
    try:
        descuento = controller.calcular_descuentos(id_envio)
        
        if descuento is None:
            return jsonify({
                'success': False,
                'error': f'Envío {id_envio} no encontrado'
            }), 404
        
        envio = controller.obtener_envio(id_envio)
        
        return jsonify({
            'success': True,
            'data': {
                'id': id_envio,
                'descuento': descuento,
                'costo_original': envio.costo,
                'costo_con_descuento': envio.costo - descuento
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/envios/<id_envio>/reporte', methods=['GET'])
def generar_reporte(id_envio):
    """Genera un reporte completo del envío"""
    try:
        reporte = controller.generar_reporte_envio(id_envio)
        
        if reporte is None:
            return jsonify({
                'success': False,
                'error': f'Envío {id_envio} no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': id_envio,
                'reporte': reporte
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Servidor Backend iniciando...")
    print("="*60)
    print("API REST para Sistema de Transportes")
    print("Puerto: 5000")
    print("URL: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
