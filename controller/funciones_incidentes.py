from tkinter import messagebox
from model import incidentes
from model import laboratorios
class incidente:
    @staticmethod
    def insertar(id_usuario, incidente, id_laboratorio):
       
       enviar=incidentes.incidentes.insertar(id_usuario,incidente,id_laboratorio)
       if enviar:
           messagebox.showinfo(message="..::REPORTE HECHO CON EXITO::..")
           return True
       else:
           messagebox.showerror(message="..::POR EL MOMENTO NO SE ES POSIBLE HACER UN REPORTE::..")
           return False

    @staticmethod
    def consulta_Tabla(id):
        consulta_incidente=incidentes.incidentes.consulta_tabla(id)

        return consulta_incidente

    @staticmethod        
    def consulta_Tabla_lab(id):
        consulta_incidente=incidentes.incidentes.consulta_tabla_lab(id)

        return consulta_incidente
                  
                  
    @staticmethod        
    def consulta_Tabla_edificio(id):
        consulta_incidente=incidentes.incidentes.consulta_tabla_edifico(id)

        return consulta_incidente
    
    @staticmethod        
    def consulta_Tabla_fechaAsc(id):
        consulta_incidente=incidentes.incidentes.consulta_tabla_fehca_Asc(id)

        return consulta_incidente
    
    staticmethod        
    def consulta_Tabla_fechaDesc(id):
        consulta_incidente=incidentes.incidentes.consulta_tabla_fehca_Desc(id)

        return consulta_incidente
    
    @staticmethod
    def consulta_Tabla_Proceso(id):
        consulta_incidente=incidentes.incidentes.consulta_tabla_proceso(id)

        return consulta_incidente

    @staticmethod
    def consulta_Tabla_Proceso_terminado(id):
        consulta_incidente=incidentes.incidentes.consulta_tabla_proceso_terminado(id)

        return consulta_incidente


                  