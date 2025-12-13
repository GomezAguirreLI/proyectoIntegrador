import mysql.connector
import contextlib
from mysql.connector import Error as DbError
from view import constantes  # Asegúrate de tener las credenciales en constantes.py

@contextlib.contextmanager
def get_conexion():
    """
    Maneja la conexión a la base de datos de manera segura.
    Abre la conexión, entrega el cursor, y cierra todo al finalizar automáticamente.
    """
    conexion = None
    cursor = None
    try:
        # Usamos las variables definidas en view/constantes.py
        # Si no las has puesto ahí, cámbialas aquí directamente por tus strings
        conexion = mysql.connector.connect(
            host=constantes.DB_HOST,
            user=constantes.DB_USER,
            password=constantes.DB_PASSWORD,
            database=constantes.DB_DATABASE
        )
        cursor = conexion.cursor(buffered=True)
        
        # 'yield' entrega el control al código que llamó a la función (usuarios.py)
        yield conexion, cursor
        
    except DbError as err:
        print(f"Error de conexión a MySQL: {err}")
        if conexion and conexion.is_connected():
            conexion.rollback()
        raise # Re-lanzar el error para que lo maneje el modelo
    
    finally:
        # Esto se ejecuta SIEMPRE, haya error o no, cerrando la conexión
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()