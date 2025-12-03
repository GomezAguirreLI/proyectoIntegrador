from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
from view import constantes
from tkinter import ttk
from tkinter import *


class UsuariosAdmin:
    """
    Clase que construye el dashboard para los profesores.
    
    Cada interfaz está separada en métodos:
      - mostrar_dashboard()
      - mostrar_perfil()
      - mostrar_laboratorios()

    Todas las interfaces usan el mismo menú lateral.
    """

    def __init__(self, ventana):
        self.ventana = ventana

        # Limpiar la ventana recibida
        for w in self.ventana.winfo_children():
            w.destroy()

        # ====== CONTENEDOR PRINCIPAL ======
        self.container = ctk.CTkFrame(self.ventana, fg_color="white")
        self.container.pack(fill="both", expand=True)

        # ====== SIDEBAR (MENU LATERAL) ======
        self.sidebar = ctk.CTkFrame(
            self.container,
            fg_color=constantes.color,
            width=220,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ====== ÁREA PRINCIPAL (DONDE CAMBIA TODO) ======
        self.main = ctk.CTkFrame(self.container, fg_color="white")
        self.main.pack(side="left", fill="both", expand=True)

        # Crear botones del menú
        self._build_sidebar()

        # Mostrar interfaz inicial
        self.mostrar_dashboard()

    # =====================================================
    #   MÉTODOS PARA DIBUJAR CADA INTERFAZ
    # =====================================================

    def mostrar_dashboard(self):
        self._clear_main()
        messagebox.showinfo(message="¡Bienvenido  al panel de adminstradores! Aqui podra ver los reportes que se han hecho en la UTD")
        # ---------------- TITULO ----------------
        titulo = ctk.CTkLabel(
            self.main,
            text="Seleccionar Laboratorio",
            text_color="#32df57",
            font=("Arial", 50, "bold")
        )
        titulo.pack(pady=20)

        # ------------ CONTENEDOR BARRA DE BUSQUEDA ------------
        contenedor = ctk.CTkFrame(self.main, fg_color="transparent")
        contenedor.pack(pady=10)

        lbl_buscar = ctk.CTkLabel(
            contenedor,
            text="Busca por ID",
            font=("Arial", 14)
        )
        lbl_buscar.pack(anchor="w", pady=(0, 5))

        fila = ctk.CTkFrame(contenedor, fg_color="transparent")
        fila.pack(pady=5, anchor="center")   # ⬅ Centrar toda la fila

        # Entry
        txt_buscar = ctk.CTkEntry(
            fila,
            width=350,
            height=40,
            corner_radius=20,
            placeholder_text="Escribe el ID...",
            fg_color="#e6e6e6"
        )
        txt_buscar.pack(side="left", padx=5)

        # Botón BUSCAR
        btn_buscar = ctk.CTkButton(
            fila,
            text="BUSCAR",
            fg_color="#32df57",
            hover_color="#28c94b",
            text_color="white",
            corner_radius=20,
            width=120,
            height=40
        )
        btn_buscar.pack(side="left", padx=10)

         # Botón REPORTAR
        btn_reportar = ctk.CTkButton(
            fila,
            text="REPORTAR",
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="white",
            corner_radius=20,
            width=120,
            height=40,
            command=lambda:self.generar_reportes()
        )
        btn_reportar.pack(side="left", padx=10)


        # ---------------- TABLA ----------------
        tabla_frame = ctk.CTkFrame(self.main, fg_color="#e5e5e5", corner_radius=10)
        tabla_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # --------- ESTILOS DEL TREEVIEW PARA QUE COMBINE ---------
        style = ttk.Style()
        style.configure("Treeview",
                        background="#f2f2f2",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="#f2f2f2",
                        font=("Arial", 13))
        style.configure("Treeview.Heading",
                        background="#c3c3c3",
                        foreground="black",
                        font=("Arial", 14, "bold"))
        style.map("Treeview",
                background=[("selected", "#32df57")])

        # --------- CREAR TREEVIEW ---------
        columnas = ("id_lab", "edificio", "piso", "idiomas", "cant_pc")

        tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)

        tabla.heading("id_lab", text="ID")
        tabla.heading("edificio", text="Edificio")
        tabla.heading("piso", text="Piso")
        tabla.heading("idiomas", text="Idiomas")
        tabla.heading("cant_pc", text="Cantidad de equipos")

        tabla.column("id_lab", width=80, anchor="center")
        tabla.column("edificio", width=200, anchor="center")
        tabla.column("piso", width=80, anchor="center")
        tabla.column("idiomas", width=120, anchor="center")
        tabla.column("cant_pc", width=180, anchor="center")

        tabla.pack(fill="both", expand=True, padx=10, pady=10)
       
    def mostrar_perfil(self):
        self._clear_main()

    # ----- TÍTULO -----
        titulo = ctk.CTkLabel(
            self.main,
            text="Perfil del Usuario",
            text_color="#32df57",
            font=("Arial", 40, "bold")
        )
        titulo.pack(pady=25)

        # ----- FRAME CONTENEDOR -----
        contenedor = ctk.CTkFrame(self.main, fg_color="#f2f2f2", corner_radius=20)
        contenedor.pack(pady=20, padx=40, fill="both", expand=False)

        # ================= ENTRIES ESTILO UNIFICADO =================

        entry_style = {
            "width": 450,
            "height": 45,
            "font": ("Arial", 16),
            "fg_color": "#f7f5f2",          # Fondo hueso
            "text_color": "black",          # Texto negro
            "placeholder_text_color": "#8e8e8e"
        }

        # Nombre
        lbl_nombre = ctk.CTkLabel(contenedor, text="Nombre completo:", font=("Arial", 18))
        lbl_nombre.pack(anchor="w", padx=20, pady=(20, 5))

        txt_nombre = ctk.CTkEntry(
            contenedor,
            placeholder_text="Ingresa tu nombre",
            **entry_style
        )
        txt_nombre.pack(padx=20, pady=5)

        # Correo
        lbl_correo = ctk.CTkLabel(contenedor, text="Correo:", font=("Arial", 18))
        lbl_correo.pack(anchor="w", padx=20, pady=(15, 5))

        txt_correo = ctk.CTkEntry(
            contenedor,
            placeholder_text="correo@ejemplo.com",
            **entry_style
        )
        txt_correo.pack(padx=20, pady=5)

        # Teléfono
        lbl_tel = ctk.CTkLabel(contenedor, text="Teléfono:", font=("Arial", 18))
        lbl_tel.pack(anchor="w", padx=20, pady=(15, 5))

        txt_tel = ctk.CTkEntry(
            contenedor,
            placeholder_text="10 dígitos",
            **entry_style
        )
        txt_tel.pack(padx=20, pady=5)

        # ================== BOTONES ==================
        botones = ctk.CTkFrame(contenedor, fg_color="transparent")
        botones.pack(pady=25)

        btn_actualizar = ctk.CTkButton(
            botones,
            text="Actualizar",
            fg_color="#32df57",
            hover_color="#28c94b",
            width=180,
            height=45,
            font=("Arial", 18, "bold")
        )
        btn_actualizar.pack(side="left", padx=20)

        btn_borrar = ctk.CTkButton(
            botones,
            text="Borrar perfil",
            fg_color="#b33c3c",
            hover_color="#912f2f",
            width=180,
            height=45,
            font=("Arial", 18, "bold")
        )
        btn_borrar.pack(side="left", padx=20)

        # ================== ENTER ENTRE CAMPOS ==================

        txt_nombre.bind("<Return>", lambda e: txt_correo.focus())
        txt_correo.bind("<Return>", lambda e: txt_tel.focus())
        txt_tel.bind("<Return>", lambda e: btn_actualizar.invoke())

        # Foco inicial
        txt_nombre.focus()



    def mostrar_laboratorios(self):
        self._clear_main()
         # ----- TÍTULO -----
        titulo = ctk.CTkLabel(
            self.main,
            text="Historial de reportes",
            text_color="#32df57",
            font=("Arial", 40, "bold")
        )
        titulo.pack(pady=25)
        # ---------------- TABLA ----------------
        tabla_frame = ctk.CTkFrame(self.main, fg_color="#e5e5e5", corner_radius=10)
        tabla_frame.pack(pady=20, padx=40, fill="both", expand=True)

        # --------- ESTILOS DEL TREEVIEW PARA QUE COMBINE ---------
        style = ttk.Style()
        style.configure("Treeview",
                        background="#f2f2f2",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="#f2f2f2",
                        font=("Arial", 13))
        style.configure("Treeview.Heading",
                        background="#c3c3c3",
                        foreground="black",
                        font=("Arial", 14, "bold"))
        style.map("Treeview",
                background=[("selected", "#32df57")])

        # --------- CREAR TREEVIEW ---------
        columnas = ("id_lab", "edificio", "piso", "idiomas", "cant_pc")

        tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)

        tabla.heading("id_lab", text="ID")
        tabla.heading("edificio", text="Edificio")
        tabla.heading("piso", text="Piso")
        tabla.heading("idiomas", text="Idiomas")
        tabla.heading("cant_pc", text="Cantidad de equipos")

        tabla.column("id_lab", width=80, anchor="center")
        tabla.column("edificio", width=200, anchor="center")
        tabla.column("piso", width=80, anchor="center")
        tabla.column("idiomas", width=120, anchor="center")
        tabla.column("cant_pc", width=180, anchor="center")
         # ----- FRAME CONTENEDOR -----
        contenedor = ctk.CTkFrame(self.main, fg_color="#f2f2f2", corner_radius=20)
        contenedor.pack(pady=20, padx=40, fill="both", expand=False)

        # ================== BOTONES ==================
        botones = ctk.CTkFrame(contenedor, fg_color="transparent")
        botones.pack(pady=25)

        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        btn_actualizar = ctk.CTkButton(
            botones,
            text="Actualizar",
            fg_color="#32df57",
            hover_color="#28c94b",
            width=180,
            height=45,
            font=("Arial", 18, "bold")
        )
        btn_actualizar.pack(side="left", padx=20)

        btn_borrar = ctk.CTkButton(
            botones,
            text="Borrar reporte",
            fg_color="#b33c3c",
            hover_color="#912f2f",
            width=180,
            height=45,
            font=("Arial", 18, "bold")
        )
        btn_borrar.pack(side="left", padx=20)

    

    def _build_sidebar(self):

        btn_inicio = ctk.CTkButton(
            self.sidebar,
            text="Inicio",
            fg_color=constantes.color,
            hover_color="#3b6b4b",
            text_color="white",
            corner_radius=8,
            font=("Arial",30),
            command=self.mostrar_dashboard
        )
        btn_inicio.pack(padx=12, pady=(30, 20))

        btn_perfil = ctk.CTkButton(
            self.sidebar,
            text="Perfil 👤",
            fg_color=constantes.color,
            hover_color="#3b6b4b",
            text_color="white",
            corner_radius=8,
            font=("Arial",30),
            command=self.mostrar_perfil
        )
        btn_perfil.pack(padx=12, pady=20)

        btn_labs = ctk.CTkButton(
            self.sidebar,
            text="Historia 🗂️",
            fg_color=constantes.color,
            hover_color="#3b6b4b",
            text_color="white",
            corner_radius=8,
            font=("Arial",28),
            command=self.mostrar_laboratorios
        )
        btn_labs.pack(padx=12, pady=20)

        btn_salir = ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesión",
            fg_color="#b33c3c",
            hover_color="#912f2f",
            text_color="white",
            corner_radius=8,
            font=("Arial",30),
            command=lambda: messagebox.showinfo("Salir", "Sesión cerrada")
        )
        btn_salir.pack(padx=12, pady=(20, 30))

    def generar_reportes(self):
    # Crear NUEVA ventana independiente
        nueva = Tk()
        nueva.title("Solucionar  Incidente")
        nueva.geometry("500x420")
        nueva.resizable(False, False)
        
        # ========= TITULO =========
        titulo = ctk.CTkLabel(
            nueva,
            text="Formulario de reporte",
            font=("Arial", 22, "bold"),
            text_color="black"
        )
        titulo.pack(pady=15)

        # ========= PREGUNTA =========
        lbl = ctk.CTkLabel(
            nueva,
            text="Describa la solucion del incidente:",
            font=("Arial", 14)
        )
        lbl.pack(pady=5)

        # ========= TEXTO =========
        txt_incidente = ctk.CTkTextbox(
            nueva,
            width=420,
            height=200,
            corner_radius=10
        )
        txt_incidente.pack(pady=10)

        # ========= BOTÓN ENVIAR =========
        btn_enviar = ctk.CTkButton(
            nueva,
            text="Enviar reporte",
            fg_color="#32df57",
            hover_color="#28c94b",
            text_color="white",
            corner_radius=12,
            width=180,
            command=nueva.destroy
        )
        btn_enviar.pack(pady=15)

        # Ejecutar la ventana
        nueva.mainloop()



    # =====================================================
    #   LIMPIAR ÁREA PRINCIPAL
    # =====================================================

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()
