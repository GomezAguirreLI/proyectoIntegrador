from tkinter import messagebox
from model import usuarios

class Funciones:
    @staticmethod
    def verificacion_registro(nom_1, nom_2, apellido, telf, correo, contrasena):
        flag = True
        
        if nom_1 == "": 
            messagebox.showerror(title="Error de Registro", message="Por favor ingrese su primer nombre")
            flag = False            
        elif apellido == "":
            messagebox.showerror(title="Error de Registro", message="Por favor ingrese su primer apellido")
            flag = False  
        elif telf == "":
            messagebox.showerror(title="Error de Registro", message="Por favor ingrese su teléfono")
            flag = False  
        elif correo == "":
            messagebox.showerror(title="Error de Registro", message="Por favor ingrese su correo")
            flag = False  
        elif contrasena == "": 
            messagebox.showerror(title="Error de Registro", message="Por favor ingrese su contraseña")
            flag = False  
        
        if flag:
            # Confirmación general
            pregunta = messagebox.askquestion(
                message=f"¿Está seguro que quiere guardar estos datos? {nom_1} {nom_2} {apellido} {telf} {correo} {contrasena}",
                icon="question", title="ALERTA"
            )
            if pregunta == "yes":
                # Si no hay segundo nombre, confirmar
                if nom_2 == "":
                    pregunta_segundo = messagebox.askquestion(
                        message="¿Está seguro que no quiere guardar un segundo nombre?",
                        icon="question", title="ALERTA"
                    )
                    if pregunta_segundo != "yes":
                        return False  # No proceder si no confirma
                
                # Intentar insertar
                exito, error_tipo = usuarios.Usuarios.insertar(nom_1, nom_2, apellido, telf, correo, contrasena)
                if exito:
                    # Registro exitoso: devolver True (no mostrar messagebox aquí, lo hará Vista)
                    return True
                else:
                    # Manejar errores con messagebox
                    if error_tipo == "check_utd":
                        messagebox.showerror("Correo Inválido", "NO SE ACEPTAN CORREOS QUE NO SEAN DE LA UTD")
                    elif error_tipo == "duplicado":
                        messagebox.showerror("Error de Registro", "DATOS YA USADOS EN LA BASE DE DATOS (El correo ya existe)")
                    else:
                        messagebox.showerror("Error Inesperado", f"REGISTRO fallido. Error: {error_tipo}")
                    return False
        return False  # Si no pasó las validaciones iniciales
    
    @staticmethod
    def verificacion_login(correo, contrasena):
        flag = True  # Inicializar flag
        
        if correo == "":
            messagebox.showerror(title="Error de Login", message="Por favor ingrese su correo")
            flag = False  
        elif contrasena == "": 
            messagebox.showerror(title="Error de Login", message="Por favor ingrese su contraseña")
            flag = False  
        
        if flag:
            # Llamar a login y desempaquetar los tres valores
            exito, usuario, error_msg = usuarios.Usuarios.login(correo, contrasena)
            if exito:
                return True  # Login exitoso
            else:
                # Mostrar error basado en error_msg
                messagebox.showerror("Error de Login", error_msg or "Credenciales incorrectas o error inesperado")
                return False
        return False  # Si no pasó las validaciones iniciales