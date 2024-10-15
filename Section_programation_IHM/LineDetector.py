import sys
import serial
from PyQt5 import QtCore, QtGui, QtWidgets

class SerialReader(QtCore.QThread):
    message_received = QtCore.pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.serial = serial.Serial(port, baudrate)

    def run(self):
        while True:
            if self.serial.in_waiting:
                message = self.serial.readline().decode().strip()
                self.message_received.emit(message)

class LineDector(QtWidgets.QMainWindow):
    def __init__(self):
        super(LineDector, self).__init__()
        self.setWindowTitle("Line Detect")  

        # Obtenir la taille de l'écran
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()

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
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Créer la mise en page principale
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.setSpacing(10)

        # Créer le conteneur pour le titre
        title_container = QtWidgets.QWidget(self.centralwidget)
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_layout.setAlignment(QtCore.Qt.AlignLeft)

        # Ajouter l'icône de contrôle
        control_icon = QtWidgets.QLabel(title_container)
        pixmap = QtGui.QPixmap('icons/line.png')  # Changez le chemin vers votre icône
        pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        control_icon.setPixmap(pixmap)
        control_icon.setStyleSheet("margin-right: 10px;")

        # Ajouter le texte du titre
        title_label = QtWidgets.QLabel("Line Detect", title_container)
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
        main_layout.addSpacerItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # Créer les boutons Start et Stop
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setText("Start")
        self.button_start.setIcon(QtGui.QIcon('icons/start.png'))  # Changez le chemin vers votre icône
        self.button_start.setIconSize(QtCore.QSize(40, 40))
        self.button_start.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
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
                background-color: #4cae4c;
                box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background-color: #449d44;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        self.button_start.clicked.connect(self.send_start_command)
        main_layout.addWidget(self.button_start, alignment=QtCore.Qt.AlignCenter)

        self.button_stop = QtWidgets.QPushButton(self.centralwidget)
        self.button_stop.setText("Stop")
        self.button_stop.setIcon(QtGui.QIcon('icons/stop_b.png'))  # Changez le chemin vers votre icône
        self.button_stop.setIconSize(QtCore.QSize(40, 40))
        self.button_stop.setStyleSheet("""
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
        self.button_stop.clicked.connect(self.send_stop_command)
        main_layout.addWidget(self.button_stop, alignment=QtCore.Qt.AlignCenter)

        # Créer le terminal
        self.terminal = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.terminal.setReadOnly(True)
        main_layout.addWidget(self.terminal)

        # Créer un espaceur flexible en dessous du terminal
        main_layout.addSpacerItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # Ajouter un bouton Exit
        exit_button = QtWidgets.QPushButton("Exit", self.centralwidget)
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
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button, alignment=QtCore.Qt.AlignCenter)

        self.setCentralWidget(self.centralwidget)

        # Serial communication setup
        self.serial_port = "COM4"  # Change to your serial port
        self.serial_baudrate = 115200  # Change to your baud rate
        self.serial_thread = SerialReader(self.serial_port, self.serial_baudrate)
        self.serial_thread.message_received.connect(self.display_received_message)
        self.serial_thread.start()

    def send_start_command(self):
        if self.serial_thread.serial.is_open:
            command = b'\x6C'  # Change the start command as needed
            self.serial_thread.serial.write(command)
            self.terminal.appendPlainText("start")  # Display sent command in the terminal
        else:
            print("Serial port is not open.")
    
    def send_stop_command(self):
        if self.serial_thread.serial.is_open:
            command = b'\x73'  # Change the stop command as needed
            self.serial_thread.serial.write(command)
            self.terminal.appendPlainText("stop")  # Display sent command in the terminal
        else:
            print("Serial port is not open.")

    def display_received_message(self, message):
        self.terminal.appendPlainText("Received: " + message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LineDector()
    window.show()
    sys.exit(app.exec_())
