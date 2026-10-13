import React from "react";
import { NavLink } from "react-router-dom";

function Navbar() {
  const handleLogout = () => {
    // PASO 1: Borrar TODO
    sessionStorage.clear();
    localStorage.clear();
    
    // PASO 2: Reemplazar el historial actual con login
    window.history.pushState(null, null, "/login");
    
    // PASO 3: Hacer que el botón back no funcione
    window.onpopstate = function() {
      window.history.pushState(null, null, "/login");
    };
    
    // PASO 4: Redirigir
    window.location.href = "/login";
  };

  return (
    <nav className="sidebar">
      <div className="logo">
        <img src="/assets/img/logo.png" alt="CreditWise" className="logo-nav" />
      </div>
      <nav>
        <NavLink to="/home" className={({ isActive }) => (isActive ? "active" : "")}>
          <img src="/assets/img/hogar.png" alt="Inicio" className="icon" /> Home
        </NavLink>
        <NavLink to="/missions" className={({ isActive }) => (isActive ? "active" : "")}>
          <img src="/assets/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Missions
        </NavLink>
        <NavLink to="/dollar" className={({ isActive }) => (isActive ? "active" : "")}>
          <img src="/assets/img/inversion.png" alt="Dólar" className="icon" /> Dollar
        </NavLink>
        <NavLink to="/recommendation" className={({ isActive }) => (isActive ? "active" : "")}>
          <img src="/assets/img/recomendacion.png" alt="Recomendación" className="icon" /> Recommendation
        </NavLink>
        <NavLink to="/history" className={({ isActive }) => (isActive ? "active" : "")}>
          <img src="/assets/img/historial-de-transacciones.png" alt="Historial" className="icon" /> History
        </NavLink>
        <NavLink to="/profile" className={({ isActive }) => (isActive ? "active" : "")}>
          <img src="/assets/img/usuario.png" alt="Perfil" className="icon" /> Profile
        </NavLink>
        <NavLink to="/achievements" className={({ isActive }) => (isActive ? "active" : "")}>
          <img src="/assets/img/medalla.png" alt="Logros" className="icon" /> Achievements
        </NavLink>
        <button 
          onClick={handleLogout} 
          style={{
            width: "100%",
            padding: "12px",
            marginTop: "20px",
            backgroundColor: "#ff6b6b",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "14px",
            fontWeight: "bold",
            transition: "background-color 0.3s ease"
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = "#ee5a5a"}
          onMouseOut={(e) => e.target.style.backgroundColor = "#ff6b6b"}
          title="Cerrar sesión"
        >
          🚪 Cerrar Sesión
        </button>
      </nav>
    </nav>
  );
}

export default Navbar;

