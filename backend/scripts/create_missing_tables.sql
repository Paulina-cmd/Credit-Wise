-- Script seguro para crear tablas faltantes (IF NOT EXISTS)
-- Ejecuta esto en tu cliente MySQL (phpMyAdmin, MySQL CLI, etc.)
-- Selecciona la BD: USE creditwise;
-- Y pega todo el contenido

USE creditwise;

-- Tabla actividad_usuario (relación usuario-actividad)
CREATE TABLE IF NOT EXISTS actividad_usuario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    UsuarioID INT NOT NULL,
    ActividadID INT NOT NULL,
    Completada BOOLEAN DEFAULT FALSE,
    FechaCompletada DATE NULL,
    FOREIGN KEY (UsuarioID) REFERENCES usuario(ID) ON DELETE CASCADE,
    FOREIGN KEY (ActividadID) REFERENCES actividad(ID) ON DELETE CASCADE,
    UNIQUE KEY unique_user_activity (UsuarioID, ActividadID)
) ENGINE=InnoDB;

-- Tabla historialmisiones (historial de misiones completadas)
CREATE TABLE IF NOT EXISTS historialmisiones (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    UsuarioID INT NOT NULL,
    MisionID INT NOT NULL,
    PuntosObtenidos INT DEFAULT 0,
    EstadoFinal VARCHAR(50) DEFAULT 'Pendiente',
    FechaCompletado DATE DEFAULT CURDATE(),
    FOREIGN KEY (UsuarioID) REFERENCES usuario(ID) ON DELETE CASCADE,
    FOREIGN KEY (MisionID) REFERENCES mision(ID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Verificar que se crearon (opcional)
SHOW TABLES;
SELECT COUNT(*) FROM actividad_usuario;
SELECT COUNT(*) FROM historialmisiones;
