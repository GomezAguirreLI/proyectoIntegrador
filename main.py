# main.py

# from tkinter import * # <--- ELIMINAR
import customtkinter as ctk # <--- NUEVA IMPORTACIÓN
from view import interfaz

# 1. Configuración global de la apariencia de customtkinter
ctk.set_appearance_mode("Light") # O "Dark" si lo prefieres
ctk.set_default_color_theme("green") # Usar el color del tema

class App:
    # Ahora la ventana es una CTk (ventana principal)
    def __init__(self,ventana):
        self.view = interfaz.Vista(ventana)
        

if __name__=="__main__":
    # 2. Usar ctk.CTk() en lugar de Tk()
    ventana = ctk.CTk()
    app = App(ventana)
    ventana.mainloop()