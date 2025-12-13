import customtkinter as ctk
from tkinter import messagebox
from controller import funciones_login
from view import constantes, usuarios
from PIL import Image
import os

class Vista:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("ControlLabs System")
        self.ventana.geometry("1100x700")
        
        # Configuración de rutas de imagen
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        IMAGES_DIR = os.path.join(BASE_DIR, "view", "imagenes")
        
        self.logo_utd = None
        try:
            # Cargamos el logo de la UTD (asegúrate que el archivo exista)
            img_path = os.path.join(IMAGES_DIR, "logo_utd.png")
            if os.path.exists(img_path):
                # Un tamaño más grande para el login
                self.logo_utd = ctk.CTkImage(Image.open(img_path), size=(180, 80)) 
        except Exception as e:
            print(f"Error cargando logo: {e}")

        # Frame Principal (Fondo Verde)
        self.fondo = ctk.CTkFrame(self.ventana, fg_color=constantes.COLOR_PRIMARY)
        self.fondo.pack(fill="both", expand=True)

        # Muestra la pantalla de Login por defecto
        self.login()

    def _limpiar_frame(self):
        for widget in self.fondo.winfo_children():
            widget.destroy()

    def login(self):
        self._limpiar_frame()
        
        # --- CUADRO BLANCO (LOGIN CARD) ---
        # Hacemos el cuadro más ancho (width=500) y alto
        self.frame_login = ctk.CTkFrame(self.fondo, fg_color="white", width=500, height=650, corner_radius=20)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        # Evita que el frame se encoja a sus widgets internos
        self.frame_login.pack_propagate(False)

        # 1. LOGO UTD
        if self.logo_utd:
            label_logo = ctk.CTkLabel(self.frame_login, text="", image=self.logo_utd)
            label_logo.pack(pady=(50, 20))

        # 2. TÍTULO PRINCIPAL
        titulo = ctk.CTkLabel(self.frame_login, text="ControlLabs", font=("Roboto", 36, "bold"), text_color=constantes.COLOR_PRIMARY)
        titulo.pack(pady=(0, 10))

        subtitulo = ctk.CTkLabel(self.frame_login, text="Welcome Back! Please sign in.", font=("Roboto", 16), text_color="gray")
        subtitulo.pack(pady=(0, 40))

        # 3. CAMPOS DE ENTRADA
        # Usamos un frame interno para un mejor control del padding horizontal
        input_frame = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        input_frame.pack(fill="x", padx=50)

        # Email
        lbl_email = ctk.CTkLabel(input_frame, text="Email Address", font=("Roboto", 14, "bold"), text_color="#555")
        lbl_email.pack(anchor="w", pady=(0, 5))
        txt_email = ctk.CTkEntry(input_frame, width=400, height=45, font=("Roboto", 14), border_color="#E0E0E0", corner_radius=10)
        txt_email.pack(fill="x", pady=(0, 25))

        # Password
        lbl_password = ctk.CTkLabel(input_frame, text="Password", font=("Roboto", 14, "bold"), text_color="#555")
        lbl_password.pack(anchor="w", pady=(0, 5))
        txt_password = ctk.CTkEntry(input_frame, width=400, height=45, font=("Roboto", 14), show="*", border_color="#E0E0E0", corner_radius=10)
        txt_password.pack(fill="x", pady=(0, 10))

        # 4. BOTÓN DE LOGIN
        def manejar_login():
            email = txt_email.get().strip()
            contra = txt_password.get().strip()
            
            # Llamamos al controlador
            exito, usuario_data = funciones_login.Funciones.verificacion_login(email, contra)
            
            if exito:
                # usuario_data: (id, nom, seg_nom, ape, telf, email, rol)
                rol = usuario_data[6]
                
                # Redirección según el rol
                if rol == 'admin':
                    from view.usuarios import interfaz_admin
                    interfaz_admin.UsuariosAdmin(self.fondo)
                elif rol == 'usuario':
                    from view.usuarios import interfaz_profes
                    interfaz_profes.UsuariosProfes(self.fondo, usuario_data)
                else:
                    messagebox.showerror("Error", f"Rol desconocido: {rol}")

        btn_login = ctk.CTkButton(self.frame_login, text="SIGN IN", fg_color=constantes.COLOR_ACCENT, hover_color="#b87608", width=400, height=50, font=("Roboto", 16, "bold"), corner_radius=10, command=manejar_login)
        btn_login.pack(pady=(30, 20), padx=50)

        # 5. PIE DE PÁGINA (CREAR CUENTA)
        footer_frame = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        footer_frame.pack(pady=(10, 30))

        lbl_no_account = ctk.CTkLabel(footer_frame, text="Don't have an account?", font=("Roboto", 12), text_color="gray")
        lbl_no_account.pack(side="left")

        btn_registro = ctk.CTkButton(footer_frame, text="Create Account", fg_color="transparent", text_color=constantes.COLOR_PRIMARY, hover_color="#E8F5E9", font=("Roboto", 12, "bold"), width=100, command=self.registro)
        btn_registro.pack(side="left", padx=5)

        # Atajo de teclado
        txt_password.bind("<Return>", lambda event: manejar_login())

    def registro(self):
        self._limpiar_frame()
        
        # Frame de Registro (Más ancho también)
        self.frame_registro = ctk.CTkFrame(self.fondo, fg_color="white", width=600, height=750, corner_radius=20)
        self.frame_registro.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_registro.pack_propagate(False)

        # LOGO UTD
        if self.logo_utd:
            # Usamos una versión un poco más pequeña para el registro
            logo_small = ctk.CTkImage(Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "view", "imagenes", "logo_utd.png")), size=(140, 60))
            label_logo = ctk.CTkLabel(self.frame_registro, text="", image=logo_small)
            label_logo.pack(pady=(30, 10))

        titulo = ctk.CTkLabel(self.frame_registro, text="Create Account", font=("Roboto", 32, "bold"), text_color=constantes.COLOR_PRIMARY)
        titulo.pack(pady=(0, 5))

        subtitulo = ctk.CTkLabel(self.frame_registro, text="Join ControlLabs today.", font=("Roboto", 14), text_color="gray")
        subtitulo.pack(pady=(0, 30))

        # Contenedor de formulario (Grid para dos columnas)
        form_frame = ctk.CTkFrame(self.frame_registro, fg_color="transparent")
        form_frame.pack(fill="x", padx=50)
        form_frame.columnconfigure((0, 1), weight=1, uniform="column")

        # --- Estilo de los Entries ---
        entry_style = {"height": 45, "font": ("Roboto", 14), "border_color": "#E0E0E0", "corner_radius": 10}
        label_style = {"font": ("Roboto", 14, "bold"), "text_color": "#555", "anchor": "w"}

        # --- Columna Izquierda ---
        col1 = ctk.CTkFrame(form_frame, fg_color="transparent")
        col1.grid(row=0, column=0, padx=(0, 15), sticky="nsew")

        ctk.CTkLabel(col1, text="First Name", **label_style).pack(fill="x", pady=(0, 5))
        txt_nombre1 = ctk.CTkEntry(col1, **entry_style)
        txt_nombre1.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(col1, text="Last Name", **label_style).pack(fill="x", pady=(0, 5))
        txt_apellido = ctk.CTkEntry(col1, **entry_style)
        txt_apellido.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(col1, text="Phone Number", **label_style).pack(fill="x", pady=(0, 5))
        txt_telf = ctk.CTkEntry(col1, **entry_style)
        txt_telf.pack(fill="x", pady=(0, 20))

        # --- Columna Derecha ---
        col2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        col2.grid(row=0, column=1, padx=(15, 0), sticky="nsew")

        ctk.CTkLabel(col2, text="Middle Name (Optional)", **label_style).pack(fill="x", pady=(0, 5))
        txt_nombre2 = ctk.CTkEntry(col2, **entry_style)
        txt_nombre2.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(col2, text="Email (@utd.edu.mx)", **label_style).pack(fill="x", pady=(0, 5))
        txt_correo = ctk.CTkEntry(col2, **entry_style)
        txt_correo.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(col2, text="Password", **label_style).pack(fill="x", pady=(0, 5))
        txt_contrasena = ctk.CTkEntry(col2, show="*", **entry_style)
        txt_contrasena.pack(fill="x", pady=(0, 20))

        # --- Botón de Registro ---
        def manejar_registro():
            datos = (
                txt_nombre1.get().strip(),
                txt_nombre2.get().strip(),
                txt_apellido.get().strip(),
                txt_telf.get().strip(),
                txt_correo.get().strip(),
                txt_contrasena.get().strip()
            )
            # Llamamos al controlador
            if funciones_login.Funciones.verificacion_registro(*datos):
                messagebox.showinfo("Success", "Account created successfully!\nPlease sign in.")
                self.login()

        btn_crear = ctk.CTkButton(self.frame_registro, text="SIGN UP", fg_color=constantes.COLOR_ACCENT, hover_color="#b87608", width=400, height=50, font=("Roboto", 16, "bold"), corner_radius=10, command=manejar_registro)
        btn_crear.pack(pady=(30, 20), padx=50)

        # --- Pie de página ---
        footer_frame = ctk.CTkFrame(self.frame_registro, fg_color="transparent")
        footer_frame.pack(pady=(10, 30))
        
        ctk.CTkLabel(footer_frame, text="Already have an account?", font=("Roboto", 12), text_color="gray").pack(side="left")
        ctk.CTkButton(footer_frame, text="Sign In", fg_color="transparent", text_color=constantes.COLOR_PRIMARY, hover_color="#E8F5E9", font=("Roboto", 12, "bold"), width=80, command=self.login).pack(side="left", padx=5)