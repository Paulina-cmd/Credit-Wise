import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import MenuMas from "../components/MenuMas";
import "../assets/css/estilos.css";

const History = () => {
  const [historial, setHistorial] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const cargarHistorial = async () => {
      try {
        setLoading(true);
        const usuarioId = sessionStorage.getItem('usuarioId');
        
        console.log("📍 usuarioId desde sessionStorage:", usuarioId);
        
        if (!usuarioId) {
          setError("No hay usuario autenticado. Por favor inicia sesión.");
          setLoading(false);
          return;
        }

        // Traer historial de misiones completadas
        const responseMisiones = await fetch(`http://localhost:8000/historial/usuario/${usuarioId}`);
        if (!responseMisiones.ok) throw new Error("Error al obtener historial de misiones");
        
        const dataMisiones = await responseMisiones.json();
        console.log("📊 Respuesta del historial (completa):", JSON.stringify(dataMisiones, null, 2));
        console.log("📊 dataMisiones.success:", dataMisiones.success);
        console.log("📊 dataMisiones.data:", dataMisiones.data);

        // Traer evaluaciones completadas (opcional, puede no devolver datos del usuario específico)
        let evaluaciones = [];
        try {
          const responseEvaluaciones = await fetch(`http://localhost:8000/evaluaciones/`);
          if (responseEvaluaciones.ok) {
            const dataEval = await responseEvaluaciones.json();
            if (dataEval.data) {
              evaluaciones = dataEval.data.filter(e => e.UsuarioID == usuarioId || e.usuario_id == usuarioId);
            }
          }
        } catch (e) {
          console.warn("⚠️ No se pudo cargar evaluaciones:", e);
        }

        // Mapear historial de misiones
        let historialCompleto = [];
        
        if (dataMisiones.success && dataMisiones.data && dataMisiones.data.length > 0) {
          historialCompleto = dataMisiones.data.map(item => {
            console.log("🔹 Item del historial:", item);
            return {
              id: `mision-${item.ID}`,
              tipo: "mision-completada",
              titulo: `🎯 ${item.MisionTitulo || 'Misión Completada'}`,
              descripcion: `Misión completada - ${item.Dificultad || 'N/A'}`,
              fecha: item.FechaCompletado ? new Date(item.FechaCompletado).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              }) : new Date().toLocaleDateString('es-ES'),
              puntos: item.PuntosObtenidos || 0,
              exp: (item.PuntosObtenidos || 0) * 2,
              icono: "✅"
            };
          });
        } else {
          console.warn("⚠️ No hay datos de historial o respuesta inválida:", dataMisiones);
        }

        // Mapear evaluaciones completadas
        const historialEvaluaciones = evaluaciones.map(item => ({
          id: `evaluacion-${item.ID}`,
          tipo: "evaluacion-completada",
          titulo: `📝 ${item.Titulo || 'Evaluación Completada'}`,
          descripcion: `Resultado: ${item.Resultado || 'Completada'}`,
          fecha: item.FechaCreacion ? new Date(item.FechaCreacion).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          }) : new Date().toLocaleDateString('es-ES'),
          puntos: item.PuntajeObtenido || 0,
          exp: item.PuntajeObtenido ? item.PuntajeObtenido * 1.5 : 0,
          icono: "📊"
        }));

        // Combinar y ordenar por fecha
        historialCompleto = [...historialCompleto, ...historialEvaluaciones].sort((a, b) => {
          const dateA = new Date(a.fecha);
          const dateB = new Date(b.fecha);
          return dateB - dateA;
        });

        console.log("✅ Historial completo procesado:", historialCompleto);
        setHistorial(historialCompleto);
        setError(null);
      } catch (err) {
        console.error("❌ Error cargando historial:", err);
        setError(err.message || "Error al cargar el historial");
      } finally {
        setLoading(false);
      }
    };

    cargarHistorial();

    // Escuchar cambios en localStorage para recargar si se completa una misión
    const handleStorageChange = () => {
      console.log("📢 Cambio detectado, recargando historial...");
      cargarHistorial();
    };

    window.addEventListener('localStorageChange', handleStorageChange);
    return () => window.removeEventListener('localStorageChange', handleStorageChange);
  }, []);

  return (
    <div className="app-container page-transition">
      <aside className="sidebar sidebar-appear">
        <h2 className="logo">CreditWise</h2>
        <nav>
          <Link to="/home">
            <img src="/img/hogar.png" alt="Inicio" className="icon" /> Inicio
          </Link>
          <Link to="/missions">
            <img src="/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Misiones
          </Link>
          <Link to="/dollar">
            <img src="/img/inversion.png" alt="Dólar" className="icon" /> Dólar
          </Link>
          <Link to="/recommendation">
            <img src="/img/recomendacion.png" alt="Recomendaciones" className="icon" /> Recomendaciones
          </Link>
          <Link to="/history" className="active">
            <img src="/img/historial-de-transacciones.png" alt="Historial" className="icon" /> Historial
          </Link>
          <Link to="/profile">
            <img src="/img/usuario.png" alt="Perfil" className="icon" /> Perfil
          </Link>
          <MenuMas />
        </nav>
      </aside>

      <main className="main-content content-appear">
        <header className="header">
          <h1>Historial de Actividad</h1>
          <button 
            onClick={() => window.location.reload()} 
            className="btn btn-hover"
            style={{marginLeft: 'auto'}}
          >
            🔄 Actualizar
          </button>
        </header>

        <section className="historial-container">
          {loading ? (
            <p className="loading-text">Cargando historial...</p>
          ) : error ? (
            <div className="empty-state stagger-item">
              <p style={{ color: "red" }}>{error}</p>
              <Link to="/missions" className="btn btn-hover">
                Volver a Misiones
              </Link>
            </div>
          ) : historial.length === 0 ? (
            <div className="empty-state stagger-item">
              <p>No hay actividad registrada aún.</p>
              <p>¡Completa misiones para ver tu progreso aquí!</p>
              <Link to="/missions" className="btn btn-hover">
                Comenzar misiones
              </Link>
            </div>
          ) : (
            <div className="history-grid">
              {historial.map((item, index) => (
                <article key={item.id || index} className={`history-card ${item.tipo === 'mision-completada' ? 'history-mision' : 'history-evaluacion'}`}>
                  <div className="history-left">
                    <div className="history-icon">{item.icono || '📌'}</div>
                  </div>
                  <div className="history-main">
                    <div className="history-row">
                      <h3 className="history-title">{item.titulo}</h3>
                      <div className="history-badges">
                        {item.puntos > 0 && <span className="badge points">+{item.puntos} pts</span>}
                        {item.exp > 0 && <span className="badge exp">+{item.exp.toFixed(0)} EXP</span>}
                      </div>
                    </div>
                    <p className="history-desc">{item.descripcion}</p>
                    <div className="history-meta">
                      <time className="history-date">{item.fecha}</time>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
};

export default History;