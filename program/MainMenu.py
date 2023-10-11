import sys
import os
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QVBoxLayout, QGridLayout, QWidget,
    QLabel, QMessageBox, QFrame, QLineEdit, QPushButton, QFileDialog, QGraphicsView, QGraphicsScene,
    QStatusBar
)
from PySide6.QtGui import QPixmap, QIcon, QFont, QColor, QPalette
from PySide6.QtCore import QRect, QSize, QMetaObject, QCoreApplication, Qt

from w.codigo import *
from w.codificar import *
from w.funcao import *
from w.decodificar import *
from w.esconder import *


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


class ClickableImage(QLabel):
    def __init__(self, pixmap, info, parent=None):
        super(ClickableImage, self).__init__(parent)
        self.setPixmap(pixmap)
        self.info = info

    def mousePressEvent(self, event):
        self.show_info()

    def show_info(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(self.info)
        msg.setWindowTitle("Informações da Imagem")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #353535;
            }
            QLabel{
                color: #ffffff;
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
        msg.exec_()


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

            img_label = ClickableImage(pixmap.scaled(150, 150, Qt.KeepAspectRatio), image_info)
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
        self.openImageGallery(directory)

    def openImageGallery(self, directory):
        if os.path.exists(directory):
            image_paths = [os.path.join(directory, f) for f in os.listdir(directory) if
                           os.path.isfile(os.path.join(directory, f))]
            if image_paths:
                self.gallery = ImageGallery(image_paths)
                self.gallery.show()
                self.close()  # fecha a janela principal
            else:
                QMessageBox.warning(self, "Sem imagens", "Não há imagens no diretório selecionado.")
        else:
            QMessageBox.warning(self, "Diretório não encontrado", "O diretório selecionado não existe.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_theme(app)
    mainWin = MainWindow()
    cript = cripto()
    binary_sequence = nume_binary(cript)
    output_string = lista_para_string(binary_sequence)

    key = fill_matrix_with_primes()
    seq_bin()

    print("KEY: ")
    print(key)
    print()
    print("Codigo ASCII")
    print(vet)
    print()
    print("Codigo Criptografado")
    print(cript)
    print()
    print("sequncia binaria com o tamanho")
    print(binary_sequence)
    print()
    print("sequncia binaria STR")
    print(output_string)
    mainWin.show()

    sys.exit(app.exec_())
