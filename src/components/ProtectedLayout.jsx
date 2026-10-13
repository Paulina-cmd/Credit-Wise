import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import { isAuthenticated } from "../utils/authUtils";

/**
 * ProtectedLayout
 * Componente que envuelve las páginas protegidas con Navbar y verificación de sesión
 */
function ProtectedLayout({ children }) {
  const navigate = useNavigate();

  useEffect(() => {
    // Verificar si hay sesión activa
    if (!isAuthenticated()) {
      // Si no hay sesión, redirigir al login
      window.location.href = "/login";
    }
  }, [navigate]);

  if (!isAuthenticated()) {
    return null; // No renderizar nada si no hay autenticación
  }

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Navbar />
      <div style={{ flex: 1 }}>
        {children}
      </div>
    </div>
  );
}

export default ProtectedLayout;
