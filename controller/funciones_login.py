from tkinter import messagebox
from model import usuarios
# 'usuarios' no se usará en esta función,
# pero sí en la siguiente (guardar_registro)
# from model import usuarios 

class Funciones:
    
    @staticmethod
    def verificacion_registro(nom_1, nom_2, apellido, telf, correo, contrasena):
        flag=True
        
        if nom_1=="": 
            messagebox.showerror(title="Error de Registro",message="Por favor ingrese su primer nombre")
            flag=False            
        elif apellido=="":
            messagebox.showerror(title="Error de Registro", 
                                 message="Por favor ingrese su primer apellido")
            flag=False  
        elif telf=="":
            messagebox.showerror(title="Error de Registro", 
                                 message="Por favor ingrese su teléfono")
            flag=False  
        elif correo=="":
            messagebox.showerror(title="Error de Registro", 
                                 message="Por favor ingrese su correo")
            flag=False  
        elif contrasena=="": 
            messagebox.showerror(title="Error de Registro", 
                                 message="Por favor ingrese su contraseña")
            flag=False  
        if flag:
            pregunta=messagebox.askquestion(message=f"Esta seguro que quiere guardar estos datos {nom_1, nom_2, apellido, telf, correo, contrasena}",icon="question",title="ALERTA")
            if nom_2=="":
                pregunta=messagebox.askquestion(message="Esta seguro que no quiere guardar un segundo nombre",icon="question",title="ALERTA")
                if pregunta=="yes":
                    usuarios.Usuarios.insertar(nom_1, nom_2, apellido, telf, correo, contrasena)
            if pregunta=="yes":
                    exito,error_tipo=usuarios.Usuarios.insertar(nom_1, nom_2, apellido, telf, correo, contrasena)
                    if exito:
                        alerta=messagebox.showinfo(message="REGISTRO EXITOSO")
                    else:
                       if error_tipo == "check_utd":
                        messagebox.showerror("Correo Inválido", "NO SE ACEPTAN CORREOS QUE NO SEAN DE LA UTD")
                       elif error_tipo == "duplicado":
                         messagebox.showerror("Error de Registro", "DATOS YA USADOS EN LA BASE DE DATOS (El correo ya existe)")
                       else:
                         # Mensaje genérico para cualquier OTRO error
                         messagebox.showerror("Error Inesperado", f"REGISTRO fallido. Error: {error_tipo}")
