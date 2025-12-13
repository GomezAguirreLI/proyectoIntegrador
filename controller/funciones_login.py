from tkinter import messagebox
from model.usuarios import Usuarios 
from view import constantes

class Funciones:
    @staticmethod
    def verificacion_registro(nom_1, nom_2, apellido, telf, correo, contrasena):
        # 1. Validaciones de campos vacíos
        if not nom_1: 
            messagebox.showerror(title="Error Registro", message="Please enter your first name.")
            return False
        if not apellido:
            messagebox.showerror(title="Error Registro", message="Please enter your last name.")
            return False
        if not telf:
            messagebox.showerror(title="Error Registro", message="Please enter your phone number.")
            return False
        if not correo:
            messagebox.showerror(title="Error Registro", message="Please enter your email.")
            return False
        if not contrasena: 
            messagebox.showerror(title="Error Registro", message="Please enter your password.")
            return False
        
        # 2. VALIDACIÓN ESTRICTA DE DOMINIO UTD
        # Convertimos a minúsculas para evitar errores si escriben "UTD.EDU.MX"
        if not correo.lower().endswith("@utd.edu.mx"):
            messagebox.showerror("Invalid Email", "Registration restricted.\nOnly institutional emails (@utd.edu.mx) are allowed.")
            return False
        
        # 3. Llamar al modelo si pasó las validaciones
        exito, error_tipo = Usuarios.insertar(nom_1, nom_2, apellido, telf, correo, contrasena)
        
        if exito:
            return True
        else:
            # Manejo de errores de BD (Doble seguridad)
            if error_tipo == "check_utd":
                messagebox.showerror("Email Inválido", "ONLY UTD EMAILS ARE ACCEPTED (Database restriction).")
            elif error_tipo == "duplicado":
                messagebox.showerror("Error Registro", "Email or phone number already exists.")
            else:
                messagebox.showerror("Error", "Registration failed. Check system logs.")
            return False

    @staticmethod
    def verificacion_login(correo, contrasena):
        if not correo:
            messagebox.showerror(title="Login Error", message="Please enter your email.")
            return False, None
        if not contrasena: 
            messagebox.showerror(title="Login Error", message="Please enter your password.")
            return False, None
        
        # Llamar al modelo
        exito, usuario_data, error_msg = Usuarios.login(correo, contrasena)
        
        if exito:
            return True, usuario_data
        else:
            messagebox.showerror("Login Error", error_msg or "Unexpected error")
            return False, None