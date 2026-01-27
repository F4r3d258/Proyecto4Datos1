import socket
import threading
from auth import AuthManager
from Grafo import SocialtecGrafo

HOST = "127.0.0.1"
PORT = 5000


class SocialtecServer:
    def __init__(self):
        self.auth = AuthManager()
        self.grafo = SocialtecGrafo()

        # Datos de prueba
        self.auth.registrar_usuario("ana01", "1234")
        self.auth.registrar_usuario("bob02", "abcd")

        self.grafo.agregar_usuario("ana01", "Ana")
        self.grafo.agregar_usuario("bob02", "Bob")
        self.grafo.agregar_amistad("ana01", "bob02")

    def manejar_cliente(self, conn, addr):
        print(f"[+] Cliente conectado: {addr}")

        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                respuesta = self.procesar_mensaje(data)
                conn.send(respuesta.encode())

        except Exception as e:
            print("Error:", e)

        finally:
            conn.close()
            print(f"[-] Cliente desconectado: {addr}")

    def procesar_mensaje(self, mensaje):
        partes = mensaje.split("|")
        comando = partes[0]

        if comando == "LOGIN":
            usuario = partes[1]
            password = partes[2]

            if self.auth.login(usuario, password):
                return "LOGIN_OK"
            else:
                return "LOGIN_ERROR"

        return "COMANDO_DESCONOCIDO"

    def iniciar(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()

        print(f"[SERVER] Escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            hilo = threading.Thread(
                target=self.manejar_cliente,
                args=(conn, addr),
                daemon=True
            )
            hilo.start()
     
    def procesar_mensaje(self, mensaje):
        partes = mensaje.split("|")
        comando = partes[0]

        if comando == "LOGIN":
            usuario = partes[1]
            password = partes[2]

            if self.auth.login(usuario, password):
                return "LOGIN_OK"
            else:
                return "LOGIN_ERROR"

        elif comando == "BUSCAR":
            nombre = partes[1].lower()
            resultados = []

            for user, data in self.grafo.grafo.nodes(data=True):
                if nombre in data["nombre"].lower():
                    resultados.append(user)

            if resultados:
                return "RESULTADOS|" + ",".join(resultados)
            else:
                return "SIN_RESULTADOS"

        elif comando == "ELIMINAR_AMISTAD":
            u1 = partes[1]
            u2 = partes[2]

            if self.grafo.grafo.has_edge(u1, u2):
                self.grafo.eliminar_amistad(u1, u2)
                return "AMISTAD_ELIMINADA"
            else:
                return "NO_SON_AMIGOS"

        return "COMANDO_DESCONOCIDO"

if __name__ == "__main__":
    SocialtecServer().iniciar()