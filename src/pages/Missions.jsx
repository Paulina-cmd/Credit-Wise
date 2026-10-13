import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import MenuMas from "../components/MenuMas";
import "../assets/css/estilos.css";

export default function Missions() {
  const navigate = useNavigate();
  const [misiones, setMisiones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedMision, setSelectedMision] = useState(null);

  // 🔵 Cargar misiones desde la base de datos
  useEffect(() => {
    const cargarMisiones = async () => {
      try {
        setLoading(true);
        const usuarioId = sessionStorage.getItem('usuarioId');
        console.log("👤 usuarioId actual:", usuarioId);

        const response = await fetch("http://localhost:8000/misiones");
        if (!response.ok) throw new Error("Error al obtener misiones");
        
        const misionesDB = await response.json();
        
        // Mapear datos de BD a formato del componente
        const misionesMapeadas = misionesDB.map((m, index) => ({
          id: m.IDMision || m.ID,
          title: m.Titulo,
          desc: m.Descripcion || "Sin descripción",
          dificultad: m.Dificultad || "Media",
          progress: 0,
          estado: "En progreso",
          clase: "pendiente",
          bloqueada: index > 0, // Primera misión desbloqueada, resto bloqueadas
          recompensa: m.RecompensaPuntos || 0,
        }));

        // Revisar misiones completadas en localStorage (con clave específica del usuario)
        const claveMisiones = `misionesCompletadas_${usuarioId}`;
        const completadas = JSON.parse(localStorage.getItem(claveMisiones)) || [];
        console.log(`📋 Misiones completadas para usuario ${usuarioId}:`, completadas);

        const misionesActualizadas = misionesMapeadas.map((m, index) => {
          if (completadas.includes(m.id)) {
            return { ...m, progress: 100, estado: "Completada", clase: "completada", bloqueada: false };
          }
          // Desbloquear la siguiente misión si la anterior está completada
          if (index > 0 && completadas.includes(misionesMapeadas[index - 1].id)) {
            return { ...m, bloqueada: false, estado: "En progreso", clase: "pendiente" };
          }
          return m;
        });

        setMisiones(misionesActualizadas);
        setError(null);
      } catch (err) {
        console.error("Error cargando misiones:", err);
        setError("Error al cargar las misiones");
      } finally {
        setLoading(false);
      }
    };

    cargarMisiones();

    // Escuchar cambios de localStorage (cuando se complete una misión)
    const handleStorageChange = () => {
      console.log("📢 Cambio en localStorage detectado, recargando misiones...");
      cargarMisiones();
    };

    window.addEventListener('localStorageChange', handleStorageChange);
    return () => window.removeEventListener('localStorageChange', handleStorageChange);
  }, []);

  // 🔵 Nueva función para manejar el click en "Realizar misión"
  const handleRealizarMision = (mision) => {
    // Guardar la misión actual en localStorage para que MissionTask pueda leerla
    localStorage.setItem("misionActual", JSON.stringify(mision));
    // Navegar a la misión
    navigate("/mission-task");
  };

  // Mostrar estado de carga
  if (loading) {
    return (
      <div className="missions-page page-transition">
        <aside className="sidebar sidebar-appear">
          <h2 className="logo">CreditWise</h2>
        </aside>
        <main className="main-content content-appear">
          <header className="header">
            <h1>Misiones</h1>
          </header>
          <section className="misiones">
            <p>Cargando misiones...</p>
          </section>
        </main>
      </div>
    );
  }

  // Mostrar error si hay
  if (error) {
    return (
      <div className="missions-page page-transition">
        <aside className="sidebar sidebar-appear">
          <h2 className="logo">CreditWise</h2>
        </aside>
        <main className="main-content content-appear">
          <header className="header">
            <h1>Misiones</h1>
          </header>
          <section className="misiones">
            <p style={{ color: "red" }}>{error}</p>
          </section>
        </main>
      </div>
    );
  }

  return (
    <div className="missions-page page-transition">
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

      {/* Contenido principal */}
      <main className="main-content content-appear">
        <header className="header">
          <h1>Misiones</h1>
        </header>

        <section className="misiones">
          {misiones.map((mision) => (
            <div
              key={mision.id}
              className={`card mision ${mision.clase} stagger-item`}
              onClick={() => !mision.bloqueada && setSelectedMision(mision)}
            >
              <h3>{mision.title}</h3>
              <p>{mision.desc}</p>

              {/* Barra de progreso */}
              <div className="progress-section">
                <div className="progress-container">
                  <div
                    className={`progress-bar ${mision.bloqueada ? "progress-bar-blocked" : ""}`}
                    style={{ width: `${mision.progress}%` }}
                  ></div>
                </div>
                <span className="progress-text">{mision.progress}%</span>
              </div>

              {/* Estado */}
              <span className={`estado ${mision.bloqueada ? "bloqueada" : "activa"}`}>
                {mision.bloqueada ? "🔒 Bloqueada" : mision.estado}
              </span>
            </div>
          ))}
        </section>
      </main>

      {/* Modal */}
      {selectedMision && (
        <div className="modal-overlay" onClick={() => setSelectedMision(null)}>
          <div className="modal-content modal-appear" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close btn-hover" onClick={() => setSelectedMision(null)}>
              ✖
            </button>
            <h2>{selectedMision.title}</h2>
            <p>{selectedMision.desc}</p>
            <p>
              <strong>Dificultad:</strong> {selectedMision.dificultad}
            </p>
            <button
              className="btn-ingresar btn-hover"
              onClick={() => handleRealizarMision(selectedMision)}
            >
              Realizar misión
            </button>
          </div>
        </div>
      )}
    </div>
  );
}