from tkinter import messagebox
from model import incidentes

class incidente:
    @staticmethod
    def insertar(id_usuario, incidente, id_laboratorio):
       
       enviar=incidentes.incidentes.insertar(id_usuario,incidente,id_laboratorio)
       if enviar:
           messagebox.showinfo(message="..::REPORTE HECHO CON EXITO::..")
       else:
           messagebox.showerror(message="..::POR EL MOMENTO NO SE ES POSIBLE HACER UN REPORTE::..")
                  
  