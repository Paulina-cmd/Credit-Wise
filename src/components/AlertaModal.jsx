import "../assets/css/alertaModal.css";

export default function AlertaModal({ mensaje, onClose }) {
  if (!mensaje) return null; // no renderiza nada si no hay mensaje

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>⚠️ Atención</h3>
        <p>{mensaje}</p>
        <button onClick={onClose}>Cerrar</button>
      </div>
    </div>
  );
}

