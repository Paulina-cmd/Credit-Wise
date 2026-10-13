import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import MenuMas from "../components/MenuMas";
import "../assets/css/estilos.css";

const Recommendation = () => {
  const [recomendaciones, setRecomendaciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [recomendacionSeleccionada, setRecomendacionSeleccionada] = useState(null);

  useEffect(() => {
    const cargarRecomendaciones = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://localhost:8000/recomendaciones");
        if (!response.ok) throw new Error("Error al obtener recomendaciones");
        
        const data = await response.json();
        if (data.success && data.data) {
          setRecomendaciones(data.data);
        } else {
          // Recomendaciones por defecto si no hay en BD
          setRecomendaciones([
            {
              ID: 1,
              Titulo: "💰 Crea un fondo de emergencia",
              Descripcion: "Reserva al menos 3 meses de gastos básicos.",
              DescripcionDetallada: "Un fondo de emergencia te protege ante imprevistos como pérdida de empleo, gastos médicos o reparaciones urgentes. Calcula tus gastos mensuales esenciales y multiplica por 3."
            },
            {
              ID: 2,
              Titulo: "💳 Usa máximo el 30% de tu crédito",
              Descripcion: "Protege tu puntaje crediticio.",
              DescripcionDetallada: "Mantener tu utilización de crédito por debajo del 30% demuestra manejo responsable y mejora tu score crediticio. Revisa tus límites y ajusta tu gasto mensual."
            }
          ]);
        }
        setError(null);
      } catch (err) {
        console.error("Error cargando recomendaciones:", err);
        setError("Error al cargar recomendaciones");
      } finally {
        setLoading(false);
      }
    };

    cargarRecomendaciones();
  }, []);

  const abrirDetalle = (recomendacion) => {
    setRecomendacionSeleccionada(recomendacion);
  };

  const cerrarDetalle = () => {
    setRecomendacionSeleccionada(null);
  };

  if (loading) {
    return (
      <div className="app-container page-transition">
        <aside className="sidebar sidebar-appear">
          <h2 className="logo">CreditWise</h2>
        </aside>
        <main className="main-content content-appear">
          <p>Cargando recomendaciones...</p>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container page-transition">
        <aside className="sidebar sidebar-appear">
          <h2 className="logo">CreditWise</h2>
        </aside>
        <main className="main-content content-appear">
          <p style={{ color: "red" }}>{error}</p>
        </main>
      </div>
    );
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
          <Link to="/missions">
            <img src="/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Misiones
          </Link>
          <Link to="/dollar">
            <img src="/img/inversion.png" alt="Dólar" className="icon" /> Dólar
          </Link>
          <Link to="/recommendation" className="active">
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

      {/* Main */}
      <main className="main-content content-appear">
        <header className="header">
          <h1>Recomendaciones Financieras</h1>
        </header>

        <section className="recommendations-intro card-appear">
          <p>Mejora tu salud financiera con estas recomendaciones prácticas.</p>
        </section>

        <div className="recommend-container">
          {recomendaciones.map((rec, index) => (
            <div 
              key={rec.ID || rec.id} 
              className="recommend-card stagger-item btn-hover"
              onClick={() => abrirDetalle(rec)}
              style={{ cursor: 'pointer' }}
            >
              <h3>{rec.Titulo || rec.titulo}</h3>
              <p>{rec.Descripcion || rec.resumen}</p>
            </div>
          ))}
        </div>

        {/* Modal de detalle */}
        {recomendacionSeleccionada && (
          <div className="modal-overlay" onClick={cerrarDetalle}>
            <div className="modal-content modal-appear" onClick={(e) => e.stopPropagation()}>
              <button className="modal-close btn-hover" onClick={cerrarDetalle}>×</button>
              
              <h2>{recomendacionSeleccionada.Titulo || recomendacionSeleccionada.titulo}</h2>

              <div className="recomendacion-detalle">
                <h4>Resumen:</h4>
                <p>{recomendacionSeleccionada.Descripcion || recomendacionSeleccionada.resumen}</p>
                
                <h4>Detalles:</h4>
                <p>{recomendacionSeleccionada.DescripcionDetallada || recomendacionSeleccionada.detalle}</p>
              </div>

              <div className="modal-actions">
                <button className="btn btn-hover" onClick={cerrarDetalle}>
                  Entendido
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Recommendation;