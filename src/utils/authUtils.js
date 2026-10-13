/**
 * AUTH UTILITIES
 * Funciones centralizadas para manejar autenticación y sesión
 */

/**
 * Verifica si hay una sesión activa
 */
export const isAuthenticated = () => {
  try {
    const usuarioId = sessionStorage.getItem('usuarioId');
    return usuarioId !== null && usuarioId !== undefined && usuarioId !== '';
  } catch (e) {
    console.error('Error checking authentication:', e);
    return false;
  }
};

/**
 * Obtiene el ID del usuario autenticado
 */
export const getUserId = () => {
  try {
    return sessionStorage.getItem('usuarioId');
  } catch (e) {
    return null;
  }
};

/**
 * Guarda los datos de sesión del usuario
 */
export const setUserSession = (usuario) => {
  try {
    if (usuario && usuario.ID) {
      // Limpiar primero cualquier sesión anterior
      clearUserSession();
      
      // Guardar datos del usuario
      sessionStorage.setItem('usuarioId', usuario.ID.toString());
      sessionStorage.setItem('usuarioNombre', usuario.Nombre || '');
      sessionStorage.setItem('usuarioDocumento', usuario.Documento || '');
      sessionStorage.setItem('sessionStart', Date.now().toString());
      
      console.log('Sesión iniciada para usuario:', usuario.ID);
    }
  } catch (e) {
    console.error('Error setting user session:', e);
  }
};

/**
 * Limpia completamente la sesión del usuario
 * Esto es lo que se ejecuta en el logout
 */
export const clearUserSession = () => {
  try {
    // 1. Limpiar sessionStorage (almacenamiento por pestaña/sesión)
    sessionStorage.clear();
    
    // 2. Limpiar localStorage (almacenamiento persistente)
    localStorage.clear();
    
    // 3. Limpiar todas las cookies
    document.cookie.split(";").forEach((c) => {
      const cookieName = c.split("=")[0].trim();
      if (cookieName) {
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
      }
    });
    
    console.log('Sesión limpiada completamente');
  } catch (e) {
    console.error('Error clearing session:', e);
  }
};

/**
 * Logout completo
 * Limpia sesión y redirige a login
 */
export const logout = () => {
  clearUserSession();
  window.location.href = '/login';
};

export default {
  isAuthenticated,
  getUserId,
  setUserSession,
  clearUserSession,
  logout
};
