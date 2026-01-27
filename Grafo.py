import networkx as nx
from collections import deque


class SocialtecGrafo:
    def __init__(self):
        # Grafo no dirigido (amistad es bidireccional)
        self.grafo = nx.Graph()

    # USUARIOS
    def agregar_usuario(self, username, nombre, foto=None):
        if username in self.grafo:
            raise ValueError("El usuario ya existe")

        self.grafo.add_node(username, nombre=nombre, foto=foto)

    def usuario_existe(self, username):
        return username in self.grafo

    # AMISTADES
    def agregar_amistad(self, user1, user2):
        if user1 not in self.grafo or user2 not in self.grafo:
            raise ValueError("Uno o ambos usuarios no existen")

        if user1 == user2:
            raise ValueError("Un usuario no puede ser amigo de sí mismo")

        self.grafo.add_edge(user1, user2)

    def eliminar_amistad(self, user1, user2):
        if self.grafo.has_edge(user1, user2):
            self.grafo.remove_edge(user1, user2)

    def obtener_amigos(self, username):
        if username not in self.grafo:
            raise ValueError("Usuario no existe")

        return list(self.grafo.neighbors(username))

    # PATH ENTRE AMIGOS (ID 010)
    def existe_path(self, origen, destino):
        if origen not in self.grafo or destino not in self.grafo:
            return None

        if nx.has_path(self.grafo, origen, destino):
            return nx.shortest_path(self.grafo, origen, destino)
        else:
            return None

    # ESTADÍSTICAS (ID 011)
    def estadisticas(self):
        if self.grafo.number_of_nodes() == 0:
            return None

        grados = dict(self.grafo.degree())

        usuario_mas_amigos = max(grados, key=grados.get)
        usuario_menos_amigos = min(grados, key=grados.get)

        promedio = sum(grados.values()) / len(grados)

        return {
            "mas_amigos": (usuario_mas_amigos, grados[usuario_mas_amigos]),
            "menos_amigos": (usuario_menos_amigos, grados[usuario_menos_amigos]),
            "promedio_amigos": round(promedio, 2)
        }

    # IMPRESIÓN DEL GRAFO (ID 002)
    def imprimir_grafo(self):
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 6))
        nx.draw(
            self.grafo,
            with_labels=True,
            node_size=2000,
            node_color="lightblue",
            font_weight="bold"
        )
        plt.show()

    # BFS, PATH ENTRE AMIGOS
    def bfs_path(self, origen, destino):
        if origen not in self.grafo or destino not in self.grafo:
            return None

        visitados = set()
        cola = deque()

        # (nodo_actual, camino_hasta_ahora)
        cola.append((origen, [origen]))
        visitados.add(origen)

        while cola:
            actual, camino = cola.popleft()

            # Si llegamos al destino
            if actual == destino:
                return camino

            # Explorar vecinos
            for vecino in self.grafo.neighbors(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, camino + [vecino]))

        # Si no existe path
        return None
