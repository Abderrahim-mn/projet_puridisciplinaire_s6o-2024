from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
import serial
from Moves import Move
import keyboard

class Control(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        # Obtenir la taille de l'écran
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calculer la taille de la fenêtre (moitié de la taille de l'écran)
        window_width = screen_geometry.width() // 2
        window_height = screen_geometry.height() // 2

        # Définir la taille de la fenêtre et la centrer
        MainWindow.setGeometry(
            screen_geometry.width() // 2 - window_width // 2,
            screen_geometry.height() // 2 - window_height // 2,
            window_width,
            window_height
        )

        # Créer le widget central
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Créer la mise en page principale
        main_layout = QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setSpacing(10)

        # Créer le conteneur pour le titre
        title_container = QWidget(self.centralwidget)
        title_layout = QHBoxLayout(title_container)
        title_layout.setAlignment(QtCore.Qt.AlignLeft)

        # Ajouter l'icône de contrôle
        control_icon = QLabel(title_container)
        pixmap = QPixmap('icons/control.png')  # Changez le chemin vers votre icône
        pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        control_icon.setPixmap(pixmap)
        control_icon.setStyleSheet("margin-right: 10px;")

        # Ajouter le texte du titre
        title_label = QLabel("Mode Manuel", title_container)
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

        # Créer la mise en page des boutons en forme de joystick
        grid_layout = QGridLayout()
        grid_layout.setAlignment(QtCore.Qt.AlignCenter)
        grid_layout.setSpacing(10)

        # Créer et positionner les boutons
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setIcon(QtGui.QIcon('icons/left.png'))  # Changez le chemin vers votre icône
        self.pushButton_2.setIconSize(QtCore.QSize(40, 40))

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setIcon(QtGui.QIcon('icons/right.png'))  # Changez le chemin vers votre icône
        self.pushButton_3.setIconSize(QtCore.QSize(40, 40))

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setIcon(QtGui.QIcon('icons/down.png'))  # Changez le chemin vers votre icône
        self.pushButton_4.setIconSize(QtCore.QSize(40, 40))

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setIcon(QtGui.QIcon('icons/up.png'))  # Changez le chemin vers votre icône
        self.pushButton.setIconSize(QtCore.QSize(40, 40))

        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setIcon(QtGui.QIcon('icons/stop.png'))  # Changez le chemin vers votre icône
        self.pushButton_stop.setIconSize(QtCore.QSize(40, 40))

        # Ajouter les boutons à la mise en page du grid
        grid_layout.addWidget(self.pushButton, 0, 1)
        grid_layout.addWidget(self.pushButton_2, 1, 0)
        grid_layout.addWidget(self.pushButton_stop, 1, 1)
        grid_layout.addWidget(self.pushButton_3, 1, 2)
        grid_layout.addWidget(self.pushButton_4, 2, 1)

        # Ajouter la mise en page des boutons à la mise en page principale
        main_layout.addLayout(grid_layout)

        # Créer un espaceur flexible en dessous des boutons
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Ajouter un bouton Exit
        exit_button = QPushButton("Exit", self.centralwidget)
        exit_button.setIcon(QtGui.QIcon('icons/exit.png'))  # Changez le chemin vers votre icône
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
        exit_button.clicked.connect(MainWindow.close)
        main_layout.addWidget(exit_button, alignment=QtCore.Qt.AlignCenter)

        # Configurer le widget central avec la mise en page principale
        self.centralwidget.setLayout(main_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        # Configurer la barre de menus
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Configurer la barre d'état
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Connecter les boutons aux fonctions de mouvement
        self.pushButton.pressed.connect(Move.avancer)
        self.pushButton.released.connect(Move.stop)
        self.pushButton_4.pressed.connect(Move.reculer)
        self.pushButton_4.released.connect(Move.stop)
        self.pushButton_2.pressed.connect(Move.avant_gauche)
        self.pushButton_2.released.connect(Move.stop)
        self.pushButton_3.pressed.connect(Move.avant_droite)
        self.pushButton_3.released.connect(Move.stop)
        self.pushButton_stop.pressed.connect(Move.stop)

        # Configurer les contrôles de clavier
        keyboard.on_press_key('up', lambda event: Move.avancer())
        keyboard.on_release_key('up', lambda event: Move.stop())

        keyboard.on_press_key('down', lambda event: Move.reculer())
        keyboard.on_release_key('down', lambda event: Move.stop())

        keyboard.on_press_key('up', lambda event: Move.avant_droite() if keyboard.is_pressed('right') else Move.avant_gauche() if keyboard.is_pressed('left') else Move.avance_rapide() if keyboard.is_pressed('shift') else None)
        keyboard.on_press_key('right', lambda event: Move.avant_droite() if keyboard.is_pressed('up') else Move.arriere_droite() if keyboard.is_pressed('down') else None)
        keyboard.on_release_key('right', lambda event: Move.avancer() if keyboard.is_pressed('up') else Move.reculer() if keyboard.is_pressed('down') else None)

        keyboard.on_press_key('left', lambda event: Move.avant_gauche() if keyboard.is_pressed('up') else Move.arriere_gauche() if keyboard.is_pressed('down') else None)
        keyboard.on_release_key('left', lambda event: Move.avancer() if keyboard.is_pressed('up') else Move.reculer() if keyboard.is_pressed('down') else None)
        keyboard.on_release_key('up', lambda event: Move.stop())

        keyboard.on_press_key('down', lambda event: Move.arriere_droite() if keyboard.is_pressed('right') else Move.arriere_gauche() if keyboard.is_pressed('left') else Move.recule_rapide() if keyboard.is_pressed('shift') else None)
        keyboard.on_release_key('down', lambda event: Move.stop())

        keyboard.on_press_key('shift', lambda event: Move.avance_rapide() if keyboard.is_pressed('up') else Move.recule_rapide() if keyboard.is_pressed('down') else None)
        keyboard.on_release_key('shift', lambda event: Move.avancer() if keyboard.is_pressed('up') else Move.reculer() if keyboard.is_pressed('down') else None)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mode Manuel"))
       

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Control()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
