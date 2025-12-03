from conexionBD import *
from mysql.connector import Error as DbErrorS


class laboratorios:
    @staticmethod
    def consultar():
        try:
            cursor.execute("SELECT nombre, edificio, piso, cant_pc FROM laboratorios")
            return cursor.fetchall()
        except:
            return []
        
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
    



