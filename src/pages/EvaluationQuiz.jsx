import React, { useState, useEffect } from "react";
import { useNavigate, Link, useSearchParams } from "react-router-dom";
import MenuMas from "../components/MenuMas";
import "../assets/css/estilos.css";

const EvaluationQuiz = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const misionId = searchParams.get("misionId");
  
  const [preguntaActual, setPreguntaActual] = useState(0);
  const [respuestasUsuario, setRespuestasUsuario] = useState({});
  const [mostrarResultado, setMostrarResultado] = useState(false);
  const [puntaje, setPuntaje] = useState(0);
  const [evaluacionCompletada, setEvaluacionCompletada] = useState(false);
  const [loading, setLoading] = useState(true);

  // Preguntas hardcodeadas por misión (después podemos traerlas de BD)
  const preguntasPorMision = {
    1: [
      {
        id: 1,
        pregunta: "¿Cuál es el propósito principal del crédito?",
        opciones: [
          { id: "a", texto: "Obtener dinero gratis" },
          { id: "b", texto: "Acceder a dinero prestado con la obligación de devolverlo" },
          { id: "c", texto: "Invertir en el mercado de valores" },
          { id: "d", texto: "Evitar pagar impuestos" }
        ],
        respuestaCorrecta: "b",
        explicacion: "El crédito te permite usar dinero prestado que debes devolver, generalmente con intereses. Es una herramienta financiera fundamental."
      },
      {
        id: 2,
        pregunta: "¿Cuál es un ejemplo de crédito de consumo?",
        opciones: [
          { id: "a", texto: "Hipoteca para comprar casa" },
          { id: "b", texto: "Crédito para comprar electrodomésticos" },
          { id: "c", texto: "Crédito empresarial" },
          { id: "d", texto: "Crédito agrícola" }
        ],
        respuestaCorrecta: "b",
        explicacion: "El crédito de consumo se utiliza para adquirir bienes de consumo como electrodomésticos, muebles, etc."
      },
      {
        id: 3,
        pregunta: "¿Qué son los intereses en un crédito?",
        opciones: [
          { id: "a", texto: "El dinero que te presta el banco" },
          { id: "b", texto: "El costo adicional por usar dinero prestado" },
          { id: "c", texto: "Una rebaja en el monto a pagar" },
          { id: "d", texto: "Un impuesto del gobierno" }
        ],
        respuestaCorrecta: "b",
        explicacion: "Los intereses son el costo que pagas por usar dinero prestado. Es lo que gana el acreedor por prestar dinero."
      },
      {
        id: 4,
        pregunta: "¿Cuál es la diferencia entre deuda buena y deuda mala?",
        opciones: [
          { id: "a", texto: "La deuda buena es pequeña y la mala es grande" },
          { id: "b", texto: "La deuda buena genera valor futuro (educación, vivienda) y la mala es para gastos impulsivos" },
          { id: "c", texto: "No hay diferencia" },
          { id: "d", texto: "La deuda mala nunca se debe contraer" }
        ],
        respuestaCorrecta: "b",
        explicacion: "La deuda buena invierte en tu futuro (casa, educación), mientras que la deuda mala se usa en gastos sin valor duradero."
      },
      {
        id: 5,
        pregunta: "¿Cómo puedes mantener una buena relación con el crédito?",
        opciones: [
          { id: "a", texto: "Pidiendo crédito frecuentemente" },
          { id: "b", texto: "Pagando tus deudas a tiempo y usando crédito responsablemente" },
          { id: "c", texto: "Evitando todo tipo de crédito" },
          { id: "d", texto: "Pidiendo máxima cantidad posible" }
        ],
        respuestaCorrecta: "b",
        explicacion: "La responsabilidad financiera incluye pagar a tiempo, usar crédito conscientemente y mantener un buen historial de pagos."
      }
    ],
    2: [
      {
        id: 1,
        pregunta: "¿Cómo se calcula el interés simple?",
        opciones: [
          { id: "a", texto: "Capital × Tasa × Tiempo" },
          { id: "b", texto: "Capital + Tasa + Tiempo" },
          { id: "c", texto: "Capital / Tasa / Tiempo" },
          { id: "d", texto: "No se calcula, es fijo" }
        ],
        respuestaCorrecta: "a",
        explicacion: "La fórmula de interés simple es I = C × r × t, donde C es capital, r es tasa y t es tiempo."
      },
      {
        id: 2,
        pregunta: "Si pides un préstamo de $1000 al 10% anual por 1 año, ¿cuánto es el interés?",
        opciones: [
          { id: "a", texto: "$100" },
          { id: "b", texto: "$10" },
          { id: "c", texto: "$110" },
          { id: "d", texto: "$1100" }
        ],
        respuestaCorrecta: "a",
        explicacion: "Interés = $1000 × 0.10 × 1 = $100. Este es el costo adicional que pagarás."
      },
      {
        id: 3,
        pregunta: "¿Cuál es la diferencia entre interés simple e interés compuesto?",
        opciones: [
          { id: "a", texto: "No hay diferencia" },
          { id: "b", texto: "El simple se calcula solo sobre el capital; el compuesto se calcula sobre capital + intereses" },
          { id: "c", texto: "El compuesto siempre es menor" },
          { id: "d", texto: "El simple es para negocios" }
        ],
        respuestaCorrecta: "b",
        explicacion: "En interés compuesto, los intereses generan más intereses (interés sobre interés), por eso es más alto con el tiempo."
      },
      {
        id: 4,
        pregunta: "Un banco te ofrece dos opciones de préstamo. ¿Cuál es mejor?",
        opciones: [
          { id: "a", texto: "5% de interés anual" },
          { id: "b", texto: "0.5% de interés mensual" },
          { id: "c", texto: "Ambas son iguales" },
          { id: "d", texto: "Depende de otros factores además de la tasa" }
        ],
        respuestaCorrecta: "d",
        explicacion: "La mejor opción depende no solo de la tasa, sino también del plazo, el monto, las comisiones y tu capacidad de pago."
      },
      {
        id: 5,
        pregunta: "¿Cuál es la importancia de entender los intereses antes de solicitar un crédito?",
        opciones: [
          { id: "a", texto: "No es importante, solo importa el monto" },
          { id: "b", texto: "Entender los intereses te ayuda a calcular el costo real y tomar mejores decisiones" },
          { id: "c", texto: "Solo es importante para préstamos grandes" },
          { id: "d", texto: "Los intereses siempre son iguales" }
        ],
        respuestaCorrecta: "b",
        explicacion: "Conocer los intereses te permite comparar opciones, calcular cuánto pagarás realmente y tomar decisiones financieras informadas."
      }
    ],
    3: [
      {
        id: 1,
        pregunta: "¿Cuál es la mejor estrategia de ahorro?",
        opciones: [
          { id: "a", texto: "Ahorrar solo cuando sobre dinero" },
          { id: "b", texto: "Ahorrar una cantidad fija regularmente" },
          { id: "c", texto: "No ahorrar, usar todo el dinero" },
          { id: "d", texto: "Ahorrar solo para emergencias" }
        ],
        respuestaCorrecta: "b",
        explicacion: "El ahorro sistemático (cantidad fija regularmente) es más efectivo que esperar a que sobre dinero."
      },
      {
        id: 2,
        pregunta: "¿Qué es un fondo de emergencia?",
        opciones: [
          { id: "a", texto: "Dinero para vacaciones" },
          { id: "b", texto: "Dinero para compras impulsivas" },
          { id: "c", texto: "Ahorros para imprevistos (3-6 meses de gastos)" },
          { id: "d", texto: "Un tipo de inversión" }
        ],
        respuestaCorrecta: "c",
        explicacion: "Un fondo de emergencia es dinero ahorrado para cubrir gastos inesperados y te protege de deudas innecesarias."
      },
      {
        id: 3,
        pregunta: "¿A qué edad es mejor empezar a ahorrar?",
        opciones: [
          { id: "a", texto: "A los 40 años" },
          { id: "b", texto: "Cuando ganes mucho dinero" },
          { id: "c", texto: "Cuanto antes mejor, incluso desde joven" },
          { id: "d", texto: "Nunca es importante ahorrar" }
        ],
        respuestaCorrecta: "c",
        explicacion: "Empezar a ahorrar joven aprovecha el poder del interés compuesto y crea buenos hábitos financieros."
      },
      {
        id: 4,
        pregunta: "¿Cuál es la regla 50/30/20 de presupuesto?",
        opciones: [
          { id: "a", texto: "50% ahorro, 30% gasto, 20% inversión" },
          { id: "b", texto: "50% necesidades, 30% deseos, 20% ahorro/deuda" },
          { id: "c", texto: "50% impuestos, 30% salario, 20% gasto" },
          { id: "d", texto: "No existe tal regla" }
        ],
        respuestaCorrecta: "b",
        explicacion: "La regla 50/30/20 es una guía: 50% para necesidades, 30% para deseos y 20% para ahorro e inversión."
      },
      {
        id: 5,
        pregunta: "¿Qué beneficio tiene el ahorro automático?",
        opciones: [
          { id: "a", texto: "Ninguno" },
          { id: "b", texto: "Te olvidas del dinero y lo ahorras sin pensar" },
          { id: "c", texto: "Garantiza que ahorres consistentemente sin depender de tu disciplina" },
          { id: "d", texto: "Solo funciona si tienes mucho dinero" }
        ],
        respuestaCorrecta: "c",
        explicacion: "El ahorro automático elimina la tentación de gastar, asegurando que ahorres de forma consistente."
      }
    ]
  };

  const preguntas = preguntasPorMision[misionId] || preguntasPorMision[1];

  useEffect(() => {
    setLoading(false);
  }, []);

  const seleccionarRespuesta = (opcionId) => {
    setRespuestasUsuario({
      ...respuestasUsuario,
      [preguntaActual]: opcionId
    });
    setMostrarResultado(true);
  };

  const siguientePregunta = () => {
    if (preguntaActual < preguntas.length - 1) {
      setPreguntaActual(preguntaActual + 1);
      setMostrarResultado(false);
    } else {
      finalizarEvaluacion();
    }
  };

  const finalizarEvaluacion = async () => {
    // Calcular puntaje
    let puntosTotales = 0;
    preguntas.forEach((pregunta, index) => {
      if (respuestasUsuario[index] === pregunta.respuestaCorrecta) {
        puntosTotales += 20; // 100 puntos / 5 preguntas = 20 por pregunta
      }
    });

    setPuntaje(puntosTotales);
    setEvaluacionCompletada(true);

    // Guardar en backend
    try {
      const usuarioId = sessionStorage.getItem('usuarioId');
      if (!usuarioId || !misionId) return;
      const response = await fetch("http://localhost:8000/evaluaciones/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          Tipo: "Quiz",
          Resultado: puntosTotales >= 60 ? "Aprobado" : "Desaprobado",
          PuntajeObtenido: puntosTotales,
          Feedback: `Obtuviste ${puntosTotales} puntos. ${puntosTotales >= 60 ? "¡Excelente!" : "Intenta de nuevo"}`,
          Dificultad: "Media",
          MisionID: parseInt(misionId),
          UsuarioID: parseInt(usuarioId)
        })
      });

      if (response.ok) {
        console.log("✅ Evaluación guardada en backend");
        // Emitir evento para que History se actualice si está abierto
        window.dispatchEvent(new Event('localStorageChange'));
      }
    } catch (err) {
      console.error("❌ Error guardando evaluación:", err);
    }
  };

  if (loading) {
    return (
      <div className="app-container page-transition">
        <aside className="sidebar sidebar-appear">
          <h2 className="logo">CreditWise</h2>
        </aside>
        <main className="main-content content-appear">
          <p>Cargando evaluación...</p>
        </main>
      </div>
    );
  }

  const pregunta = preguntas[preguntaActual];
  const respuestaSeleccionada = respuestasUsuario[preguntaActual];
  const esCorrecta = respuestaSeleccionada === pregunta.respuestaCorrecta;

  return (
    <div className="app-container page-transition">
      <aside className="sidebar sidebar-appear">
        <h2 className="logo">CreditWise</h2>
        <nav>
          <Link to="/home">
            <img src="/img/hogar.png" alt="Inicio" className="icon" /> Inicio
          </Link>
          <Link to="/missions">
            <img src="/img/medalla-de-oro.png" alt="Misiones" className="icon" /> Misiones
          </Link>
          <Link to="/evaluation-quiz" className="active">
            <img src="/img/evaluacion.png" alt="Evaluación" className="icon" /> Evaluación
          </Link>
          <Link to="/history">
            <img src="/img/historial-de-transacciones.png" alt="Historial" className="icon" /> Historial
          </Link>
          <Link to="/profile">
            <img src="/img/usuario.png" alt="Perfil" className="icon" /> Perfil
          </Link>
          <MenuMas />
        </nav>
      </aside>

      <main className="main-content content-appear">
        <header className="header">
          <h1>Evaluación - Misión {misionId}</h1>
        </header>

        {evaluacionCompletada ? (
          <div className="evaluation-result card-appear">
            <h2>¡Evaluación Completada!</h2>
            <div className={`puntaje-circle ${puntaje >= 60 ? 'aprobado' : 'desaprobado'}`}>
              {puntaje}%
            </div>
            <p className="evaluation-message">
              {puntaje >= 60 ? "¡Excelente! Has aprobado la evaluación." : "Necesitas mejorar. Intenta nuevamente."}
            </p>
            <button 
              className="btn btn-hover" 
              onClick={() => navigate("/missions")}
              style={{ marginRight: "10px" }}
            >
              Volver a Misiones
            </button>
            {puntaje < 60 && (
              <button 
                className="btn btn-hover"
                onClick={() => {
                  setPreguntaActual(0);
                  setRespuestasUsuario({});
                  setMostrarResultado(false);
                  setEvaluacionCompletada(false);
                }}
              >
                Reintentar
              </button>
            )}
          </div>
        ) : (
          <div className="evaluation-quiz card-appear">
            <div className="progress-container">
              <div className="progress-bar" style={{ width: `${((preguntaActual + 1) / preguntas.length) * 100}%` }}></div>
            </div>
            <p className="evaluation-subtitle">
              Pregunta {preguntaActual + 1} de {preguntas.length}
            </p>

            <h3 className="evaluation-question">{pregunta.pregunta}</h3>

            <div className="opciones">
              {pregunta.opciones.map((opcion) => (
                <button
                  key={opcion.id}
                  onClick={() => seleccionarRespuesta(opcion.id)}
                  disabled={mostrarResultado}
                  className={`opcion-btn ${respuestaSeleccionada === opcion.id ? (esCorrecta ? 'correcta' : 'incorrecta') : (mostrarResultado && opcion.id === pregunta.respuestaCorrecta ? 'correcta' : '')}`}
                >
                  {opcion.texto}
                </button>
              ))}
            </div>

            {mostrarResultado && (
              <div
                style={{
                  marginTop: "20px",
                  padding: "15px",
                  borderRadius: "8px",
                  background: esCorrecta ? "#E8F5E9" : "#FFEBEE",
                  borderLeft: `4px solid ${esCorrecta ? "#4CAF50" : "#FF6B6B"}`
                }}
              >
                <p style={{ margin: "0 0 10px 0", fontWeight: "bold" }}>
                  {esCorrecta ? "✅ ¡Correcto!" : "❌ Incorrecto"}
                </p>
                <p style={{ margin: 0, fontSize: "14px" }}>{pregunta.explicacion}</p>
              </div>
            )}

            {mostrarResultado && (
              <button
                className="btn btn-hover"
                onClick={siguientePregunta}
                style={{ marginTop: "20px", width: "100%" }}
              >
                {preguntaActual < preguntas.length - 1 ? "Siguiente Pregunta →" : "Ver Resultados"}
              </button>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default EvaluationQuiz;
