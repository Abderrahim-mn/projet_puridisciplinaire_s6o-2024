import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from Moves import Move

class SerialReader(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ser = serial.Serial('COM3', 115200)

    def run(self):
        while True:
            data = self.ser.readline().decode().strip()
            if data:
                self.data_received.emit(data)

class GestureDetector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
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
        self.setWindowTitle('Détection de geste')

        # Créer le widget central
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Créer la mise en page principale
        main_layout = QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(10)

        # Créer le conteneur pour le titre
        title_container = QWidget(self.centralwidget)
        title_layout = QHBoxLayout(title_container)
        title_layout.setAlignment(Qt.AlignLeft)

        # Ajouter l'icône de contrôle
        control_icon = QLabel(title_container)
        pixmap = QPixmap('icons/gesture.png')  # Changez le chemin vers votre icône
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        control_icon.setPixmap(pixmap)
        control_icon.setStyleSheet("margin-right: 10px;")

        # Ajouter le texte du titre
        title_label = QLabel("Détection de geste", title_container)
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

        # Créer un espaceur flexible au-dessus des boutons
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Créer le bouton Stop
        self.btn_stop = QPushButton('Stop', self.centralwidget)
        self.btn_stop.setObjectName('btn_stop')
        self.btn_stop.setIcon(QIcon('icons/stop.png'))  # Changez le chemin vers votre icône
        self.btn_stop.setIconSize(QSize(40, 40))
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
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
                background-color: #1E88E5;
                box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background-color: #1976D2;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        self.btn_stop.clicked.connect(Move.stop)
        main_layout.addWidget(self.btn_stop, alignment=Qt.AlignCenter)

        # Ajouter un bouton Exit
        exit_button = QPushButton("Exit", self.centralwidget)
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

        # Configurer le widget central avec la mise en page principale
        self.centralwidget.setLayout(main_layout)
        self.setCentralWidget(self.centralwidget)

        # Thread pour lire les données série
        self.serial_reader = SerialReader()
        self.serial_reader.data_received.connect(self.handle_movement)
        self.serial_reader.start()

    def handle_movement(self, data):
        # Fonction à exécuter lorsque le mouvement est détecté
        if data == 'Up':
            Move.avancer()
            print("Avancer")
        elif data == 'Down':
            Move.reculer()
            print("Reculer")
        elif data == 'Left':
            Move.avant_gauche()
            print("Avant gauche")
        elif data == 'Right':
            Move.avant_droite()
            print("Avant Droit")
        elif data == 'Forward':
            Move.stop()
            print("Stop")
        elif data == 'Backward':
            Move.avancer()
            print("Avancer")

    def closeEvent(self, event):
        # Fermer la connexion série lorsque la fenêtre est fermée
        self.serial_reader.ser.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    move_controller = GestureDetector()
    move_controller.show()
    sys.exit(app.exec_())
