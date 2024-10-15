import sys
import time
import math
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QSpacerItem
from Moves import Move

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.path = []
        self.executed_path = []  # Liste pour stocker les vecteurs exécutés
        self.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #337ab7;
            border-radius: 10px;
        """)
        self.pen = QPen(Qt.black, 5, Qt.SolidLine)
        self.start_point = None
        self.end_point = None
        self.drawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_point = event.pos()
            self.path.append((self.start_point, self.start_point))

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing:
            painter = QPainter(self)
            painter.setPen(self.pen)
            painter.drawLine(self.start_point, event.pos())
            self.path[-1] = (self.start_point, event.pos())
            self.start_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.end_point = event.pos()
            print(f"Start Point: {self.path[0][0]}")
            print(f"End Point: {self.end_point}")

    def clear(self):
        self.path = []
        self.executed_path = []  # Effacer les vecteurs exécutés
        self.start_point = None
        self.end_point = None
        self.update()

    def paintEvent(self, event):
        canvas = QPainter(self)
        canvas.setPen(self.pen)
        
        # Dessiner les axes X et Y
        axis_pen = QPen(Qt.gray, 1, Qt.SolidLine)
        canvas.setPen(axis_pen)
        mid_x = self.width() // 2
        mid_y = self.height() // 2

        canvas.drawLine(mid_x, 0, mid_x, self.height())  # Axe Y
        canvas.drawLine(0, mid_y, self.width(), mid_y)  # Axe X

        # Dessiner les étiquettes des axes
        label_pen = QPen(Qt.black, 1, Qt.SolidLine)
        canvas.setPen(label_pen)
        font = canvas.font()
        font.setPointSize(8)
        canvas.setFont(font)

        for i in range(0, self.width(), 50):
            canvas.drawText(i, mid_y + 15, str(i - mid_x))
        for i in range(0, self.height(), 50):
            canvas.drawText(mid_x + 5, i, str(mid_y - i))

        # Dessiner le chemin dessiné
        canvas.setPen(self.pen)
        for line in self.path:
            canvas.drawLine(line[0], line[1])
        if self.start_point:
            self.draw_indicator(canvas, self.start_point, "green")
        if self.end_point:
            self.draw_indicator(canvas, self.end_point, "red")

        # Tracer les vecteurs exécutés en rouge
        executed_pen = QPen(Qt.red, 3, Qt.SolidLine)
        canvas.setPen(executed_pen)
        for line in self.executed_path:
            canvas.drawLine(line[0], line[1])

    def draw_indicator(self, painter, point, color):
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(Qt.green if color == "green" else Qt.red)
        painter.drawEllipse(point, 5, 5)

class TrajectoryControl(QMainWindow):
    def __init__(self):
        super(TrajectoryControl, self).__init__()
        self.setWindowTitle("Trajectory Control")  

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
        pixmap = QPixmap('icons/trajectory.png')  # Changez le chemin vers votre icône
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        control_icon.setPixmap(pixmap)
        control_icon.setStyleSheet("margin-right: 10px;")

        # Ajouter le texte du titre
        title_label = QLabel("Controler de Trajectoire", title_container)
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

        # Ajouter le widget de dessin
        self.drawing_widget = DrawingWidget()
        main_layout.addWidget(self.drawing_widget)

        # Créer la section des boutons
        button_layout = QHBoxLayout()

        self.button_execute = QPushButton()
        self.button_execute.setObjectName("button_execute")
        self.button_execute.setIcon(QIcon('icons/execute.png'))  # Changez le chemin vers votre icône
        self.button_execute.setIconSize(QSize(40, 40))
        self.button_execute.setStyleSheet("""
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
        self.button_execute.clicked.connect(self.execute_trajectory)
        button_layout.addWidget(self.button_execute)

        self.button_clear = QPushButton()
        self.button_clear.setObjectName("button_clear")
        self.button_clear.setIcon(QIcon('icons/clear.png'))  # Changez le chemin vers votre icône
        self.button_clear.setIconSize(QSize(40, 40))
        self.button_clear.setStyleSheet("""
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
        self.button_clear.clicked.connect(self.drawing_widget.clear)
        button_layout.addWidget(self.button_clear)

        self.button_stop = QPushButton()
        self.button_stop.setObjectName("button_stop")
        self.button_stop.setIcon(QIcon('icons/stop_b.png'))  # Changez le chemin vers votre icône
        self.button_stop.setIconSize(QSize(40, 40))
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

    def execute_trajectory(self):
        def move_robot(direction, duration):
            if direction == "forward":
                Move.avancer()
            elif direction == "backward":
                Move.reculer()
            elif direction == "left":
                Move.avant_gauche()
            elif direction == "right":
                Move.avant_droite()
            time.sleep(duration)
            Move.stop()
            time.sleep(0.5)  # Pause to allow the stop to take effect

        def calculate_angle(dx, dy):
            angle = math.degrees(math.atan2(dy, dx))
            return angle

        for start, end in self.drawing_widget.path:
            dx = end.x() - start.x()
            dy = end.y() - start.y()
            distance = (dx**2 + dy**2)**0.5
            duration = (distance / 50) * 2  # Adjust this value according to your needs
            angle = calculate_angle(dx, dy)

            print(f"Start: ({start.x()}, {start.y()}), End: ({end.x()}, {end.y()}), Angle: {angle}")

            if -45 <= angle < 45:
                move_robot("forward", duration)
            elif 45 <= angle < 135:
                move_robot("left", duration)
            elif -135 <= angle < -45:
                move_robot("right", duration)
            else:
                move_robot("backward", duration)

            # Ajouter le segment exécuté à la liste et redessiner
            self.drawing_widget.executed_path.append((start, end))
            self.drawing_widget.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrajectoryControl()
    window.show()
    sys.exit(app.exec_())
