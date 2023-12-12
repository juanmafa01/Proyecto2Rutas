import json
from Aeropuerto import Aeropuerto
from Ruta import Ruta
import networkx as nx

class Grafo:
    def __init__(self, aeropuertos_file="aeropuertos.json", rutas_file="rutas.json"):
        self.aeropuertos = []
        self.rutas = []
        self.grafo = nx.DiGraph()

        self.cargar_aeropuertos(aeropuertos_file)
        self.cargar_rutas(rutas_file)
        self.actualizar_grafo()

    def agregar_aeropuerto(self, aeropuerto, filename="aeropuertos.json"):
        if any(a.codigo == aeropuerto.codigo for a in self.aeropuertos):
            print("El aeropuerto ya está registrado.")
        else:
            self.aeropuertos.append(aeropuerto)
            print("Aeropuerto agregado correctamente.")

        self.guardar_aeropuertos(filename)
        self.actualizar_grafo()

    def agregar_ruta(self, ruta, filename="rutas.json"):
        if ruta.origen in self.aeropuertos and ruta.destino in self.aeropuertos:
            self.rutas.append(ruta)
            print("Ruta agregada correctamente.")
        else:
            print("Aeropuertos de origen o destino no encontrados.")

        self.guardar_rutas(filename)
        self.actualizar_grafo()

    def actualizar_grafo(self):
        self.grafo.clear()
        for aeropuerto in self.aeropuertos:
            self.grafo.add_node(aeropuerto.codigo, label=aeropuerto.nombre)

        for ruta in self.rutas:
            self.grafo.add_edge(ruta.origen.codigo, ruta.destino.codigo, weight=ruta.distancia, tiempo_vuelo=ruta.tiempo_vuelo)

    def buscar_rutas_entre_aeropuertos(self, origen, destino):
        try:
            rutas = list(nx.all_simple_paths(self.grafo, source=origen, target=destino, cutoff=None))
            return rutas
        except nx.NetworkXNoPath:
            print(f"No se encontraron rutas entre {origen} y {destino}.")
            return None

    def buscar_mejor_ruta(self, origen, destino):
        rutas = self.buscar_rutas_entre_aeropuertos(origen, destino)

        if rutas:
            print(f"Rutas entre {origen} y {destino}:")

            # Inicializamos la distancia mínima, el tiempo mínimo y las rutas mejores
            distancia_minima = float('inf')
            tiempo_minimo = float('inf')
            rutas_mejores = []

            for i, ruta in enumerate(rutas, start=1):
                distancia_total = sum(self.grafo[u][v]['weight'] for u, v in zip(ruta[:-1], ruta[1:]))
                tiempo_total = sum(self.grafo[u][v]['tiempo_vuelo'] for u, v in zip(ruta[:-1], ruta[1:]))
                
                print(f"Ruta {i}: {ruta} - Distancia total: {distancia_total} km - Tiempo total de vuelo: {tiempo_total} horas")

                # Verificamos si es la ruta con la menor distancia y tiempo de vuelo
                if distancia_total < distancia_minima or (distancia_total == distancia_minima and tiempo_total < tiempo_minimo):
                    distancia_minima = distancia_total
                    tiempo_minimo = tiempo_total
                    rutas_mejores = [ruta]
                elif distancia_total == distancia_minima and tiempo_total == tiempo_minimo:
                    rutas_mejores.append(ruta)

            print(f"\nMejor(s) ruta(s) entre {origen} y {destino}:")

            for mejor_ruta in rutas_mejores:
                print(f"Mejor Ruta: {mejor_ruta} - Distancia total: {distancia_minima} km - Tiempo total de vuelo: {tiempo_minimo} horas")

            return rutas_mejores[0]
        else:
            return None
    def obtener_distancia_entre_aeropuertos(self, origen, destino):
    # Buscar la ruta que conecta origen y destino
        ruta = next((ruta for ruta in self.rutas if ruta.origen.codigo == origen and ruta.destino.codigo == destino), None)

        if ruta:
            return ruta.distancia
        else:
            return None
    
    def obtener_tiempo_entre_aeropuertos(self, origen, destino):
    # Buscar la ruta que conecta origen y destino
        ruta = next((ruta for ruta in self.rutas if ruta.origen.codigo == origen and ruta.destino.codigo == destino), None)

        if ruta:
            return ruta.tiempo_vuelo
        else:
            return None

    def guardar_aeropuertos(self, filename="aeropuertos.json"):
        with open(filename, 'w') as file:
            aeropuertos_data = [{"codigo": a.codigo, "nombre": a.nombre, "ubicacion": a.ubicacion} for a in self.aeropuertos]
            json.dump(aeropuertos_data, file)

    def guardar_rutas(self, filename="rutas.json"):
        with open(filename, 'w') as file:
            rutas_data = [{"origen": r.origen.codigo, "destino": r.destino.codigo, "distancia": r.distancia, "tiempo_vuelo": r.tiempo_vuelo} for r in self.rutas]
            json.dump(rutas_data, file)

    def cargar_aeropuertos(self, filename="aeropuertos.json"):
        try:
            with open(filename, 'r') as file:
                aeropuertos_data = json.load(file)
                self.aeropuertos = [Aeropuerto(a['codigo'], a['nombre'], a['ubicacion']) for a in aeropuertos_data]
        except FileNotFoundError:
            print(f"El archivo {filename} no existe. Se creará uno nuevo al guardar datos.")

    def cargar_rutas(self, filename="rutas.json"):
        try:
            with open(filename, 'r') as file:
                rutas_data = json.load(file)
                self.rutas = [Ruta(self.buscar_aeropuerto_por_codigo(r['origen']), self.buscar_aeropuerto_por_codigo(r['destino']), r['distancia'], r['tiempo_vuelo']) for r in rutas_data]
        except FileNotFoundError:
            print(f"El archivo {filename} no existe. Se creará uno nuevo al guardar datos.")

    def buscar_aeropuerto_por_codigo(self, codigo):
        for aeropuerto in self.aeropuertos:
            if aeropuerto.codigo == codigo:
                return aeropuerto
        return None

    def modificar_aeropuerto(self, codigo, nuevo_nombre, nueva_ubicacion):
        aeropuerto = self.buscar_aeropuerto_por_codigo(codigo)

        if aeropuerto:
            aeropuerto.nombre = nuevo_nombre
            aeropuerto.ubicacion = nueva_ubicacion
            print(f"Aeropuerto {codigo} modificado correctamente.")
            self.guardar_aeropuertos()  # Guardar cambios en el archivo
            self.actualizar_grafo()  # Actualizar el grafo con los cambios
        else:
            print(f"Aeropuerto {codigo} no encontrado.")

    def modificar_ruta(self, codigo_origen, codigo_destino, nueva_distancia, nuevo_tiempo_vuelo):
        # Buscar la ruta que conecta los aeropuertos de origen y destino
        ruta = next((ruta for ruta in self.rutas if ruta.origen.codigo == codigo_origen and ruta.destino.codigo == codigo_destino), None)

        if ruta:
            # Modificar la distancia de la ruta
            ruta.distancia = nueva_distancia
            ruta.tiempo_vuelo = nuevo_tiempo_vuelo
            print(f"Ruta modificada correctamente. Nueva distancia: {nueva_distancia} km. Nuevo tiempo: {nuevo_tiempo_vuelo} Hrs")
            self.actualizar_grafo()
            self.guardar_rutas()  # Guardar cambios en el archivo JSON de rutas
        else:
            print("Ruta no encontrada.")