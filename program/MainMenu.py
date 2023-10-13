import sys
import os

import cv2
import numpy as np  # Certifique-se de importar numpy aqui
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QVBoxLayout, QGridLayout, QWidget,
    QLabel, QMessageBox, QFrame, QLineEdit, QPushButton, QFileDialog, QGraphicsView, QGraphicsScene,
    QStatusBar, QTextEdit, QDialog
)
from PySide6.QtGui import QPixmap, QIcon, QFont, QColor, QPalette
from PySide6.QtCore import QRect, QSize, QMetaObject, QCoreApplication, Qt
from concurrent.futures import ThreadPoolExecutor
from codigo import *
from codificar import *
from dct import jpg_to_png
from model import iaChecker
from program.track.header_add_track import addTrack
from program.track.jpg_to_tjpg import jpg_to_tjpg
from program.track.tjpg_to_jpg import tjpg_to_jpg


def set_dark_theme(app):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
    dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
import os
from concurrent.futures import ThreadPoolExecutor

#multithreading para melhorar o desempenho.
#imput
#image_path = 'note.jpg'
#image = cv2.imread(image_path)
#secret_data = seq_bin()

# Escondendo os dados
#image_with_hidden_data = hide_data(image.copy(), secret_data)
#cv2.imwrite('teste_imagem.jpg', image_with_hidden_data)

def process_image(file_name, directory):
    if file_name.endswith(".jpg"):
        file_path = os.path.join(directory, file_name)
        print("NOME DA IMAGEM ESCOLHIDA: " + file_name)

        tjpg_path = file_path[:-4] + ".tjpg"
        if os.path.exists(tjpg_path):
            print("O arquivo .tjpg já existe!")
            addTrack(tjpg_path)
            print("Foi Adicionado!")
            tjpg_text = tjpg_to_jpg(tjpg_path)
            formatted_info = format_trackers_from_tjpg(tjpg_text)
            # Use formatted_info conforme necessário
        else:
            print("O arquivo .tjpg não existe!")
            jpg_to_tjpg(file_path)
            #hide_data(image, codificar)
            #cv2.imwrite(file_path, image)
            print("Foi criado!")
            # Lógica adicional aqui, se necessário

def process_images(directory):
    with ThreadPoolExecutor(max_workers=4) as executor:  # Ajuste max_workers conforme necessário
        # Submeta todas as tarefas ao executor
        futures = [executor.submit(process_image, file_name, directory) for file_name in os.listdir(directory)]
        # Espere até que todas sejam concluídas
        for future in futures:
            future.result()  # Pode adicionar tratamento de exceções aqui

class InfoDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informações da Imagem")

        # Crie um layout vertical
        layout = QVBoxLayout()

        # Crie um QTextEdit para exibir o texto
        text_edit = QTextEdit(self)
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)

        # Adicione o QTextEdit ao layout
        layout.addWidget(text_edit)

            # Defina o layout para o diálogo
        self.setLayout(layout)
class ClickableImage(QLabel):
    def __init__(self, pixmap, info, idunico, np_var, parent=None):
        super(ClickableImage, self).__init__(parent)
        self.setPixmap(pixmap)
        self.info = info
        self.idunico = idunico
        self.np_var = np_var

    def mousePressEvent(self, event):
        self.show_info()

    # ...
    def show_info(self, info_text=None):
        print("NOME DA IMAGEM ESCOLHIDA: " + self.np_var)
        tjpg_path = self.np_var[:-4] + ".tjpg"

        # Lendo a imagem original
        #image = cv2.imread(self.np_var)

        # Escondendo a mensagem na imagem
        #image_with_hidden_data = hide_data(image, codificar())

        # Salvando a imagem com a mensagem escondida
        # Aqui, substitua 'output_image_path' pelo caminho onde você deseja salvar a nova imagem
        #output_image_path = self.np_var  # substitua pelo seu caminho desejado
        #cv2.imwrite(output_image_path, image_with_hidden_data, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        # Lendo a imagem com dados escondidos
        #image_with_data = cv2.imread(output_image_path)

        # Revelando a mensagem
        #print("msg escondida: " + reveal_data(image_with_data))

        tjpg_text = tjpg_to_jpg(tjpg_path)
        formatted_info = format_trackers_from_tjpg(tjpg_text)

        # Inicialize info_text como uma string vazia se for None
        if info_text is None:
            info_text = ""

        info_text += formatted_info

        # Crie um texto com as informações restantes
        info_text += "\nFLAG IA = " + str(iaChecker(self.np_var))

        # Crie e exiba o diálogo personalizado
        info_dialog = InfoDialog(info_text, self)
        info_dialog.exec()


class ImageGallery(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()

        self.setWindowTitle("Galeria de Imagens")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        row, col = 0, 0
        for img_path in image_paths:
            pixmap = QPixmap(img_path)
            image_info = os.path.basename(img_path)

            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: #2a82da;
                    border-radius: 5px;
                }
            """)
            frame_layout = QVBoxLayout(frame)

            img_label = ClickableImage(pixmap.scaled(150, 150, Qt.KeepAspectRatio), image_info, "",img_path)
            frame_layout.addWidget(img_label, alignment=Qt.AlignCenter)
            self.scroll_layout.addWidget(frame, row, col)

            col += 1
            if col >= 3:
                col = 0
                row += 1
        self.show()


class Ui_PVPI(object):
    def setupUi(self, PVPI):
        if not PVPI.objectName():
            PVPI.setObjectName(u"PVPI")
        PVPI.resize(800, 600)
        icon = QIcon()
        icon.addFile(u"iconImage.png", QSize(), QIcon.Normal, QIcon.Off)
        PVPI.setWindowIcon(icon)
        self.centralwidget = QWidget(PVPI)
        self.centralwidget.setObjectName(u"centralwidget")

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 10, 721, 81))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 160, 721, 81))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_2.setFont(font1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(450, 190, 150, 25))

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(635, 190, 100, 25))

        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(240, 260, 358, 240))

        self.scene = QGraphicsScene(self.graphicsView)
        pixmap = QPixmap("iconqT.png")
        self.scene.addPixmap(pixmap)
        self.graphicsView.setScene(self.scene)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(230, 490, 400, 51))

        PVPI.setCentralWidget(self.centralwidget)

        self.statusbar = QStatusBar(PVPI)
        self.statusbar.setObjectName(u"statusbar")
        PVPI.setStatusBar(self.statusbar)

        self.retranslateUi(PVPI)

        QMetaObject.connectSlotsByName(PVPI)

    def retranslateUi(self, PVPI):
        PVPI.setWindowTitle(QCoreApplication.translate("PVPI", u"PVPI", None))
        self.label.setText(QCoreApplication.translate("PVPI", u"     Bem-vindo a Plataforma PVPI", None))
        self.label_2.setText(QCoreApplication.translate("PVPI", u"Por favor, insira o diret\u00f3rio das imagens que deseja visualizar:", None))
        self.pushButton.setText(QCoreApplication.translate("PVPI", u"Procurar", None))
        self.label_3.setText(QCoreApplication.translate("PVPI", u"Feito com \u2764\ufe0f, Por Nicolas Sales, Wyllgner França, Jader Louis - Versao 0.0.1", None))


class MainWindow(QMainWindow, Ui_PVPI):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setStyleSheet("""
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #353535;
                color: #ffffff;
                border: 2px solid #2a82da;
                border-radius: 5px;
            }
            QPushButton {
                color: #ffffff;
                background-color: #353535;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: #2a82da;
                font: bold 14px;
                padding: 6px;
            }
            QPushButton:pressed {
                background-color: #2a82da;
                border-style: inset;
            }
        """)

        self.pushButton.clicked.connect(self.on_buttonClick)

    def on_buttonClick(self):
        directory = QFileDialog.getExistingDirectory(self, "Selecionar diretório")
        self.lineEdit.setText(directory)  # exibe o diretório selecionado no campo de texto
        process_images(directory)
        self.openImageGallery(directory)

    def openImageGallery(self, directory):
        jpg_to_png(directory)
        if os.path.exists(directory):
            # Lista de extensões de arquivo de imagem válidas
            valid_image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff",
                                      ".gif"]  # você pode adicionar ou remover tipos de arquivo conforme necessário

            # Obtém todos os arquivos no diretório e filtra por extensões de arquivo de imagem
            image_paths = [os.path.join(directory, f) for f in os.listdir(directory)
                           if os.path.isfile(os.path.join(directory, f)) and any(
                    f.lower().endswith(ext) for ext in valid_image_extensions)]

            if image_paths:
                self.gallery = ImageGallery(image_paths)
                self.gallery.show()
                self.close()  # fecha a janela principal
            else:
                QMessageBox.warning(self, "Sem imagens", "Não há imagens no diretório selecionado.")
        else:
            QMessageBox.warning(self, "Diretório não encontrado", "O diretório selecionado não existe.")


def format_trackers_from_tjpg(tjpg_text):
    # Divide o texto usando '#' como delimitador para obter os trackers individuais
    trackers = tjpg_text.split('#')

    # Inicializa uma lista para armazenar as informações formatadas dos trackers
    formatted_trackers = []

    # Processa cada tracker individual
    for tracker in trackers:
        # Divide o tracker usando '|' como delimitador
        parts = tracker.split('|')

        # Verifica se há informações suficientes (pelo menos 2 partes)
        if len(parts) >= 2:
            # Primeira parte: Número total de usuários
            num_users = parts[0]

            # Segunda parte: Informações dos usuários
            user_info = parts[1:]

            # Formata as informações para exibição
            formatted_tracker = f"Número Total de Usuários: {num_users}\n"
            formatted_tracker += "\n".join([f"Usuário {i + 1}: {info}" for i, info in enumerate(user_info)])

            # Adiciona o tracker formatado à lista
            formatted_trackers.append(formatted_tracker)

    # Verifica se há algum tracker formatado
    if formatted_trackers:
        # Retorna a lista de informações dos trackers formatadas como uma string
        return "\n\nInformações dos Trackers:\n\n" + "\n\n".join(formatted_trackers)
    else:
        # Retorna uma mensagem se nenhum tracker for encontrado
        return "\n\nNenhum Tracker encontrado."



if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_theme(app)
    mainWin = MainWindow()

    mainWin.show()

    sys.exit(app.exec())
