import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.*;
import java.util.List;
import javax.swing.*;
import javax.swing.tree.*;

public class SerieMundialArbol extends JFrame {
    private JTree arbol;
    private DefaultMutableTreeNode raiz;
    private JTextArea estadisticas;
    private int totalSecuencias = 0;
    
    public SerieMundialArbol() {

        setTitle("Serie Mundial - Diagrama de Árbol");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
        
        crearArbol();
        
        crearInterfaz();
        
        setSize(1000, 700);
        setLocationRelativeTo(null);
    }
    
    private void crearArbol() {
        raiz = new DefaultMutableTreeNode("🏆 SERIE MUNDIAL (Primer equipo en ganar 4 juegos)");
        generarArbolRecursivo(raiz, "", 0, 0, 1);
        arbol = new JTree(raiz);
        
        arbol.setFont(new Font("Monospaced", Font.PLAIN, 12));
        arbol.setRowHeight(20);
        
        for (int i = 0; i < 3; i++) {
            arbol.expandRow(i);
        }
    }
    
    private void generarArbolRecursivo(DefaultMutableTreeNode nodoActual, String secuencia, int victoriasA, int victoriasB, int juego) {

        // Caso base: algún equipo ya ganó 4 juegos
        if (victoriasA == 4) {
            String resultado = String.format("🎉 EQUIPO A GANA (%s) - %d juegos", formatearSecuencia(secuencia), juego - 1);
            nodoActual.add(new DefaultMutableTreeNode(resultado));
            totalSecuencias++;
            return;
        }

        if (victoriasB == 4) {
            String resultado = String.format("🎉 EQUIPO B GANA (%s) - %d juegos", formatearSecuencia(secuencia), juego - 1);
            nodoActual.add(new DefaultMutableTreeNode(resultado));
            totalSecuencias++;
            return;
        }
        
        // Crear nodos para las dos posibilidades
        String infoJuego = String.format("Juego %d (A:%d-B:%d)", juego, victoriasA, victoriasB);
        
        // Equipo A gana este juego
        DefaultMutableTreeNode nodoA = new DefaultMutableTreeNode(String.format("⚾ %s → A gana", infoJuego));
        nodoActual.add(nodoA);
        generarArbolRecursivo(nodoA, secuencia + "A", victoriasA + 1, victoriasB, juego + 1);
        
        // Equipo B gana este juego
        DefaultMutableTreeNode nodoB = new DefaultMutableTreeNode(String.format("⚾ %s → B gana", infoJuego));
        nodoActual.add(nodoB);
        generarArbolRecursivo(nodoB, secuencia + "B", victoriasA, victoriasB + 1, juego + 1);
    }
    
    private void crearInterfaz() {

        // Panel principal con el árbol
        JScrollPane scrollArbol = new JScrollPane(arbol);
        scrollArbol.setPreferredSize(new Dimension(600, 500));
        
        // Panel de estadísticas
        estadisticas = new JTextArea();
        estadisticas.setFont(new Font("Monospaced", Font.PLAIN, 11));
        estadisticas.setEditable(false);
        estadisticas.setBackground(new Color(240, 248, 255));
        actualizarEstadisticas();
        
        JScrollPane scrollEstadisticas = new JScrollPane(estadisticas);
        scrollEstadisticas.setPreferredSize(new Dimension(350, 500));
        

        JPanel panelBotones = new JPanel(new FlowLayout());
        
        JButton btnExpandir = new JButton("🔍 Expandir Todo");
        btnExpandir.addActionListener(e -> expandirTodo());
        
        JButton btnContraer = new JButton("📁 Contraer Todo");
        btnContraer.addActionListener(e -> contraerTodo());
        
        JButton btnMostrarSecuencias = new JButton("📋 Ver Todas las Secuencias");
        btnMostrarSecuencias.addActionListener(e -> mostrarTodasLasSecuencias());
        
        JButton btnAyuda = new JButton("❓ Ayuda");
        btnAyuda.addActionListener(e -> mostrarAyuda());
        
        panelBotones.add(btnExpandir);
        panelBotones.add(btnContraer);
        panelBotones.add(btnMostrarSecuencias);
        panelBotones.add(btnAyuda);
        
        // Organizar componentes
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, scrollArbol, scrollEstadisticas);
        splitPane.setDividerLocation(600);
        
        add(splitPane, BorderLayout.CENTER);
        add(panelBotones, BorderLayout.SOUTH);
        
        // Panel de título
        JLabel titulo = new JLabel("🏆 SERIE MUNDIAL - DIAGRAMA DE ÁRBOL", SwingConstants.CENTER);
        titulo.setFont(new Font("Arial", Font.BOLD, 16));
        titulo.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        add(titulo, BorderLayout.NORTH);
    }
    
    private void actualizarEstadisticas() {
        StringBuilder sb = new StringBuilder();
        sb.append("📊 ESTADÍSTICAS DE LA SERIE MUNDIAL\n");
        sb.append("═".repeat(35)).append("\n\n");
        
        sb.append("🎯 REGLAS:\n");
        sb.append("• Primer equipo en ganar 4 juegos es campeón\n");
        sb.append("• Mínimo: 4 juegos (4-0)\n");
        sb.append("• Máximo: 7 juegos (4-3)\n\n");
        
        sb.append("📈 RESULTADOS:\n");
        sb.append("• Total de formas posibles: ").append(totalSecuencias).append("\n");
        sb.append("• Cada equipo puede ganar: ").append(totalSecuencias/2).append(" formas\n\n");
        
        sb.append("🎲 DISTRIBUCIÓN POR DURACIÓN:\n");
        sb.append("• 4 juegos: 2 formas (2.9%)\n");
        sb.append("• 5 juegos: 8 formas (11.4%)\n");
        sb.append("• 6 juegos: 20 formas (28.6%)\n");
        sb.append("• 7 juegos: 40 formas (57.1%)\n\n");
        
        sb.append("🔍 NAVEGACIÓN:\n");
        sb.append("• Haz clic en los nodos para expandir\n");
        sb.append("• Usa los botones para expandir/contraer\n");
        sb.append("• Los 🎉 indican finales del torneo\n\n");
        
        sb.append("📝 LEYENDA:\n");
        sb.append("• A = Equipo A gana el juego\n");
        sb.append("• B = Equipo B gana el juego\n");
        sb.append("• (A:X-B:Y) = Victorias actuales\n");
        
        estadisticas.setText(sb.toString());
    }
    
    private void expandirTodo() {
        for (int i = 0; i < arbol.getRowCount(); i++) {
            arbol.expandRow(i);
        }
    }
    
    private void contraerTodo() {
        for (int i = arbol.getRowCount() - 1; i >= 0; i--) {
            arbol.collapseRow(i);
        }
    }
    
    private void mostrarTodasLasSecuencias() {
        java.util.List<String> secuencias = new ArrayList<>();
        recopilarSecuencias(raiz, "", secuencias);
        
        StringBuilder sb = new StringBuilder();
        sb.append("TODAS LAS SECUENCIAS POSIBLES DE LA SERIE MUNDIAL\n");
        sb.append("═".repeat(50)).append("\n\n");
        
        Map<Integer, java.util.List<String>> porDuracion = new TreeMap<>();
        
        for (String secuencia : secuencias) {
            String[] partes = secuencia.split(" - ");
            int duracion = Integer.parseInt(partes[1].split(" ")[0]);
            porDuracion.computeIfAbsent(duracion, k -> new ArrayList<>()).add(secuencia);
        }
        
        for (Map.Entry<Integer, java.util.List<String>> entrada : porDuracion.entrySet()) {
            int duracion = entrada.getKey();
            java.util.List<String> lista = entrada.getValue();
            
            sb.append(String.format("🏆 TORNEOS DE %d JUEGOS (%d formas):\n", duracion, lista.size()));
            sb.append("─".repeat(40)).append("\n");
            
            for (int i = 0; i < lista.size(); i++) {
                sb.append(String.format("%2d. %s\n", i + 1, lista.get(i)));
            }
            sb.append("\n");
        }
        
        JTextArea textArea = new JTextArea(sb.toString());
        textArea.setFont(new Font("Monospaced", Font.PLAIN, 11));
        textArea.setEditable(false);
        
        JScrollPane scrollPane = new JScrollPane(textArea);
        scrollPane.setPreferredSize(new Dimension(600, 500));
        
        JOptionPane.showMessageDialog(this, scrollPane, "Todas las Secuencias Posibles", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void recopilarSecuencias(DefaultMutableTreeNode nodo, String secuenciaActual, 
                                   java.util.List<String> secuencias) {
        String nodoTexto = nodo.toString();
        
        if (nodoTexto.contains("🎉")) {
            // Es un nodo final
            String ganador = nodoTexto.contains("EQUIPO A") ? "Equipo A" : "Equipo B";
            String secuencia = nodoTexto.substring(nodoTexto.indexOf("(") + 1, nodoTexto.indexOf(")"));
            String duracion = nodoTexto.substring(nodoTexto.lastIndexOf("-") + 2);
            secuencias.add(secuencia + " → " + ganador + " - " + duracion);

        } else {
    
            for (int i = 0; i < nodo.getChildCount(); i++) {
                DefaultMutableTreeNode hijo = (DefaultMutableTreeNode) nodo.getChildAt(i);
                recopilarSecuencias(hijo, secuenciaActual, secuencias);
            }
        }
    }
    
    private void mostrarAyuda() {
        String ayuda = """
            🏆 SERIE MUNDIAL - AYUDA
            ═══════════════════════════════════
            
            📖 CÓMO USAR:
            • El árbol muestra todas las formas posibles de terminar la Serie Mundial
            • Cada nodo representa un juego y su resultado
            • Los nodos 🎉 muestran el final del torneo
            
            🎯 REGLAS:
            • Primer equipo en ganar 4 juegos es el campeón
            • El torneo puede durar entre 4 y 7 juegos
            
            🔍 NAVEGACIÓN:
            • Clic en los nodos para expandir/contraer
            • Usa los botones para expandir/contraer todo
            • El panel derecho muestra estadísticas
            
            📊 INTERPRETACIÓN:
            • (A:X-B:Y) = Victorias actuales de cada equipo
            • A/B = Equipo que gana ese juego específico
            • Total: 70 formas posibles de terminar
            """;
        
        JOptionPane.showMessageDialog(this, ayuda, "Ayuda", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private String formatearSecuencia(String secuencia) {

        if (secuencia.isEmpty()) return "";

        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < secuencia.length(); i++) {
            if (i > 0) sb.append("-");
            sb.append(secuencia.charAt(i));
        }

        return sb.toString();
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {

            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());

            } catch (Exception e) {

                e.printStackTrace();
            }
            
            new SerieMundialArbol().setVisible(true);
        });
    }
}