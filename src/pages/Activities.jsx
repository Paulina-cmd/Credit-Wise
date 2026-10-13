import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import MenuMas from "../components/MenuMas";
import "../assets/css/estilos.css";

export default function Actividades() {
  const [actividades, setActividades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updatingId, setUpdatingId] = useState(null);
  const [mensaje, setMensaje] = useState(null);

  useEffect(() => {
    const cargarActividades = async () => {
      try {
        setLoading(true);
        const usuarioId = sessionStorage.getItem('usuarioId');
        
        if (!usuarioId) {
          setError("No hay usuario autenticado");
          setLoading(false);
          return;
        }

        // Traer actividades del usuario
        const response = await fetch(`http://localhost:8000/actividades/usuario/${usuarioId}`);
        if (!response.ok) throw new Error("Error al obtener actividades");
        
        const data = await response.json();
        if (data.success && data.data) {
          const actividades = data.data.map(act => ({
            id: act.ID || act.IDActividad,
            titulo: act.Titulo || act.titulo || "Actividad",
            descripcion: act.Descripcion || act.descripcion || "Actividad sin descripción",
            completada: act.Completada === 1 || act.Completada === true,
            misionId: act.MisionID
          }));
          setActividades(actividades);
        } else {
          setActividades([]);
        }
        setError(null);
      } catch (err) {
        console.error("Error cargando actividades:", err);
        setError(err.message || "Error al cargar actividades");
        setActividades([]);
      } finally {
        setLoading(false);
      }
    };

    cargarActividades();
  }, []);

  const completadas = actividades.filter((a) => a.completada).length;

  const handleMarcar = async (act) => {
    // Solo marcar si no está completada y no hay otra actualización en curso
    if (act.completada || updatingId) return;

    const usuarioId = sessionStorage.getItem('usuarioId');
    if (!usuarioId) {
      setMensaje({ tipo: 'error', texto: 'Usuario no autenticado' });
      return;
    }

    try {
      setUpdatingId(act.id);
      // Optimistic UI: marcar localmente
      setActividades((prev) => prev.map(a => a.id === act.id ? { ...a, completada: true } : a));

      // Llamada para marcar completada en backend
      const resp = await fetch(`http://localhost:8000/actividades/${act.id}/usuario/${usuarioId}`, {
        method: 'PUT'
      });

      if (!resp.ok) throw new Error('Error marcando actividad');

      // Obtener usuario y actualizar puntaje (recompensa local: +10 pts)
      const userResp = await fetch(`http://localhost:8000/usuarios/${usuarioId}`);
      if (!userResp.ok) throw new Error('Error obteniendo usuario para recompensa');
      const userJson = await userResp.json();
      const userData = userJson.data || userJson.usuario || userJson;

      // Mapear propiedades que pueden venir en mayúsculas desde el backend
      const nombre = userData.Nombre || userData.nombre || '';
      const contrasena = userData.Contrasena || userData.contrasena || '';
      const documento = userData.Documento || userData.documento || '';
      const puntajeActual = Number(userData.PuntajeCrediticio ?? userData.puntaje ?? 0);
      const nivel = Number(userData.NivelProgreso ?? userData.nivel ?? 0);
      const rol = userData.RolID ?? userData.rolID ?? 2;

      const nuevoPuntaje = puntajeActual + 10;

      // Enviar PUT para actualizar puntaje
      const putPayload = {
        nombre,
        contrasena,
        documento,
        PuntajeCrediticio: nuevoPuntaje,
        NivelProgreso: nivel,
        RolID: rol
      };

      const updateResp = await fetch(`http://localhost:8000/usuarios/${usuarioId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(putPayload)
      });

      if (!updateResp.ok) {
        // No abortar flow si no se pudo actualizar puntaje; mostrar aviso
        console.warn('No se pudo actualizar puntaje via PUT usuarios');
        setMensaje({ tipo: 'info', texto: 'Actividad marcada. Puntaje será actualizado pronto.' });
      } else {
        setMensaje({ tipo: 'exito', texto: '+10 puntos añadidos' });
      }

      // Forzar recarga en otras páginas
      window.dispatchEvent(new Event('localStorageChange'));

      // Refrescar lista de actividades desde backend para evitar desincronía
      const lista = await fetch(`http://localhost:8000/actividades/usuario/${usuarioId}`);
      if (lista.ok) {
        const listaJson = await lista.json();
        if (listaJson.success && listaJson.data) {
          const actividadesMapeadas = listaJson.data.map(actdb => ({
            id: actdb.ID || actdb.IDActividad || actdb.ActividadID,
            titulo: actdb.Titulo || actdb.titulo || actdb.Titulo || 'Actividad',
            descripcion: actdb.Descripcion || actdb.descripcion || actdb.Contenido || '',
            completada: actdb.Completada === 1 || actdb.Completada === true,
            misionId: actdb.MisionID
          }));
          setActividades(actividadesMapeadas);
        }
      }

    } catch (err) {
      console.error('Error al marcar actividad:', err);
      setMensaje({ tipo: 'error', texto: 'No se pudo marcar la actividad. Intenta de nuevo.' });
      // Revertir optimistic UI
      setActividades((prev) => prev.map(a => a.id === act.id ? { ...a, completada: false } : a));
    } finally {
      setUpdatingId(null);
      // limpiar el mensaje después de 2.6s
      setTimeout(() => setMensaje(null), 2600);
    }
  };

  if (loading) {
    return (
      <div className="app-container page-transition">
        <aside className="sidebar sidebar-appear">
          <h2 className="logo">CreditWise</h2>
          <nav>
            <Link to="/home"><img src="/img/hogar.png" alt="Inicio" className="icon" /> Inicio</Link>
            <Link to="/missions"><img src="/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Misiones</Link>
            <Link to="/dollar"><img src="/img/inversion.png" alt="Dólar" className="icon" /> Dólar</Link>
            <Link to="/recommendation"><img src="/img/recomendacion.png" alt="Recomendaciones" className="icon" /> Recomendaciones</Link>
            <Link to="/history"><img src="/img/historial-de-transacciones.png" alt="Historial" className="icon" /> Historial</Link>
            <Link to="/profile"><img src="/img/usuario.png" alt="Perfil" className="icon" /> Perfil</Link>
            <MenuMas />
          </nav>
        </aside>
        <main className="main-content content-appear">
          <p>Cargando actividades...</p>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container page-transition">
        <aside className="sidebar sidebar-appear">
          <h2 className="logo">CreditWise</h2>
          <nav>
            <Link to="/home"><img src="/img/hogar.png" alt="Inicio" className="icon" /> Inicio</Link>
            <Link to="/missions"><img src="/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Misiones</Link>
            <Link to="/dollar"><img src="/img/inversion.png" alt="Dólar" className="icon" /> Dólar</Link>
            <Link to="/recommendation"><img src="/img/recomendacion.png" alt="Recomendaciones" className="icon" /> Recomendaciones</Link>
            <Link to="/history"><img src="/img/historial-de-transacciones.png" alt="Historial" className="icon" /> Historial</Link>
            <Link to="/profile"><img src="/img/usuario.png" alt="Perfil" className="icon" /> Perfil</Link>
            <MenuMas />
          </nav>
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
          <Link to="/home"><img src="/img/hogar.png" alt="Inicio" className="icon" /> Inicio</Link>
          <Link to="/missions"><img src="/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Misiones</Link>
          <Link to="/dollar"><img src="/img/inversion.png" alt="Dólar" className="icon" /> Dólar</Link>
          <Link to="/recommendation"><img src="/img/recomendacion.png" alt="Recomendaciones" className="icon" /> Recomendaciones</Link>
          <Link to="/history"><img src="/img/historial-de-transacciones.png" alt="Historial" className="icon" /> Historial</Link>
          <Link to="/profile"><img src="/img/usuario.png" alt="Perfil" className="icon" /> Perfil</Link>
          <MenuMas />
        </nav>
      </aside>

      {/* Contenido principal */}
      <main className="main-content content-appear">
        <div className="actividades-header">
          <div>
            <h1>Mis Actividades</h1>
            <p className="subtitulo-actividades">
              Completa tus misiones y evaluaciones para marcar tu progreso.
            </p>
          </div>
          <div className="contador-actividades">
            <span>
              <strong>{completadas}</strong> de {actividades.length} completadas
            </span>
            <span className="emoji-check">✅</span>
          </div>
        </div>
        {mensaje && (
          <div className={`mensaje ${mensaje.tipo === 'exito' ? 'exito' : mensaje.tipo === 'error' ? 'error' : ''}`}>
            {mensaje.texto}
          </div>
        )}

        <section className="actividades-checklist">
          {actividades.map((act) => (
            <label
              key={act.id}
              className={`actividad-item-check ${act.completada ? "completada" : ""} ${updatingId === act.id ? 'updating' : ''}`}
            >
              <input
                type="checkbox"
                checked={act.completada}
                onChange={() => handleMarcar(act)}
                disabled={act.completada || updatingId !== null}
              />
              <div className="actividad-texto">
                <h3>{act.titulo}</h3>
                <p>{act.descripcion}</p>
              </div>
              <div className="actividad-meta">
                {act.completada ? <span className="badge puntos">Completada</span> : <span className="hint">Toca para completar</span>}
              </div>
            </label>
          ))}
        </section>
      </main>
    </div>
  );
}





