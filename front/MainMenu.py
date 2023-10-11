from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys

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
        self.lineEdit.setGeometry(QRect(420, 190, 200, 25))

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(635, 190, 100, 25))

        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(240, 260, 358, 240))

        # Create a QGraphicsScene instance for the QGraphicsView
        self.scene = QGraphicsScene(self.graphicsView)
        pixmap = QPixmap("iconqT.png")

        # Add the pixmap to the scene
        self.scene.addPixmap(pixmap)

        # Set the scene to the QGraphicsView
        self.graphicsView.setScene(self.scene)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(510, 560, 291, 20))
        font2 = QFont()
        font2.setPointSize(7)
        self.label_3.setFont(font2)

        PVPI.setCentralWidget(self.centralwidget)

        self.statusbar = QStatusBar(PVPI)
        self.statusbar.setObjectName(u"statusbar")
        PVPI.setStatusBar(self.statusbar)

        self.retranslateUi(PVPI)

        QMetaObject.connectSlotsByName(PVPI)
        self.pushButton.clicked.connect(self.openFileDialog)

    def retranslateUi(self, PVPI):
        PVPI.setWindowTitle(QCoreApplication.translate("PVPI", u"PVPI", None))
        self.label.setText(
            QCoreApplication.translate("PVPI", u"Plataforma de Verificação e Proteção de Imagens (PVPI).", None))
        self.label_2.setText(
            QCoreApplication.translate("PVPI", u"Entre o diretório de onde você deseja realizar a Proteção:", None))
        self.pushButton.setText(QCoreApplication.translate("PVPI", u"Select Directory", None))
        self.label_3.setText(QCoreApplication.translate("PVPI",
                                                        u"versão 0.0.1 (pre-alpha) - Nicolas Sales, Wyllgner França, Jáder Louis",
                                                        None))

class MainWindow(QMainWindow, Ui_PVPI):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    def openFileDialog(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Select Directory")
        if folder_path:
            self.lineEdit.setText(folder_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    qss = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #343a40, stop:1 #23272a);
    }

    QLabel {
        color: #f8f9fa;
    }

    QLineEdit {
        border: 2px solid #495057;
        border-radius: 4px;
        padding: 4px;
        background-color: #343a40;
        color: #f8f9fa;
    }

    QPushButton {
        border: 2px solid #495057;
        border-radius: 4px;
        padding: 4px;
        background-color: #343a40;
        color: #f8f9fa;
    }

    QPushButton:hover {
        background-color: #495057;
    }

    QPushButton:pressed {
        background-color: #23272a;
    }

    QGraphicsView {
        border: 2px solid #495057;
        border-radius: 4px;
        background-color: #343a40;
    }

    QStatusBar {
        border-top: 1px solid #495057;
        background: #23272a;
        color: #f8f9fa;
    }
    """

    main_window.setStyleSheet(qss)
    sys.exit(app.exec_())
