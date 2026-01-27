from auth import AuthManager

auth = AuthManager()

# Registro
auth.registrar_usuario("ana01", "1234")
auth.registrar_usuario("bob02", "abcd")

# Login correcto
print("Login Ana:", auth.login("ana01", "1234"))

# Login incorrecto
print("Login Ana (mal):", auth.login("ana01", "9999"))

# Usuario inexistente
print("Login Carlos:", auth.login("carlos03", "hola"))