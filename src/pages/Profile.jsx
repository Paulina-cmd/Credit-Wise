import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import MenuMas from "../components/MenuMas";
import "../assets/css/estilos.css";

function Profile() {
  const [usuario, setUsuario] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const obtenerDatosUsuario = async () => {
      try {
        setLoading(true);
        const usuarioId = sessionStorage.getItem('usuarioId');
        if (!usuarioId) {
          navigate('/login');
          return;
        }

        const response = await fetch(`http://localhost:8000/usuarios/${usuarioId}`);
        if (!response.ok) throw new Error("Error al obtener usuario");
        
        const data = await response.json();
        if (data.success) {
          setUsuario(data.data);
          setError(null);
        } else {
          throw new Error("No se pudo cargar el perfil");
        }
      } catch (err) {
        console.error("Error al obtener perfil:", err);
        setError(err.message || "Error al cargar el perfil");
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };

    obtenerDatosUsuario();

    const handleStorageChange = () => {
      // Volver a cargar perfil cuando hay cambios en puntuación/progreso
      obtenerDatosUsuario();
    };
    window.addEventListener('localStorageChange', handleStorageChange);
    return () => window.removeEventListener('localStorageChange', handleStorageChange);
  }, [navigate]);

  if (error) return <p className="error">{error}</p>;
  if (loading || !usuario) return <p className="loading">Cargando perfil...</p>;

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
          <Link to="/history">
            <img src="/img/historial-de-transacciones.png" alt="Historial" className="icon" /> Historial
          </Link>
          <Link to="/profile" className="active">
            <img src="/img/usuario.png" alt="Perfil" className="icon" /> Perfil
          </Link>
        </nav>
        <MenuMas />
      </aside>

      <main className="main-content content-appear">
        <header className="header">
          <h1>Perfil</h1>
        </header>

        <section className="perfil-section">
          <div className="header-perfil card-appear">
            <img
              src={usuario.FotoPerfil || "/img/icono.jpg"}
              alt="Foto perfil"
              className="foto-perfil"
            />
          </div>

          <div className="datos-usuario card-appear">
            <h2>{usuario.Nombre || "Usuario"}</h2>
            <p className="alias">@{usuario.Usuario || "usuario"}</p>
            <p className="fecha">Se unió en {new Date(usuario.FechaRegistro).toLocaleDateString('es-ES') || "N/A"}</p>
          </div>

          <div className="resumen-estadisticas">
            <div className="item-resumen card-appear stagger-item">
              <p className="dato">
                {usuario.PuntajeCrediticio || 0}
                <img src="/img/cortafuegos.png" alt="Escudo" className="icono-mini" />
              </p>
              <p className="etiqueta">Puntaje Crédito</p>
            </div>

            <div className="item-resumen card-appear stagger-item">
              <p className="dato">
                {usuario.NivelProgreso || 1}
                <img src="/img/diamante-de-pera.png" alt="Gema" className="icono-mini" />
              </p>
              <p className="etiqueta">Nivel</p>
            </div>

            <div className="item-resumen card-appear stagger-item">
              <p className="dato">
                7
                <img src="/img/fuego.png" alt="Fuego" className="icono-mini" />
              </p>
              <p className="etiqueta">Racha de días</p>
            </div>

            <div className="item-resumen card-appear stagger-item">
              <p className="dato">
                24
                <img src="/img/destello.png" alt="Rayo" className="icono-mini" />
              </p>
              <p className="etiqueta">Hoy completado</p>
            </div>
          </div>

          {/* Información adicional de progreso */}
          <div className="progreso-extra card-appear">
            <h3>📊 Tu información</h3>
            <div className="stats-progreso">
              <div className="stat-progreso">
                <span>Email:</span>
                <strong>{usuario.Email || "N/A"}</strong>
              </div>
              <div className="stat-progreso">
                <span>Teléfono:</span>
                <strong>{usuario.Telefono || "N/A"}</strong>
              </div>
              <div className="stat-progreso">
                <span>Puntaje de Crédito:</span>
                <strong>{usuario.PuntajeCrediticio || 0}</strong>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Profile;