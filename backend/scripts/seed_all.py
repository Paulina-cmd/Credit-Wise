from backend.database import get_connection
from datetime import datetime


def get_existing_tables(cursor):
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()")
    return set(r[0] for r in cursor.fetchall())


def seed():
    conn = get_connection()
    cursor = conn.cursor()
    report = {
        'checked_tables': [],
        'inserted': [],
        'skipped': [],
        'errors': []
    }

    try:
        existing = get_existing_tables(cursor)
        print('Existing tables in database:', existing)

        # Roles
        report['checked_tables'].append('rolusuario')
        if 'rolusuario' in existing:
            try:
                cursor.execute("SELECT COUNT(*) FROM rolusuario")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO rolusuario (Nombre) VALUES (%s)", ("Usuario",))
                    cursor.execute("INSERT INTO rolusuario (Nombre) VALUES (%s)", ("Admin",))
                    report['inserted'].append('rolusuario')
                    print('Inserted rolusuario')
                else:
                    report['skipped'].append('rolusuario (not empty)')
            except Exception as e:
                report['errors'].append(('rolusuario', str(e)))
        else:
            report['skipped'].append('rolusuario (missing)')

        # Usuario
        user_id = None
        report['checked_tables'].append('usuario')
        if 'usuario' in existing:
            try:
                cursor.execute("SELECT ID FROM usuario WHERE documento=%s", ("00000000",))
                found = cursor.fetchone()
                if not found:
                    cursor.execute(
                        "INSERT INTO usuario (nombre, contrasena, documento, PuntajeCrediticio, NivelProgreso, RolID) VALUES (%s,%s,%s,%s,%s,%s)",
                        ("Test User", "testpass", "00000000", 650, 20, 1)
                    )
                    user_id = cursor.lastrowid
                    report['inserted'].append(('usuario', user_id))
                    print('Inserted usuario id=', user_id)
                else:
                    user_id = found[0]
                    report['skipped'].append(('usuario', f'exists id={user_id}'))
            except Exception as e:
                report['errors'].append(('usuario', str(e)))
        else:
            report['skipped'].append('usuario (missing)')

        # Misiones
        mission_ids = []
        report['checked_tables'].append('mision')
        if 'mision' in existing:
            try:
                sample_misiones = [
                    ("Aprende presupuesto", "Completa el módulo de presupuesto personal", "Facil", 50, "presupuesto.pdf"),
                    ("Entiende intereses", "Simula 3 préstamos y calcula intereses", "Medio", 75, "intereses.pdf"),
                    ("Ahorra 10% mensual", "Configura ahorro automático del 10%", "Facil", 40, None),
                ]
                for m in sample_misiones:
                    cursor.execute("SELECT ID FROM mision WHERE Titulo=%s", (m[0],))
                    res = cursor.fetchone()
                    if not res:
                        cursor.execute("INSERT INTO mision (Titulo, Descripcion, Dificultad, RecompensaPuntos, Documento) VALUES (%s,%s,%s,%s,%s)", m)
                        mission_ids.append(cursor.lastrowid)
                        report['inserted'].append(('mision', m[0]))
                    else:
                        mission_ids.append(res[0])
                        report['skipped'].append(('mision', m[0]))
                print('Missions ensured:', mission_ids)
            except Exception as e:
                report['errors'].append(('mision', str(e)))
        else:
            report['skipped'].append('mision (missing)')

        # Actividades
        activity_ids = []
        report['checked_tables'].append('actividad')
        if 'actividad' in existing and mission_ids:
            try:
                activities = [
                    ("Revisa tu presupuesto", "Completa y sube tu presupuesto mensual", "Educacion", "Facil", mission_ids[0]),
                    ("Calcula interes simple", "Realiza 3 cálculos de interés simple", "Practica", "Medio", mission_ids[1]),
                    ("Activa ahorro automático", "Configura transferencia recurrente de ahorro", "Accion", "Facil", mission_ids[2]),
                ]
                for a in activities:
                    cursor.execute("SELECT ID FROM actividad WHERE Titulo=%s AND MisionID=%s", (a[0], a[4]))
                    res = cursor.fetchone()
                    if not res:
                        cursor.execute("INSERT INTO actividad (Titulo, Contenido, Categoria, Dificultad, MisionID) VALUES (%s,%s,%s,%s,%s)", a)
                        activity_ids.append(cursor.lastrowid)
                        report['inserted'].append(('actividad', a[0]))
                    else:
                        activity_ids.append(res[0])
                        report['skipped'].append(('actividad', a[0]))
                print('Activities ensured:', activity_ids)
            except Exception as e:
                report['errors'].append(('actividad', str(e)))
        else:
            report['skipped'].append('actividad (missing or no missions)')

        # actividad_usuario
        report['checked_tables'].append('actividad_usuario')
        if 'actividad_usuario' in existing and activity_ids and user_id:
            try:
                for aid in activity_ids:
                    cursor.execute("SELECT * FROM actividad_usuario WHERE UsuarioID=%s AND ActividadID=%s", (user_id, aid))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO actividad_usuario (UsuarioID, ActividadID, Completada, FechaCompletada) VALUES (%s,%s,%s,%s)", (user_id, aid, False, None))
                        report['inserted'].append(('actividad_usuario', aid))
                print('actividad_usuario assigned')
            except Exception as e:
                report['errors'].append(('actividad_usuario', str(e)))
        else:
            report['skipped'].append('actividad_usuario (missing or no user/activities)')

        # Evaluaciones
        eval_ids = []
        report['checked_tables'].append('evaluacion')
        if 'evaluacion' in existing and mission_ids:
            try:
                evals = [
                    ("Inicial", "Pendiente", 0.0, "", "Facil", mission_ids[0]),
                    ("Final", "Aprobado", 85.0, "Buen desempeño", "Medio", mission_ids[1])
                ]
                for ev in evals:
                    cursor.execute("SELECT ID FROM evaluacion WHERE Tipo=%s AND MisionID=%s", (ev[0], ev[5]))
                    res = cursor.fetchone()
                    if not res:
                        cursor.execute("INSERT INTO evaluacion (Tipo, Resultado, PuntajeObtenido, Feedback, Dificultad, MisionID) VALUES (%s,%s,%s,%s,%s,%s)", ev)
                        eval_ids.append(cursor.lastrowid)
                        report['inserted'].append(('evaluacion', ev[0]))
                    else:
                        eval_ids.append(res[0])
                        report['skipped'].append(('evaluacion', ev[0]))
                print('Evaluations ensured:', eval_ids)
            except Exception as e:
                report['errors'].append(('evaluacion', str(e)))
        else:
            report['skipped'].append('evaluacion (missing or no missions)')

        # Historial
        report['checked_tables'].append('historialmisiones')
        if 'historialmisiones' in existing and user_id and mission_ids:
            try:
                cursor.execute("SELECT * FROM historialmisiones WHERE UsuarioID=%s AND MisionID=%s", (user_id, mission_ids[0]))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO historialmisiones (UsuarioID, MisionID, PuntosObtenidos, EstadoFinal, FechaCompletado) VALUES (%s,%s,%s,%s,%s)", (user_id, mission_ids[0], 50, 'Completado', datetime.now().strftime('%Y-%m-%d')))
                    report['inserted'].append(('historialmisiones', mission_ids[0]))
                    print('Inserted historialmisiones')
                else:
                    report['skipped'].append('historialmisiones (exists)')
            except Exception as e:
                report['errors'].append(('historialmisiones', str(e)))
        else:
            report['skipped'].append('historialmisiones (missing or no user/missions)')

        # Recomendaciones table (create if missing) and inserts
        report['checked_tables'].append('recomendaciones')
        try:
            if 'recomendaciones' not in existing:
                print('Table recomendaciones not found — creating it (safe)')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS recomendaciones (
                        ID INT AUTO_INCREMENT PRIMARY KEY,
                        Titulo VARCHAR(255) NOT NULL,
                        Descripcion TEXT,
                        DescripcionDetallada TEXT
                    ) ENGINE=InnoDB;
                ''')
                report['inserted'].append('recomendaciones_table_created')
            cursor.execute("SELECT COUNT(*) FROM recomendaciones")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO recomendaciones (Titulo, Descripcion, DescripcionDetallada) VALUES (%s,%s,%s)", (
                    '💰 Crea un fondo de emergencia',
                    'Reserva al menos 3 meses de gastos básicos.',
                    'Un fondo de emergencia te protege ante imprevistos como pérdida de empleo, gastos médicos o reparaciones urgentes. Calcula tus gastos mensuales esenciales y multiplica por 3.'
                ))
                cursor.execute("INSERT INTO recomendaciones (Titulo, Descripcion, DescripcionDetallada) VALUES (%s,%s,%s)", (
                    '💳 Usa máximo el 30% de tu crédito',
                    'Protege tu puntaje crediticio.',
                    'Mantener tu utilización de crédito por debajo del 30% demuestra manejo responsable y mejora tu score crediticio. Revisa tus límites y ajusta tu gasto mensual.'
                ))
                report['inserted'].append('recomendaciones_samples')
                print('Inserted recomendaciones samples')
            else:
                report['skipped'].append('recomendaciones (not empty)')
        except Exception as e:
            report['errors'].append(('recomendaciones', str(e)))

        conn.commit()

        # Summary
        print('\n--- Seed Summary ---')
        print('Checked tables:', report['checked_tables'])
        print('Inserted items:', report['inserted'])
        print('Skipped items:', report['skipped'])
        print('Errors:', report['errors'])
        print('Seed finished')

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    seed()
