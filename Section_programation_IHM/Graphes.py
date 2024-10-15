import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def plot(self, x, y, title="Graph", xlabel="X-axis", ylabel="Y-axis"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Graphs Interface")  

        # Obtenir la taille de l'écran
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calculer la taille de la fenêtre (moitié de la taille de l'écran)
        window_width = screen_geometry.width() // 2
        window_height = screen_geometry.height() // 2

        # Définir la taille de la fenêtre et la centrer
        self.setGeometry(
            screen_geometry.width() // 2 - window_width // 2,
            screen_geometry.height() // 2 - window_height // 2,
            window_width,
            window_height
        )

        # Créer le widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Créer la mise en page principale
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(10)

        # Créer le conteneur pour le titre
        title_container = QWidget(self.central_widget)
        title_layout = QHBoxLayout(title_container)
        title_layout.setAlignment(Qt.AlignLeft)

        # Ajouter l'icône de contrôle
        control_icon = QLabel(title_container)
        pixmap = QPixmap('icons/graph.png')  # Changez le chemin vers votre icône
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        control_icon.setPixmap(pixmap)
        control_icon.setStyleSheet("margin-right: 10px;")

        # Ajouter le texte du titre
        title_label = QLabel("Graphs Interface", title_container)
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

        # Ajouter l'icône et le texte au layout du titre
        title_layout.addWidget(control_icon)
        title_layout.addWidget(title_label)

        # Appliquer le style à la boîte du titre
        title_container.setStyleSheet("""
            background-color:  #a93226 ;
            border-radius: 10px;
            padding: 10px;
        """)
        title_container.setLayout(title_layout)

        # Ajouter le conteneur de titre à la mise en page principale
        main_layout.addWidget(title_container)

        # Créer les widgets de graphique
        self.graph1 = GraphWidget(self)
        self.graph2 = GraphWidget(self)

        # Générer des données pour les graphiques
        x = 0
        y1 = 0
        y2 = 0

        # Tracer les données dans les graphiques
        self.graph1.plot(x, y1, title="Graphe 1", xlabel="t", ylabel="v")
        self.graph2.plot(x, y2, title="Graphe 2", xlabel="t", ylabel="v")

        # Layouts pour les graphiques
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.graph1)
        graph_layout.addWidget(self.graph2)

        main_layout.addLayout(graph_layout)

        # Créer un espaceur flexible en dessous de la section des graphiques
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Ajouter un bouton Exit
        exit_button = QPushButton("Exit", self.central_widget)
        exit_button.setIcon(QIcon('icons/exit.png'))  # Changez le chemin vers votre icône
        exit_button.setIconSize(QSize(40, 40))
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                margin: 10px;
                transition: all 0.3s ease;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background-color: #c9302c;
                box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background-color: #ac2925;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button, alignment=Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
