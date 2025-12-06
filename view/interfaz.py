from tkinter import messagebox
from controller import funciones_login
import os
from tkinter import *
from PIL import Image, ImageTk
from view import constantes
from .usuarios import interfaz_profes
from .usuarios import interfaz_admin


class Vista:
    def __init__(self, ventana):
        # 1. Usar la ventana que nos pasan (no crear otra)
        self.ventana = ventana
        self.ventana.title("ControlLabs")
        try:
            self.ventana.state('zoomed')  # Pantalla completa cuando esté disponible
        except Exception:
            pass

        # Variable para controlar qué tarjeta se muestra
        self.tarjeta_actual = None

        # 2. Creamos el FONDO VERDE (una única vez)
        self.fondo = Frame(self.ventana, bg=constantes.color)
        self.fondo.pack(fill="both", expand=True)

        # 3. Mostramos el Login al arrancar
        self.mostrar_login()

    def limpiar_pantalla(self):
        # Limpiar solo los widgets contenidos en el frame de fondo
        for widget in self.fondo.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        # Limpiar solo los widgets del frame fondo (no destruir la ventana completa)
        self.limpiar_pantalla()

        # Tarjeta de Login
        self.tarjeta_actual = Frame(self.fondo, bg="white", padx=120, pady=120)
        self.tarjeta_actual.place(relx=0.5, rely=0.5, anchor="center")

        # Títulos
        lbl_titulo = Label(self.tarjeta_actual, text="Control Labs", font=("Arial", 40, "bold"),
                           bg="white", fg="black")
        lbl_titulo.pack(pady=(0, 5))
        lbl_iniciar = Label(self.tarjeta_actual, text="iniciar sesión", font=("Arial", 20),
                            bg="white", fg="gray")
        lbl_iniciar.pack(pady=(0, 30))

        # Inputs
        lbl_correo = Label(self.tarjeta_actual, text="Ingresa tu correo", font=("Arial", 15, "bold"),
                           bg="white", fg=constantes.color, anchor="w")
        lbl_correo.pack(fill="x", pady=(10, 0))
        correo = StringVar()
        txt_correo = Entry(self.tarjeta_actual, font=("Arial", 15), bg="#e0e0e0", bd=0, width=30,
                           textvariable=correo)
        txt_correo.pack(ipady=8, pady=5)
        txt_correo.focus()

        lbl_contrasena = Label(self.tarjeta_actual, text="Ingresa tu contraseña", font=("Arial", 15, "bold"),
                               bg="white", fg=constantes.color, anchor="w")
        lbl_contrasena.pack(fill="x", pady=(15, 0))
        contrasena = StringVar()
        txt_contrasena = Entry(self.tarjeta_actual, font=("Arial", 15), bg="#e0e0e0", bd=0, show="*", width=30,
                               textvariable=contrasena)
        txt_contrasena.pack(ipady=8, pady=5)

        # Función interna para manejar el login y redirigir
        def manejar_login():
            exito,usuario = funciones_login.Funciones.verificacion_login(correo.get(), contrasena.get())
            if exito:
                if usuario[7]=="admin":
                    up = interfaz_admin.UsuariosAdmin(self.fondo)
                    up.mostrar_dashboard()
                else:
                
                    messagebox.showinfo("Login Exitoso", "¡Bienvenido a Control Labs!")
                    # Primero limpiar la pantalla actual (login)
                    self.limpiar_pantalla()
                    # Cargar la interfaz de profesores dentro del mismo contenedor
                    # Instanciar la clase que maneja el dashboard y mostrar la vista
                    up = interfaz_profes.UsuariosProfes(self.fondo,usuario)
                    up.mostrar_dashboard()
                

        # Botones
        btn_signup = Button(self.tarjeta_actual, text="Sign up", font=("Arial", 15, "bold"), 
                            bg=constantes.color, fg="white", bd=0, cursor="hand2",
                            command=self.mostrar_registro)
    
        btn_signup.pack(fill="x", pady=(30, 10), ipady=5)

        btn_login = Button(self.tarjeta_actual, text="Log in", font=("Arial", 15, "bold"), 
                           bg="#3b6b4b", fg="white", bd=0, cursor="hand2", command=manejar_login)
        btn_login.pack(fill="x", ipady=5)

        txt_correo.bind("<Return>",lambda e:txt_contrasena.focus())
        txt_contrasena.bind("<Return>",lambda event: manejar_login())
        txt_contrasena.bind("<Up>",lambda e:txt_correo.focus())
        txt_correo.bind("<Down>",lambda e:txt_contrasena.focus())

        




    def mostrar_registro(self):
        self.limpiar_pantalla()

        # Tarjeta de Registro (Con menos padding vertical para que quepan todos los campos)
        self.tarjeta_actual = Frame(self.fondo, bg="white", padx=80, pady=40)
        self.tarjeta_actual.place(relx=0.5, rely=0.5, anchor="center")

        # Títulos
        Label(self.tarjeta_actual, text="Registro", font=("Arial", 30, "bold"), bg="white", fg="black").pack(
            pady=(0, 20))

        # --- CAMPOS DE REGISTRO ---

        # 1. Primer Nombre
        primer_nombre = StringVar()
        lbl_primer_nombre = Label(self.tarjeta_actual, text="Primer nombre", font=("Arial", 10, "bold"),
                                  bg="white", fg=constantes.color, anchor="w")
        lbl_primer_nombre.pack(fill="x", pady=(5, 0))
        txt_primer_nombre = Entry(self.tarjeta_actual, textvariable=primer_nombre, font=("Arial", 11),
                                  bg="#e0e0e0", bd=0, width=35)
        txt_primer_nombre.pack(ipady=5, pady=2)
        txt_primer_nombre.focus()

        # 2. Segundo Nombre
        segundo_nombre = StringVar()
        lbl_segundo_nombre = Label(self.tarjeta_actual, text="Segundo nombre (Opcional)",
                                   font=("Arial", 10, "bold"), bg="white", fg=constantes.color, anchor="w")
        lbl_segundo_nombre.pack(fill="x", pady=(5, 0))
        txt_segundo_nombre = Entry(self.tarjeta_actual, textvariable=segundo_nombre, font=("Arial", 11),
                                   bg="#e0e0e0", bd=0, width=35)
        txt_segundo_nombre.pack(ipady=5, pady=2)

        # 3. Apellido Paterno
        apellido = StringVar()
        lbl_apellido = Label(self.tarjeta_actual, text="Apellido Paterno", font=("Arial", 10, "bold"),
                             bg="white", fg=constantes.color, anchor="w")
        lbl_apellido.pack(fill="x", pady=(5, 0))
        txt_apellido = Entry(self.tarjeta_actual, textvariable=apellido, font=("Arial", 11), bg="#e0e0e0", bd=0,
                             width=35)
        txt_apellido.pack(ipady=5, pady=2)

        # 4. Teléfono
        telf = StringVar()
        lbl_telf = Label(self.tarjeta_actual, text="Teléfono", font=("Arial", 10, "bold"), bg="white",
                         fg=constantes.color, anchor="w")
        lbl_telf.pack(fill="x", pady=(5, 0))
        txt_telf = Entry(self.tarjeta_actual, textvariable=telf, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35)
        txt_telf.pack(ipady=5, pady=2)

        # 5. Correo
        correo = StringVar()
        lbl_correo = Label(self.tarjeta_actual, text="Correo Electrónico", font=("Arial", 10, "bold"),
                           bg="white", fg=constantes.color, anchor="w")
        lbl_correo.pack(fill="x", pady=(5, 0))
        txt_correo = Entry(self.tarjeta_actual, textvariable=correo, font=("Arial", 11), bg="#e0e0e0", bd=0,
                           width=35)
        txt_correo.pack(ipady=5, pady=2)

        # 6. Contraseña
        contrasena = StringVar()
        lbl_contrasena = Label(self.tarjeta_actual, text="Contraseña", font=("Arial", 10, "bold"), bg="white",
                               fg=constantes.color, anchor="w")
        lbl_contrasena.pack(fill="x", pady=(5, 0))
        txt_contrasena = Entry(self.tarjeta_actual, textvariable=contrasena, font=("Arial", 11), bg="#e0e0e0", bd=0,
                               show="*", width=35)
        txt_contrasena.pack(ipady=5, pady=2)

        # Función interna para manejar el registro y redirigir
        def manejar_registro():
            exito = funciones_login.Funciones.verificacion_registro(
                primer_nombre.get(), segundo_nombre.get(), apellido.get(), telf.get(), correo.get(), contrasena.get()
            )
            if exito:
                messagebox.showinfo("Registro Exitoso", "¡Usuario registrado correctamente! Ahora puedes iniciar sesión.")
                self.mostrar_login()  # Redirigir al login

        # Botón Guardar
        btn_guardar = Button(self.tarjeta_actual, text="Registrarme", font=("Arial", 12, "bold"), bg=constantes.color,
                             fg="white", bd=0, cursor="hand2", command=manejar_registro)
        btn_guardar.pack(fill="x", pady=(20, 5), ipady=5)

        # Botón Volver
        btn_volver = Button(self.tarjeta_actual, text="← Volver al Login", font=("Arial", 9, "bold"), bg="white",
                            fg="gray", bd=0, cursor="hand2", command=self.mostrar_login)
        btn_volver.pack(fill="x", ipady=5)

        txt_primer_nombre.bind("<Return>",lambda e:txt_segundo_nombre.focus())
        txt_segundo_nombre.bind("<Return>",lambda e:txt_apellido.focus())
        txt_apellido.bind("<Return>",lambda e:txt_telf.focus()) 
        txt_telf.bind("<Return>",lambda e:txt_correo.focus())
        txt_correo.bind("<Return>",lambda e:txt_contrasena.focus())
        txt_contrasena.bind("<Return>",lambda event: manejar_registro())


