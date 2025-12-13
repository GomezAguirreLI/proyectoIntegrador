from tkinter import messagebox
from model import incidentes

class incidente:
    
    @staticmethod
    def insertar(id_usuario, texto_incidente, id_laboratorio):
        # Llamamos al modelo
        # No mostramos messagebox aquí porque la Vista ya lo hace (para evitar doble mensaje)
        return incidentes.incidentes.insertar(id_usuario, texto_incidente, id_laboratorio)

    @staticmethod
    def actualizar(datos):
        # datos llega como una tupla: (id_incidente, nuevo_texto)
        id_incidente = datos[0]
        nuevo_texto = datos[1]
        return incidentes.incidentes.actualizar(id_incidente, nuevo_texto)

    @staticmethod
    def borrarIncidente(datos):
        # datos es la fila seleccionada de la tabla. El ID está en la posición 0.
        try:
            id_incidente = datos[0] 
            if incidentes.incidentes.borrarIncidente(id_incidente):
                messagebox.showinfo("Success", "Report deleted successfully.")
                return True
            else:
                messagebox.showerror("Error", "Could not delete the report.")
                return False
        except Exception as e:
            print(f"Error en controlador borrar: {e}")
            return False

    # --- Consultas (Pasan directo al modelo) ---

    @staticmethod
    def consulta_Tabla(id_usuario):
        return incidentes.incidentes.consulta_tabla(id_usuario)

    @staticmethod       
    def consulta_Tabla_lab(id_usuario):
        return incidentes.incidentes.consulta_tabla_lab(id_usuario)
                  
    @staticmethod       
    def consulta_Tabla_edificio(id_usuario):
        return incidentes.incidentes.consulta_tabla_edifico(id_usuario)
    
    @staticmethod       
    def consulta_Tabla_fechaAsc(id_usuario):
        return incidentes.incidentes.consulta_tabla_fehca_Asc(id_usuario)
    
    @staticmethod       
    def consulta_Tabla_fechaDesc(id_usuario):
        return incidentes.incidentes.consulta_tabla_fehca_Desc(id_usuario)
    
    @staticmethod
    def consulta_Tabla_Proceso(id_usuario):
        return incidentes.incidentes.consulta_tabla_proceso(id_usuario)

    @staticmethod
    def consulta_Tabla_Proceso_terminado(id_usuario):
        return incidentes.incidentes.consulta_tabla_proceso_terminado(id_usuario)