import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

# A = 0, B = 1 para posicionamiento binario
def seq_to_int(seq):
    v = 0
    for ch in seq:
        v = (v << 1) | (0 if ch == 'A' else 1)
    return v

def compute_wins(seq):
    a = seq.count('A')
    b = seq.count('B')
    return a, b

def is_terminal(seq):
    a, b = compute_wins(seq)
    return a == 4 or b == 4

def winner_color(seq):
    a, b = compute_wins(seq)
    if a == 4:
        return '#69b3ff'  # azul claro A campeón
    if b == 4:
        return '#ff7f7f'  # rojo claro B campeón
    return '#8fd18f'      # verde en progreso

def label_for(seq):
    a, b = compute_wins(seq)
    if a == 0 and b == 0 and len(seq) == 0:
        return "Inicio\n0-0"
    if a == 4:
        return f"Gana A\n{seq}\n({a}-{b})"
    if b == 4:
        return f"Gana B\n{seq}\n({a}-{b})"
    return f"{seq if seq else '·'}\n({a}-{b})"

class InteractiveWorldSeriesTree:
    def __init__(self, max_level=7):
        self.max_level = max_level
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.ax.set_title("Serie Mundial - Árbol interactivo (clic para expandir)")
        self.ax.set_axis_off()
        self.ax.set_xlim(-0.05, 1.05)
        self.ax.set_ylim(-0.5, max_level + 0.5)

        # Estructuras
        # nodes: seq -> dict(x, y, artist, expanded)
        self.nodes = {}
        # edges: (parent_seq, child_seq) -> dict(line_artist)
        self.edges = {}

        # Eventos
        self.cid_pick = self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        # Dibujar raíz
        self.add_node("", level=0)
        self.fig.tight_layout()

    def seq_pos(self, seq):
        level = len(seq)
        if level == 0:
            return 0.5, self.max_level  # centro arriba
        slots = 2 ** level
        idx = seq_to_int(seq)
        # x en (0..1): separa nodos uniformemente según el índice binario
        x = (idx + 1) / (slots + 1)
        y = self.max_level - level
        return x, y

    def add_node(self, seq, level=None):
        if seq in self.nodes:
            return

        x, y = self.seq_pos(seq)
        color = winner_color(seq)

        # Dibuja círculo
        circle = Circle((x, y), 0.025, facecolor=color, edgecolor='#333333', lw=1.0, picker=True)
        self.ax.add_patch(circle)

        # Texto
        text = self.ax.text(x, y - 0.11, label_for(seq),
                            ha='center', va='top', fontsize=8, family='monospace')

        self.nodes[seq] = {
            'x': x, 'y': y, 'artist': circle, 'label': text, 'expanded': False
        }

    def add_edge(self, parent_seq, child_seq):
        key = (parent_seq, child_seq)
        if key in self.edges:
            return
        x1, y1 = self.nodes[parent_seq]['x'], self.nodes[parent_seq]['y']
        x2, y2 = self.nodes[child_seq]['x'], self.nodes[child_seq]['y']
        line = Line2D([x1, x2], [y1 - 0.025, y2 + 0.025], color='#9aa0a6', lw=1.2, alpha=0.8)
        self.ax.add_line(line)
        self.edges[key] = {'artist': line}

    def expand_node(self, seq):
        # Si ya expandido o final, no expandir
        if self.nodes[seq]['expanded'] or is_terminal(seq):
            return

        a, b = compute_wins(seq)
        next_game = len(seq) + 1
        # Hijos: A y B si no son finales; si son finales, igual se agregan como hojas
        for outcome in ['A', 'B']:
            child_seq = seq + outcome
            ca, cb = compute_wins(child_seq)
            # No expander hijos de hijos aquí; solo añadir siguiente nivel
            self.add_node(child_seq, level=next_game)
            self.add_edge(seq, child_seq)

        self.nodes[seq]['expanded'] = True
        self.fig.canvas.draw_idle()

    def on_pick(self, event):
        # Identificar si lo clicado es un círculo de nodo
        for seq, data in self.nodes.items():
            if event.artist is data['artist']:
                self.expand_node(seq)
                break

    def clear_tree(self):
        # Eliminar artistas del canvas
        for seq, data in self.nodes.items():
            try:
                data['artist'].remove()
                data['label'].remove()
            except Exception:
                pass
        for key, ed in self.edges.items():
            try:
                ed['artist'].remove()
            except Exception:
                pass
        self.nodes.clear()
        self.edges.clear()
        self.fig.canvas.draw_idle()

    def reset_to_root(self):
        self.clear_tree()
        self.add_node("", level=0)
        self.fig.canvas.draw_idle()

    def on_key(self, event):
        if event.key == 'c':
            # Colapsar todo (volver al inicio)
            self.reset_to_root()
        elif event.key == 'r':
            # Reiniciar vista (igual que 'c' aquí)
            self.reset_to_root()

def main():
    # Nota: asegúrate de usar un backend interactivo (ejecuta como script en escritorio)
    tree = InteractiveWorldSeriesTree(max_level=7)
    print("Instrucciones:")
    print("- Clic en una bolita para expandir sus hijos.")
    print("- 'c' para colapsar todo y volver al inicio.")
    print("- 'r' para reiniciar.")
    plt.show()

if __name__ == "__main__":
    main()