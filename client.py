import socket

HOST = "127.0.0.1"
PORT = 5000


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))

    usuario = input("Usuario: ")
    password = input("Password: ")

    mensaje = f"LOGIN|{usuario}|{password}"
    cliente.send(mensaje.encode())

    respuesta = cliente.recv(1024).decode()
    print("Respuesta del server:", respuesta)

    cliente.close()


if __name__ == "__main__":
    main()
