from tkinter import messagebox
from controller import funciones_login
import os
from tkinter import *
from PIL import Image,ImageTk
from view import constantes

class Vista:
    def __init__(self):
        # 1. Creamos la ventana PRINCIPAL aquí
        self.ventana = Tk()
        self.ventana.title("ControlLabs")
        self.ventana.state('zoomed')  # Pantalla completa

        # Variable para controlar qué tarjeta se muestra
        self.tarjeta_actual = None

        # 2. Creamos el FONDO VERDE (una única vez)
        self.fondo = Frame(self.ventana, bg=constantes.color)
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
        lbl_titulo = Label(self.tarjeta_actual, text="Control Labs", font=("Arial", 40, "bold"), 
              bg="white", fg="black")
        lbl_titulo.pack(pady=(0, 5))
        lbl_iniciar = Label(self.tarjeta_actual, text="iniciar sesión", font=("Arial", 20), 
              bg="white", fg="gray")
        lbl_iniciar.pack(pady=(0, 30))

        # Inputs
        lbl_correo = Label(self.tarjeta_actual, text="Ingresa tu correo", font=("Arial", 15, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_correo.pack(fill="x", pady=(10,0))
        correo = StringVar()
        txt_correo = Entry(self.tarjeta_actual, font=("Arial", 15), bg="#e0e0e0", bd=0, width=30, textvariable=correo)
        txt_correo.pack(ipady=8, pady=5)

        lbl_contrasena = Label(self.tarjeta_actual, text="Ingresa tu contraseña", font=("Arial", 15, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_contrasena.pack(fill="x", pady=(15,0))
        contrasena = StringVar()
        txt_contrasena = Entry(self.tarjeta_actual, font=("Arial", 15), bg="#e0e0e0", bd=0, show="*", width=30, textvariable=contrasena)
        txt_contrasena.pack(ipady=8, pady=5)

        # Función interna para manejar el login y redirigir
        def manejar_login():
            exito = funciones_login.Funciones.verificacion_login(correo.get(), contrasena.get())
            if exito:
                messagebox.showinfo("Login Exitoso", "¡Bienvenido a Control Labs!")
                self.mostrar_principal()  # Redirigir a pantalla principal (vacía)

        # Botones
        btn_signup = Button(self.tarjeta_actual, text="Sign up", font=("Arial", 15, "bold"), 
                            bg=constantes.color, fg="white", bd=0, cursor="hand2",
                            command=self.mostrar_registro)
        btn_signup.pack(fill="x", pady=(30, 10), ipady=5)

        btn_login = Button(self.tarjeta_actual, text="Log in", font=("Arial", 15, "bold"), 
                           bg="#3b6b4b", fg="white", bd=0, cursor="hand2", command=manejar_login)
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
        primer_nombre = StringVar()
        lbl_primer_nombre = Label(self.tarjeta_actual, text="Primer nombre", font=("Arial", 10, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_primer_nombre.pack(fill="x", pady=(5,0))
        txt_primer_nombre = Entry(self.tarjeta_actual, textvariable=primer_nombre, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35)
        txt_primer_nombre.pack(ipady=5, pady=2)

        # 2. Segundo Nombre
        segundo_nombre = StringVar()
        lbl_segundo_nombre = Label(self.tarjeta_actual, text="Segundo nombre (Opcional)", font=("Arial", 10, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_segundo_nombre.pack(fill="x", pady=(5,0))
        txt_segundo_nombre = Entry(self.tarjeta_actual, textvariable=segundo_nombre, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35)
        txt_segundo_nombre.pack(ipady=5, pady=2)

        # 3. Apellido Paterno
        apellido = StringVar()
        lbl_apellido = Label(self.tarjeta_actual, text="Apellido Paterno", font=("Arial", 10, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_apellido.pack(fill="x", pady=(5,0))
        txt_apellido = Entry(self.tarjeta_actual, textvariable=apellido, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35)
        txt_apellido.pack(ipady=5, pady=2)

        # 4. Teléfono
        telf = StringVar()
        lbl_telf = Label(self.tarjeta_actual, text="Teléfono", font=("Arial", 10, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_telf.pack(fill="x", pady=(5,0))
        txt_telf = Entry(self.tarjeta_actual, textvariable=telf, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35)
        txt_telf.pack(ipady=5, pady=2)

        # 5. Correo
        correo = StringVar()
        lbl_correo = Label(self.tarjeta_actual, text="Correo Electrónico", font=("Arial", 10, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_correo.pack(fill="x", pady=(5,0))
        txt_correo = Entry(self.tarjeta_actual, textvariable=correo, font=("Arial", 11), bg="#e0e0e0", bd=0, width=35)
        txt_correo.pack(ipady=5, pady=2)
        
        # 6. Contraseña
        contrasena = StringVar()
        lbl_contrasena = Label(self.tarjeta_actual, text="Contraseña", font=("Arial", 10, "bold"), 
              bg="white", fg=constantes.color, anchor="w")
        lbl_contrasena.pack(fill="x", pady=(5,0))
        txt_contrasena = Entry(self.tarjeta_actual, textvariable=contrasena, font=("Arial", 11), bg="#e0e0e0", bd=0, show="*", width=35)
        txt_contrasena.pack(ipady=5, pady=2)

        # Función interna para manejar el registro y redirigir
        def manejar_registro():
            exito = funciones_login.Funciones.verificacion_registro(
                primer_nombre.get(), segundo_nombre.get(), apellido.get(), 
                telf.get(), correo.get(), contrasena.get()
            )
            if exito:
                messagebox.showinfo("Registro Exitoso", "¡Usuario registrado correctamente! Ahora puedes iniciar sesión.")
                self.mostrar_login()  # Redirigir al login

        # Botón Guardar
        btn_guardar = Button(self.tarjeta_actual, text="Registrarme", font=("Arial", 12, "bold"), 
                             bg=constantes.color, fg="white", bd=0, cursor="hand2", command=manejar_registro)
        btn_guardar.pack(fill="x", pady=(20, 5), ipady=5)

        # Botón Volver
        btn_volver = Button(self.tarjeta_actual, text="← Volver al Login", font=("Arial", 9, "bold"), 
                            bg="white", fg="gray", bd=0, cursor="hand2",
                            command=self.mostrar_login)
        btn_volver.pack(fill="x", ipady=5)



     #---------------------------
     # EN PRUEBA
     # ---------------   

    def mostrar_principal(self):
        self.limpiar_pantalla()

        # === CONTENEDOR PRINCIPAL (FONDO BLANCO) ===
        self.tarjeta_actual = Frame(self.fondo, bg="white")
        self.tarjeta_actual.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.78, relheight=0.85)

        # === COLUMNA VERDE IZQUIERDA ===
        sidebar = Frame(self.fondo, bg=constantes.color)
        sidebar.place(relx=0.02, rely=0.02, relwidth=0.18, relheight=0.96)

        Label(sidebar, text="Control Labs", bg=constantes.color, fg="white",
              font=("Arial", 26, "bold")).pack(pady=(30, 20))

        Label(sidebar, text="User's name", bg=constantes.color, fg="white",
              font=("Arial", 16)).pack(pady=10)

        Button(sidebar, text="Reportar", bg=constantes.color, fg="white",
              font=("Arial", 18, "bold"), bd=0, cursor="hand2").pack(pady=40)

        Button(sidebar, text="Mi historial", bg=constantes.color, fg="white",
              font=("Arial", 18, "bold"), bd=0, cursor="hand2").pack(pady=20)

        # === TÍTULO ===
        Label(self.tarjeta_actual, text="Seleccionar Laboratorio",
              font=("Arial", 40, "bold"), bg="white", fg="#335f3a").place(x=50, y=20)

        # === BARRA DE BÚSQUEDA ===
        barra = Entry(self.tarjeta_actual, font=("Arial", 20),
                      bg="#d9d9d9", bd=0)
        barra.place(x=50, y=110, width=650, height=55)

        Button(self.tarjeta_actual, text="🔍", font=("Arial", 20),
               bg="#d9d9d9", bd=0).place(x=720, y=110, width=60, height=55)

        # ============================================
        # FUNCIÓN PARA CREAR CADA LABORATORIO
        # ============================================
        def crear_lab(y, nombre):
            cont = Frame(self.tarjeta_actual, bg="white")
            cont.place(x=40, y=y)

            # Icono (simple recuadro)
            Frame(cont, width=120, height=120, bg="white",
                  highlightbackground="black", highlightthickness=3).pack(side="left", padx=10)

            # Botón verde
            btn = Button(cont, text=nombre, font=("Arial", 22, "bold"),
                         bg=constantes.color, fg="white", bd=0,
                         width=15, height=1)
            btn.pack(pady=5, padx=25)

            # Descripción
            Label(cont, text="Laboratorio que está en el edificio C\nEn la planta baja",
                  font=("Arial", 14), bg="white", justify="left").pack(padx=25)

        # === CREAR LOS LABS ===
        crear_lab(200, "Lab 1")
        crear_lab(380, "Lab 2")
        crear_lab(560, "LAB 3")

        # === CERRAR SESIÓN ===
        Button(self.tarjeta_actual, text="Cerrar Sesión", font=("Arial", 15, "bold"),
               bg=constantes.color, fg="white", bd=0, cursor="hand2",
               command=self.mostrar_login).place(relx=0.85, rely=0.92)
