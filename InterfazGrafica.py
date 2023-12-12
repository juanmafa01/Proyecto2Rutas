import tkinter as tk
from tkinter import simpledialog
from Aeropuerto import Aeropuerto
from Ruta import Ruta
from Grafo import Grafo
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazGrafica:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Rutas Aéreas")
        self.grafo_rutas = Grafo()

        # Frame principal
        self.frame_principal = tk.Frame(self.master)
        self.frame_principal.pack()

        # Frame para la visualización gráfica del grafo
        self.frame_grafo = tk.Frame(self.frame_principal)
        self.frame_grafo.pack(side=tk.LEFT, padx=10, pady=10)

        # Frame para mostrar la mejor ruta
        self.frame_mejor_ruta = tk.Frame(self.frame_principal)
        self.frame_mejor_ruta.pack(side=tk.LEFT, padx=10, pady=10)


        # Botones para acciones
        self.btn_registrar_aeropuerto = tk.Button(self.master, text="Registrar Aeropuerto", command=self.solicitar_datos_aeropuerto)
        self.btn_registrar_aeropuerto.pack(side=tk.LEFT, padx=5)

        self.btn_registrar_ruta = tk.Button(self.master, text="Registrar Ruta", command=self.solicitar_datos_ruta)
        self.btn_registrar_ruta.pack(side=tk.LEFT, padx=5)


        self.btn_visualizar_rutas = tk.Button(self.master, text="Visualizar Rutas", command=self.visualizar_rutas_graficas)
        self.btn_visualizar_rutas.pack(side=tk.LEFT, padx=5)

        self.btn_buscar_mejor_ruta = tk.Button(self.master, text="Buscar Mejor Ruta", command=self.buscar_y_mostrar_mejor_ruta)
        self.btn_buscar_mejor_ruta.pack(side=tk.LEFT, padx=5)
        
        self.btn_modificar_aeropuerto = tk.Button(self.master, text="Modificar Aeropuerto", command=self.solicitar_modificar_aeropuerto)
        self.btn_modificar_aeropuerto.pack(side=tk.LEFT, padx=5)
        
        self.btn_modificar_ruta = tk.Button(self.master, text="Modificar Ruta", command=self.modificar_ruta)
        self.btn_modificar_ruta.pack(side=tk.LEFT, padx=5)
                

    def solicitar_datos_aeropuerto(self):
        # Crear un nuevo formulario para el aeropuerto
        formulario = tk.Toplevel(self.master)
        formulario.title("Registro de Aeropuerto")

        # Etiquetas y cuadros de entrada para el formulario
        tk.Label(formulario, text="Código del Aeropuerto:").grid(row=0, column=0, padx=10, pady=5)
        codigo_var = tk.StringVar()
        tk.Entry(formulario, textvariable=codigo_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Nombre del Aeropuerto:").grid(row=1, column=0, padx=10, pady=5)
        nombre_var = tk.StringVar()
        tk.Entry(formulario, textvariable=nombre_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Ubicación del Aeropuerto:").grid(row=2, column=0, padx=10, pady=5)
        ubicacion_var = tk.StringVar()
        tk.Entry(formulario, textvariable=ubicacion_var).grid(row=2, column=1, padx=10, pady=5)

        # Botón para registrar el aeropuerto
        tk.Button(formulario, text="Registrar", command=lambda: self.registrar_aeropuerto(formulario, codigo_var.get(), nombre_var.get(), ubicacion_var.get())).grid(row=3, column=0, columnspan=2, pady=10)

    def registrar_aeropuerto(self, formulario, codigo, nombre, ubicacion):
        # Validar la entrada antes de agregar el aeropuerto
        if codigo and nombre and ubicacion:
            nuevo_aeropuerto = Aeropuerto(codigo, nombre, ubicacion)
            self.grafo_rutas.agregar_aeropuerto(nuevo_aeropuerto)
            formulario.destroy()  # Cerrar el formulario después de registrar el aeropuerto
        else:
            tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")
        
        formulario.destroy() 

    def solicitar_datos_ruta(self):
        # Crear un nuevo formulario para la ruta
        formulario = tk.Toplevel(self.master)
        formulario.title("Registro de Ruta")

        # Etiquetas y cuadros de entrada para el formulario
        tk.Label(formulario, text="Aeropuerto de Origen:").grid(row=0, column=0, padx=10, pady=5)
        origen_var = tk.StringVar()
        tk.Entry(formulario, textvariable=origen_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Aeropuerto de Destino:").grid(row=1, column=0, padx=10, pady=5)
        destino_var = tk.StringVar()
        tk.Entry(formulario, textvariable=destino_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Distancia de la Ruta (en kilómetros):").grid(row=2, column=0, padx=10, pady=5)
        distancia_var = tk.StringVar()
        tk.Entry(formulario, textvariable=distancia_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Tiempo de Vuelo (en horas):").grid(row=3, column=0, padx=10, pady=5)
        tiempo_vuelo_var = tk.StringVar()
        tk.Entry(formulario, textvariable=tiempo_vuelo_var).grid(row=3, column=1, padx=10, pady=5)

        # Botón para registrar la ruta
        tk.Button(formulario, text="Registrar", command=lambda: self.registrar_ruta(formulario, origen_var.get(), destino_var.get(), distancia_var.get(), tiempo_vuelo_var.get())).grid(row=4, column=0, columnspan=2, pady=10)

    def registrar_ruta(self, formulario, origen, destino, distancia, tiempo_vuelo):
        # Validar la entrada antes de agregar la ruta
        if origen and destino and distancia and tiempo_vuelo:
            # Buscar los aeropuertos en el grafo
            aeropuerto_origen = next((a for a in self.grafo_rutas.aeropuertos if a.codigo == origen), None)
            aeropuerto_destino = next((a for a in self.grafo_rutas.aeropuertos if a.codigo == destino), None)

            if aeropuerto_origen and aeropuerto_destino:
                nueva_ruta = Ruta(aeropuerto_origen, aeropuerto_destino, float(distancia), float(tiempo_vuelo))
                self.grafo_rutas.agregar_ruta(nueva_ruta)
                formulario.destroy()  # Cerrar el formulario después de registrar la ruta
            else:
                tk.messagebox.showerror("Error", "Aeropuertos de origen o destino no encontrados.")
        else:
            tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")
        
        formulario.destroy() 



    def visualizar_rutas_graficas(self):
        # Limpiar el frame_grafo antes de agregar la nueva visualización del grafo
        for widget in self.frame_grafo.winfo_children():
            widget.destroy()

        G = nx.DiGraph()

        # Agregar nodos al grafo
        for aeropuerto in self.grafo_rutas.aeropuertos:
            G.add_node(aeropuerto.codigo, label=f"{aeropuerto.codigo}\n{aeropuerto.ubicacion}")

        # Agregar aristas al grafo
        for ruta in self.grafo_rutas.rutas:
            G.add_edge(ruta.origen.codigo, ruta.destino.codigo, label=f"{ruta.distancia} Km\n {ruta.tiempo_vuelo} Hrs")

        # Mostrar la visualización en el frame_grafo
        pos = nx.circular_layout(G)
        labels = nx.get_edge_attributes(G, 'label')
        # Obtener las etiquetas de los nodos
        node_labels = {node: G.nodes[node]['label'] for node in G.nodes}

        # Dibujar el grafo
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=8, font_color='black', labels=node_labels)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Crear la visualización del grafo
        figure_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame_grafo)
        figure_canvas.get_tk_widget().pack()

        plt.show()
        

    def buscar_y_mostrar_mejor_ruta(self):
        # Crear un nuevo formulario para la búsqueda de la mejor ruta
        formulario = tk.Toplevel(self.master)
        formulario.title("Búsqueda de la Mejor Ruta")

        # Etiquetas y cuadros de entrada para el formulario
        tk.Label(formulario, text="Aeropuerto de Origen:").grid(row=0, column=0, padx=10, pady=5)
        origen_var = tk.StringVar()
        tk.Entry(formulario, textvariable=origen_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Aeropuerto de Destino:").grid(row=1, column=0, padx=10, pady=5)
        destino_var = tk.StringVar()
        tk.Entry(formulario, textvariable=destino_var).grid(row=1, column=1, padx=10, pady=5)

        # Botón para realizar la búsqueda de la mejor ruta
        tk.Button(formulario, text="Buscar Mejor Ruta", command=lambda: self.mostrar_mejor_ruta(formulario, origen_var.get(), destino_var.get())).grid(row=2, column=0, columnspan=2, pady=10)

    def mostrar_mejor_ruta(self, formulario, origen, destino):
        # Limpiar el frame_mejor_ruta antes de mostrar la mejor ruta
        for widget in self.frame_mejor_ruta.winfo_children():
            widget.destroy()

        # Realizar la búsqueda de la mejor ruta
        mejor_ruta = self.grafo_rutas.buscar_mejor_ruta(origen, destino)

        # Mostrar la mejor ruta encontrada en el frame_mejor_ruta
        if mejor_ruta:
            tk.Label(self.frame_mejor_ruta, text=f"Mejor ruta entre {origen} y {destino}: {mejor_ruta}").pack()
            # Dibujar la mejor ruta
            self.dibujar_ruta_individual(mejor_ruta, self.frame_mejor_ruta)
        else:
            tk.Label(self.frame_mejor_ruta, text="No se encontró una mejor ruta.").pack()

        formulario.destroy()  # Cerrar el formulario después de mostrar la mejor ruta

    
    
    def dibujar_ruta_individual(self, ruta, frame):
        # Limpiar el frame antes de agregar la nueva ruta
        for widget in frame.winfo_children():
            widget.destroy()

        G = nx.DiGraph()

        # Agregar nodos al grafo
        for aeropuerto in self.grafo_rutas.aeropuertos:
            G.add_node(aeropuerto.codigo, label=f"{aeropuerto.codigo}\n{aeropuerto.ubicacion}")

        # Crear el grafo sin aristas
        pos = nx.spring_layout(G)

        # Agregar nodos al grafo
        for aeropuerto in self.grafo_rutas.aeropuertos:
            G.add_node(aeropuerto.codigo, label=f"{aeropuerto.codigo}\n{aeropuerto.ubicacion}")

        # Agregar aristas de la ruta al grafo
        for i in range(len(ruta) - 1):
            origen = ruta[i]
            destino = ruta[i + 1]
            distancia = self.grafo_rutas.obtener_distancia_entre_aeropuertos(origen, destino)
            tiempo_vuelo = self.grafo_rutas.obtener_tiempo_entre_aeropuertos(origen,destino) 
            G.add_edge(origen, destino, label=f"{distancia} Km\n {tiempo_vuelo} Hrs")

        pos = nx.circular_layout(G)
        labels = nx.get_edge_attributes(G, 'label')
        # Obtener las etiquetas de los nodos
        node_labels = {node: G.nodes[node]['label'] for node in G.nodes}

        # Dibujar el grafo
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=8, font_color='black', labels=node_labels)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)


        # Crear la visualización del grafo
        figure_canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
        figure_canvas.get_tk_widget().pack()
        plt.show()
        
        
    # Agregar este método a la clase InterfazGrafica
    def solicitar_modificar_aeropuerto(self):
        # Crear un nuevo formulario para modificar el aeropuerto
        formulario = tk.Toplevel(self.master)
        formulario.title("Modificar Aeropuerto")

        # Etiqueta y cuadro de entrada para el código del aeropuerto a modificar
        tk.Label(formulario, text="Código del Aeropuerto a Modificar:").grid(row=0, column=0, padx=10, pady=5)
        codigo_var = tk.StringVar()
        tk.Entry(formulario, textvariable=codigo_var).grid(row=0, column=1, padx=10, pady=5)

        # Etiquetas y cuadros de entrada para los nuevos datos del aeropuerto
        tk.Label(formulario, text="Nuevo Nombre del Aeropuerto:").grid(row=1, column=0, padx=10, pady=5)
        nuevo_nombre_var = tk.StringVar()
        tk.Entry(formulario, textvariable=nuevo_nombre_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Nueva Ubicación del Aeropuerto:").grid(row=2, column=0, padx=10, pady=5)
        nueva_ubicacion_var = tk.StringVar()
        tk.Entry(formulario, textvariable=nueva_ubicacion_var).grid(row=2, column=1, padx=10, pady=5)

        # Botón para modificar el aeropuerto
        tk.Button(formulario, text="Modificar", command=lambda: self.modificar_aeropuerto(formulario, codigo_var.get(), nuevo_nombre_var.get(), nueva_ubicacion_var.get())).grid(row=3, column=0, columnspan=2, pady=10)

    def modificar_aeropuerto(self, formulario, codigo, nuevo_nombre, nueva_ubicacion):
        # Validar la entrada antes de modificar el aeropuerto
        if codigo and nuevo_nombre and nueva_ubicacion:
            self.grafo_rutas.modificar_aeropuerto(codigo, nuevo_nombre, nueva_ubicacion)
            formulario.destroy()  # Cerrar el formulario después de modificar el aeropuerto
        else:
            tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")
            
    def modificar_ruta(self):
        # Crear un nuevo formulario para la modificación de la ruta
        formulario = tk.Toplevel(self.master)
        formulario.title("Modificar Ruta")

        # Etiquetas y cuadros de entrada para el formulario
        tk.Label(formulario, text="Código del Aeropuerto de Origen:").grid(row=0, column=0, padx=10, pady=5)
        codigo_origen_var = tk.StringVar()
        tk.Entry(formulario, textvariable=codigo_origen_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Código del Aeropuerto de Destino:").grid(row=1, column=0, padx=10, pady=5)
        codigo_destino_var = tk.StringVar()
        tk.Entry(formulario, textvariable=codigo_destino_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(formulario, text="Nueva Distancia de la Ruta (en kilómetros):").grid(row=2, column=0, padx=10, pady=5)
        nueva_distancia_var = tk.StringVar()
        tk.Entry(formulario, textvariable=nueva_distancia_var).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(formulario, text="Nuevo tiempo de la ruta (en Horas):").grid(row=3, column=0, padx=10, pady=5)
        nuevo_tiempo_vuelo_var = tk.StringVar()
        tk.Entry(formulario, textvariable=nuevo_tiempo_vuelo_var).grid(row=3, column=1, padx=10, pady=5)

        # Botón para modificar la ruta
        tk.Button(formulario, text="Modificar Ruta", command=lambda: self.modificar_ruta_accion(formulario, codigo_origen_var.get(), codigo_destino_var.get(), nueva_distancia_var.get(), nuevo_tiempo_vuelo_var.get())).grid(row=4, column=0, columnspan=2, pady=10)

    def modificar_ruta_accion(self, formulario, codigo_origen, codigo_destino, nueva_distancia, nuevo_tiempo_vuelo):
        # Validar la entrada antes de modificar la ruta
        if codigo_origen and codigo_destino and nueva_distancia and nuevo_tiempo_vuelo:
            # Modificar la ruta utilizando el método en la clase Grafo
            self.grafo_rutas.modificar_ruta(codigo_origen, codigo_destino, float(nueva_distancia), float(nuevo_tiempo_vuelo))
            formulario.destroy()  # Cerrar el formulario después de modificar la ruta
        else:
            tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")
            
    def cerrar_aplicacion(self):
        self.grafo_rutas.guardar_aeropuertos()
        self.grafo_rutas.guardar_rutas()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafica(root)
    root.protocol("WM_DELETE_WINDOW", app.cerrar_aplicacion)
    root.mainloop()

    