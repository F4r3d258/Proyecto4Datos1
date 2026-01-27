from passlib.context import CryptContext


class AuthManager:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            deprecated="auto"
        )

        # Simula base de datos
        self.usuarios = {}

    def registrar_usuario(self, username, password):
        if username in self.usuarios:
            raise ValueError("El usuario ya existe")

        password_hash = self.pwd_context.hash(password)
        self.usuarios[username] = password_hash
        return True

    def login(self, username, password):
        if username not in self.usuarios:
            return False

        password_hash = self.usuarios[username]
        return self.pwd_context.verify(password, password_hash)
