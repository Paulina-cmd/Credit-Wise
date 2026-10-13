// src/pages/Login.jsx
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import "../assets/css/estilos.css";

function Login() {
  const [documento, setDocumento] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Al cargar la página de login, limpiar sesión anterior
  useEffect(() => {
    sessionStorage.clear();
    localStorage.clear();
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    if (!documento || !contrasena) {
      setError("Por favor diligencia todos los campos");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/usuarios/login", {
        documento: documento,
        contrasena: contrasena,
      });

      console.log("Respuesta del servidor:", response.data);

      if (response.data && response.data.usuario) {
        // Guardar ID del usuario en sessionStorage
        sessionStorage.setItem("usuarioId", response.data.usuario.ID);
        navigate("/home");
      } else {
        setError("Credenciales inválidas");
      }
    } catch (error) {
      console.error("Error al iniciar sesión:", error);
      setError(error.response?.data?.detail || "Error al iniciar sesión, intente de nuevo");
    }
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <img src="img/logo.png" alt="Logo CreditWise" />
        <h2>¡La forma divertida, efectiva y gratis</h2>
        <h2>de aprender finanzas!</h2>
      </div>

      <div className="login-right">
        <h1>
          Bienvenido a <span>CreditWise</span>
        </h1>

        {error && <p className="error">{error}</p>}

        <form className="login-form" onSubmit={handleLogin}>
          <div className="input-group">
            <label htmlFor="documento">Documento <span style={{color: 'red'}}>*</span></label>
            <input
              id="documento"
              type="text"
              value={documento}
              onChange={(e) => setDocumento(e.target.value)}
              placeholder="Ingresa tu documento"
            />
          </div>

          <div className="input-group">
            <label htmlFor="contrasena">Contraseña <span style={{color: 'red'}}>*</span></label>
            <input
              id="contrasena"
              type="password"
              value={contrasena}
              onChange={(e) => setContrasena(e.target.value)}
              placeholder="Ingresa tu contraseña"
            />
          </div>

          <button type="submit" className="btn-login">
            Iniciar sesión
          </button>
        </form>

        <div className="login-extra">
          <p>
            ¿No tienes cuenta? <Link to="/registro">Regístrate</Link>
          </p>
          <p>
            <Link to="/recuperar-contrasena">¿Olvidaste tu contraseña?</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
