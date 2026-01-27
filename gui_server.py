import tkinter as tk
from tkinter import messagebox
from Grafo import SocialtecGrafo


class ServerGUI:
    def __init__(self, grafo):
        self.grafo = grafo

        self.root = tk.Tk()
        self.root.title("Socialtec - Server")
        self.root.geometry("400x400")

        tk.Label(
            self.root,
            text="GUI DEL SERVER - SOCIALTEC",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Mostrar Grafo",
            width=25,
            command=self.mostrar_grafo
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Buscar Path entre Usuarios",
            width=25,
            command=self.buscar_path
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Ver Estadísticas",
            width=25,
            command=self.ver_estadisticas
        ).pack(pady=5)

        self.root.mainloop()

    # ----------------------------
    # ID 002 - Mostrar Grafo
    # ----------------------------
    def mostrar_grafo(self):
        if self.grafo.grafo.number_of_nodes() == 0:
            messagebox.showinfo("Info", "El grafo está vacío")
            return

        self.grafo.imprimir_grafo()

    # ----------------------------
    # ID 010 - Path entre usuarios
    # ----------------------------
    def buscar_path(self):
        ventana = tk.Toplevel()
        ventana.title("Buscar Path")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Usuario origen").pack(pady=5)
        entry_origen = tk.Entry(ventana)
        entry_origen.pack()

        tk.Label(ventana, text="Usuario destino").pack(pady=5)
        entry_destino = tk.Entry(ventana)
        entry_destino.pack()

        def calcular():
            origen = entry_origen.get()
            destino = entry_destino.get()

            path = self.grafo.bfs_path(origen, destino)

            if path:
                messagebox.showinfo(
                    "Path encontrado",
                    " → ".join(path)
                )
            else:
                messagebox.showerror(
                    "Sin Path",
                    "No existe un camino entre los usuarios"
                )

        tk.Button(
            ventana,
            text="Calcular Path",
            command=calcular
        ).pack(pady=10)

    # ----------------------------
    # ID 011 - Estadísticas
    # ----------------------------
    def ver_estadisticas(self):
        stats = self.grafo.estadisticas()

        if not stats:
            messagebox.showinfo("Info", "No hay datos en el grafo")
            return

        texto = (
            f"Usuario con más amigos: {stats['mas_amigos'][0]} "
            f"({stats['mas_amigos'][1]})\n\n"
            f"Usuario con menos amigos: {stats['menos_amigos'][0]} "
            f"({stats['menos_amigos'][1]})\n\n"
            f"Promedio de amigos por usuario: "
            f"{stats['promedio_amigos']}"
        )

        messagebox.showinfo("Estadísticas del Grafo", texto)
