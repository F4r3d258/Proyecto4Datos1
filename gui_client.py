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
        tk.Label(self.root, text="Nombre completo").pack(pady=5)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.pack()

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

        tk.Button(
            self.root,
            text="Crear usuario",
            command=self.crear_usuario
        ).pack(pady=5)


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
    def crear_usuario(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        nombre = self.entry_nombre.get()

        if not usuario or not password or not nombre:
            messagebox.showerror("Error", "Debe completar todos los campos")
            return

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST, PORT))
            cliente.send(f"REGISTRAR|{usuario}|{password}|{nombre}".encode())

            respuesta = cliente.recv(1024).decode()
            cliente.close()

            if respuesta == "REGISTRO_OK":
                messagebox.showinfo(
                    "Éxito",
                    "Usuario creado. Ahora puede iniciar sesión."
                )
            else:
                messagebox.showerror(
                    "Error",
                    "El usuario ya existe"
                )

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
            text="Ver mis amigos",
            command=self.ver_amigos
        ).pack(pady=5)

        tk.Button(
            self.busqueda,
            text="Agregar amistad",
            command=self.agregar_amistad
        ).pack(pady=5)

        tk.Button(
            self.busqueda,
            text="Eliminar amistad",
            command=self.eliminar_amistad
        ).pack(pady=5)

        tk.Button(
            self.busqueda,
            text="Ver perfil",
            command=self.ver_perfil
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
    
    def agregar_amistad(self):
        seleccion = self.lista.curselection()
    
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un usuario")
            return
    
        usuario_seleccionado = self.lista.get(seleccion[0])
    
        if usuario_seleccionado == self.usuario_actual:
            messagebox.showerror("Error", "No puedes agregarte a ti mismo")
            return
    
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
    
        mensaje = f"AGREGAR_AMISTAD|{self.usuario_actual}|{usuario_seleccionado}"
        cliente.send(mensaje.encode())
    
        respuesta = cliente.recv(1024).decode()
        cliente.close()
    
        if respuesta == "AMISTAD_OK":
            messagebox.showinfo("Éxito", "Amistad agregada")
        else:
            messagebox.showerror("Error", "No se pudo agregar la amistad")
    
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


    def ver_amigos(self):
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        cliente.send(f"AMIGOS|{self.usuario_actual}".encode())

        respuesta = cliente.recv(1024).decode()
        cliente.close()

        if not respuesta.startswith("AMIGOS"):
            messagebox.showerror("Error", "No se pudieron obtener amigos")
            return
        
        amigos = respuesta.split("|")[1]

        if amigos == "":
            messagebox.showinfo("Amigos", "No tienes amigos agregados")
            return
        
        lista_amigos = amigos.split(",")

        #Merge Sort
        lista_ordenada = merge_sort(lista_amigos)

        ventana = tk.Toplevel()
        ventana.title("Mis Amigos (ordenados)")
        ventana.geometry("250x300")

        listbox = tk.Listbox(ventana)
        listbox.pack(fill=tk.BOTH, expand=True)

        for amigo in lista_ordenada:
            listbox.insert(tk.END, amigo)

    def ver_perfil(self):
        seleccion = self.lista.curselection()

        if seleccion:
            usuario = self.lista.get(seleccion[0])
        else:
            usuario = self.usuario_actual

        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        cliente.send(f"PERFIL|{usuario}".encode())

        respuesta = cliente.recv(2048).decode()
        cliente.close()

        if not respuesta.startswith("PERFIL"):
            messagebox.showerror("Error", "No se pudo cargar el perfil")
            return

        _, nombre, foto, amigos = respuesta.split("|")

        ventana = tk.Toplevel()
        ventana.title(f"Perfil de {usuario}")
        ventana.geometry("300x350")

        tk.Label(
            ventana,
            text=f"Usuario: {usuario}",
            font=("Arial", 10, "bold")
        ).pack(pady=5)

        tk.Label(ventana, text=f"Nombre: {nombre}").pack(pady=5)

        if foto == "NO_DISPONIBLE":
            tk.Label(ventana, text="Foto: No disponible").pack(pady=5)
        else:
            tk.Label(ventana, text=f"Foto: {foto}").pack(pady=5)

        tk.Label(ventana, text="Amigos:").pack(pady=5)

        listbox = tk.Listbox(ventana)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10)

        if amigos:
            lista_amigos = merge_sort(amigos.split(","))
            for amigo in lista_amigos:
                listbox.insert(tk.END, amigo)
        else:
            listbox.insert(tk.END, "No tiene amigos")

def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])

    return merge(izquierda,derecha)

def merge(izq, der):
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        if izq[i].lower() <= der [j].lower():
            resultado.append(izq[i])
            i += 1

        else:
            resultado.append(der[j])
            j += 1
    
    resultado.extend(izq[i:])
    resultado.extend(der[j:])

    return resultado


if __name__ == "__main__":
    ClienteGUI()
