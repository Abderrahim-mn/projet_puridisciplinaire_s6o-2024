import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vehicle Robot Controller")

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

        # Créer le QStackedWidget et ajouter des pages
        self.stacked_widget = QWidget()
        self.stacked_widget.setLayout(QVBoxLayout())
        self.stacked_widget.layout().addWidget(self.create_dashboard_page())

        # Créer les boutons de navigation
        nav_widget = QWidget()
        nav_layout = QVBoxLayout()
        nav_widget.setLayout(nav_layout)
        nav_widget.setObjectName("nav_widget")

        dashboard_button = QPushButton("Dashboard")
        dashboard_button.setIcon(QIcon("icons\\dashboard.png"))
        dashboard_button.clicked.connect(lambda: self.show_dashboard())
        nav_layout.addWidget(dashboard_button)

        control_button = QPushButton("Control")
        control_button.setIcon(QIcon("icons\\control.png"))
        control_button.clicked.connect(lambda: self.run_script("Control.py"))
        nav_layout.addWidget(control_button)

        gesture_button = QPushButton("Gesture Detector")
        gesture_button.setIcon(QIcon("icons/gesture.png"))
        gesture_button.clicked.connect(lambda: self.run_script("gestureDetector.py"))
        nav_layout.addWidget(gesture_button)

        line_button = QPushButton("Line Detect")
        line_button.setIcon(QIcon("icons/line.png"))
        line_button.clicked.connect(lambda: self.run_script("LineDetector.py"))
        nav_layout.addWidget(line_button)

        velocity_button = QPushButton("Velocity Control")
        velocity_button.setIcon(QIcon("icons/velocity.png"))
        velocity_button.clicked.connect(lambda: self.run_script("velocityControl.py"))
        nav_layout.addWidget(velocity_button)

        trajectory_button = QPushButton("trajectory Control")
        trajectory_button.setIcon(QIcon("icons/trajectory.png"))
        trajectory_button.clicked.connect(lambda: self.run_script("drawTrajectory.py"))
        nav_layout.addWidget(trajectory_button)

        Graphe_button = QPushButton("Graphe Control")
        Graphe_button.setIcon(QIcon("icons/graph.png"))
        Graphe_button.clicked.connect(lambda: self.run_script("Graphes.py"))
        nav_layout.addWidget(Graphe_button)


        # Ajouter un espaceur flexible pour pousser le bouton Exit vers le bas
        nav_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        exit_button = QPushButton("Exit")
        exit_button.setIcon(QIcon("icons/exit.png"))
        exit_button.clicked.connect(self.close)
        exit_button.setObjectName("exit_button")
        nav_layout.addWidget(exit_button)

        # Configurer le layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(nav_widget)
        main_layout.addWidget(self.stacked_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Appliquer des styles
        self.setStyleSheet("""
            QWidget {
                background-color: #fffaf0;
                font-family: 'Segoe UI', sans-serif;
            }
            #nav_widget {
                background-color:  #a93226 ;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                margin: 5px 0;
                text-align: left;
                transition: background-color 0.3s ease, transform 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
                transform: scale(0.95);
            }
            QPushButton#exit_button {
                background-color: transparent;
                color: white;
            }
            QPushButton#exit_button:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QPushButton#exit_button:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QLabel {
                color: #333;
                padding: 20px;
                font-size: 18px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel h1 {
                font-size: 28px;
                color: #2e6da4;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel p {
                margin: 10px 0;
                font-size: 20px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel ul {
                margin: 10px 20px;
                font-size: 18px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel li {
                margin: 5px 0;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Ajouter le texte
        text_label = QLabel("""
          
            <p>This is your main interface to control and monitor the vehicle robot.</p>
            <p>Features:</p>
            <ul>
                <li>Remote Control</li>
                <li>Line Detection</li>
                <li>Gesture Control</li>
                <li>Speed Monitoring</li>
            </ul>
            <p>Use the navigation menu on the left to select a feature.</p>
            <p>We hope you have a great experience!</p>
        """)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

        # Ajouter un espaceur pour pousser l'image vers le bas
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Ajouter l'image du robot
        self.image_label = QLabel()
        pixmap = QPixmap("icons/vehicle_robot.png")  # Assurez-vous que l'image est dans le dossier icons
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        layout.setAlignment(Qt.AlignCenter)
        page.setLayout(layout)

        

        return page

    def show_dashboard(self):
        self.stacked_widget.layout().setCurrentIndex(0)

    def run_script(self, script_name):
        self.process = QProcess(self)
        self.process.start("python", [script_name])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
