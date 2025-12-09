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
    
    @staticmethod
    def consulta_general():
        try:
            cursor.execute("SELECT  * FROM incidentes")
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []
        
    
    
    @staticmethod
    def consulta_tabla(id):
        try:
            # La consulta correcta ahora tiene el formato: SELECT ... FROM ... JOIN ...
            cursor.execute("SELECT  * FROM vista_incidentes WHERE id_usuario=%s;",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []
        

    @staticmethod
    def consulta_tabla_lab(id):
        try:
            # La consulta correcta ahora tiene el formato: SELECT ... FROM ... JOIN ...
            cursor.execute("SELECT  * FROM vista_incidentes WHERE id_usuario=%s ORDER BY nombre_laboratorio ASC;",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []



    @staticmethod
    def consulta_tabla_edifico(id):
        try:
            # La consulta correcta ahora tiene el formato: SELECT ... FROM ... JOIN ...
            cursor.execute("SELECT  * FROM vista_incidentes WHERE id_usuario=%s ORDER BY edificio ASC;",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []        



    @staticmethod
    def consulta_tabla_fehca_Asc(id):
        try:
            # La consulta correcta ahora tiene el formato: SELECT ... FROM ... JOIN ...
            #DESC SERIA EL ULTIMO REPORTE 
            #ASC SERIA EL PRIMER REPORTE
            cursor.execute("SELECT  * FROM vista_incidentes WHERE id_usuario=%s ORDER BY fecha ASC;",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return [] 

    
    @staticmethod
    def consulta_tabla_fehca_Desc(id):
        try:
            # La consulta correcta ahora tiene el formato: SELECT ... FROM ... JOIN ...
            #DESC SERIA EL ULTIMO REPORTE 
            #ASC SERIA EL PRIMER REPORTE
            cursor.execute("SELECT  * FROM vista_incidentes WHERE id_usuario=%s ORDER BY fecha DESC;",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []   



    @staticmethod
    def consulta_tabla_proceso(id):
        try:
            # La consulta correcta ahora tiene el formato: SELECT ... FROM ... JOIN ...
            #DESC SERIA SOLUCIONADO 
            #ASC SERIA EN PROCESO
            cursor.execute("SELECT  * FROM vista_incidentes WHERE id_usuario=%s ORDER BY observaciones ASC;",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []   
        

    @staticmethod
    def consulta_tabla_proceso_terminado(id):
        try:
            # La consulta correcta ahora tiene el formato: SELECT ... FROM ... JOIN ...
            #DESC SERIA SOLUCIONADO 
            #ASC SERIA EN PROCESO
            cursor.execute("SELECT  * FROM vista_incidentes WHERE id_usuario=%s ORDER BY observaciones DESC;",(id,))
            return cursor.fetchall()
        except DbErrorS as e:
            print(f"El error que te jode es {e}")
            return []       

            



