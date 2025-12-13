from conexionBD import get_conexion
from mysql.connector import Error as DbError

class incidentes:
    @staticmethod
    def insertar(id_usuario, incidente, id_laboratorio):
        try:
            with get_conexion() as (conexion, cursor):
                sql = "INSERT INTO incidentes (id_usuario, incidente, id_laboratorio, fecha, observaciones) VALUES (%s, %s, %s, NOW(), 0)"
                cursor.execute(sql, (id_usuario, incidente, id_laboratorio))
                conexion.commit()
                return True
        except: return False

    @staticmethod
    def consulta_tabla(id_usuario):
        try:
            with get_conexion() as (conexion, cursor):
                sql = "SELECT * FROM vista_incidentes WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
                return cursor.fetchall()
        except: return []

    @staticmethod
    def borrarIncidente(id_incidente):
        try:
            with get_conexion() as (conexion, cursor):
                cursor.execute("DELETE FROM incidentes WHERE id_incidente = %s", (id_incidente,))
                conexion.commit()
                return True
        except: return False

    @staticmethod
    def actualizar(id_incidente, nuevo_texto):
        try:
            with get_conexion() as (conexion, cursor):
                cursor.execute("UPDATE incidentes SET incidente = %s WHERE id_incidente = %s", (nuevo_texto, id_incidente))
                conexion.commit()
                return True
        except: return False

    # --- MÉTODOS ADMIN ---
    @staticmethod
    def marcar_resuelto(id_incidente):
        try:
            with get_conexion() as (conn, cursor):
                # 1 = Solucionado
                cursor.execute("UPDATE incidentes SET observaciones = 1 WHERE id_incidente = %s", (id_incidente,))
                conn.commit()
                return True
        except: return False
        
    @staticmethod
    def consultar_todos_admin():
        try:
            with get_conexion() as (conn, cursor):
                cursor.execute("SELECT * FROM vista_incidentes ORDER BY fecha DESC")
                return cursor.fetchall()
        except: return []