from conexionBD import get_conexion
from mysql.connector import Error as DbError

class laboratorios:
    @staticmethod
    def consultar():
        try:
            with get_conexion() as (conexion, cursor):
                # Traemos estatus también si existe columna, si no, ajusta el SELECT
                cursor.execute("SELECT nombre, edificio, piso, cant_pc, id_lab, estatus FROM laboratorios")
                return cursor.fetchall()
        except Exception as e:
            return []

    @staticmethod
    def consultar_filtro(texto_busqueda):
        try:
            with get_conexion() as (conexion, cursor):
                patron = f"%{texto_busqueda}%"
                sql = """
                    SELECT nombre, edificio, piso, cant_pc, id_lab, estatus 
                    FROM laboratorios 
                    WHERE nombre LIKE %s OR edificio LIKE %s OR CAST(piso AS CHAR) LIKE %s
                """
                cursor.execute(sql, (patron, patron, patron))
                return cursor.fetchall()
        except Exception: return []

    @staticmethod
    def buscar_id(datos_tupla):
        try:
            with get_conexion() as (conexion, cursor):
                sql = "SELECT id_lab FROM laboratorios WHERE nombre=%s AND edificio=%s AND piso=%s"
                cursor.execute(sql, (datos_tupla[0], datos_tupla[1], datos_tupla[2]))
                return cursor.fetchone()
        except Exception: return None

    # --- MÉTODOS DE ADMINISTRADOR ---
    @staticmethod
    def insertar(nombre, edificio, piso, equipos):
        try:
            with get_conexion() as (conn, cursor):
                cursor.execute("INSERT INTO laboratorios (nombre, edificio, piso, cant_pc, estatus) VALUES (%s,%s,%s,%s, 1)", 
                               (nombre, edificio, piso, equipos))
                conn.commit()
                return True
        except: return False

    @staticmethod
    def actualizar(id_lab, nombre, edificio, piso, equipos):
        try:
            with get_conexion() as (conn, cursor):
                cursor.execute("UPDATE laboratorios SET nombre=%s, edificio=%s, piso=%s, cant_pc=%s WHERE id_lab=%s", 
                               (nombre, edificio, piso, equipos, id_lab))
                conn.commit()
                return True
        except: return False

    @staticmethod
    def cambiar_estatus(id_lab, nuevo_estatus):
        try:
            with get_conexion() as (conn, cursor):
                cursor.execute("UPDATE laboratorios SET estatus=%s WHERE id_lab=%s", (nuevo_estatus, id_lab))
                conn.commit()
                return True
        except: return False