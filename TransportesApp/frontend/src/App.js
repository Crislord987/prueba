import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [activeView, setActiveView] = useState('list');
  const [envios, setEnvios] = useState([]);
  const [selectedEnvio, setSelectedEnvio] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterEstado, setFilterEstado] = useState('todos');
  const [filterTipo, setFilterTipo] = useState('todos');
  const [formData, setFormData] = useState({
    tipo: 'Estándar',
    remitente: '',
    destinatario: '',
    direccion_origen: '',
    direccion_destino: '',
    peso: '',
    descripcion: '',
    es_fragil: false
  });

  useEffect(() => {
    loadEnvios();
  }, []);

  const loadEnvios = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/envios`);
      setEnvios(response.data.data);
    } catch (error) {
      showMessage('Error al cargar envíos', 'error');
    }
    setLoading(false);
  };

  const showMessage = (text, type = 'success') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 5000);
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API_URL}/envios`, formData);
      showMessage('Envío creado exitosamente', 'success');
      setFormData({
        tipo: 'Estándar',
        remitente: '',
        destinatario: '',
        direccion_origen: '',
        direccion_destino: '',
        peso: '',
        descripcion: '',
        es_fragil: false
      });
      loadEnvios();
      setActiveView('list');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error al crear envío', 'error');
    }
    setLoading(false);
  };

  const handleAvanzarEstado = async (id) => {
    setLoading(true);
    try {
      await axios.post(`${API_URL}/envios/${id}/avanzar`);
      showMessage('Estado avanzado exitosamente', 'success');
      loadEnvios();
      if (selectedEnvio && selectedEnvio.id === id) {
        loadEnvioDetails(id);
      }
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error al avanzar estado', 'error');
    }
    setLoading(false);
  };

  const handleCancelarEnvio = async (id) => {
    if (!window.confirm('¿Está seguro de cancelar este envío?')) return;
    
    setLoading(true);
    try {
      await axios.post(`${API_URL}/envios/${id}/cancelar`);
      showMessage('Envío cancelado exitosamente', 'success');
      loadEnvios();
      setSelectedEnvio(null);
      setActiveView('list');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error al cancelar envío', 'error');
    }
    setLoading(false);
  };

  const loadEnvioDetails = async (id) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/envios/${id}`);
      setSelectedEnvio(response.data.data);
      setActiveView('details');
    } catch (error) {
      showMessage('Error al cargar detalles', 'error');
    }
    setLoading(false);
  };

  const getEstadoClass = (estado) => {
    const estadoMap = {
      'Pendiente de validación': 'estado-pendiente',
      'En proceso de preparación': 'estado-proceso',
      'En tránsito hacia destino': 'estado-transito',
      'En distribución local': 'estado-distribucion',
      'Entregado exitosamente': 'estado-entregado',
      'Cancelado': 'estado-cancelado'
    };
    return estadoMap[estado] || 'estado-pendiente';
  };

  const getEnviosFiltrados = () => {
    return envios.filter(envio => {
      const matchSearch = envio.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         envio.remitente.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         envio.destinatario.toLowerCase().includes(searchTerm.toLowerCase());
      const matchEstado = filterEstado === 'todos' || envio.estado === filterEstado;
      const matchTipo = filterTipo === 'todos' || envio.tipo === filterTipo;
      return matchSearch && matchEstado && matchTipo;
    });
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🚚 Sistema de Gestión de Transportes</h1>
        <p>Implementación de Patrones de Diseño</p>
      </header>

      <nav className="navigation">
        <button
          className={`nav-button ${activeView === 'list' ? 'active' : ''}`}
          onClick={() => setActiveView('list')}
        >
          📋 Lista de Envíos
        </button>
        <button
          className={`nav-button ${activeView === 'create' ? 'active' : ''}`}
          onClick={() => setActiveView('create')}
        >
          📦 Crear Envío
        </button>
        {selectedEnvio && (
          <>
            <button
              className={`nav-button ${activeView === 'modify' ? 'active' : ''}`}
              onClick={() => setActiveView('modify')}
            >
              ✏️ Modificar
            </button>
            <button
              className={`nav-button ${activeView === 'history' ? 'active' : ''}`}
              onClick={() => setActiveView('history')}
            >
              📜 Historial
            </button>
            <button
              className={`nav-button ${activeView === 'reports' ? 'active' : ''}`}
              onClick={() => setActiveView('reports')}
            >
              📊 Reportes
            </button>
          </>
        )}
        <button
          className={`nav-button ${activeView === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveView('dashboard')}
        >
          📈 Dashboard
        </button>
      </nav>

      {message && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <main className="main-content">
        {activeView === 'list' && <ListaEnvios />}
        {activeView === 'create' && <CrearEnvio />}
        {activeView === 'details' && <DetallesEnvio />}
        {activeView === 'modify' && <ModificarEnvio />}
        {activeView === 'history' && <HistorialEnvio />}
        {activeView === 'reports' && <ReportesEnvio />}
        {activeView === 'dashboard' && <Dashboard />}
      </main>
    </div>
  );

  function ListaEnvios() {
    const enviosFiltrados = getEnviosFiltrados();

    if (loading) {
      return (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      );
    }

    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ color: '#667eea' }}>
            Envíos Registrados ({enviosFiltrados.length})
          </h2>
        </div>

        {/* Filtros y búsqueda */}
        <div className="filters-container">
          <div className="form-group" style={{ marginBottom: '0' }}>
            <input
              type="text"
              placeholder="🔍 Buscar por ID, remitente o destinatario..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <div className="form-group" style={{ marginBottom: '0', flex: 1 }}>
              <select value={filterEstado} onChange={(e) => setFilterEstado(e.target.value)}>
                <option value="todos">Todos los estados</option>
                <option value="Pendiente de validación">Pendiente de validación</option>
                <option value="En proceso de preparación">En proceso de preparación</option>
                <option value="En tránsito hacia destino">En tránsito hacia destino</option>
                <option value="En distribución local">En distribución local</option>
                <option value="Entregado exitosamente">Entregado exitosamente</option>
                <option value="Cancelado">Cancelado</option>
              </select>
            </div>
            <div className="form-group" style={{ marginBottom: '0', flex: 1 }}>
              <select value={filterTipo} onChange={(e) => setFilterTipo(e.target.value)}>
                <option value="todos">Todos los tipos</option>
                <option value="Express">Express</option>
                <option value="Estándar">Estándar</option>
                <option value="Económico">Económico</option>
              </select>
            </div>
          </div>
        </div>

        {enviosFiltrados.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📦</div>
            <h3>No hay envíos que coincidan</h3>
            <p>Intenta ajustar los filtros de búsqueda</p>
          </div>
        ) : (
          <div className="envios-list">
            {enviosFiltrados.map(envio => (
              <div
                key={envio.id}
                className="envio-card"
                onClick={() => loadEnvioDetails(envio.id)}
              >
                <h3>{envio.id}</h3>
                <div className="envio-card-info">
                  <p><strong>De:</strong> {envio.remitente}</p>
                  <p><strong>Para:</strong> {envio.destinatario}</p>
                  <p><strong>Tipo:</strong> {envio.tipo}</p>
                  <p><strong>Peso:</strong> {envio.peso} kg</p>
                  <p><strong>Costo:</strong> ${envio.costo.toFixed(2)}</p>
                  <p>
                    <span className={`envio-estado ${getEstadoClass(envio.estado)}`}>
                      {envio.estado}
                    </span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  function CrearEnvio() {
    return (
      <div>
        <h2 style={{ marginBottom: '30px', color: '#667eea', textAlign: 'center' }}>
          📦 Crear Nuevo Envío
        </h2>
        <form className="form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Tipo de Envío</label>
            <select name="tipo" value={formData.tipo} onChange={handleInputChange} required>
              <option value="Express">Express (24 horas)</option>
              <option value="Estándar">Estándar (3-5 días)</option>
              <option value="Económico">Económico (7-10 días)</option>
            </select>
          </div>

          <div className="form-group">
            <label>Remitente</label>
            <input
              type="text"
              name="remitente"
              value={formData.remitente}
              onChange={handleInputChange}
              required
              placeholder="Nombre del remitente"
            />
          </div>

          <div className="form-group">
            <label>Dirección de Origen</label>
            <input
              type="text"
              name="direccion_origen"
              value={formData.direccion_origen}
              onChange={handleInputChange}
              required
              placeholder="Dirección completa de origen"
            />
          </div>

          <div className="form-group">
            <label>Destinatario</label>
            <input
              type="text"
              name="destinatario"
              value={formData.destinatario}
              onChange={handleInputChange}
              required
              placeholder="Nombre del destinatario"
            />
          </div>

          <div className="form-group">
            <label>Dirección de Destino</label>
            <input
              type="text"
              name="direccion_destino"
              value={formData.direccion_destino}
              onChange={handleInputChange}
              required
              placeholder="Dirección completa de destino"
            />
          </div>

          <div className="form-group">
            <label>Peso (kg)</label>
            <input
              type="number"
              name="peso"
              value={formData.peso}
              onChange={handleInputChange}
              required
              min="0.1"
              step="0.1"
              placeholder="Peso en kilogramos"
            />
          </div>

          <div className="form-group">
            <label>Descripción del Contenido (opcional)</label>
            <textarea
              name="descripcion"
              value={formData.descripcion}
              onChange={handleInputChange}
              placeholder="Descripción breve del contenido"
            />
          </div>

          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              name="es_fragil"
              checked={formData.es_fragil}
              onChange={handleInputChange}
              id="es_fragil"
            />
            <label htmlFor="es_fragil">¿El paquete es frágil?</label>
          </div>

          <div className="button-group">
            <button type="submit" className="button" disabled={loading}>
              {loading ? 'Creando...' : 'Crear Envío'}
            </button>
            <button
              type="button"
              className="button button-danger"
              onClick={() => setActiveView('list')}
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    );
  }

  function DetallesEnvio() {
    const [tiempoEntrega, setTiempoEntrega] = useState(null);
    const [descuentos, setDescuentos] = useState(null);

    useEffect(() => {
      if (selectedEnvio) {
        loadTiempoEntrega();
        loadDescuentos();
      }
    }, [selectedEnvio]);

    const loadTiempoEntrega = async () => {
      try {
        const response = await axios.get(`${API_URL}/envios/${selectedEnvio.id}/tiempo-entrega`);
        setTiempoEntrega(response.data.data);
      } catch (error) {
        console.error('Error al cargar tiempo de entrega:', error);
      }
    };

    const loadDescuentos = async () => {
      try {
        const response = await axios.get(`${API_URL}/envios/${selectedEnvio.id}/descuentos`);
        setDescuentos(response.data.data);
      } catch (error) {
        console.error('Error al cargar descuentos:', error);
      }
    };

    if (!selectedEnvio) return null;

    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
          <h2 style={{ color: '#667eea' }}>Detalles del Envío {selectedEnvio.id}</h2>
          <button className="button button-danger" onClick={() => setActiveView('list')}>
            ← Volver
          </button>
        </div>

        <div className="details-section">
          <h3>Información General</h3>
          <div className="details-grid">
            <div className="detail-item">
              <div className="detail-label">ID</div>
              <div className="detail-value">{selectedEnvio.id}</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Tipo de Servicio</div>
              <div className="detail-value">{selectedEnvio.tipo}</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Estado Actual</div>
              <div className="detail-value">
                <span className={`envio-estado ${getEstadoClass(selectedEnvio.estado)}`}>
                  {selectedEnvio.estado}
                </span>
              </div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Fecha de Creación</div>
              <div className="detail-value">{selectedEnvio.fecha_creacion}</div>
            </div>
          </div>
        </div>

        <div className="details-section">
          <h3>Remitente y Destinatario</h3>
          <div className="details-grid">
            <div className="detail-item">
              <div className="detail-label">Remitente</div>
              <div className="detail-value">{selectedEnvio.remitente}</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Dirección de Origen</div>
              <div className="detail-value">{selectedEnvio.origen}</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Destinatario</div>
              <div className="detail-value">{selectedEnvio.destinatario}</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Dirección de Destino</div>
              <div className="detail-value">{selectedEnvio.destino}</div>
            </div>
          </div>
        </div>

        <div className="details-section">
          <h3>Detalles del Paquete</h3>
          <div className="details-grid">
            <div className="detail-item">
              <div className="detail-label">Peso</div>
              <div className="detail-value">{selectedEnvio.peso} kg</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Distancia</div>
              <div className="detail-value">{selectedEnvio.distancia} km</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Frágil</div>
              <div className="detail-value">{selectedEnvio.es_fragil ? 'Sí' : 'No'}</div>
            </div>
            <div className="detail-item">
              <div className="detail-label">Requiere Seguro</div>
              <div className="detail-value">{selectedEnvio.requiere_seguro ? 'Sí' : 'No'}</div>
            </div>
          </div>
          {selectedEnvio.descripcion && (
            <div className="detail-item" style={{ marginTop: '15px' }}>
              <div className="detail-label">Descripción</div>
              <div className="detail-value">{selectedEnvio.descripcion}</div>
            </div>
          )}
        </div>

        {/* Tiempo de Entrega */}
        {tiempoEntrega && (
          <div className="details-section" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
            <h3>⏱️ Tiempo de Entrega</h3>
            <div className="details-grid">
              <div className="detail-item">
                <div className="detail-label" style={{ color: 'rgba(255,255,255,0.9)' }}>Días Estimados</div>
                <div className="detail-value" style={{ fontSize: '2rem', color: 'white' }}>
                  {tiempoEntrega.dias_estimados} días
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Descuentos */}
        {descuentos && (
          <div className="details-section">
            <h3>💰 Costos y Descuentos</h3>
            <div className="details-grid">
              <div className="detail-item">
                <div className="detail-label">Costo Original</div>
                <div className="detail-value">${descuentos.costo_original.toFixed(2)}</div>
              </div>
              {descuentos.descuento > 0 && (
                <div className="detail-item">
                  <div className="detail-label">Descuento Aplicado</div>
                  <div className="detail-value" style={{ color: '#10b981' }}>
                    - ${descuentos.descuento.toFixed(2)}
                  </div>
                </div>
              )}
              <div className="detail-item">
                <div className="detail-label">Total a Pagar</div>
                <div className="detail-value" style={{ fontSize: '1.5rem', color: '#667eea' }}>
                  ${descuentos.costo_con_descuento.toFixed(2)}
                </div>
              </div>
            </div>
            {descuentos.descuento > 0 && (
              <p style={{ textAlign: 'center', color: '#10b981', marginTop: '10px' }}>
                🎉 ¡Ahorraste {((descuentos.descuento / descuentos.costo_original) * 100).toFixed(1)}%!
              </p>
            )}
          </div>
        )}

        <div className="button-group">
          {selectedEnvio.estado !== 'Cancelado' && selectedEnvio.estado !== 'Entregado exitosamente' && (
            <>
              <button
                className="button button-success"
                onClick={() => handleAvanzarEstado(selectedEnvio.id)}
                disabled={loading}
              >
                ➡️ Avanzar Estado
              </button>
              <button
                className="button"
                onClick={() => setActiveView('modify')}
              >
                ✏️ Modificar Envío
              </button>
              <button
                className="button button-danger"
                onClick={() => handleCancelarEnvio(selectedEnvio.id)}
                disabled={loading}
              >
                ❌ Cancelar Envío
              </button>
            </>
          )}
        </div>
      </div>
    );
  }

function ModificarEnvio() {
  const getValorInicial = (campo) => {
    if (!selectedEnvio) return '';
    if (campo === 'peso') return selectedEnvio.peso;
    if (campo === 'descripcion') return selectedEnvio.descripcion || '';
    if (campo === 'es_fragil') return selectedEnvio.es_fragil;
    return '';
  };

  const [campo, setCampo] = useState('peso');
  const [valor, setValor] = useState(() => getValorInicial('peso'));

  const handleCampoChange = (e) => {
    const nuevoCampo = e.target.value;
    setCampo(nuevoCampo);
    setValor(getValorInicial(nuevoCampo));
  };

  const handleModificar = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      let valorFinal = valor;
      if (campo === 'peso') valorFinal = parseFloat(valor);
      else if (campo === 'es_fragil') valorFinal = valor === 'true' || valor === true;

      await axios.put(`${API_URL}/envios/${selectedEnvio.id}/modificar`, {
        campo,
        valor: valorFinal
      });
      showMessage('Cambio guardado exitosamente', 'success');
      await loadEnvioDetails(selectedEnvio.id);
      setActiveView('details');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error al modificar', 'error');
    }
    setLoading(false);
  };

  if (!selectedEnvio) return null;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h2 style={{ color: '#667eea' }}>✏️ Modificar Envío {selectedEnvio.id}</h2>
        <button className="button button-danger" onClick={() => setActiveView('details')}>
          ← Volver
        </button>
      </div>

      <form className="form" onSubmit={handleModificar}>
        <div className="form-group">
          <label>Campo a Modificar</label>
          <select value={campo} onChange={handleCampoChange}>
            <option value="peso">Peso (kg)</option>
            <option value="descripcion">Descripción</option>
            <option value="es_fragil">¿Es Frágil?</option>
          </select>
        </div>

        <div className="form-group">
          <label>Valor Actual</label>
          <input
            type="text"
            value={campo === 'es_fragil' ? (selectedEnvio.es_fragil ? 'Sí' : 'No') : selectedEnvio[campo] || 'Sin información'}
            disabled
            style={{ background: '#f3f4f6', color: '#6b7280' }}
          />
        </div>

        <div className="form-group">
          <label>Nuevo Valor</label>
          {campo === 'peso' && (
            <input
              type="number"
              value={valor}
              onChange={(e) => setValor(e.target.value)}
              min="0.1"
              step="0.1"
              required
              placeholder="Nuevo peso en kg"
            />
          )}
          {campo === 'descripcion' && (
            <textarea
              value={valor}
              onChange={(e) => setValor(e.target.value)}
              rows="4"
              placeholder="Nueva descripción"
            />
          )}
          {campo === 'es_fragil' && (
            <select value={valor.toString()} onChange={(e) => setValor(e.target.value)}>
              <option value="true">Sí</option>
              <option value="false">No</option>
            </select>
          )}
        </div>

        <div className="button-group">
          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Guardando...' : '💾 Guardar Cambio'}
          </button>
          <button
            type="button"
            className="button button-danger"
            onClick={() => setActiveView('details')}
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}

  function HistorialEnvio() {
    const [historial, setHistorial] = useState([]);
    const [indiceActual, setIndiceActual] = useState(0);

    useEffect(() => {
      if (selectedEnvio) {
        loadHistorial();
      }
    }, [selectedEnvio]);

    const loadHistorial = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`${API_URL}/envios/${selectedEnvio.id}/historial`);
        setHistorial(response.data.data);
        setIndiceActual(response.data.indice_actual);
      } catch (error) {
        showMessage('Error al cargar historial', 'error');
      }
      setLoading(false);
    };

    const handleDeshacer = async () => {
      setLoading(true);
      try {
        await axios.post(`${API_URL}/envios/${selectedEnvio.id}/deshacer`);
        showMessage('Cambio deshecho', 'success');
        await loadHistorial();
        await loadEnvioDetails(selectedEnvio.id);
      } catch (error) {
        showMessage(error.response?.data?.error || 'No hay cambios que deshacer', 'error');
      }
      setLoading(false);
    };

    const handleRehacer = async () => {
      setLoading(true);
      try {
        await axios.post(`${API_URL}/envios/${selectedEnvio.id}/rehacer`);
        showMessage('Cambio rehecho', 'success');
        await loadHistorial();
        await loadEnvioDetails(selectedEnvio.id);
      } catch (error) {
        showMessage(error.response?.data?.error || 'No hay cambios que rehacer', 'error');
      }
      setLoading(false);
    };

    if (!selectedEnvio) return null;

    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
          <h2 style={{ color: '#667eea' }}>📜 Historial de Cambios - {selectedEnvio.id}</h2>
          <button className="button button-danger" onClick={() => setActiveView('details')}>
            ← Volver
          </button>
        </div>

        {loading ? (
          <div className="loading"><div className="spinner"></div></div>
        ) : (
          <>
            <div className="historial-actions">
              <button
                className="button"
                onClick={handleDeshacer}
                disabled={loading || indiceActual === 0}
              >
                ⬅️ Deshacer
              </button>
              <span style={{ padding: '10px 20px', background: '#667eea', color: 'white', borderRadius: '8px' }}>
                Cambio {indiceActual + 1} de {historial.length}
              </span>
              <button
                className="button"
                onClick={handleRehacer}
                disabled={loading || indiceActual === historial.length - 1}
              >
                Rehacer ➡️
              </button>
            </div>

            <div className="historial-timeline">
              {historial.map((cambio, idx) => (
                <div
                  key={idx}
                  className={`historial-item ${idx === indiceActual ? 'actual' : idx < indiceActual ? 'pasado' : 'futuro'}`}
                >
                  <div className="historial-numero">#{idx}</div>
                  <div className="historial-content">
                    <div className="historial-fecha">{cambio.timestamp}</div>
                    <div className="historial-cambio">{cambio.cambio}</div>
                    {idx === indiceActual && (
                      <div className="historial-badge">Actual</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    );
  }

  function ReportesEnvio() {
    const [reporte, setReporte] = useState('');

    useEffect(() => {
      if (selectedEnvio) {
        loadReporte();
      }
    }, [selectedEnvio]);

    const loadReporte = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`${API_URL}/envios/${selectedEnvio.id}/reporte`);
        setReporte(response.data.data.reporte);
      } catch (error) {
        showMessage('Error al generar reporte', 'error');
      }
      setLoading(false);
    };

    const handleCopiar = () => {
      navigator.clipboard.writeText(reporte);
      showMessage('Reporte copiado al portapapeles', 'success');
    };

    const handleImprimir = () => {
      const ventana = window.open('', '_blank');
      ventana.document.write(`
        <html>
          <head>
            <title>Reporte - ${selectedEnvio.id}</title>
            <style>
              body { font-family: 'Courier New', monospace; padding: 20px; }
              pre { white-space: pre-wrap; }
            </style>
          </head>
          <body>
            <pre>${reporte}</pre>
          </body>
        </html>
      `);
      ventana.document.close();
      ventana.print();
    };

    if (!selectedEnvio) return null;

    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
          <h2 style={{ color: '#667eea' }}>📊 Reporte Completo - {selectedEnvio.id}</h2>
          <button className="button button-danger" onClick={() => setActiveView('details')}>
            ← Volver
          </button>
        </div>

        {loading ? (
          <div className="loading"><div className="spinner"></div></div>
        ) : (
          <>
            <div className="button-group" style={{ marginBottom: '20px' }}>
              <button className="button" onClick={handleCopiar}>
                📋 Copiar al Portapapeles
              </button>
              <button className="button" onClick={handleImprimir}>
                🖨️ Imprimir
              </button>
            </div>

            <div className="reporte-container">
              <pre className="reporte-content">{reporte}</pre>
            </div>
          </>
        )}
      </div>
    );
  }

  function Dashboard() {
    const [stats, setStats] = useState({
      total: 0,
      porEstado: {},
      porTipo: {},
      ingresoTotal: 0,
      pesoTotal: 0
    });

    useEffect(() => {
      calcularEstadisticas();
    }, [envios]);

    const calcularEstadisticas = () => {
      const porEstado = {};
      const porTipo = {};
      let ingresoTotal = 0;
      let pesoTotal = 0;

      envios.forEach(envio => {
        porEstado[envio.estado] = (porEstado[envio.estado] || 0) + 1;
        porTipo[envio.tipo] = (porTipo[envio.tipo] || 0) + 1;
        ingresoTotal += envio.costo;
        pesoTotal += envio.peso;
      });

      setStats({
        total: envios.length,
        porEstado,
        porTipo,
        ingresoTotal,
        pesoTotal
      });
    };

    return (
      <div>
        <h2 style={{ marginBottom: '30px', color: '#667eea', textAlign: 'center' }}>
          📈 Dashboard General
        </h2>

        <div className="dashboard-grid">
          <div className="dashboard-card">
            <div className="dashboard-card-icon">📦</div>
            <div className="dashboard-card-value">{stats.total}</div>
            <div className="dashboard-card-label">Total Envíos</div>
          </div>

          <div className="dashboard-card">
            <div className="dashboard-card-icon">💰</div>
            <div className="dashboard-card-value">${stats.ingresoTotal.toFixed(2)}</div>
            <div className="dashboard-card-label">Ingresos Totales</div>
          </div>

          <div className="dashboard-card">
            <div className="dashboard-card-icon">⚖️</div>
            <div className="dashboard-card-value">{stats.pesoTotal.toFixed(1)} kg</div>
            <div className="dashboard-card-label">Peso Total</div>
          </div>

          <div className="dashboard-card">
            <div className="dashboard-card-icon">📊</div>
            <div className="dashboard-card-value">
              ${stats.total > 0 ? (stats.ingresoTotal / stats.total).toFixed(2) : '0.00'}
            </div>
            <div className="dashboard-card-label">Costo Promedio</div>
          </div>
        </div>

        <div className="dashboard-section">
          <h3>Envíos por Estado</h3>
          <div className="stats-list">
            {Object.entries(stats.porEstado).map(([estado, cantidad]) => (
              <div key={estado} className="stat-item">
                <span className={`envio-estado ${getEstadoClass(estado)}`}>
                  {estado}
                </span>
                <span className="stat-value">{cantidad} envío(s)</span>
                <span className="stat-percentage">
                  {((cantidad / stats.total) * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-section">
          <h3>Envíos por Tipo</h3>
          <div className="stats-list">
            {Object.entries(stats.porTipo).map(([tipo, cantidad]) => (
              <div key={tipo} className="stat-item">
                <span className="stat-label">{tipo}</span>
                <span className="stat-value">{cantidad} envío(s)</span>
                <span className="stat-percentage">
                  {((cantidad / stats.total) * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="dashboard-section">
          <h3>Envíos Recientes</h3>
          <div className="envios-list">
            {envios.slice(-5).reverse().map(envio => (
              <div
                key={envio.id}
                className="envio-card"
                onClick={() => loadEnvioDetails(envio.id)}
                style={{ cursor: 'pointer' }}
              >
                <h3>{envio.id}</h3>
                <div className="envio-card-info">
                  <p><strong>De:</strong> {envio.remitente}</p>
                  <p><strong>Para:</strong> {envio.destinatario}</p>
                  <p><strong>Costo:</strong> ${envio.costo.toFixed(2)}</p>
                  <p>
                    <span className={`envio-estado ${getEstadoClass(envio.estado)}`}>
                      {envio.estado}
                    </span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
}

export default App;