import customtkinter as ctk
from tkinter import messagebox, ttk, Menu
from view import constantes
from model import laboratorios, usuarios
from controller import funciones_incidentes
from PIL import Image
import os
from datetime import date

class UsuariosProfes:
    def __init__(self, frame_padre, usuario):
        self.frame_padre = frame_padre
        self.ventana = frame_padre.winfo_toplevel() 
        self.usuario = list(usuario) 
        
        self.menu_buttons = {}

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        IMAGES_DIR = os.path.join(BASE_DIR, "view", "imagenes")

        self.img_logo_utd = None
        try:
            self.img_logo_utd = ctk.CTkImage(Image.open(os.path.join(IMAGES_DIR, "logo_utd.png")), size=(140, 60))
        except Exception:
            self.img_logo_utd = None

        for w in self.frame_padre.winfo_children(): w.destroy()

        self.main_container = ctk.CTkFrame(self.frame_padre, fg_color="#F5F5F5")
        self.main_container.pack(fill="both", expand=True)

        # --- Sidebar Blanco ---
        self.sidebar = ctk.CTkFrame(self.main_container, fg_color="white", width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#F5F5F5")
        self.content_area.pack(side="right", fill="both", expand=True)

        self._build_sidebar()
        self.mostrar_dashboard()

    def _build_sidebar(self):
        if self.img_logo_utd:
            ctk.CTkLabel(self.sidebar, text="", image=self.img_logo_utd).pack(pady=(30, 10))

        ctk.CTkLabel(self.sidebar, text="ControlLabs", font=("Roboto", 24, "bold"), text_color=constantes.COLOR_PRIMARY).pack(pady=(10, 20))
        
        nombre_corto = f"{self.usuario[1]} {self.usuario[3]}"
        ctk.CTkLabel(self.sidebar, text=f"Welcome,\n{nombre_corto}", font=("Roboto", 16), text_color="gray").pack(pady=(0, 40))

        self.menu_buttons["home"] = self._crear_btn_menu("Home / Labs", self.mostrar_dashboard)
        self.menu_buttons["home"].pack(fill="x", pady=5, padx=10)

        self.menu_buttons["profile"] = self._crear_btn_menu("My Profile", self.mostrar_perfil)
        self.menu_buttons["profile"].pack(fill="x", pady=5, padx=10)

        self.menu_buttons["history"] = self._crear_btn_menu("Report History", self.mostrar_historial)
        self.menu_buttons["history"].pack(fill="x", pady=5, padx=10)

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

    def _limpiar_contenido(self):
        for w in self.content_area.winfo_children(): w.destroy()

    # --- RESTO DE MÉTODOS SIN CAMBIOS ---
    # Copia los métodos mostrar_dashboard, mostrar_perfil, mostrar_historial
    # y los auxiliares (_cargar_labs, _abrir_ventana, etc) del código anterior.
    # El cambio importante aquí fue en __init__, _build_sidebar y _highlight_menu.
    
    # ... (Pega aquí el resto del código de la versión anterior)
    
    # Para ahorrar espacio y no cortar la respuesta, te pongo el resto aquí:
    
    def mostrar_dashboard(self):
        self._highlight_menu("home")
        self._limpiar_contenido()
        header = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=40)
        ctk.CTkLabel(header, text="Select Laboratory", font=("Roboto", 32, "bold"), text_color="#333").pack(anchor="w")
        ctk.CTkLabel(header, text="Select a laboratory to report an incident.", font=("Roboto", 14), text_color="gray").pack(anchor="w")
        actions = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=10)
        actions.pack(fill="x", padx=40, pady=(0, 20))
        search_var = ctk.StringVar()
        entry_search = ctk.CTkEntry(actions, textvariable=search_var, placeholder_text="Search Lab name, building, floor...", width=300, height=40)
        entry_search.pack(side="left", padx=20, pady=20)
        btn_search = ctk.CTkButton(actions, text="Search", fg_color=constantes.COLOR_PRIMARY, command=lambda: self._buscar_lab(search_var.get(), tabla))
        btn_search.pack(side="left", padx=10)
        btn_report = ctk.CTkButton(actions, text="REPORT INCIDENT", fg_color=constantes.COLOR_ACCENT, hover_color="#b87608", font=("Roboto", 14, "bold"), height=40, command=lambda: self._iniciar_reporte(tabla))
        btn_report.pack(side="right", padx=20)
        frame_tabla = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        self._configurar_estilo_tabla()
        cols = ("Nombre", "Edificio", "Piso", "Equipos")
        tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=15)
        tabla.heading("Nombre", text="Lab Name")
        tabla.heading("Edificio", text="Building")
        tabla.heading("Piso", text="Floor")
        tabla.heading("Equipos", text="Computers")
        tabla.column("Nombre", width=150)
        tabla.column("Edificio", width=100, anchor="center")
        tabla.column("Piso", width=80, anchor="center")
        tabla.column("Equipos", width=100, anchor="center")
        tabla.pack(fill="both", expand=True)
        self._cargar_labs(tabla)

    def _cargar_labs(self, tabla, texto_filtro=None):
        for item in tabla.get_children(): tabla.delete(item)
        if texto_filtro: datos = laboratorios.laboratorios.consultar_filtro(texto_filtro)
        else: datos = laboratorios.laboratorios.consultar()
        for fila in datos: tabla.insert("", "end", values=fila)

    def _buscar_lab(self, texto, tabla): self._cargar_labs(tabla, texto.strip() if texto else None)

    def mostrar_perfil(self):
        self._highlight_menu("profile")
        self._limpiar_contenido()
        ctk.CTkLabel(self.content_area, text="User Profile", font=("Roboto", 32, "bold"), text_color="#333").pack(anchor="w", padx=40, pady=(40, 20))
        card = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=20)
        card.pack(pady=10, padx=40, fill="both", expand=True)
        banner = ctk.CTkFrame(card, fg_color=constantes.COLOR_PRIMARY, height=140, corner_radius=20)
        banner.pack(fill="x", padx=20, pady=20)
        header_content = ctk.CTkFrame(banner, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20)
        avatar_frame = ctk.CTkFrame(header_content, width=80, height=80, corner_radius=40, fg_color="white")
        avatar_frame.pack(side="left", pady=20)
        ctk.CTkLabel(avatar_frame, text="👤", font=("Arial", 40), text_color=constantes.COLOR_PRIMARY).place(relx=0.5, rely=0.5, anchor="center")
        text_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        text_frame.pack(side="left", padx=20, fill="y", pady=25)
        nombre_completo = f"{self.usuario[1]} {self.usuario[2]} {self.usuario[3]}"
        ctk.CTkLabel(text_frame, text=nombre_completo, font=("Roboto", 26, "bold"), text_color="white", anchor="w").pack(anchor="w")
        ctk.CTkLabel(text_frame, text=self.usuario[6].upper(), font=("Roboto", 14, "bold"), text_color="#E0E0E0", anchor="w").pack(anchor="w", pady=(2, 0))
        info_grid = ctk.CTkFrame(card, fg_color="transparent")
        info_grid.pack(pady=(10, 30), padx=50, fill="x")
        def crear_celda(row, col, icon, title, value):
            f = ctk.CTkFrame(info_grid, fg_color="#F9F9F9", corner_radius=10, border_width=1, border_color="#EEE")
            f.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(f, text=icon, font=("Arial", 24)).pack(side="left", padx=15)
            tf = ctk.CTkFrame(f, fg_color="transparent")
            tf.pack(side="left", pady=10)
            ctk.CTkLabel(tf, text=title, font=("Roboto", 11), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(tf, text=value, font=("Roboto", 14, "bold"), text_color="#333").pack(anchor="w")
        info_grid.columnconfigure((0,1), weight=1)
        crear_celda(0, 0, "📧", "Email Address", self.usuario[5])
        crear_celda(0, 1, "📞", "Phone Number", self.usuario[4])
        crear_celda(1, 0, "🆔", "User ID", str(self.usuario[0]))
        btn_edit = ctk.CTkButton(card, text="Edit Contact Info", fg_color="transparent", border_width=2, border_color=constantes.COLOR_PRIMARY, text_color=constantes.COLOR_PRIMARY, font=("Roboto", 14, "bold"), height=45, command=self._editar_perfil_popup)
        btn_edit.pack(side="bottom", pady=30)
        def on_enter(e): btn_edit.configure(fg_color=constantes.COLOR_PRIMARY, text_color="white")
        def on_leave(e): btn_edit.configure(fg_color="transparent", text_color=constantes.COLOR_PRIMARY)
        btn_edit.bind("<Enter>", on_enter)
        btn_edit.bind("<Leave>", on_leave)

    def _editar_perfil_popup(self):
        toplevel = ctk.CTkToplevel(self.ventana)
        toplevel.title("Edit Contact Info")
        toplevel.geometry("400x350")
        toplevel.transient(self.ventana)
        toplevel.grab_set()
        toplevel.update_idletasks()
        x = (toplevel.winfo_screenwidth() // 2) - (200)
        y = (toplevel.winfo_screenheight() // 2) - (175)
        toplevel.geometry(f'+{x}+{y}')
        frame = ctk.CTkFrame(toplevel, fg_color="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(frame, text="Edit Contact Info", font=("Roboto", 20, "bold"), text_color=constantes.COLOR_PRIMARY).pack(pady=(10, 20))
        ctk.CTkLabel(frame, text="Phone Number:", font=("Roboto", 12)).pack(anchor="w", padx=20)
        entry_phone = ctk.CTkEntry(frame)
        entry_phone.pack(fill="x", padx=20, pady=(0, 15))
        entry_phone.insert(0, self.usuario[4])
        ctk.CTkLabel(frame, text="Email Address:", font=("Roboto", 12)).pack(anchor="w", padx=20)
        entry_email = ctk.CTkEntry(frame)
        entry_email.pack(fill="x", padx=20, pady=(0, 20))
        entry_email.insert(0, self.usuario[5])
        def guardar_cambios():
            new_phone = entry_phone.get()
            new_email = entry_email.get()
            if not new_phone or not new_email:
                messagebox.showerror("Error", "All fields are required.")
                return
            if usuarios.Usuarios.actualizar_contacto(self.usuario[0], new_phone, new_email):
                messagebox.showinfo("Success", "Profile updated successfully.")
                self.usuario[4] = new_phone
                self.usuario[5] = new_email
                toplevel.destroy()
                self.mostrar_perfil()
            else:
                messagebox.showerror("Error", "Could not update profile.")
        ctk.CTkButton(frame, text="SAVE CHANGES", fg_color=constantes.COLOR_PRIMARY, command=guardar_cambios).pack(fill="x", padx=20, pady=10)

    def mostrar_historial(self):
        self._highlight_menu("history")
        self._limpiar_contenido()
        header = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=40)
        ctk.CTkLabel(header, text="Report History", font=("Roboto", 32, "bold"), text_color="#333").pack(anchor="w")
        ctk.CTkLabel(header, text="Manage your incident reports.", font=("Roboto", 12), text_color="gray").pack(anchor="w")
        actions = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=10)
        actions.pack(fill="x", padx=40, pady=(0, 20))
        hist_search_var = ctk.StringVar()
        entry_hist = ctk.CTkEntry(actions, textvariable=hist_search_var, placeholder_text="Filter history...", width=350, height=40)
        entry_hist.pack(side="left", padx=20, pady=20)
        btn_hist_search = ctk.CTkButton(actions, text="Filter", fg_color=constantes.COLOR_PRIMARY, command=lambda: self._buscar_historial(hist_search_var.get(), tabla))
        btn_hist_search.pack(side="left", padx=10)
        frame_tabla = ctk.CTkFrame(self.content_area, fg_color="transparent")
        frame_tabla.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        self._configurar_estilo_tabla()
        cols = ("ID", "Date", "Incident", "Lab Name", "Building", "Status", "Actions")
        tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=15)
        for col in cols:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center")
        tabla.column("ID", width=50)
        tabla.column("Incident", width=250, anchor="w")
        tabla.column("Actions", width=100, anchor="center") 
        tabla.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tabla.bind("<ButtonRelease-1>", lambda event: self._manejar_clic_tabla(event, tabla))
        self._cargar_historial(tabla)

    def _cargar_historial(self, tabla, filtro=""):
        for item in tabla.get_children(): tabla.delete(item)
        datos = funciones_incidentes.incidente.consulta_Tabla(self.usuario[0])
        tabla.tag_configure("process", background="#FFF3E0")
        tabla.tag_configure("ended", background="#E8F5E9")
        filtro = filtro.lower().strip()
        for fila in datos:
            if filtro:
                texto_fila = f"{fila[0]} {fila[2]} {fila[3]} {fila[4]}".lower()
                if filtro not in texto_fila: continue
            estado_txt = "In Process" if fila[5] == 0 else "Resolved"
            tag = "process" if fila[5] == 0 else "ended"
            acciones_txt = "📄  ✎  🗑" 
            valores = (fila[0], fila[1], fila[2], fila[3], fila[4], estado_txt, acciones_txt)
            tabla.insert("", "end", values=valores, tags=(tag,))

    def _buscar_historial(self, texto, tabla): self._cargar_historial(tabla, texto)

    def _manejar_clic_tabla(self, event, tabla):
        region = tabla.identify("region", event.x, event.y)
        if region == "cell":
            columna = tabla.identify_column(event.x)
            if columna == "#7": 
                item_id = tabla.identify_row(event.y)
                if item_id:
                    tabla.selection_set(item_id)
                    self._mostrar_menu_acciones(event, tabla, item_id)

    def _mostrar_menu_acciones(self, event, tabla, item_id):
        menu = Menu(self.ventana, tearoff=0)
        menu.add_command(label="📄 View Details", command=lambda: self._accion_ver(tabla, item_id))
        menu.add_command(label="✎ Edit Report", command=lambda: self._accion_editar(tabla, item_id))
        menu.add_separator()
        menu.add_command(label="🗑 Delete Report", command=lambda: self._accion_borrar(tabla, item_id))
        menu.tk_popup(event.x_root, event.y_root)

    def _accion_ver(self, tabla, item_id):
        datos = tabla.item(item_id, "values")
        self._abrir_ventana_reporte("View Details", None, datos[0], es_edicion=False, datos_completos=datos, solo_lectura=True)

    def _accion_borrar(self, tabla, item_id):
        datos = tabla.item(item_id, "values") 
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this report?"):
            if funciones_incidentes.incidente.borrarIncidente(datos):
                self._cargar_historial(tabla) 

    def _accion_editar(self, tabla, item_id):
        datos = tabla.item(item_id, "values")
        self._abrir_ventana_reporte("Edit Report", None, datos[0], es_edicion=True, texto_actual=datos[2])

    def _iniciar_reporte(self, tabla):
        seleccion = tabla.focus()
        if not seleccion:
            messagebox.showwarning("Selection Required", "Please select a laboratory to report.")
            return
        datos_lab = tabla.item(seleccion, "values") 
        id_tupla = laboratorios.laboratorios.buscar_id(datos_lab)
        if not id_tupla:
             messagebox.showerror("Error", "Could not identify laboratory ID.")
             return
        self._abrir_ventana_reporte("New Report", datos_lab, id_tupla[0])

    def _abrir_ventana_reporte(self, titulo, datos_lab, id_referencia, es_edicion=False, texto_actual="", datos_completos=None, solo_lectura=False):
        toplevel = ctk.CTkToplevel(self.ventana)
        toplevel.title(titulo)
        toplevel.geometry("500x600")
        toplevel.transient(self.ventana)
        toplevel.grab_set()
        toplevel.update_idletasks()
        width = toplevel.winfo_width()
        height = toplevel.winfo_height()
        x = (toplevel.winfo_screenwidth() // 2) - (width // 2)
        y = (toplevel.winfo_screenheight() // 2) - (height // 2)
        toplevel.geometry(f'{width}x{height}+{x}+{y}')
        frame = ctk.CTkFrame(toplevel, fg_color="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(frame, text=titulo, font=("Roboto", 24, "bold"), text_color=constantes.COLOR_PRIMARY).pack(pady=(10, 20))
        if solo_lectura and datos_completos:
            grid = ctk.CTkFrame(frame, fg_color="#F9F9F9")
            grid.pack(fill="x", padx=10, pady=10)
            campos = [("Report ID:", datos_completos[0]), ("Date:", datos_completos[1]),
                      ("Status:", datos_completos[5]), ("Laboratory:", datos_completos[3]),
                      ("Building:", datos_completos[4])]
            for label, val in campos:
                f = ctk.CTkFrame(grid, fg_color="transparent")
                f.pack(fill="x", padx=10, pady=5)
                ctk.CTkLabel(f, text=label, width=100, anchor="w", font=("Roboto", 12, "bold"), text_color="gray").pack(side="left")
                ctk.CTkLabel(f, text=val, anchor="w", font=("Roboto", 12), text_color="#333").pack(side="left")
            ctk.CTkLabel(frame, text="Incident Details:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
            txt = ctk.CTkTextbox(frame, height=150, border_color="gray", border_width=1, fg_color="#F0F0F0")
            txt.pack(fill="x", padx=10)
            txt.insert("1.0", datos_completos[2])
            txt.configure(state="disabled")
            ctk.CTkButton(frame, text="Close", fg_color="gray", command=toplevel.destroy).pack(fill="x", padx=10, pady=20)
            return
        if datos_lab:
            info_box = ctk.CTkFrame(frame, fg_color="#F5F5F5")
            info_box.pack(fill="x", pady=10, padx=10)
            ctk.CTkLabel(info_box, text=f"Lab: {datos_lab[0]}", font=("Roboto", 14, "bold")).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(info_box, text=f"Building: {datos_lab[1]} - Floor: {datos_lab[2]}", font=("Roboto", 12)).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(info_box, text=f"Date: {date.today()}", font=("Roboto", 12)).pack(anchor="w", padx=10, pady=2)
        ctk.CTkLabel(frame, text="Describe the incident:", font=("Roboto", 14)).pack(anchor="w", padx=10, pady=(10, 5))
        txt_desc = ctk.CTkTextbox(frame, height=150, border_color="gray", border_width=1)
        txt_desc.pack(fill="x", padx=10)
        txt_desc.focus()
        if texto_actual: txt_desc.insert("1.0", texto_actual)
        lbl_chars = ctk.CTkLabel(frame, text="0 / 150 chars", text_color="gray", font=("Roboto", 12))
        lbl_chars.pack(anchor="e", padx=10)
        def check_chars(event):
            texto = txt_desc.get("1.0", "end-1c")
            if len(texto) > 150:
                txt_desc.delete("end-2c")
            lbl_chars.configure(text=f"{len(txt_desc.get('1.0', 'end-1c'))} / 150 chars")
        txt_desc.bind("<KeyRelease>", check_chars)
        def enviar():
            texto = txt_desc.get("1.0", "end-1c")
            if not texto.strip():
                messagebox.showerror("Error", "Description cannot be empty.")
                return
            if es_edicion:
                funciones_incidentes.incidente.actualizar((id_referencia, texto)) 
                messagebox.showinfo("Success", "Report updated.")
                self.mostrar_historial()
            else:
                exito = funciones_incidentes.incidente.insertar(self.usuario[0], texto, id_referencia)
                if exito: messagebox.showinfo("Success", "Report submitted successfully.")
            toplevel.destroy()
        ctk.CTkButton(frame, text="SUBMIT", fg_color=constantes.COLOR_PRIMARY, height=45, command=enviar).pack(fill="x", padx=10, pady=20)

    def _configurar_estilo_tabla(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", rowheight=35, fieldbackground="white", font=("Roboto", 12))
        style.configure("Treeview.Heading", background="#E0E0E0", foreground="#333", font=("Roboto", 13, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", constantes.COLOR_HOVER)])