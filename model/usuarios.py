
from conexionBD import *
from mysql.connector import Error as DbError

class Usuarios:
    

    @staticmethod
    def insertar(primer_nom,segundo_nom,apellido_p,telf,email,contrasena):
          try:
              # La consulta SQL "Pro"
              sql_query = """
                  INSERT INTO usuarios 
                  (primer_nombre, segundo_nombre, apellido_paterno, telefono, email, contrasena) 
                  VALUES (%s, %s, %s, %s, %s, %s)
              """
              
              # Los valores (en el orden de la consulta de arriba)
              valores = (primer_nom, segundo_nom, apellido_p, telf, email, contrasena)

              cursor.execute(sql_query, valores)
              
              conexion.commit()
              return (True,None)
          
          except DbError as db_err:
            # Capturamos el error de la Base de Datos
            conexion.rollback() # Deshacer cambios
            print(f"[Error de BD] Código: {db_err.errno}, Mensaje: {db_err.msg}")

            # Error 1062: Entrada Duplicada (Email ya existe)
            if db_err.errno == 1062:
                # Le decimos al controlador que fue un error "duplicado"
                return (False, "duplicado")
            
            # Error 3819: Falla en la restricción "CHECK"
            # (Esto solo funciona si tu tabla tiene: CHECK (email LIKE '%@utd.edu.mx'))
            elif db_err.errno == 3819:
                # Le decimos al controlador que fue un error "check_utd"
                return (False, "check_utd")
            
            # Cualquier otro error de BD
            else:
                return (False, "otro_bd")

    @staticmethod
    def consultar():
        try:
          cursor.execute("select * from usuarios")
          return cursor.fetchall()
        except:    
          return []

    @staticmethod
    def actualizar(primer_nom,segundo_nom,apellido_p,telf,email,contrasena,id):
       try:
         cursor.execute(
            "update usuarios set primer_nombre=%s,segundo=nombre=%s,apellido_paterno=%s,telefono=%s,email=%s,contrasena=%s where id=%s",
            (primer_nom,segundo_nom,apellido_p,telf,email,contrasena,id)
         )
         conexion.commit()
         return True
       except: 
         return False
    
    @staticmethod
    def eliminar(id):
        try:
          cursor.execute(
            "delete from operaciones where id=%s",
            (id,)
          ) 
          conexion.commit() 
          return True  
        except:    
          return False
        
    @staticmethod
    def login(email,contrasena):
      try:
          
            cursor.execute(
                "SELECT * FROM usuarios WHERE email=%s AND contrasena=%s",
                (email, contrasena)
            )
            usuario = cursor.fetchone() 
            
            if usuario:
                return usuario 
            else:
                return None    
      except Exception as e:
            print(f"Error en login: {e}") 