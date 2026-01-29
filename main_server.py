import threading
from server import SocialtecServer
from gui_server import ServerGUI

def iniciar_server():
    server = SocialtecServer()
    server.iniciar()

if __name__ == "__main__":
    server = SocialtecServer()

    hilo_server = threading.Thread(
        target=server.iniciar,
        daemon=True
    )
    hilo_server.start()

    ServerGUI(server.grafo)
