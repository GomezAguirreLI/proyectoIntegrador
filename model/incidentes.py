from conexionBD import *
from mysql.connector import Error as DbErrorS
'''
INSERT INTO usuarios 
                (primer_nombre, segundo_nombre, apellido_paterno, telefono, email, contrasena) 
                VALUES (%s, %s, %s, %s, %s, %s)

'''

class incidentes:
    @staticmethod
    def insertar(id_usuario, incidente, id_laboratorio):
        try:
            '''
             cursor.execute("INSERT INTO incidentes(id_usuario,incidente,id_laboratorio) VALUES (%s,%s,%s,)",(id_usuario, incidente, id_laboratorio))
            
            
            '''
            sql_query = """
                INSERT INTO incidentes(id_usuario,incidente,id_laboratorio) VALUES (%s,%s,%s)
            """
            
            # Los valores (en el orden de la consulta de arriba)
            valores = (id_usuario, incidente, id_laboratorio)

            cursor.execute(sql_query, valores)
            
            conexion.commit()
           

            return True
        except DbErrorS as e:
            print(f"EL ERROR QUE ME ESTA JODIENDO ES  {e}")
            return False
        
    @staticmethod
    def consultar_id(id):
        try:
            cursor.execute("SELECT nombre, edificio, piso, cant_pc FROM laboratorios WHERE id_lab=%s",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []

        

    @staticmethod
    def buscar_id(datos):
        try:
            cursor.execute("SELECT id_lab FROM laboratorios WHERE nombre=%s AND edificio=%s AND piso=%s",(datos[0],datos[1],datos[2]))
            return cursor.fetchone()
        except:
            return []
    



