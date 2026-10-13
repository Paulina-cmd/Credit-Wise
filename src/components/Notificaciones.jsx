// src/components/Notificaciones.jsx
import { useState, useEffect, useRef } from "react";
import "../assets/css/estilos.css";

const Notificaciones = () => {
  const [open, setOpen] = useState(false);
  const [notificaciones, setNotificaciones] = useState([]);
  const [nuevas, setNuevas] = useState(false);
  const ref = useRef();

  // Simula notificaciones cargadas desde BD
  useEffect(() => {
    const demoNotifs = [
      { id: 1, mensaje: "Has completado la misión diaria", leida: false },
      { id: 2, mensaje: "Nuevo consejo financiero disponible", leida: false },
      { id: 3, mensaje: "Tu puntaje de crédito ha mejorado", leida: false },
    ];
    setNotificaciones(demoNotifs);
    setNuevas(demoNotifs.some(n => !n.leida));
  }, []);

  // Cerrar al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const toggleOpen = () => {
    setOpen(!open);
    // Marcar todas como leídas al abrir
    if (!open) {
      const leidas = notificaciones.map(n => ({ ...n, leida: true }));
      setNotificaciones(leidas);
      setNuevas(false);
    }
  };

  return (
    <div className="notificaciones-container" ref={ref}>
      <button className="btn-icon" onClick={toggleOpen} style={{ position: "relative" }}>
        <img src="/img/campana.png" alt="Notificaciones" />
        {nuevas && <span className="notif-dot"></span>}
      </button>

      {open && (
        <div className="notif-panel">
          {notificaciones.length === 0 ? (
            <p className="notif-empty">No tienes notificaciones</p>
          ) : (
            notificaciones.map(n => (
              <div key={n.id} className={`notif-item ${n.leida ? "leida" : "nueva"}`}>
                {n.mensaje}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default Notificaciones;

