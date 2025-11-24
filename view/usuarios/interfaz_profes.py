from tkinter import messagebox
from controller import funciones_login
import os
from PIL import Image,ImageTk
from view import constantes
import customtkinter as ctk

def usuarios_profes(parent):

    # Limpiar solo el parent recibido para reemplazar contenido
    for w in parent.winfo_children():
        w.destroy()

    # Contenedor principal (usa CTkFrame, NO Frame)
    container = ctk.CTkFrame(parent, fg_color="white")
    container.pack(fill="both", expand=True)

    # Sidebar verde
    sidebar = ctk.CTkFrame(
        container,
        fg_color=constantes.color,
        width=220,
        border_color=constantes.color,
        corner_radius=20,
        border_width=2
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)   # <<< IMPORTANTE: para que respete el ancho/alto

    # Área principal (blanco)
    main = ctk.CTkFrame(container, fg_color="white")
    main.pack(side="left", fill="both", expand=True)

    # Header dentro del main
    header = ctk.CTkFrame(main, fg_color="white", height=70)
    header.pack(fill="x")

    title = ctk.CTkLabel(
        header,
        text="Dashboard",
        text_color="black",
        font=("Arial", 20, "bold")
    )
    title.pack(padx=20, pady=15, anchor="w")

    # Contenido de ejemplo en el main
    ctk.CTkLabel(
        main,
        text="Contenido principal aquí",
        text_color="black",
        font=("Arial", 16)
    ).pack(pady=20)

    # --- Botones del sidebar (usa CTkButton) ---
    btn_inicio = ctk.CTkButton(
        sidebar,
        text="Inicio",
        fg_color=constantes.color,
        hover_color="#3b6b4b",
        text_color="white",
        corner_radius=8,
        command=lambda: messagebox.showinfo("Inicio", "Se presionó Inicio")
    )
    btn_inicio.pack(fill="x", padx=12, pady=(20, 8))

    btn_perfil = ctk.CTkButton(
        sidebar,
        text="Perfil",
        fg_color=constantes.color,
        hover_color="#3b6b4b",
        text_color="white",
        corner_radius=8,
        command=lambda: messagebox.showinfo("Perfil", "Se presionó Perfil")
    )
    btn_perfil.pack(fill="x", padx=12, pady=8)

    btn_salir = ctk.CTkButton(
        sidebar,
        text="Cerrar Sesión",
        fg_color="#b33c3c",
        hover_color="#912f2f",
        text_color="white",
        corner_radius=8,
        command=lambda: messagebox.showinfo("Salir", "Cerrar sesión")
    )
    btn_salir.pack(fill="x", padx=12, pady=(8, 20))
