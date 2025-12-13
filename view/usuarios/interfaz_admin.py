import customtkinter as ctk
from tkinter import messagebox, ttk, Menu
from view import constantes
from model import laboratorios, incidentes, usuarios
from PIL import Image
import os

class UsuariosAdmin:
    def __init__(self, frame_padre):
        self.frame_padre = frame_padre
        # Obtenemos la ventana raíz para los popups
        self.ventana = frame_padre.winfo_toplevel()
        
        self.menu_buttons = {}

        # Configuración de imágenes
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        IMAGES_DIR = os.path.join(BASE_DIR, "view", "imagenes")

        self.img_logo_utd = None
        try:
            # Cargar Logo UTD
            self.img_logo_utd = ctk.CTkImage(Image.open(os.path.join(IMAGES_DIR, "logo_utd.png")), size=(140, 60))
        except Exception:
            self.img_logo_utd = None

        # Limpiar frame padre
        for w in self.frame_padre.winfo_children():
            w.destroy()

        # Frame Principal
        self.main_container = ctk.CTkFrame(self.frame_padre, fg_color="#F5F5F5")
        self.main_container.pack(fill="both", expand=True)

        # --- Sidebar (FONDO BLANCO) ---
        self.sidebar = ctk.CTkFrame(self.main_container, fg_color="white", width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # --- Área de Contenido ---
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#F5F5F5")
        self.content_area.pack(side="right", fill="both", expand=True)

        self._build_sidebar()
        
        # Iniciamos con la vista de Incidentes
        self.mostrar_incidentes() 

    def _build_sidebar(self):
        # 1. LOGO UTD
        if self.img_logo_utd:
            ctk.CTkLabel(self.sidebar, text="", image=self.img_logo_utd).pack(pady=(30, 10))

        # 2. TÍTULO
        ctk.CTkLabel(self.sidebar, text="ControlLabs\nADMIN", font=("Roboto", 22, "bold"), text_color=constantes.COLOR_PRIMARY).pack(pady=(10, 5))
        ctk.CTkLabel(self.sidebar, text="Administrator Panel", font=("Roboto", 12), text_color="gray").pack(pady=(0, 30))

        # Menú
        self.menu_buttons["incidents"] = self._crear_btn_menu("View Incidents", self.mostrar_incidentes)
        self.menu_buttons["incidents"].pack(fill="x", pady=5, padx=10)

        self.menu_buttons["labs"] = self._crear_btn_menu("Manage Labs", self.mostrar_dashboard_labs)
        self.menu_buttons["labs"].pack(fill="x", pady=5, padx=10)

        self.menu_buttons["users"] = self._crear_btn_menu("Manage Users", self.mostrar_usuarios)
        self.menu_buttons["users"].pack(fill="x", pady=5, padx=10)

        # Logout
        ctk.CTkButton(self.sidebar, text="Sign Out", fg_color="#c62828", hover_color="#8e0000", height=40, command=self._cerrar_sesion).pack(side="bottom", fill="x", pady=30, padx=20)

    def _crear_btn_menu(self, text, command):
        return ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", text_color="gray", hover_color="#F0F0F0", anchor="w", height=50, font=("Roboto", 14, "bold"), command=command)

    def _highlight_menu(self, active_key):
        for key, btn in self.menu_buttons.items():
            if key == active_key:
                btn.configure(fg_color=constantes.COLOR_PRIMARY, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color="gray")

    def _cerrar_sesion(self):
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            root = self.frame_padre.winfo_toplevel()
            for widget in root.winfo_children():
                widget.destroy()
            from view import interfaz 
            interfaz.Vista(root)

    # Método puente para compatibilidad
    def mostrar_dashboard(self):
        self.mostrar_incidentes()

    def _limpiar_contenido(self):
        for w in self.content_area.winfo_children():
            w.destroy()

    def _crear_encabezado(self, titulo, subtitulo):
        header = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header, text=titulo, font=("Roboto", 32, "bold"), text_color="#333").pack(anchor="w")
        ctk.CTkLabel(header, text=subtitulo, font=("Roboto", 14), text_color="gray").pack(anchor="w")

    # =====================================================
    #  1. GESTIÓN DE LABORATORIOS (Labs)
    # =====================================================
    def mostrar_dashboard_labs(self):
        self._highlight_menu("labs")
        self._limpiar_contenido()
        self._crear_encabezado("Laboratory Management", "Add, edit or disable laboratories.")

        actions = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=10)
        actions.pack(fill="x", padx=40, pady=10)

        search_var = ctk.StringVar()
        entry = ctk.CTkEntry(actions, textvariable=search_var, placeholder_text="Search Lab...", width=300, height=40)
        entry.pack(side="left", padx=20, pady=20)
        ctk.CTkButton(actions, text="Search", fg_color=constantes.COLOR_PRIMARY, command=lambda: self._cargar_labs(tabla, search_var.get())).pack(side="left", padx=10)

        ctk.CTkButton(actions, text="+ Add Lab", fg_color=constantes.COLOR_ACCENT, hover_color="#b87608", command=lambda: self._popup_lab(None)).pack(side="right", padx=20)

        frame_tabla = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        self._configurar_estilo_tabla()
        
        cols = ("ID", "Nombre", "Edificio", "Piso", "Equipos", "Status", "Actions")
        tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=15)
        
        for col in cols: 
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center")
        
        tabla.column("ID", width=50)
        tabla.column("Nombre", width=200)
        tabla.column("Actions", width=80)
        tabla.pack(fill="both", expand=True)

        tabla.bind("<ButtonRelease-1>", lambda event: self._manejar_clic_lab(event, tabla))
        self._cargar_labs(tabla)

    def _cargar_labs(self, tabla, filtro=None):
        for item in tabla.get_children(): tabla.delete(item)
        
        if filtro: datos = laboratorios.laboratorios.consultar_filtro(filtro)
        else: datos = laboratorios.laboratorios.consultar()

        for fila in datos:
            # fila: (nombre, edificio, piso, cant_pc, id_lab, estatus)
            id_lab = fila[4]
            nombre = fila[0]
            edificio = fila[1]
            piso = fila[2]
            equipos = fila[3]
            try: estatus = "Active" if fila[5] == 1 else "Disabled"
            except: estatus = "Active"
            
            valores = (id_lab, nombre, edificio, piso, equipos, estatus, "✎  🚫")
            item_id = tabla.insert("", "end", values=valores)
            tabla.set(item_id, column="Actions", value="✎  🚫") 

    def _manejar_clic_lab(self, event, tabla):
        region = tabla.identify("region", event.x, event.y)
        if region == "cell" and tabla.identify_column(event.x) == "#7": 
            item = tabla.identify_row(event.y)
            if item:
                vals = tabla.item(item, "values")
                id_lab_tupla = laboratorios.laboratorios.buscar_id((vals[1], vals[2], vals[3]))
                if not id_lab_tupla: return
                id_lab = id_lab_tupla[0]

                menu = Menu(self.ventana, tearoff=0)
                datos_lab = (id_lab, vals[1], vals[2], vals[3], vals[4])
                
                menu.add_command(label="✎ Edit Lab", command=lambda: self._popup_lab(datos_lab))
                
                if vals[5] == "Active":
                    menu.add_command(label="🚫 Disable Lab", command=lambda: self._toggle_lab(id_lab, vals[1], 0))
                else:
                    menu.add_command(label="✅ Enable Lab", command=lambda: self._toggle_lab(id_lab, vals[1], 1))
                
                menu.tk_popup(event.x_root, event.y_root)

    def _popup_lab(self, datos):
        top = ctk.CTkToplevel(self.ventana)
        top.geometry("400x500")
        top.title("Laboratory")
        top.grab_set()
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (200)
        y = (top.winfo_screenheight() // 2) - (250)
        top.geometry(f'+{x}+{y}')
        
        ctk.CTkLabel(top, text="Lab Details", font=("Roboto", 20, "bold")).pack(pady=20)
        entries = {}
        campos = ["Name", "Building", "Floor", "Computers"]
        
        for campo in campos:
            ctk.CTkLabel(top, text=campo).pack(anchor="w", padx=20)
            e = ctk.CTkEntry(top)
            e.pack(fill="x", padx=20, pady=(0, 10))
            entries[campo] = e

        if datos: 
            entries["Name"].insert(0, datos[1])
            entries["Building"].insert(0, datos[2])
            entries["Floor"].insert(0, datos[3])
            entries["Computers"].insert(0, datos[4])

        def guardar():
            try:
                if datos:
                    laboratorios.laboratorios.actualizar(datos[0], entries["Name"].get(), entries["Building"].get(), entries["Floor"].get(), entries["Computers"].get())
                    messagebox.showinfo("Success", "Lab updated")
                else:
                    laboratorios.laboratorios.insertar(entries["Name"].get(), entries["Building"].get(), entries["Floor"].get(), entries["Computers"].get())
                    messagebox.showinfo("Success", "Lab added")
                top.destroy()
                self.mostrar_dashboard_labs()
            except Exception as e:
                messagebox.showerror("Error", f"Error saving lab: {e}")

        ctk.CTkButton(top, text="Save", fg_color=constantes.COLOR_PRIMARY, command=guardar).pack(pady=20)

    def _toggle_lab(self, id_lab, nombre, nuevo_estado):
        accion = "Disable" if nuevo_estado == 0 else "Enable"
        if messagebox.askyesno(accion, f"{accion} lab '{nombre}'?"):
            laboratorios.laboratorios.cambiar_estatus(id_lab, nuevo_estado)
            self.mostrar_dashboard_labs()

    # =====================================================
    #  2. GESTIÓN DE USUARIOS (Users)
    # =====================================================
    def mostrar_usuarios(self):
        self._highlight_menu("users")
        self._limpiar_contenido()
        self._crear_encabezado("User Management", "Manage roles and access.")

        actions = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=10)
        actions.pack(fill="x", padx=40, pady=10)

        search_var = ctk.StringVar()
        entry_search = ctk.CTkEntry(actions, textvariable=search_var, placeholder_text="Search user...", width=300, height=40)
        entry_search.pack(side="left", padx=20, pady=20)
        
        btn_search = ctk.CTkButton(actions, text="Search", fg_color=constantes.COLOR_PRIMARY, command=lambda: self._cargar_usuarios(tabla, search_var.get()))
        btn_search.pack(side="left", padx=10)

        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=40, pady=20)

        self._configurar_estilo_tabla()
        cols = ("ID", "Name", "Email", "Role", "Status", "Actions")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        for c in cols: 
            tabla.heading(c, text=c)
            tabla.column(c, anchor="center")
        
        tabla.column("ID", width=50)
        tabla.column("Name", width=200)
        tabla.column("Email", width=250)
        tabla.column("Actions", width=100)
        tabla.pack(fill="both", expand=True)

        tabla.bind("<ButtonRelease-1>", lambda event: self._manejar_clic_usuario(event, tabla))
        self._cargar_usuarios(tabla)

    def _cargar_usuarios(self, tabla, filtro=""):
        for i in tabla.get_children(): tabla.delete(i)
        
        datos = usuarios.Usuarios.consultar_todos() 
        filtro = filtro.lower().strip()

        for fila in datos:
            if filtro:
                texto_busqueda = f"{fila[1]} {fila[2]} {fila[3]} {fila[4]}".lower()
                if filtro not in texto_busqueda: continue

            estatus_txt = "Active" if fila[5] == 1 else "Inactive"
            acciones = "👑  🚫" 
            nombre_completo = f"{fila[1]} {fila[2]}"
            
            tabla.insert("", "end", values=(fila[0], nombre_completo, fila[3], fila[4], estatus_txt, acciones))

    def _manejar_clic_usuario(self, event, tabla):
        if tabla.identify_column(event.x) == "#6":
            item = tabla.identify_row(event.y)
            if item:
                vals = tabla.item(item, "values") 
                menu = Menu(self.ventana, tearoff=0)
                
                uid = vals[0]
                rol_actual = vals[3]
                estatus_actual = vals[4]

                if rol_actual != "admin":
                    menu.add_command(label="👑 Make Admin", command=lambda: self._cambiar_rol(uid, "admin"))
                else:
                    menu.add_command(label="⬇ Remove Admin", command=lambda: self._cambiar_rol(uid, "usuario"))
                
                if estatus_actual == "Active":
                    menu.add_command(label="🚫 Disable User", command=lambda: self._cambiar_estatus_user(uid, 0))
                else:
                    menu.add_command(label="✅ Enable User", command=lambda: self._cambiar_estatus_user(uid, 1))
                
                menu.tk_popup(event.x_root, event.y_root)

    def _cambiar_rol(self, uid, rol):
        if messagebox.askyesno("Change Role", f"Change user role to {rol}?"):
            usuarios.Usuarios.cambiar_rol(uid, rol)
            self.mostrar_usuarios()

    def _cambiar_estatus_user(self, uid, estatus):
        action = "Disable" if estatus == 0 else "Enable"
        if messagebox.askyesno(action, f"{action} this user?"):
            usuarios.Usuarios.cambiar_estatus(uid, estatus)
            self.mostrar_usuarios()

    # =====================================================
    #  3. GESTIÓN DE INCIDENTES (Incidents)
    # =====================================================
    def mostrar_incidentes(self):
        self._highlight_menu("incidents")
        self._limpiar_contenido()
        self._crear_encabezado("All Incidents", "View and resolve reported incidents.")

        actions = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=10)
        actions.pack(fill="x", padx=40)
        
        sv = ctk.StringVar()
        ctk.CTkEntry(actions, textvariable=sv, placeholder_text="Filter incidents...", width=300).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(actions, text="Filter", fg_color=constantes.COLOR_PRIMARY, command=lambda: self._cargar_incidentes(tabla, sv.get())).pack(side="left")

        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=40, pady=20)

        cols = ("ID", "Date", "Reporter", "Lab", "Description", "Status", "Actions")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", height=15)
        
        for c in cols: 
            tabla.heading(c, text=c)
            tabla.column(c, anchor="center") 
        
        tabla.column("Description", width=250, anchor="w")
        tabla.column("ID", width=50)
        tabla.pack(fill="both", expand=True)

        tabla.bind("<ButtonRelease-1>", lambda e: self._manejar_clic_incidente(e, tabla))
        self._cargar_incidentes(tabla)

    def _cargar_incidentes(self, tabla, filtro=""):
        for i in tabla.get_children(): tabla.delete(i)
        
        datos = incidentes.incidentes.consultar_todos_admin()
        filtro = filtro.lower()
        
        for fila in datos:
            # 0:id_reporte, 1:fecha, 2:desc, 3:lab, 4:edif, 5:estado, 6:ID_USUARIO, 7:NOMBRE, 8:APELLIDO
            
            try: 
                # Intenta poner Nombre + Apellido
                nombre_completo = f"{fila[7]} {fila[8]}"
            except: 
                # Si falla (ej. no viene el apellido), entra aquí.
                try: 
                    # CORRECCIÓN: Antes era f"{fila[6]} {fila[7]}", lo que incluía el ID (fila[6]).
                    # Ahora solo ponemos fila[7] (Nombre)
                    nombre_completo = f"{fila[7]}"
                except: 
                    nombre_completo = "Unknown"

            if filtro and filtro not in str(fila).lower(): continue
            
            # Estado (0=Pendiente, 1=Resuelto)
            estado = "Resolved" if fila[5] == 1 else "Pending"
            acciones = "📄  ✅" if fila[5] == 0 else "📄  ✔" 
            
            # Insertar en la tabla
            tabla.insert("", "end", values=(fila[0], fila[1], nombre_completo, fila[3], fila[2], estado, acciones))

    def _manejar_clic_incidente(self, event, tabla):
        if tabla.identify_column(event.x) == "#7":
            item = tabla.identify_row(event.y)
            if item:
                vals = tabla.item(item, "values")
                
                menu = Menu(self.ventana, tearoff=0)
                menu.add_command(label="📄 View Details", command=lambda: self._ver_detalle_incidente(vals))
                
                if vals[5] == "Pending":
                    menu.add_command(label="✅ Mark Resolved", command=lambda: self._resolver_incidente(vals[0], tabla))
                
                menu.tk_popup(event.x_root, event.y_root)

    def _resolver_incidente(self, id_incidente, tabla):
        if messagebox.askyesno("Solve", "Mark this incident as RESOLVED?"):
            incidentes.incidentes.marcar_resuelto(id_incidente)
            self._cargar_incidentes(tabla)

    def _ver_detalle_incidente(self, datos):
        top = ctk.CTkToplevel(self.ventana)
        top.geometry("500x500")
        top.title("Incident Details")
        top.grab_set()
        
        ctk.CTkLabel(top, text="Incident Report", font=("Roboto", 22, "bold"), text_color=constantes.COLOR_PRIMARY).pack(pady=20)
        
        container = ctk.CTkFrame(top, fg_color="white", corner_radius=15)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        info = [
            ("Report ID", datos[0]),
            ("Date", datos[1]),
            ("Status", datos[5]),
            ("Reporter", datos[2]),
            ("Laboratory", datos[3])
        ]
        
        for label, value in info:
            row = ctk.CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=label+":", width=100, anchor="w", font=("Roboto", 12, "bold"), text_color="gray").pack(side="left")
            ctk.CTkLabel(row, text=value, anchor="w", font=("Roboto", 12, "bold")).pack(side="left")
            
        ctk.CTkLabel(container, text="Description:", font=("Roboto", 12, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(20, 5))
        
        txt = ctk.CTkTextbox(container, height=150, fg_color="#F9F9F9", border_width=1, border_color="#EEE")
        txt.pack(fill="x", padx=20)
        txt.insert("1.0", datos[4])
        txt.configure(state="disabled")
        
        ctk.CTkButton(container, text="Close", fg_color="gray", command=top.destroy).pack(pady=20)

    def _configurar_estilo_tabla(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", rowheight=35, fieldbackground="white", font=("Roboto", 12))
        style.configure("Treeview.Heading", background="#E0E0E0", foreground="#333", font=("Roboto", 13, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", constantes.COLOR_HOVER)])