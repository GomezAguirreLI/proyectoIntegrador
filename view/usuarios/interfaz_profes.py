from tkinter import messagebox
from controller import funciones_login
import os
from tkinter import *
from PIL import Image,ImageTk
from view import constantes
import customtkinter as ctk
def usuarios_profes(parent):
    """Construye el dashboard dentro del `parent` (no crear una nueva Tk).

    Layout: sidebar (verde = `constantes.color`) a la izquierda
    y área principal blanca a la derecha.
    """
    # Limpiar solo el parent recibido para reemplazar contenido
    for w in parent.winfo_children():
        w.destroy()

    # Contenedor principal (blanco de fondo)
    container = Frame(parent, bg="white")
    container.pack(fill="both", expand=True)
    


    # Sidebar verde
    sidebar = ctk.CTkFrame(container, fg_color=constantes.color, width=220,border_color=constantes.color,corner_radius=20,border_width=2)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)


    # Área principal (blanco)
    main = Frame(container, bg="white")
    main.pack(side=LEFT, fill=BOTH, expand=True)

    # Header dentro del main
    header = Frame(main, bg="white", height=70)
    header.pack(fill="x")
    title = Label(header, text="Dashboard", bg="white", fg="black",
                  font=("Arial", 20, "bold"))
    title.pack(padx=20, pady=15, anchor="w")

    # Contenido de ejemplo en el main
    Label(main, text="Contenido principal aquí", bg="white", fg="black",
          font=("Arial", 16)).pack(pady=20)

    # Elementos del sidebar (botones de ejemplo)
    btn_inicio = Button(sidebar, text="Inicio", bg=constantes.color, fg="white",
                        bd=0, activebackground="#3b6b4b", cursor="hand2",
                        command=lambda: messagebox.showinfo("Inicio", "Se presionó Inicio"))
    btn_inicio.pack(fill="x", padx=12, pady=(20, 8))

    btn_perfil = Button(sidebar, text="Perfil", bg=constantes.color, fg="white",
                       bd=0, activebackground="#3b6b4b", cursor="hand2",
                       command=lambda: messagebox.showinfo("Perfil", "Se presionó Perfil"))
    btn_perfil.pack(fill="x", padx=12, pady=8)

    btn_salir = Button(sidebar, text="Cerrar Sesión", bg="#b33c3c", fg="white",
                       bd=0, cursor="hand2",
                       command=lambda: messagebox.showinfo("Salir", "Cerrar sesión"))
    btn_salir.pack(fill="x", padx=12, pady=(8, 20))



     
