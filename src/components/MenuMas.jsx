import { useState } from "react";
import { useNavigate } from "react-router-dom";


const MenuMas = () => {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    //Limpiar localStorage
    localStorage.removeItem("usuario");
    localStorage.removeItem("progreso");

    // Redirigir al login
    navigate("/");
  };

  return (
    <div className="menu-mas">
      <button 
        onClick={() => setOpen(!open)} 
        className="btn-mas"
      >
        <img src="/img/mass.png" alt="Más" className="icon" /> Más
      </button>

      {open && (
        <div className="dropdown-mas">
          <hr />
<a
  href="/Manual/index.html"
  target="_blank"
  rel="noopener noreferrer"
  className="dropdown-item"
>
  <img src="/img/signo-de-interrogacion.png" alt="Ayuda" className="icon" /> Ayuda
</a>

          <div 
            className="dropdown-item salir" 
            onClick={handleLogout}
          >
            <img src="/img/cerrar-sesion.png" alt="Salir" className="icon" /> Cerrar sesión
          </div>
        </div>
      )}
    </div>
  );
};

export default MenuMas;

