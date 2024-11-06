import time
from batch_extractor import find_gif_files, extract_gif_data
from data_storage import save_data, load_data, information
import os
import sys
from tkinter import Tk, filedialog

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QFileDialog, QTextEdit, QTabWidget
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer


class Gif(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_widget = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Información de GIF")
        self.setGeometry(50, 50, 1200, 1000)

        self.setStyleSheet("""
                    QWidget {
                        background-color: black;
                        color: white;
                    }
                    QPushButton {
                        background-color: gray;
                        color: white;
                        font-weight: bold;
                    }
                    QLineEdit {
                        background-color: #333;
                        color: white;
                    }
                    QLabel {
                        color: white;
                    }
                """)

        self.folderButton = QPushButton("Seleccionar Carpeta", self)
        self.folderButton.clicked.connect(self.recopilar_info)

        self.gifsaveButton = QPushButton("Guardar info GIF", self)
        self.gifsaveButton.clicked.connect(self.saveInfo)

        self.open_button = QPushButton("Abrir archivo .txt")
        self.open_button.clicked.connect(self.open_file)

        self.gifLabel = QLabel(self)
        self.gifLabel.setFixedSize(300, 300)
        self.gifLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gifLabel2 = QLabel(self)
        self.gifLabel2.setFixedSize(300, 300)
        self.gifLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.infoLayout = QGridLayout()
        self.timer = QTimer(self)
        self.timer.start(2500)
        self.data = "datos_gif.txt"





































































































































































































































































































































        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setStyleSheet("background-color: black; color: white;")

        mainLayout = QHBoxLayout()
        gifLayout = QVBoxLayout()
        gifLayout.addWidget(self.folderButton)
        gifLayout.addWidget(self.gifsaveButton)
        gifLayout.addWidget(self.open_button)
        gifLayout.addWidget(self.gifLabel)
        gifLayout.addWidget(self.gifLabel2)
        gifLayout.addLayout(self.tab_widget)
        gifinfo = QVBoxLayout()
        gifinfo.addWidget(QLabel("Información del GIF:"))
        gifinfo.addWidget(self.info_display)

        mainLayout.addLayout(gifLayout)
        mainLayout.addLayout(gifinfo)
        mainLayout.addLayout(self.infoLayout)

        self.setLayout(mainLayout)

        self.gif_data = []
        self.current_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showNextGif)

    def loadGif(self, ruta_archivo):
        if ruta_archivo:
            movie = QMovie(ruta_archivo)
            self.gifLabel.setMovie(movie)
            movie.start()

    def displayGifInfo(self, gif_info):
        info_text = "\n".join(f"{key}: {value}" for key, value in gif_info.items())
        self.info_display.setText(info_text)


    def recopilar_info(self):
        ruta_carpeta = filedialog.askdirectory(
            title="Selecciona una carpeta")
        ruta = ruta_carpeta
        self.saveInfo1(ruta_carpeta)
        self.gif_data = find_gif_files(ruta)
        if self.gif_data:
            self.gif_data = information(self.gif_data)
            self.current_index = 0
            self.timer.start(1000)

    def saveInfo1(self, ruta):
        archivo = self.data
        gif_data = find_gif_files(ruta)
        if gif_data:
            save_data(archivo, gif_data)

    def saveInfo(self):
        ruta_carpeta = filedialog.askdirectory(
            title="Selecciona una carpeta")
        ruta = ruta_carpeta
        archivo = self.data
        gif_data = find_gif_files(ruta)
        if gif_data:
            save_data(archivo, gif_data)

    def showNextGif(self):
        if self.current_index < len(self.gif_data):
            gif_info_raw = self.gif_data[self.current_index:self.current_index + 11]
            if len(gif_info_raw) == 11:
                gif_info = {
                    "Número de versión:": gif_info_raw[0],
                    "Tamaño imagen": str(gif_info_raw[1]),
                    "Cantidad de Colores": str(gif_info_raw[2]),
                    "Tipo": str(gif_info_raw[4]),
                    "Formato": str(gif_info_raw[5]),
                    "Color fondo": str(gif_info_raw[6]),
                    "Cantidad de imágenes": str(gif_info_raw[7]),
                    "Creación": str(gif_info_raw[8]),
                    "Modificación": str(gif_info_raw[9]),
                    "Comentarios": str(gif_info_raw[10])
                }
                self.displayGifInfo(gif_info)
                self.loadGif(gif_info_raw[3])

            self.current_index += 11
        else:
            self.timer.stop()

    def open_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Abrir archivo .txt", "", "Text Files (*.txt)")

        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            contenido = file.read()
            self.info_display.setText(contenido)


app = QApplication(sys.argv)
window = Gif()
window.show()
sys.exit(app.exec())
