from Grafo import SocialtecGrafo

grafo = SocialtecGrafo()

# Crear usuarios
grafo.agregar_usuario("ana01", "Ana")
grafo.agregar_usuario("bob02", "Bob")
grafo.agregar_usuario("carlos03", "Carlos")
grafo.agregar_usuario("diana04", "Diana")

# Crear amistades
grafo.agregar_amistad("ana01", "bob02")
grafo.agregar_amistad("bob02", "carlos03")
grafo.agregar_amistad("carlos03", "diana04")

# Path
path = grafo.existe_path("ana01", "diana04")
print("Path:", path)

# Estadísticas
stats = grafo.estadisticas()
print("Estadísticas:", stats)

# Mostrar grafo
grafo.imprimir_grafo()

# BFS manual
path_bfs = grafo.bfs_path("ana01", "diana04")
print("Path BFS:", path_bfs)
