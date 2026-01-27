import socket
import tkinter as tk
from tkinter import messagebox

HOST = "127.0.0.1"
PORT = 5000


class ClienteGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Socialtec - Cliente")
        self.root.geometry("300x200")

        # --- Usuario ---
        tk.Label(self.root, text="Usuario").pack(pady=5)
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack()

        # --- Password ---
        tk.Label(self.root, text="Contraseña").pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        # --- Botón ---
        tk.Button(
            self.root,
            text="Iniciar Sesión",
            command=self.login
        ).pack(pady=15)

        self.root.mainloop()

    def login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, PORT))

            cliente.send(f"LOGIN|{usuario}|{password}".encode())
            respuesta = cliente.recv(1024).decode()
            cliente.close()

            if respuesta == "LOGIN_OK":
                self.usuario_actual = usuario
                self.abrir_busqueda()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_busqueda(self):
        self.root.destroy()

        self.busqueda = tk.Tk()
        self.busqueda.title("Buscar usuarios")
        self.busqueda.geometry("350x300")

        tk.Label(self.busqueda, text="Buscar por nombre").pack(pady=5)
        self.entry_buscar = tk.Entry(self.busqueda)
        self.entry_buscar.pack()

        tk.Button(
            self.busqueda,
            text="Buscar",
            command=self.buscar_usuario
        ).pack(pady=5)

        self.lista = tk.Listbox(self.busqueda)
        self.lista.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Button(
            self.busqueda,
            text="Eliminar amistad",
            command=self.eliminar_amistad
        ).pack(pady=5)

        self.busqueda.mainloop()

    def buscar_usuario(self):
        nombre = self.entry_buscar.get()

        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        cliente.send(f"BUSCAR|{nombre}".encode())

        respuesta = cliente.recv(1024).decode()
        cliente.close()

        self.lista.delete(0, tk.END)

        if respuesta.startswith("RESULTADOS"):
            usuarios = respuesta.split("|")[1].split(",")
            for u in usuarios:
                self.lista.insert(tk.END, u)
        else:
            messagebox.showinfo("Info", "No se encontraron usuarios")

    def eliminar_amistad(self):
        seleccion = self.lista.curselection()

        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario")
            return

        usuario_seleccionado = self.lista.get(seleccion[0])

        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))

        mensaje = f"ELIMINAR_AMISTAD|{self.usuario_actual}|{usuario_seleccionado}"
        cliente.send(mensaje.encode())

        respuesta = cliente.recv(1024).decode()
        cliente.close()

        if respuesta == "AMISTAD_ELIMINADA":
            messagebox.showinfo("Éxito", "Amistad eliminada")
        else:
            messagebox.showerror("Error", "No son amigos")


if __name__ == "__main__":
    ClienteGUI()
