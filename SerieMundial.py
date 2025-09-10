import matplotlib.pyplot as plt
import networkx as nx
import math

def generar_arbol_serie_mundial():
    G = nx.DiGraph()
    contador_nodos = 0
    
    # Función para generar el árbol con todas las secuencias
    def agregar_nodos(equipoA, equipoB, secuencia="", padre=None):
        nonlocal contador_nodos
        
        # Si algún equipo ya tiene 4 victorias, crear nodo final
        if equipoA == 4 or equipoB == 4:
            contador_nodos += 1
            nodo_final = f"final_{contador_nodos}_{equipoA}-{equipoB}_{secuencia}"
            G.add_node(nodo_final, winsA=equipoA, winsB=equipoB, secuencia=secuencia, es_final=True)
            
            if padre:
                G.add_edge(padre, nodo_final)
            return
        
        # Crear identificador único para este nodo (incluye la secuencia)
        contador_nodos += 1
        nodo_actual = f"nodo_{contador_nodos}_{equipoA}-{equipoB}_{secuencia}"
        
        # Agregar nodo actual
        G.add_node(nodo_actual, winsA=equipoA, winsB=equipoB, secuencia=secuencia, es_final=False)
        
        # Conectar con el nodo padre si existe
        if padre:
            G.add_edge(padre, nodo_actual)
        
        # Generar nodos hijos (próximos juegos) - TODAS las secuencias posibles
        agregar_nodos(equipoA + 1, equipoB, secuencia + "A", nodo_actual)  # Gana equipo A
        agregar_nodos(equipoA, equipoB + 1, secuencia + "B", nodo_actual)  # Gana equipo B
    
    # Iniciar desde 0-0
    agregar_nodos(0, 0)
    
    return G

def dibujar_arbol(G):
    # Configurar el tamaño de la figura
    plt.figure(figsize=(25, 20))
    
    # Crear un layout jerárquico basado en niveles
    pos = {}
    
    # Agrupar nodos por nivel (número de juegos jugados)
    niveles = {}
    for node in G.nodes():
        data = G.nodes[node]
        nivel = len(data['secuencia'])
        if nivel not in niveles:
            niveles[nivel] = []
        niveles[nivel].append(node)
    
    # Asignar posiciones
    for nivel, nodos in niveles.items():
        y = 7 - nivel  # Nivel más alto arriba
        num_nodos = len(nodos)
        
        for i, node in enumerate(nodos):
            # Distribuir horizontalmente
            if num_nodos == 1:
                x = 0
            else:
                x = (i - (num_nodos - 1) / 2) * (15 / max(1, num_nodos - 1))
            
            pos[node] = (x, y)
    
    # Dibujar nodos
    node_colors = []
    node_sizes = []
    for node in G.nodes():
        data = G.nodes[node]
        if data['es_final']:
            if data['winsA'] == 4:
                node_colors.append('lightblue')  # Equipo A ganó
            else:
                node_colors.append('lightcoral')  # Equipo B ganó
            node_sizes.append(1500)
        else:
            node_colors.append('lightgreen')  # Juego en progreso
            node_sizes.append(1200)
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    
    # Dibujar bordes
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', 
                          arrowsize=10, edge_color='gray', width=1, alpha=0.6)
    
    # Dibujar etiquetas
    labels = {}
    for node in G.nodes():
        data = G.nodes[node]
        if data['es_final']:
            ganador = "A" if data['winsA'] == 4 else "B"
            labels[node] = f"Gana {ganador}\n{data['secuencia']}\n({data['winsA']}-{data['winsB']})"
        else:
            if data['secuencia'] == "":
                labels[node] = "Inicio\n0-0"
            else:
                labels[node] = f"{data['secuencia']}\n({data['winsA']}-{data['winsB']})"
    
    nx.draw_networkx_labels(G, pos, labels, font_size=6, font_weight='bold')
    
    # Configurar el gráfico
    plt.title('Diagrama Completo de la Serie Mundial - Todas las 70 Secuencias Posibles', 
              fontsize=16, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('serie_mundial_completa.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Contar y mostrar resultados finales
    victorias_A = 0
    victorias_B = 0
    secuencias_A = []
    secuencias_B = []
    
    for node in G.nodes():
        data = G.nodes[node]
        if data['es_final']:
            if data['winsA'] == 4:
                victorias_A += 1
                secuencias_A.append(data['secuencia'])
            elif data['winsB'] == 4:
                victorias_B += 1
                secuencias_B.append(data['secuencia'])
    
    print("="*60)
    print("RESULTADOS DE LA SERIE MUNDIAL")
    print("="*60)
    print(f"Total de formas en que puede terminar la serie: {victorias_A + victorias_B}")
    print(f"Formas en que gana el Equipo A: {victorias_A}")
    print(f"Formas en que gana el Equipo B: {victorias_B}")
    print()
    
    # Agrupar por duración
    duraciones = {}
    for seq in secuencias_A + secuencias_B:
        duracion = len(seq)
        if duracion not in duraciones:
            duraciones[duracion] = []
        ganador = "A" if seq in secuencias_A else "B"
        duraciones[duracion].append((seq, ganador))
    
    print("DISTRIBUCIÓN POR DURACIÓN:")
    print("-" * 30)
    for duracion in sorted(duraciones.keys()):
        secuencias = duraciones[duracion]
        print(f"Torneos de {duracion} juegos: {len(secuencias)} formas")
        for seq, ganador in sorted(secuencias):
            print(f"  {seq} → Gana equipo {ganador}")
        print()
    
    print(f"Imagen guardada como 'serie_mundial_completa.png'")
    print(f"Total de nodos en el grafo: {G.number_of_nodes()}")
    print(f"Total de aristas en el grafo: {G.number_of_edges()}")

# Generar y dibujar el árbol completo
print("Generando árbol completo de la Serie Mundial...")
G = generar_arbol_serie_mundial()
dibujar_arbol(G)