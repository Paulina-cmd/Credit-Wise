// src/pages/Terminos.jsx
import "../assets/css/estilos.css";

function Terminos() {
  return (
    <div className="app-container">
      <main className="main-content">
        <header className="header">
          <h1>Términos y Condiciones</h1>
        </header>

        <section className="terminos-section">
          <div className="terminos-card">
            <p>
              <strong>Fecha de última actualización:</strong> 16/09/2025
            </p>

            <h2>1. Aceptación de los Términos</h2>
            <p>
              Al descargar, acceder o utilizar la aplicación móvil CreditWise
              (en adelante, "la Aplicación" o "el Servicio"), propiedad de
              CreditWise ("nosotros", "nuestro"), usted ("Usuario") acepta
              quedar vinculado por estos Términos y Condiciones de Uso y por
              nuestra Política de Privacidad. Si no está de acuerdo con alguno
              de estos términos, no podrá utilizar nuestra Aplicación.
            </p>

            <h2>2. Definición del Servicio</h2>
            <p>
              CreditWise es una plataforma educativa e interactiva diseñada
              para ofrecer:
            </p>
            <ul>
              <li>Educación financiera y crediticia mediante misiones y simulaciones.</li>
              <li>Seguimiento y gamificación: progreso, metas, logros y niveles.</li>
              <li>Información de contexto: valor del dólar y otras referencias financieras.</li>
              <li>Sistema de recompensas: participación en desafíos.</li>
            </ul>

            <h2>3. Registro y Cuenta</h2>
            <ul>
              <li>Veracidad de la información.</li>
              <li>Confidencialidad de la cuenta.</li>
            </ul>

            <h2>4. Licencia de Uso</h2>
            <p>
              Licencia limitada, no exclusiva, intransferible y revocable para uso personal.
            </p>

            <h2>5. Conducta del Usuario</h2>
            <p>
              Queda prohibido el uso fraudulento, suplantación, interferir con la app, ingeniería inversa, o uso de bots.
            </p>

            <h2>6. Contenido Educativo y Simulaciones</h2>
            <p>
              Todo el contenido es únicamente educativo e informativo. No constituye asesoría profesional.
            </p>

            <h2>7. Sistema de Puntos y Recompensas</h2>
            <p>
              Los puntos obtenidos son virtuales, sin valor monetario, y pueden ser modificados por CreditWise.
            </p>

            <h2>8. Modificación del Servicio y Términos</h2>
            <p>
              Nos reservamos el derecho de modificar el servicio o los términos en cualquier momento.
            </p>

            <h2>9. Terminación</h2>
            <p>
              Podemos suspender o terminar el acceso a la app si incumple estos términos.
            </p>

            <h2>10. Renuncia de Garantías</h2>
            <p>
              La Aplicación se proporciona "TAL CUAL" y "SEGÚN DISPONIBILIDAD", sin garantías.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Terminos;
