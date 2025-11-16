from tkinter import messagebox
from controller import funciones_login
import os
from tkinter import *

class Vista:
    def __init__(self):
        # 1. Creamos la ventana PRINCIPAL aquí
        self.ventana = Tk()
        self.ventana.title("ControlLabs")
        self.ventana.state('zoomed') # Pantalla completa

        # Variable para controlar qué tarjeta se muestra
        self.tarjeta_actual = None

        # 2. Creamos el FONDO VERDE (una única vez)
        self.fondo = Frame(self.ventana, bg="#4e8c64")
        self.fondo.pack(fill="both", expand=True)

     

        # 3. Mostramos el Login al arrancar
        self.mostrar_login()

        # 4. Arrancamos el loop (SOLO UNA VEZ)
        self.ventana.mainloop()

    def limpiar_pantalla(self):
        """Elimina la tarjeta blanca actual para poner otra"""
        if self.tarjeta_actual:
            self.tarjeta_actual.destroy()

    def mostrar_login(self):
        self.limpiar_pantalla()
        
        # Tarjeta de Login
        self.tarjeta_actual = Frame(self.fondo, bg="white", padx=120, pady=120)
        self.tarjeta_actual.place(relx=0.5, rely=0.5, anchor="center")
        
        # Títulos
        Label(self.tarjeta_actual, text="Control Labs", font=("Arial", 40, "bold"), 
              bg="white", fg="black").pack(pady=(0, 5))
        Label(self.tarjeta_actual, text="iniciar sesión", font=("Arial", 20), 
              bg="white", fg="gray").pack(pady=(0, 30))

        # Inputs
        Label(self.tarjeta_actual, text="Ingresa tu usuario", font=("Arial", 15, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(10,0))
        Entry(self.tarjeta_actual, font=("Arial", 15), bg="#e0e0e0", bd=0, width=30).pack(ipady=8, pady=5)

        Label(self.tarjeta_actual, text="Ingresa tu contraseña", font=("Arial", 15, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(15,0))
        Entry(self.tarjeta_actual, font=("Arial", 15), bg="#e0e0e0", bd=0, show="*", width=30).pack(ipady=8, pady=5)

        # Botones
        # NOTA: Aquí llamamos a self.mostrar_registro SIN paréntesis
        btn_signup = Button(self.tarjeta_actual, text="Sign up", font=("Arial", 15, "bold"), 
                            bg="#4e8c64", fg="white", bd=0, cursor="hand2",
                            command=self.mostrar_registro) 
        btn_signup.pack(fill="x", pady=(30, 10), ipady=5)

        btn_login = Button(self.tarjeta_actual, text="Log in", font=("Arial", 15, "bold"), 
                           bg="#3b6b4b", fg="white", bd=0, cursor="hand2")
        btn_login.pack(fill="x", ipady=5)

    def mostrar_registro(self):
        self.limpiar_pantalla()
        
        # Tarjeta de Registro (Con menos padding vertical para que quepan todos los campos)
        self.tarjeta_actual = Frame(self.fondo, bg="white", padx=80, pady=40)
        self.tarjeta_actual.place(relx=0.5, rely=0.5, anchor="center")
        
        # Títulos
        Label(self.tarjeta_actual, text="Registro", font=("Arial", 30, "bold"), 
              bg="white", fg="black").pack(pady=(0, 20))

        # --- CAMPOS DE REGISTRO ---
        
        # 1. Primer Nombre
        primer_nombre=StringVar()
        lbl_primer_nombre=Label(self.tarjeta_actual, text="Primer nombre", font=("Arial", 10, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(5,0))
        txt_primer_nombre=Entry(self.tarjeta_actual, textvariable=primer_nombre,font=("Arial", 11), bg="#e0e0e0", bd=0, width=35).pack(ipady=5, pady=2)

        # 2. Segundo Nombre
        segundo_nombre=StringVar()
        lbl_segundo_nombre=Label(self.tarjeta_actual, text="Segundo nombre (Opcional)", font=("Arial", 10, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(5,0))
        txt_segundo_nombre=Entry(self.tarjeta_actual,textvariable=segundo_nombre, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35).pack(ipady=5, pady=2)

        # 3. Apellido Paterno
        apellido=StringVar()
        lbl_apellido=Label(self.tarjeta_actual, text="Apellido Paterno", font=("Arial", 10, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(5,0))
        txt_apellido=Entry(self.tarjeta_actual,textvariable=apellido, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35).pack(ipady=5, pady=2)

        # 4. Teléfono
        telf=StringVar()
        lbl_telf=Label(self.tarjeta_actual, text="Teléfono", font=("Arial", 10, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(5,0))
        txt_telf=Entry(self.tarjeta_actual,textvariable=telf, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35).pack(ipady=5, pady=2)

        # 5. Correo
        correo=StringVar()
        lbl_correo=Label(self.tarjeta_actual, text="Correo Electrónico", font=("Arial", 10, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(5,0))
        txt_correo=Entry(self.tarjeta_actual,textvariable=correo, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35).pack(ipady=5, pady=2)
        
        # 6. Contraseña
        contrasena=StringVar()
        lbl_contrasena=Label(self.tarjeta_actual, text="Contraseña", font=("Arial", 10, "bold"), 
              bg="white", fg="#4e8c64", anchor="w").pack(fill="x", pady=(5,0))
        txt_contrasena=Entry(self.tarjeta_actual,textvariable=contrasena, font=("Arial", 11), bg="#e0e0e0", bd=0, show="*", width=35).pack(ipady=5, pady=2)

        # Botón Guardar
        btn_guardar = Button(self.tarjeta_actual, text="Registrarme", font=("Arial", 12, "bold"), 
                             bg="#4e8c64", fg="white", bd=0, cursor="hand2",command=lambda:funciones_login.Funciones.verificacion_registro(primer_nombre.get(),segundo_nombre.get(),apellido.get(),telf.get(),correo.get(),contrasena.get()))
        btn_guardar.pack(fill="x", pady=(20, 5), ipady=5)

        # Botón Volver
        btn_volver = Button(self.tarjeta_actual, text="← Volver al Login", font=("Arial", 9, "bold"), 
                            bg="white", fg="gray", bd=0, cursor="hand2",
                            command=self.mostrar_login)
        btn_volver.pack(fill="x", ipady=5)