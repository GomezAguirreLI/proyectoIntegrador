from view import interfaz

class App:
    def __init__(self):
        # Simplemente llamamos a la Vista. Ella se encarga de crear la ventana.
        self.view = interfaz.Vista()

if __name__ == "__main__":
    app = App()