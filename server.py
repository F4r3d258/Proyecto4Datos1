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
        self.grafo.cargar()

    # MANEJO DE CLIENTES
    def manejar_cliente(self, conn, addr):
        print(f"[+] Cliente conectado: {addr}")

        try:
            while True:
                data = conn.recv(2048).decode()
                if not data:
                    break

                respuesta = self.procesar_mensaje(data)
                conn.send(respuesta.encode())

        except Exception as e:
            print("Error:", e)

        finally:
            conn.close()
            print(f"[-] Cliente desconectado: {addr}")

    # PROCESADOR DE MENSAJES
    def procesar_mensaje(self, mensaje):
        partes = mensaje.split("|")
        comando = partes[0]

        # ---------- LOGIN ----------
        if comando == "LOGIN":
            usuario = partes[1]
            password = partes[2]

            if self.auth.login(usuario, password):
                return "LOGIN_OK"
            else:
                return "LOGIN_ERROR"

        # ---------- REGISTRO ----------
        elif comando == "REGISTRAR":
            usuario = partes[1]
            password = partes[2]
            nombre = partes[3]

            try:
                self.auth.registrar_usuario(usuario, password)
                self.grafo.agregar_usuario(usuario, nombre)
                self.grafo.guardar()
                return "REGISTRO_OK"
            except:
                return "REGISTRO_ERROR"

        # ---------- BUSCAR USUARIOS ----------
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

        # ---------- AGREGAR AMISTAD ----------
        elif comando == "AGREGAR_AMISTAD":
            u1 = partes[1]
            u2 = partes[2]

            try:
                self.grafo.agregar_amistad(u1, u2)
                self.grafo.guardar()
                return "AMISTAD_OK"
            except:
                return "ERROR"

        # ---------- ELIMINAR AMISTAD ----------
        elif comando == "ELIMINAR_AMISTAD":
            u1 = partes[1]
            u2 = partes[2]

            if self.grafo.grafo.has_edge(u1, u2):
                self.grafo.eliminar_amistad(u1, u2)
                self.grafo.guardar()
                return "AMISTAD_ELIMINADA"
            else:
                return "NO_SON_AMIGOS"

        # ---------- VER AMIGOS ----------
        elif comando == "AMIGOS":
            usuario = partes[1]

            if not self.grafo.usuario_existe(usuario):
                return "ERROR"

            amigos = self.grafo.obtener_amigos(usuario)
            return "AMIGOS|" + ",".join(amigos)

        # ---------- PERFIL ----------
        elif comando == "PERFIL":
            usuario = partes[1]

            if not self.grafo.usuario_existe(usuario):
                return "ERROR"

            data = self.grafo.grafo.nodes[usuario]
            nombre = data.get("nombre", "")
            foto = data.get("foto")

            amigos = self.grafo.obtener_amigos(usuario)

            foto_str = foto if foto else "NO_DISPONIBLE"
            amigos_str = ",".join(amigos) if amigos else ""

            return f"PERFIL|{nombre}|{foto_str}|{amigos_str}"

        return "COMANDO_DESCONOCIDO"

    # INICIAR SERVIDOR
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


if __name__ == "__main__":
    SocialtecServer().iniciar()
