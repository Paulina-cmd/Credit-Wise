// src/pages/Home.jsx
import { Link, useNavigate } from "react-router-dom";
import MenuMas from "../components/MenuMas";
import { useEffect, useState } from "react";
import "../assets/css/estilos.css";

const Home = () => {
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState(null);
  const [progreso, setProgreso] = useState(0);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const obtenerDatosUsuario = async () => {
      try {
        setLoading(true);
        const usuarioId = sessionStorage.getItem('usuarioId');
        
        if (!usuarioId) {
          setError("No hay sesión activa");
          navigate('/login');
          return;
        }

        const response = await fetch(`http://localhost:8000/usuarios/${usuarioId}`);
        
        if (!response.ok) {
          throw new Error("No se pudo cargar la información del usuario");
        }

        const data = await response.json();
        
        if (data.success) {
          setUsuario(data.data);
          
          const nivelProgreso = Math.min(data.data.NivelProgreso || 1, 20);
          const porcentajeProgreso = (nivelProgreso / 20) * 100;
          setProgreso(Math.round(porcentajeProgreso));
        } else {
          setError("No se pudo cargar la información del usuario");
          navigate('/login');
        }
      } catch (error) {
        console.error("Error al obtener datos:", error);
        setError(error.message || "Error al cargar los datos");
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };

    obtenerDatosUsuario();

    const handleStorageChange = () => {
      obtenerDatosUsuario();
    };
    window.addEventListener('localStorageChange', handleStorageChange);
    return () => window.removeEventListener('localStorageChange', handleStorageChange);
  }, [navigate]);

  if (loading) return <p className="loading">Cargando...</p>;
  if (!usuario) return <p className="error">{error || "Error al cargar datos"}</p>;

  return (
    <div className="app-container page-transition">
      {/* Sidebar */}
      <aside className="sidebar sidebar-appear">
        <h2 className="logo">CreditWise</h2>
        <nav>
          <Link to="/home" className="active">
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
        {/* Encabezado con bienvenida */}
        <div className="home-header card-appear">
          <div className="greeting-container">
            <h1>¡Hola, {usuario.Nombre || "Usuario"}! 👋</h1>
            <p>Bienvenido a tu panel de aprendizaje financiero</p>
          </div>
        </div>

        {/* Tarjeta de estadísticas rápidas */}
        <section className="stats-overview card-appear">
          <div className="stat-card stat-credit">
            <div className="stat-icon">🛡️</div>
            <div className="stat-content">
              <p className="stat-label">Puntaje Crédito</p>
              <p className="stat-value">{usuario.PuntajeCrediticio || 0}</p>
            </div>
          </div>

          <div className="stat-card stat-level">
            <div className="stat-icon">⭐</div>
            <div className="stat-content">
              <p className="stat-label">Nivel</p>
              <p className="stat-value">{usuario.NivelProgreso || 1}</p>
            </div>
          </div>

          <div className="stat-card stat-progress">
            <div className="stat-icon">🚀</div>
            <div className="stat-content">
              <p className="stat-label">Progreso General</p>
              <p className="stat-value">{progreso}%</p>
            </div>
          </div>
        </section>

        {/* Círculo de progreso mejorado */}
        <section className="progress-circle-section card-appear">
          <div className="progress-circle-container">
            <svg className="progress-ring" width="200" height="200">
              <defs>
                <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#9333ea" />
                  <stop offset="100%" stopColor="#c084fc" />
                </linearGradient>
              </defs>
              <circle
                className="progress-ring-circle-bg"
                cx="100"
                cy="100"
                r="90"
              />
              <circle
                className="progress-ring-circle"
                cx="100"
                cy="100"
                r="90"
                style={{
                  strokeDashoffset: 565 - (565 * progreso) / 100
                }}
              />
            </svg>
            <div className="progress-info">
              <h2>{progreso}%</h2>
              <p>Nivel {usuario.NivelProgreso || 1}</p>
            </div>
          </div>
          <div className="progress-text">
            <p>🎯 Continúa completando misiones para subir de nivel</p>
          </div>
        </section>

        {/* Tarjeta de acciones rápidas */}
        <h2 className="section-title">Acciones Rápidas</h2>
        <section className="quick-cards">
          <Link to="/missions" className="quick-card quick-card-missions card-appear stagger-item">
            <div className="quick-card-icon">🎯</div>
            <h3>Misiones</h3>
            <p>Completa desafíos y gana puntos</p>
          </Link>

          <Link to="/evaluation" className="quick-card quick-card-eval card-appear stagger-item">
            <div className="quick-card-icon">📝</div>
            <h3>Evaluaciones</h3>
            <p>Prueba tus conocimientos</p>
          </Link>

          <Link to="/recommendation" className="quick-card quick-card-rec card-appear stagger-item">
            <div className="quick-card-icon">💡</div>
            <h3>Recomendaciones</h3>
            <p>Consejos financieros personalizados</p>
          </Link>

          <Link to="/activities" className="quick-card quick-card-act card-appear stagger-item">
            <div className="quick-card-icon">✅</div>
            <h3>Actividades</h3>
            <p>Tu lista de tareas pendientes</p>
          </Link>
        </section>

        {/* Motivación */}
        <section className="motivation card-appear">
          <div className="motivation-content">
            <h3>💪 ¡Vas muy bien!</h3>
            <p>Has alcanzado el nivel {usuario.NivelProgreso || 1}. Sigue adelante con las misiones para seguir mejorando tu crédito.</p>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Home;
