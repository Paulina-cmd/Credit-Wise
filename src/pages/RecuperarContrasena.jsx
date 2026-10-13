import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../assets/css/estilos.css";

export default function RecuperarContrasena() {
  const [documento, setDocumento] = useState("");
  const [nuevaContrasena, setNuevaContrasena] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");

    if (!documento || !nuevaContrasena) {
      setMensaje("⚠️ Por favor completa todos los campos");
      return;
    }

    try {
      setCargando(true);

      // ✅ Endpoint correcto según tu backend
      const response = await axios.put(
        "http://127.0.0.1:8000/recuperacion/restablecer",
        {
          documento: documento.trim(),
          nueva_contrasena: nuevaContrasena.trim(),
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        setMensaje("✅ Contraseña actualizada correctamente.");
        setTimeout(() => navigate("/"), 2000);
      } else {
        setMensaje("❌ No se pudo actualizar la contraseña.");
      }
    } catch (error) {
      console.error("Error al actualizar contraseña:", error);
      if (error.response) {
        setMensaje(error.response.data.detail || "❌ Error desde el servidor");
      } else if (error.request) {
        setMensaje("⚠️ No se pudo conectar con el servidor");
      } else {
        setMensaje("❌ Error inesperado al procesar la solicitud");
      }
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-right">
        <h1>Recuperar contraseña</h1>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="documento">Documento</label>
            <input
              id="documento"
              type="text"
              value={documento}
              onChange={(e) => setDocumento(e.target.value)}
              placeholder="Ingresa tu documento"
            />
          </div>

          <div className="input-group">
            <label htmlFor="nuevaContrasena">Nueva contraseña</label>
            <input
              id="nuevaContrasena"
              type="password"
              value={nuevaContrasena}
              onChange={(e) => setNuevaContrasena(e.target.value)}
              placeholder="Ingresa tu nueva contraseña"
            />
          </div>

          <button type="submit" className="btn-login" disabled={cargando}>
            {cargando ? "Actualizando..." : "Cambiar contraseña"}
          </button>
        </form>

        {mensaje && <p className="mensaje">{mensaje}</p>}
      </div>
    </div>
  );
}
