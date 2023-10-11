import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QScrollArea, QVBoxLayout,
                             QGridLayout, QWidget, QLabel, QMessageBox, QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


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
        msg.exec_()


class ImageGallery(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()

        self.setWindowTitle("Galeria de Imagens")

        # Estilo do gradiente para o widget central
        gradient_style = """
        QMainWindow {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(70, 70, 70, 255), stop:1 rgba(30, 30, 30, 255));
        }
        """
        self.setStyleSheet(gradient_style)

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

            # Criamos um QFrame como contêiner para dar destaque
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(100, 100, 100, 80);
                    border-radius: 5px;
                }
            """)
            frame_layout = QVBoxLayout(frame)

            img_label = ClickableImage(pixmap.scaled(150, 150, Qt.KeepAspectRatio), image_info)
            frame_layout.addWidget(img_label, alignment=Qt.AlignCenter)
            self.scroll_layout.addWidget(frame, row, col)

            col += 1
            if col >= 3:  # Suponha que queremos 3 imagens por linha.
                col = 0
                row += 1

        self.show()


def get_image_paths(directory):
    all_files = os.listdir(directory)
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    return [os.path.join(directory, f) for f in image_files]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_directory = "images_data_base/real_images"
    gallery = ImageGallery(get_image_paths(image_directory))
    sys.exit(app.exec_())
