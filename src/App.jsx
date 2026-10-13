import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Registro from './pages/Registro';
import Home from './pages/Home';
import Missions from './pages/Missions';
import MissionTask from './pages/MissionTask';
import Dollar from './pages/Dollar';
import Recommendation from './pages/Recommendation';
import History from './pages/History';
import Profile from './pages/Profile';
import Terminos from './pages/Terminos';
import RecuperarContrasena from './pages/RecuperarContrasena'; 
import Evaluation from './pages/Evaluation';
import EvaluationQuiz from './pages/EvaluationQuiz';
import Activities from './pages/Activities';
import './assets/css/estilos.css';

// Proteger rutas que requieren autenticación
function ProtectedRoute({ element }) {
  const usuarioId = sessionStorage.getItem('usuarioId');
  
  if (!usuarioId) {
    return <Navigate to="/login" replace />;
  }
  
  return element;
}

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/registro" element={<Registro />} />
          <Route path="/recuperar-contrasena" element={<RecuperarContrasena />} />
          <Route path="/terminos" element={<Terminos />} />
          
          {/* Rutas protegidas */}
          <Route path="/home" element={<ProtectedRoute element={<Home />} />} />
          <Route path="/missions" element={<ProtectedRoute element={<Missions />} />} />
          <Route path="/mission-task" element={<ProtectedRoute element={<MissionTask />} />} />
          <Route path="/dollar" element={<ProtectedRoute element={<Dollar />} />} />
          <Route path="/recommendation" element={<ProtectedRoute element={<Recommendation />} />} />
          <Route path="/history" element={<ProtectedRoute element={<History />} />} />
          <Route path="/profile" element={<ProtectedRoute element={<Profile />} />} />
          <Route path="/evaluation" element={<ProtectedRoute element={<Evaluation />} />} />
          <Route path="/evaluation-quiz" element={<ProtectedRoute element={<EvaluationQuiz />} />} />
          <Route path="/activities" element={<ProtectedRoute element={<Activities />} />} />
          
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;