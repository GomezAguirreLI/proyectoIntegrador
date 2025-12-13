from conexionBD import get_conexion
from mysql.connector import Error as DbError
import hashlib

class Usuarios:
    
    @staticmethod
    def _hash_contrasena(contrasena):
        return hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

    @staticmethod
    def insertar(primer_nom, segundo_nom, apellido_p, telf, email, contrasena):
        contrasena_hashed = Usuarios._hash_contrasena(contrasena)
        
        try:
            with get_conexion() as (conexion, cursor): 
                # Se asume que la columna 'estatus' existe (1=Activo). Si no, quítalo del INSERT.
                sql_query = """
                    INSERT INTO usuarios 
                    (primer_nombre, segundo_nombre, apellido_paterno, telefono, email, contrasena, rol, estatus) 
                    VALUES (%s, %s, %s, %s, %s, %s, 'usuario', 1)
                    """ 
                values = (primer_nom, segundo_nom, apellido_p, telf, email, contrasena_hashed)
                cursor.execute(sql_query, values)
                conexion.commit()
                return (True, None)
        
        except DbError as db_err:
            print(f"[Error BD] Código: {db_err.errno}, Mensaje: {db_err.msg}")
            if db_err.errno == 1062:
                return (False, "duplicado") 
            elif db_err.errno == 3819:
                return (False, "check_utd") 
            else:
                return (False, "otro_bd")
        except Exception as e:
             return (False, "error_conexion")

    @staticmethod
    def login(email, contrasena):
        try:
            with get_conexion() as (_, cursor): 
                # Traemos 'estatus' también para verificar si está activo
                cursor.execute(
                    "SELECT contrasena, id_usuario, primer_nombre, segundo_nombre, apellido_paterno, telefono, email, rol, estatus FROM usuarios WHERE email=%s",
                    (email,)
                )
                resultado = cursor.fetchone() 
                
                if resultado:
                    # Verificar estatus (índice 8)
                    if resultado[8] == 0: 
                        return (False, None, "User account is disabled.")

                    contrasena_almacenada = resultado[0]
                    contrasena_ingresada_hashed = Usuarios._hash_contrasena(contrasena)
                    
                    if contrasena_ingresada_hashed == contrasena_almacenada:
                        # Devolvemos info (id, nom, seg_nom, ape, telf, email, rol)
                        # Indices en resultado: 1, 2, 3, 4, 5, 6, 7
                        usuario_info = (resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6], resultado[7])
                        return (True, usuario_info, None)
                    else:
                        return (False, None, "Incorrect password")
                else:
                    return (False, None, "Incorrect username or password") 
        
        except DbError as db_err:
            print(f"[Error BD] {db_err}")
            return (False, None, "Database error")
        except Exception as e:
            return (False, None, "Unexpected system error")
        
    @staticmethod
    def actualizar_contacto(id_usuario, nuevo_telefono, nuevo_email):
        try:
            with get_conexion() as (conexion, cursor):
                sql = "UPDATE usuarios SET telefono=%s, email=%s WHERE id_usuario=%s"
                cursor.execute(sql, (nuevo_telefono, nuevo_email, id_usuario))
                conexion.commit()
                return True
        except Exception as e:
            print(f"Error actualizando contacto: {e}")
            return False

    # --- MÉTODOS PARA ADMINISTRADOR ---

    @staticmethod
    def consultar_todos():
        try:
            with get_conexion() as (conn, cursor):
                cursor.execute("SELECT id_usuario, primer_nombre, apellido_paterno, email, rol, estatus FROM usuarios")
                return cursor.fetchall()
        except: return []

    @staticmethod
    def cambiar_estatus(id_usuario, nuevo_estatus):
        try:
            with get_conexion() as (conn, cursor):
                cursor.execute("UPDATE usuarios SET estatus=%s WHERE id_usuario=%s", (nuevo_estatus, id_usuario))
                conn.commit()
                return True
        except: return False

    @staticmethod
    def cambiar_rol(id_usuario, nuevo_rol):
        try:
            with get_conexion() as (conn, cursor):
                cursor.execute("UPDATE usuarios SET rol=%s WHERE id_usuario=%s", (nuevo_rol, id_usuario))
                conn.commit()
                return True
        except: return False