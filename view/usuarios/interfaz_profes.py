from tkinter import messagebox
import customtkinter as ctk
from view import constantes
from tkinter import ttk
from tkinter import *
from model import laboratorios

from datetime import date
from controller import funciones_incidentes
from PIL import Image
from view  import interfaz

import os

#de la rama vieja a l main

class UsuariosProfes:
    """
    Clase que construye el dashboard para los profesores.
    
    Cada interfaz está separada en métodos:
      - mostrar_dashboard()
      - mostrar_perfil()
      - mostrar_laboratorios()

    Todas las interfaces usan el mismo menú lateral.
    """
  

    def __init__(self, ventana,usuario):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
        IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")

        self.ventana = ventana
        self.usuario = usuario
        self.img_logo = ctk.CTkImage(
           light_image=Image.open(os.path.join(IMAGES_DIR, "logo.png")),
           dark_image=Image.open(os.path.join(IMAGES_DIR, "logo.png")),
           size=(100,90)
        )
        self.img_usuario = ctk.CTkImage(
            light_image=Image.open(os.path.join(IMAGES_DIR,"usuario.png")),
            dark_image=Image.open(os.path.join(IMAGES_DIR,"usuario.png")),
            size=(100,90)
        )
        self.img_historial=ctk.CTkImage(
            light_image=Image.open(os.path.join(IMAGES_DIR,"historial.png")),
            dark_image=Image.open(os.path.join(IMAGES_DIR,"historial.png")),
            size=(80,90)
        )
        self.img_usuario_dos=ctk.CTkImage(
            light_image=Image.open(os.path.join(IMAGES_DIR,"usuario2.png")),
            dark_image=Image.open(os.path.join(IMAGES_DIR,"usuario2.png")),
            size=(200,200)
        )


       

        




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
            scroll=ctk.CTkScrollableFrame(
                master=self.main,
                height=600,
                width=600,
                fg_color="#ffffff"

            )
            scroll.pack(padx=20, pady=20, fill="both", expand=True)

        

            # ---------------- TITULO ----------------
            titulo = ctk.CTkLabel(
                scroll,
                text="Bitacora",
                text_color="#000000",
                font=("Arial", 50, "bold")
            )
            titulo.pack(pady=20)
            lbl_h2=ctk.CTkLabel(
                scroll,
                text="Seleccionar Laboratorio",
                font=("Arial", 30, "bold"),
                text_color="#132301"
            )
            lbl_h2.pack(pady=5)
            lbl_text=ctk.CTkLabel(
                scroll,
                text="En esta area usted podra poner un reporte acerca \n de algun equipo dañado dentro la Universidad tecnologica de Durango",
                font=("Arial",25),
                text_color="#132301"
            )
            lbl_text.pack()
            # ------------ CONTENEDOR BARRA DE BUSQUEDA ------------
            contenedor = ctk.CTkFrame(scroll, fg_color="transparent")
            contenedor.pack(pady=10)

            lbl_buscar = ctk.CTkLabel(
                contenedor,
                text="Busca por ID",
                font=("Arial", 14),
                text_color="#161616"
                
            )
            lbl_buscar.pack(anchor="w", pady=(0, 5))

            fila = ctk.CTkFrame(scroll, fg_color="transparent")
            fila.pack(pady=5, anchor="center")   # ⬅ Centrar toda la fila
            id=StringVar()

            # Entry
            txt_buscar = ctk.CTkEntry(
                fila,
                width=350,
                height=40,
                corner_radius=20,
                placeholder_text="Escribe el ID...",
                textvariable=id,
                fg_color="#e6e6e6",
                text_color="#1A1919"
            )
            txt_buscar.pack(side="left", padx=5)
            txt_buscar.focus()
            
            # Botón BUSCAR
            btn_buscar = ctk.CTkButton(
                fila,
                text="BUSCAR",
                fg_color="#32df57",
                hover_color="#28c94b",
                text_color="white",
                corner_radius=20,
                width=120,
                height=40,
                
                command=lambda:buscar(id.get())
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
                command=lambda:consultar_seleccion()
            )
            btn_reportar.pack(side="left", padx=10)
            #hover botton


            # ---------------- TABLA ----------------
            # FALTA AGREGAR COLORES SI EL LABORATORIO ESTA REPORTADO YA CON INCIDENTES
            # ROJO - Urgente
            # AMARILLO - PRECAUCIÓN
            tabla_frame = ctk.CTkFrame(scroll, fg_color="#e5e5e5", corner_radius=10)
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
            columnas = ("Nombre", "edificio", "piso","Cantidad de computadoras")

            tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)

            tabla.heading("Nombre", text="nombre")
            tabla.heading("edificio", text="Edificio")
            tabla.heading("piso", text="Piso")
            tabla.heading("Cantidad de computadoras", text="Cantidad de equipos")

            tabla.column("Nombre", width=80, anchor="center")
            tabla.column("edificio", width=200, anchor="center")
            tabla.column("piso", width=80, anchor="center")
            tabla.column("Cantidad de computadoras", width=180, anchor="center")

            tabla.pack(fill="both", expand=True, padx=10, pady=10)

            #----------------------
            # MOSTRAR DATOS REALES |
            #-----------------------

            datos=laboratorios.laboratorios.consultar()
            for item in tabla.get_children():
                tabla.delete(item)

            for fila in datos:
                # fila ahora = (nombre, edificio, piso, cant_pc)
                tabla.insert("", "end", values=fila)

            def buscar(id):
                if not id.isdigit():
                      messagebox.showerror("Error", "Debes ingresar un ID numérico válido.")
                else:
                    datos=laboratorios.laboratorios.consultar_id(id)
                    for item in tabla.get_children():
                        tabla.delete(item)

                    for fila in datos:
                        # fila ahora = (nombre, edificio, piso, cant_pc)
                        tabla.insert("", "end", values=fila)
            def consultar_seleccion():
                seleccion = tabla.focus()  # obtiene el ID interno del ítem seleccionado

                if not seleccion:
                    messagebox.showwarning("Advertencia", "Debes seleccionar un laboratorio.")
                    return

                datos = tabla.item(seleccion, "values")  # obtiene la tupla de valores

                # datos será algo como: ("Lab A1", "Pesado 1", "2", "35")

                self.generar_reportes(datos)   # mandas la tupla a tu método

                        #----------------
            # accesibilidad  |          
            #----------------
            txt_buscar.bind("<Return>",lambda event: buscar(id.get()))
       
    def mostrar_perfil(self):
        self._clear_main()

        # ----- TÍTULO -----
        titulo = ctk.CTkLabel(
            self.main,
            text="Edit Profile",
            text_color="#0F0F0F",
            font=("Arial", 45, "bold")
        )
        titulo.pack(pady=25, anchor="w", padx=40)

        scroll = ctk.CTkScrollableFrame(
            master=self.main,
            height=600,
            width=600,
            fg_color="#ffffff"
        )
        scroll.pack(padx=20, pady=20, fill="both", expand=True)
        
        # ----------------------------------------------------
        # SECCIÓN 1: HEADER DEL PERFIL (Imagen, Upload, Info)
        # ----------------------------------------------------
        
        # 1. Contenedor principal para la cabecera (Imagen y texto de subida)
        # Lo empaquetamos en el scroll frame y lo anclamos al oeste (izquierda)
        user_header_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        user_header_frame.pack(pady=30, padx=40, anchor="w") # Espacio debajo del título
        
        # === Columna 0: Imagen de Usuario (lbl_user) ===
        lbl_user = ctk.CTkLabel(
            user_header_frame,
            image=self.img_usuario_dos,
            text="" # Asegúrate de que no tenga texto
        )
        # Usamos grid para posicionarla en la columna 0, abarcando 2 filas (rowspan=2)
        lbl_user.grid(row=0, column=0, rowspan=2, padx=(0, 20), sticky="n") # sticky="n" para alinear arriba
        
        # === Columna 1: Texto de Subida y Recomendación ===
        
        # Botón/Etiqueta para "Upload new photo"
        lbl_user_name = ctk.CTkLabel(
            user_header_frame,
            text=f"{self.usuario[1]} {self.usuario[2]}",
            text_color="#1C1D1E", # Un color azul para indicar que es clickeable
            font=("Arial", 40, "bold"),
            cursor="hand2" # Indica que es interactivo
        )
        lbl_user_name.grid(row=0, column=1, sticky="w", pady=(0, 5)) 

        # Texto de recomendación (800x800, formatos)
        lbl_recommendation = ctk.CTkLabel(
            user_header_frame,
            text="Here you will be available to modify your personal info.",
            text_color="#888888",
            font=("Arial", 25)
        )
        lbl_recommendation.grid(row=1, column=1, sticky="w") 

        # ----------------------------------------------------
        # SECCIÓN 2: HEADER "Personal Info" + Edit button
        # ----------------------------------------------------

        header_info_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        header_info_frame.pack(fill="x", padx=40, pady=(40, 5))

        # Título a la izquierda
        titulo_info = ctk.CTkLabel(
            header_info_frame,
            text="Personal Info",
            font=("Arial", 22, "bold"),
            text_color="black"
        )
        titulo_info.grid(row=0, column=0, sticky="w")

        # Botón EDIT a la derecha
        btn_edit = ctk.CTkButton(
            header_info_frame,
            text="Edit",
            width=80,
            height=35,
            corner_radius=12,
            fg_color="#FFFFFF",
            text_color="#000000",
            border_color="#D0D0D0",
            border_width=2,
        )
        btn_edit.grid(row=0, column=1, sticky="e")

        # Fuerza el espacio entre izquierda y derecha
        header_info_frame.grid_columnconfigure(0, weight=1)

        # Separador debajo
        separador = ctk.CTkFrame(scroll, height=2, fg_color="#E0E0E0")
        separador.pack(fill="x", padx=40, pady=(0, 20))
        # ====== CONTENEDOR PRINCIPAL DE PERSONAL INFO ======
        info_frame = ctk.CTkFrame(
            scroll,
            fg_color="#F8F8F8",
            corner_radius=20
        )
        info_frame.pack(fill="x", padx=40, pady=25)

       

        # ======== SECCIÓN DE CAMPOS ========
        content = ctk.CTkFrame(info_frame, fg_color="transparent")
        content.grid(row=2, column=0, padx=20, pady=20, sticky="w")

        # ---- Columna 0: Full Name ----
        lbl_fullname_title = ctk.CTkLabel(
            content,
            text="Full Name",
            text_color="#7A7A7A",
            font=("Arial", 14)
        )
        lbl_fullname_title.grid(row=0,padx=150,column=0, sticky="w")

        lbl_fullname_value = ctk.CTkLabel(
            content,
            text=f"{self.usuario[1]} {self.usuario[2]}",
            font=("Arial", 16, "bold"),
            text_color="#1C1D1E"
        )
        lbl_fullname_value.grid(row=1,padx=150, column=0,sticky="w", pady=(5, 0))

        # ---- Columna 1: Email ----
        lbl_email_title = ctk.CTkLabel(
            content,
            text="Email",
            text_color="#7A7A7A",
            font=("Arial", 14)
        )
        lbl_email_title.grid(row=0, column=1, sticky="w", padx=(250, 0))

        lbl_email_value = ctk.CTkLabel(
            content,
            text=self.usuario[5],  # email
            font=("Arial", 16, "bold"),
            text_color="#1C1D1E"
        )
        lbl_email_value.grid(row=1, column=1, sticky="w", padx=(200, 0), pady=(5, 0))

        # ---- Columna 2: Phone ----
        lbl_phone_title = ctk.CTkLabel(
            content,
            text="Phone",
            text_color="#7A7A7A",
            font=("Arial", 14)
        )
        lbl_phone_title.grid(row=0, column=2, sticky="w", padx=(200, 0))

        lbl_phone_value = ctk.CTkLabel(
            content,
            text=self.usuario[4],  # telefono
            font=("Arial", 16, "bold"),
            text_color="#1C1D1E"
        )
        lbl_phone_value.grid(row=1, column=2, sticky="w", padx=(200, 0), pady=(5, 0))


        
        

    def mostrar_laboratorios(self):
        self._clear_main()

        # ==================== TÍTULO ====================
        titulo = ctk.CTkLabel(
            self.main,
            text="Historial de reportes",
            text_color="#000000",
            font=("Arial", 40, "bold")
        )
        titulo.pack(pady=25)

        lbl_h2 = ctk.CTkLabel(
            self.main,
            text="En esta área usted podrá visualizar los reportes que ha hecho",
            text_color="#000000",
            font=("Arial", 30)
        )
        lbl_h2.pack(pady=5)

        # ==================== MENÚ DENTRO DEL FRAME ====================
        
        # --- Contenedor ---
        menu_frame = ctk.CTkFrame(self.main, fg_color="#d9d9d9", corner_radius=10)
        menu_frame.pack(fill="x", padx=40, pady=0)

        # --- Popup menú de FECHA ---
        popup_fecha = Menu(menu_frame, tearoff=0)
        popup_fecha.add_command(label="Ordenar por último reporte",command=lambda:self.ordenarFechaDesc(tabla))
        popup_fecha.add_command(label="Ordenar por primer reporte",command=lambda:self.ordenarFechaAsc(tabla))

        def mostrar_popup_fecha(event):
            popup_fecha.tk_popup(event.x_root, event.y_root)

        btn_fecha = ctk.CTkButton(
            menu_frame,
            text="Organizar por fecha",
            width=180,
            height=38,
            fg_color="#c7c7c7",
            text_color="black"
        )
        btn_fecha.pack(side="left", padx=10)
        btn_fecha.bind("<Button-1>", mostrar_popup_fecha)

        # --- Popup menú de estado ---
        popup_estado = Menu(menu_frame, tearoff=0)
        popup_estado.add_command(label="Order by in PROCESS",command=lambda:self.ordenarProcesso(tabla))
        popup_estado.add_command(label="Order by ENDED",command=lambda:self.ordenarProcesso_terminado(tabla))

        def mostrar_popup_estado(event):
            popup_estado.tk_popup(event.x_root, event.y_root)

        btn_estado = ctk.CTkButton(
            menu_frame,
            text="STATE",
            width=180,
            height=38,
            fg_color="#c7c7c7",
            text_color="black"
        )
        btn_estado.pack(side="left", padx=10, expand=True)
        btn_estado.bind("<Button-1>", mostrar_popup_estado)

        # --- Popup menú de EDIFICIO ---
        popup_edificio = Menu(menu_frame, tearoff=0)
        popup_edificio.add_command(label="Ordenar por edificio",command=lambda:self.ordenarEdificio(tabla))
        popup_edificio.add_command(label="Ordenar por laboratorio", command=lambda:self.ordenarlab(tabla))

        def mostrar_popup_edificio(event):
            popup_edificio.tk_popup(event.x_root, event.y_root)

        btn_edificio = ctk.CTkButton(
            menu_frame,
            text="Edificio",
            width=180,
            height=38,
            fg_color="#c7c7c7",
            text_color="black"
        )
        btn_edificio.pack(side="left", padx=10)
        btn_edificio.bind("<Button-1>", mostrar_popup_edificio)

        # ==================== TABLA ====================
        tabla_frame = ctk.CTkFrame(self.main, fg_color="#e5e5e5", corner_radius=10)
        tabla_frame.pack(pady=20, padx=40, fill="both", expand=True)

        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#f2f2f2",
            foreground="black",
            rowheight=30,
            fieldbackground="#f2f2f2",
            font=("Arial", 13)
        )
        style.configure(
            "Treeview.Heading",
            background="#c3c3c3",
            foreground="black",
            font=("Arial", 14, "bold")
        )
        style.map("Treeview", background=[("selected", "#32df57")])

        columnas = ("ID_Incident", "Date and hour", "Incident", "name", "building","Observations")
        tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=8)

        tabla.heading("ID_Incident", text="ID_incident")
        tabla.heading("Date and hour", text="date")
        tabla.heading("Incident", text="Incident")
        tabla.heading("name", text="name")
        tabla.heading("building", text="building")
        tabla.heading("Observations", text="Observations")


        tabla.column("ID_Incident", width=80, anchor="center")
        tabla.column("Date and hour", width=200, anchor="center")
        tabla.column("Incident", width=120, anchor="center")
        tabla.column("name", width=80, anchor="center")
        tabla.column("building", width=80, anchor="center")
        tabla.column("Observations", width=80, anchor="center")


        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # ==================== BOTONES ====================
        contenedor = ctk.CTkFrame(self.main, fg_color="#f2f2f2", corner_radius=20)
        contenedor.pack(pady=20, padx=40, fill="both", expand=False)

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
            text="Borrar reporte",
            fg_color="#b33c3c",
            hover_color="#912f2f",
            width=180,
            height=45,
            font=("Arial", 18, "bold")
        )
        btn_borrar.pack(side="left", padx=20)
        datos_incidentes=funciones_incidentes.incidente.consulta_Tabla(self.usuario[0])
        tabla.tag_configure("rojo", background="#f6b2b2")
        tabla.tag_configure("verde", background="#ccffcc")
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in datos_incidentes:
            # fila ahora = (nombre, edificio, piso, cant_pc)
            id_incident = fila[0]
            fecha = fila[1]
            incidente = fila[2]
            name = fila[3]
            building = fila[4]
            obs_raw = fila[5]  # 0 o 1

            # Transformación
            observations =  "Process" if obs_raw == 0 else "END"
           
            tag = "rojo" if observations == "Process" else "verde"



            # Insertamos con la observación convertida
            tabla.insert("", "end", values=(id_incident, fecha, incidente, name, building, observations),tags=(tag,)
            )
       
    def _build_sidebar(self):

        btn_inicio = ctk.CTkButton(
            self.sidebar,
            text="Inicio",
            image=self.img_logo,
            compound="left",
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
            text="Perfil",
            image=self.img_usuario,
            compound="left",
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
            text="Historial",
            image=self.img_historial,
            compound="left",
            fg_color=constantes.color,
            hover_color="#3b6b4b",
            text_color="white",
            corner_radius=8,
            font=("Arial",28),
            command=self.mostrar_laboratorios
        )
        btn_labs.pack(padx=12, pady=50)

        btn_salir = ctk.CTkButton(
            self.sidebar,
            text="Cerrar Sesión",
            fg_color="#b33c3c",
            hover_color="#912f2f",
            text_color="white",
            corner_radius=8,
            font=("Arial",30),
            command=lambda:interfaz.Vista.mostrar_login(self.ventana)
        )
        btn_salir.pack(padx=12, pady=(180, 30))

    def generar_reportes(self, datos):

        from datetime import date

        MAX_CHARS = 150

        # Crear NUEVA ventana independiente
        nueva = Tk()
        nueva.title("Reportar incidente")
        nueva.geometry("500x600")
        nueva.resizable(False, False)

        scroll = ctk.CTkScrollableFrame(
            master=nueva,
            height=600,
            width=600,
            fg_color="#ffffff"
        )
        scroll.pack(padx=20, pady=20, fill="both", expand=True)

        # Obtener ID del laboratorio
        id_tupla = laboratorios.laboratorios.buscar_id(datos)
        id = id_tupla[0]

        # ========= TITULO =========
        titulo = ctk.CTkLabel(
            scroll,
            text="Formulario de reporte",
            font=("Arial", 22, "bold"),
            text_color="black"
        )
        titulo.pack(pady=15)

        lbl_h2 = ctk.CTkLabel(
            scroll,
            text=f"Del laboratorio {id}",
            font=("Arial", 20),
            text_color="black"
        )
        lbl_h2.pack(pady=2)

        # ========= Nombre =========
        lbl_h3 = ctk.CTkLabel(
            scroll,
            text="Nombre del laboratorio:",
            font=("Arial", 20),
            text_color="black"
        )
        lbl_h3.pack(pady=1)

        txt_nombre = ctk.CTkEntry(
            scroll,
            width=len(datos[0]) * 10,
            text_color="#000000",
            corner_radius=5,
            fg_color="#ffffff"
        )
        txt_nombre.pack(pady=5)
        txt_nombre.insert(0, f"{datos[0]}")
        txt_nombre.configure(state="readonly")

        # ========= Edificio =========
        lbl_h4 = ctk.CTkLabel(
            scroll,
            text="Edificio:",
            font=("Arial", 20),
            text_color="black"
        )
        lbl_h4.pack(pady=1)

        txt_edificio = ctk.CTkEntry(
            scroll,
            width=len(datos[1]) * 10,
            text_color="#000000",
            corner_radius=5,
            fg_color="#ffffff"
        )
        txt_edificio.pack(pady=5)
        txt_edificio.insert(0, f"{datos[1]}")
        txt_edificio.configure(state="readonly")

        # ========= Piso =========
        lbl_h5 = ctk.CTkLabel(
            scroll,
            text="Piso:",
            font=("Arial", 20),
            text_color="black"
        )
        lbl_h5.pack(pady=1)

        txt_piso = ctk.CTkEntry(
            scroll,
            width=len(datos[2]) * 10,
            text_color="#000000",
            corner_radius=5,
            fg_color="#ffffff"
        )
        txt_piso.pack(pady=5)
        txt_piso.insert(0, f"{datos[2]}")
        txt_piso.configure(state="readonly")

        # ========= Fecha =========
        fecha = date.today().strftime("%Y-%m-%d")

        lbl_h6 = ctk.CTkLabel(
            scroll,
            text="Fecha del reporte:",
            font=("Arial", 20),
            text_color="black"
        )
        lbl_h6.pack(pady=1)

        txt_fecha = ctk.CTkEntry(
            scroll,
            width=len(fecha) * 10,
            text_color="#000000",
            corner_radius=5,
            fg_color="#ffffff"
        )
        txt_fecha.pack(pady=5)
        txt_fecha.insert(0, fecha)
        txt_fecha.configure(state="readonly")

        # ========= Pregunta =========
        lbl = ctk.CTkLabel(
            scroll,
            text="Describe el incidente:",
            font=("Arial", 16),
            text_color="#000000"
        )
        lbl.pack(pady=5)

        # ========= Contador =========
        lbl_contador = ctk.CTkLabel(
            scroll,
            text=f"0 / {MAX_CHARS} caracteres",
            text_color="black",
            font=("Arial", 12)
        )
        lbl_contador.pack(pady=5)

        # ========= TextArea =========
        txt_incidente = ctk.CTkTextbox(
            scroll,
            width=420,
            height=200,
            corner_radius=10,
            fg_color="#ffffff",
            text_color="#000000",
            border_color="#000000",
            border_width=4,
        )
        txt_incidente.pack(pady=10)
        txt_incidente.focus()

        # ========= Funciones para límite y contador =========
        def actualizar_contador(event=None):
            texto = txt_incidente.get("1.0", "end-1c")

            # Corta el exceso
            if len(texto) > MAX_CHARS:
                txt_incidente.delete(f"1.0 + {MAX_CHARS} chars", "end")
                texto = txt_incidente.get("1.0", "end-1c")

            lbl_contador.configure(
                text=f"{len(texto)} / {MAX_CHARS} caracteres"
            )

        def limitar_caracteres(event=None):
            texto = txt_incidente.get("1.0", "end-1c")
            if len(texto) == MAX_CHARS:
                lbl_contador.configure(text_color="red")
            else:
                lbl_contador.configure(text_color="black")

            if len(texto) >= MAX_CHARS:
                return "break"   # bloquea la tecla

        # Bind correctos
        txt_incidente.bind("<KeyRelease>", actualizar_contador)
        txt_incidente.bind("<<Paste>>", actualizar_contador)
        txt_incidente.bind("<Key>", limitar_caracteres)
            
        # ========= Botón enviar =========
        btn_enviar = ctk.CTkButton(
            scroll,
            text="Enviar reporte",
            fg_color="#32df57",
            hover_color="#28c94b",
            text_color="white",
            corner_radius=12,
            width=180,
            command=lambda: self.insertar_reporte(
                nueva,
                txt_incidente.get("1.0", "end-1c"),
                id
            )

        )
        btn_enviar.pack(pady=15)


        nueva.mainloop()

    def insertar_reporte(self,ventana,txt_incidente,id):
        exito=funciones_incidentes.incidente.insertar(
            self.usuario[0],
                txt_incidente,
                id
        )
        if exito:
            ventana.destroy()
            
    def ordenarlab(self,tabla):
            datos_incidentes=funciones_incidentes.incidente.consulta_Tabla_lab(self.usuario[0])
            tabla.tag_configure("rojo", background="#f6b2b2")
            tabla.tag_configure("verde", background="#ccffcc")
            for item in tabla.get_children():
                tabla.delete(item)
            for fila in datos_incidentes:
                # fila ahora = (nombre, edificio, piso, cant_pc)
                id_incident = fila[0]
                fecha = fila[1]
                incidente = fila[2]
                name = fila[3]
                building = fila[4]
                obs_raw = fila[5]  # 0 o 1

                # Transformación
                observations =  "Process" if obs_raw == 0 else "END"
            
                tag = "rojo" if observations == "Process" else "verde"



                # Insertamos con la observación convertida
                tabla.insert("", "end", values=(id_incident, fecha, incidente, name, building, observations),tags=(tag,)
                )

    def ordenarEdificio(self,tabla):
        datos_incidentes=funciones_incidentes.incidente.consulta_Tabla_edificio(self.usuario[0])
        tabla.tag_configure("rojo", background="#f6b2b2")
        tabla.tag_configure("verde", background="#ccffcc")
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in datos_incidentes:
            # fila ahora = (nombre, edificio, piso, cant_pc)
            id_incident = fila[0]
            fecha = fila[1]
            incidente = fila[2]
            name = fila[3]
            building = fila[4]
            obs_raw = fila[5]  # 0 o 1

                # Transformación
            observations =  "Process" if obs_raw == 0 else "END"
            
            tag = "rojo" if observations == "Process" else "verde"



                # Insertamos con la observación convertida
            tabla.insert("", "end", values=(id_incident, fecha, incidente, name, building, observations),tags=(tag,)
                )

    def ordenarFechaAsc(self,tabla):
        #PRIMER REPORTE
        datos_incidentes=funciones_incidentes.incidente.consulta_Tabla_fechaAsc(self.usuario[0])
        tabla.tag_configure("rojo", background="#f6b2b2")
        tabla.tag_configure("verde", background="#ccffcc")
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in datos_incidentes:
            # fila ahora = (nombre, edificio, piso, cant_pc)
            id_incident = fila[0]
            fecha = fila[1]
            incidente = fila[2]
            name = fila[3]
            building = fila[4]
            obs_raw = fila[5]  # 0 o 1

                # Transformación
            observations =  "Process" if obs_raw == 0 else "END"
            
            tag = "rojo" if observations == "Process" else "verde"



                # Insertamos con la observación convertida
            tabla.insert("", "end", values=(id_incident, fecha, incidente, name, building, observations),tags=(tag,)
                )

    def ordenarFechaDesc(self,tabla):
        #PRIMER REPORTE
        datos_incidentes=funciones_incidentes.incidente.consulta_Tabla_fechaDesc(self.usuario[0])
        tabla.tag_configure("rojo", background="#f6b2b2")
        tabla.tag_configure("verde", background="#ccffcc")
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in datos_incidentes:
            # fila ahora = (nombre, edificio, piso, cant_pc)
            id_incident = fila[0]
            fecha = fila[1]
            incidente = fila[2]
            name = fila[3]
            building = fila[4]
            obs_raw = fila[5]  # 0 o 1

                # Transformación
            observations =  "Process" if obs_raw == 0 else "END"
            
            tag = "rojo" if observations == "Process" else "verde"



                # Insertamos con la observación convertida
            tabla.insert("", "end", values=(id_incident, fecha, incidente, name, building, observations),tags=(tag,)
                )

    def ordenarProcesso(self,tabla):
        #PRIMER REPORTE
        datos_incidentes=funciones_incidentes.incidente.consulta_Tabla_Proceso(self.usuario[0])
        tabla.tag_configure("rojo", background="#f6b2b2")
        tabla.tag_configure("verde", background="#ccffcc")
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in datos_incidentes:
            # fila ahora = (nombre, edificio, piso, cant_pc)
            id_incident = fila[0]
            fecha = fila[1]
            incidente = fila[2]
            name = fila[3]
            building = fila[4]
            obs_raw = fila[5]  # 0 o 1

                # Transformación
            observations =  "Process" if obs_raw == 0 else "END"
            
            tag = "rojo" if observations == "Process" else "verde"



                # Insertamos con la observación convertida
            tabla.insert("", "end", values=(id_incident, fecha, incidente, name, building, observations),tags=(tag,)
                )

    def ordenarProcesso_terminado(self,tabla):
        #PRIMER REPORTE
        datos_incidentes=funciones_incidentes.incidente.consulta_Tabla_Proceso_terminado(self.usuario[0])
        tabla.tag_configure("rojo", background="#f6b2b2")
        tabla.tag_configure("verde", background="#ccffcc")
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in datos_incidentes:
            # fila ahora = (nombre, edificio, piso, cant_pc)
            id_incident = fila[0]
            fecha = fila[1]
            incidente = fila[2]
            name = fila[3]
            building = fila[4]
            obs_raw = fila[5]  # 0 o 1

                # Transformación
            observations =  "Process" if obs_raw == 0 else "END"
            
            tag = "rojo" if observations == "Process" else "verde"



                # Insertamos con la observación convertida
            tabla.insert("", "end", values=(id_incident, fecha, incidente, name, building, observations),tags=(tag,)
                )

    # =====================================================
    #   LIMPIAR ÁREA PRINCIPAL  
    # =====================================================

    def _clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()
