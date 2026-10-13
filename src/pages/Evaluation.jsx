import React, { useState, useEffect } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import MenuMas from "../components/MenuMas";
import "../assets/css/estilos.css";

export default function Evaluation() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [evaluacion, setEvaluacion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  

  // 🔵 Cargar evaluación desde la base de datos
  useEffect(() => {
    const cargarEvaluaciones = async () => {
      try {
        setLoading(true);

        const usuarioId = sessionStorage.getItem('usuarioId');

        if (id) {
          // Traer evaluación específica
          const resp = await fetch(`http://localhost:8000/evaluaciones/${id}`);
          if (!resp.ok) throw new Error('Error al obtener la evaluación');
          const json = await resp.json();
          setEvaluacion(json.data);
          setError(null);
        } else {
          // Traer todas las evaluaciones y mostrar las del usuario si existe
          const resp = await fetch('http://localhost:8000/evaluaciones/');
          if (!resp.ok) throw new Error('Error al obtener evaluaciones');
          const json = await resp.json();
          let list = Array.isArray(json.data) ? json.data : [];
          if (usuarioId) {
            list = list.filter(e => (e.UsuarioID == usuarioId) || (e.usuario_id == usuarioId) );
          }
          setEvaluacion(list);
          setError(null);
        }
      } catch (err) {
        console.error('Error cargando evaluaciones:', err);
        setError(err.message || 'Error al cargar evaluaciones');
      } finally {
        setLoading(false);
      }
    };

    cargarEvaluaciones();
  }, [id]);

  // Nota: el manejo de respuestas se realiza en `EvaluationQuiz.jsx`.
  // Preparar lista por misión y estado (evitar duplicados)
  let listaPorMision = [];
  if (Array.isArray(evaluacion)) {
    const usuarioId = sessionStorage.getItem('usuarioId');
    const mapa = new Map();
    evaluacion.forEach(ev => {
      const mid = ev.MisionID || ev.misionid || ev.MisionId;
      if (!mid) return;
      const exists = mapa.get(mid);
      const isCompleted = (ev.UsuarioID && usuarioId && ev.UsuarioID == usuarioId) || (ev.usuario_id && usuarioId && ev.usuario_id == usuarioId);
      if (!exists) {
        mapa.set(mid, { ev, completed: !!isCompleted });
      } else {
        // Prioriza estado completado si alguno lo indica
        if (isCompleted && !exists.completed) {
          mapa.set(mid, { ev, completed: true });
        }
      }
    });
    listaPorMision = Array.from(mapa.values()).map(x => ({ ...x.ev, completed: x.completed }));
    // Ordenar: disponibles (no completadas) primero
    listaPorMision.sort((a, b) => (a.completed === b.completed ? 0 : a.completed ? 1 : -1));
  }

  return (
    <div className="app-container page-transition">
      {/* Sidebar */}
      <aside className="sidebar sidebar-appear">
        <h2 className="logo">CreditWise</h2>
        <nav>
          <Link to="/home">
            <img src="/img/hogar.png" alt="Inicio" className="icon" /> Inicio
          </Link>
          <Link to="/missions" className="active">
            <img src="/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Misiones
          </Link>
          <Link to="/dollar">
            <img src="/img/inversion.png" alt="Dólar" className="icon" /> Dólar
          </Link>
          <Link to="/recommendation">
            <img src="/img/recomendacion.png" alt="Recomendaciones" className="icon" /> Recomendaciones
          </Link>
          <Link to="/history">
            <img src="/img/historial-de-transacciones.png" alt="Historial" className="icon" /> Historial
          </Link>
          <Link to="/profile">
            <img src="/img/usuario.png" alt="Perfil" className="icon" /> Perfil
          </Link>
          <MenuMas />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content content-appear">
        <header className="header">
          <h1>Evaluación</h1>
          <button className="btn btn-hover" onClick={() => navigate("/missions")}>
            ← Volver a Misiones
          </button>
        </header>

        {loading ? (
          <div className="card-appear" style={{ textAlign: 'center', padding: '40px' }}>
            <p>Cargando evaluaciones...</p>
          </div>
        ) : error ? (
          <div className="card-appear" style={{ textAlign: 'center', padding: '40px', color: 'red' }}>
            <p>{error}</p>
            <button className="btn btn-hover" onClick={() => navigate('/missions')}>Volver a Misiones</button>
          </div>
        ) : Array.isArray(evaluacion) ? (
          <div className="evaluation-list">
            {listaPorMision.length === 0 ? (
              <div className="empty-state">
                <p>No tienes evaluaciones registradas aún.</p>
                <Link to="/missions" className="btn btn-hover">Ir a Misiones</Link>
              </div>
            ) : (
              listaPorMision.map((ev) => {
                const mid = ev.MisionID || ev.misionid || ev.MisionId;
                const isBlocked = ev.Bloqueada || ev.bloqueada || ev.bloqueo || false;
                const completed = !!ev.completed;
                return (
                <div key={mid} className="evaluation-card card-appear">
                  <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                    <h3 style={{ margin: 0 }}>{ev.MisionTitulo || ev.Titulo || `Misión ${mid}`}</h3>
                    <span className={`evaluation-status ${completed ? 'completada' : (isBlocked ? 'bloqueada' : 'disponible')}`}>{completed ? 'Completada' : (isBlocked ? 'Bloqueada' : 'Disponible')}</span>
                  </div>
                  <p className="evaluation-meta">{ev.Descripcion || ev.Feedback || ''}</p>
                  <div className="evaluation-actions">
                    {completed ? (
                      <Link to={`/evaluaciones/${ev.ID || ev.id || ''}`} className="btn btn-outline">Ver detalle</Link>
                    ) : isBlocked ? (
                      <button className="btn btn-outline" disabled>Requiere desbloqueo</button>
                    ) : (
                      <Link to={`/evaluation-quiz?misionId=${mid}`} className="btn btn-hover">Realizar evaluación</Link>
                    )}
                    <Link to={`/missions`} className="btn btn-outline">Ver misión</Link>
                  </div>
                </div>
                )
              })
            )}
          </div>
        ) : (
          // Caso: evaluacion es un objeto único
          <div className="evaluation-container card-appear">
            <h2>{evaluacion.Titulo || 'Evaluación'}</h2>
            <p className="evaluation-scenario">{evaluacion.Descripcion || evaluacion.Escenario || 'Sin descripción'}</p>
          </div>
        )}
      </main>
    </div>
  );
}
