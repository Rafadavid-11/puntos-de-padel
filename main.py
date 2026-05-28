from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

# Constantes
ANCHO, ALTO = 900, 600 
WIN_TITLE = 'Marcador de Pádel'

class MainWindow(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        # Lógica del juego
        self.puntos_opciones = ["0", "15", "30", "40", "Adv"]
        self.idx_p1 = 0
        self.idx_p2 = 0
        self.sets_p1 = 0
        self.sets_p2 = 0

        # Inicializar métodos
        self.config_window()
        self.set_window()
        self.event_handler()
        self.actualizar_marcador()
        self.show()

    def set_window(self):
        # Layout principal vertical
        self.main_layout = QVBoxLayout()

        # Nombres de las parejas (Inputs)
        self.layout_nombres = QHBoxLayout()
        self.input_p1 = QLineEdit("Pareja 1")
        self.input_p2 = QLineEdit("Pareja 2")
        self.layout_nombres.addWidget(self.input_p1)
        self.layout_nombres.addWidget(self.input_p2)

        # Marcador de Sets (Visualización)
        self.layout_sets = QHBoxLayout()
        self.label_sets_p1 = QLabel("Sets: 0")
        self.label_sets_p2 = QLabel("Sets: 0")
        self.label_sets_p1.setAlignment(Qt.AlignCenter)
        self.label_sets_p2.setAlignment(Qt.AlignCenter)
        # Un toque de estilo para diferenciar los Sets
        self.label_sets_p1.setStyleSheet("font-size: 16px; font-weight: bold; color: gray;")
        self.label_sets_p2.setStyleSheet("font-size: 16px; font-weight: bold; color: gray;")
        self.layout_sets.addWidget(self.label_sets_p1)
        self.layout_sets.addWidget(self.label_sets_p2)

        # Marcador de Puntos (Visualización grande)
        self.layout_puntos = QHBoxLayout()
        self.label_p1 = QLabel("0")
        self.label_p2 = QLabel("0")
        self.label_p1.setAlignment(Qt.AlignCenter)
        self.label_p2.setAlignment(Qt.AlignCenter)
        self.label_p1.setStyleSheet("font-size: 48px; font-weight: bold; color: #2C3E50;")
        self.label_p2.setStyleSheet("font-size: 48px; font-weight: bold; color: #2C3E50;")
        self.layout_puntos.addWidget(self.label_p1)
        self.layout_puntos.addWidget(self.label_p2)

        # Botones para sumar puntos
        self.layout_botones = QHBoxLayout()
        self.btn_p1 = QPushButton("Punto Pareja 1")
        self.btn_p2 = QPushButton("Punto Pareja 2")
        self.layout_botones.addWidget(self.btn_p1)
        self.layout_botones.addWidget(self.btn_p2)

        # Botón de reinicio
        self.btn_reset = QPushButton("Reiniciar Partido")
        self.btn_reset.setStyleSheet("background-color: #E74C3C; color: white; font-weight: bold;")

        # Unir todo al layout principal
        self.main_layout.addLayout(self.layout_nombres)
        self.main_layout.addLayout(self.layout_sets)
        self.main_layout.addLayout(self.layout_puntos)
        self.main_layout.addLayout(self.layout_botones)
        self.main_layout.addWidget(self.btn_reset)

        self.setLayout(self.main_layout)

    def config_window(self):
        self.setWindowTitle(WIN_TITLE)
        self.resize(ANCHO, ALTO)

    def event_handler(self):
        # Eventos de los botones
        self.btn_p1.clicked.connect(lambda: self.sumar_punto(pareja=1))
        self.btn_p2.clicked.connect(lambda: self.sumar_punto(pareja=2))
        self.btn_reset.clicked.connect(self.reiniciar_partido)

    def sumar_punto(self, pareja):
        if pareja == 1:
            if self.idx_p1 == 3 and self.idx_p2 < 3:  # De 40 gana el juego
                self.ganar_juego(1)
            elif self.idx_p1 == 3 and self.idx_p2 == 3:  # De 40-40 pasa a Ventaja
                self.idx_p1 = 4
            elif self.idx_p1 == 3 and self.idx_p2 == 4:  # Si el otro tenía ventaja, vuelve a Deuce
                self.idx_p2 = 3
            elif self.idx_p1 == 4:  # De ventaja gana el juego
                self.ganar_juego(1)
            else:
                self.idx_p1 += 1
        else:
            if self.idx_p2 == 3 and self.idx_p1 < 3:
                self.ganar_juego(2)
            elif self.idx_p2 == 3 and self.idx_p1 == 3:
                self.idx_p2 = 4
            elif self.idx_p2 == 3 and self.idx_p1 == 4:
                self.idx_p1 = 3
            elif self.idx_p2 == 4:
                self.ganar_juego(2)
            else:
                self.idx_p2 += 1

        self.actualizar_marcador()

    def ganar_juego(self, pareja):
        # Resetear puntos del juego actual
        self.idx_p1 = 0
        self.idx_p2 = 0
        
        # Sumar el juego al set (para simplificar la app visual, sumamos sets directamente, 
        # pero si quieres juegos por set, se puede ampliar fácilmente).
        if pareja == 1:
            self.sets_p1 += 1
        else:
            self.sets_p2 += 1

    def actualizar_marcador(self):
        # Actualizar los textos en pantalla
        self.label_p1.setText(self.puntos_opciones[self.idx_p1])
        self.label_p2.setText(self.puntos_opciones[self.idx_p2])
        self.label_sets_p1.setText(f"Sets: {self.sets_p1}")
        self.label_sets_p2.setText(f"Sets: {self.sets_p2}")

    def reiniciar_partido(self):
        self.idx_p1 = 0
        self.idx_p2 = 0
        self.sets_p1 = 0
        self.sets_p2 = 0
        self.actualizar_marcador()

def run():
    app = QApplication([])
    window = MainWindow()
    app.exec_()

if __name__ == "__main__":
    run()