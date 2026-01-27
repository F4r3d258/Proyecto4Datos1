import json
import os
from passlib.context import CryptContext


class AuthManager:
    def __init__(self, archivo="usuarios.json"):
        self.archivo = archivo
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            deprecated="auto"
        )
        self.usuarios = {}
        self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                self.usuarios = json.load(f)

    def guardar(self):
        with open(self.archivo, "w") as f:
            json.dump(self.usuarios, f)

    def registrar_usuario(self, username, password):
        if username in self.usuarios:
            raise ValueError("Usuario ya existe")

        self.usuarios[username] = self.pwd_context.hash(password)
        self.guardar()

    def login(self, username, password):
        if username not in self.usuarios:
            return False
        return self.pwd_context.verify(password, self.usuarios[username])
