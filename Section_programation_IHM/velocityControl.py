import os
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QPixmap
import sys
from Moves import Move
import serial

class VitesseControl(QMainWindow):
    def __init__(self):
        super(VitesseControl, self).__init__()
        self.setWindowTitle("Vitesse CONTROL")  

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
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setSpacing(10)

        # Créer le conteneur pour le titre
        title_container = QWidget(self.central_widget)
        title_layout = QHBoxLayout(title_container)
        title_layout.setAlignment(QtCore.Qt.AlignLeft)

        # Ajouter l'icône de contrôle
        control_icon = QLabel(title_container)
        pixmap = QPixmap('icons/velocity.png')  # Changez le chemin vers votre icône
        pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        control_icon.setPixmap(pixmap)
        control_icon.setStyleSheet("margin-right: 10px;")

        # Ajouter le texte du titre
        title_label = QLabel("Controle De vitesse", title_container)
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

        # Créer un espaceur flexible au-dessus de la section des boutons
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Créer la section des boutons
        button_layout = QHBoxLayout()
        

        self.button_increase = QPushButton()
        self.button_increase.setObjectName("button_increase")
        self.button_increase.setIcon(QIcon('icons/plus.png'))  # Changez le chemin vers votre icône
        self.button_increase.setIconSize(QtCore.QSize(40, 40))
        self.button_increase.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.button_increase.pressed.connect(Move.augmenter)
        self.button_increase.released.connect(Move.avancer)
        button_layout.addWidget(self.button_increase)

        self.button_decrease = QPushButton()
        self.button_decrease.setObjectName("button_decrease")
        self.button_decrease.setIcon(QIcon('icons/moin.png'))  # Changez le chemin vers votre icône
        self.button_decrease.setIconSize(QtCore.QSize(40, 40))
        self.button_decrease.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                border: 2px solid #FF5722;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #F4511E;
            }
        """)
        self.button_decrease.pressed.connect(Move.diminuer)
        self.button_decrease.released.connect(Move.avancer)
        button_layout.addWidget(self.button_decrease)

        # Ajouter le bouton Stop
        self.button_stop = QPushButton()
        self.button_stop.setObjectName("button_stop")
        self.button_stop.setIcon(QIcon('icons/stop_b.png'))  # Changez le chemin vers votre icône
        self.button_stop.setIconSize(QtCore.QSize(40, 40))
        self.button_stop.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border: 2px solid #d9534f;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        self.button_stop.clicked.connect(Move.stop)
        button_layout.addWidget(self.button_stop)

        main_layout.addLayout(button_layout)

        # Créer un espaceur flexible en dessous de la section des boutons
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Ajouter un bouton Exit
        exit_button = QPushButton("Exit", self.central_widget)
        exit_button.setIcon(QIcon('icons/exit.png'))  # Changez le chemin vers votre icône
        exit_button.setIconSize(QtCore.QSize(40, 40))
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
        main_layout.addWidget(exit_button, alignment=QtCore.Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VitesseControl()
    window.show()
    sys.exit(app.exec_())
