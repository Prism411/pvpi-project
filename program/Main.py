import sys
import os
from concurrent.futures import ThreadPoolExecutor

from PIL import Image
from PySide6.QtCore import QRect, QSize, QMetaObject, QCoreApplication, Qt
from PySide6.QtGui import QPixmap, QIcon, QFont, QColor, QPalette
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QVBoxLayout, QGridLayout, QWidget,
    QLabel, QMessageBox, QFrame, QLineEdit, QPushButton, QFileDialog, QGraphicsView, QGraphicsScene,
    QStatusBar, QTextEdit, QDialog  )


from codificar import *
from program.dct import jpg_to_png, hide_data_with_delimiter, decode_fixed_length, is_logical_string
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


#Variaveis Globais para nao precisar Ficar Chamando toda hora
cod = codificar()
message_length = 10
def process_image(file_name, directory): #Função principal que é chamada assim que inicia no diretorio.
    #Verifica se a imagem é PNG para fazer a conversão para JPG
    if file_name.endswith(".png"):
        file_path = os.path.join(directory, file_name)

    # Verifica se a imagem possui a extensão .tjpg
        tjpg_path = file_path[:-4] + ".tjpg"
        if os.path.exists(tjpg_path):
            addTrack(tjpg_path)

            tjpg_text = tjpg_to_jpg(tjpg_path)
            formatted_info = format_trackers_from_tjpg(tjpg_text)
            # Use formatted_info conforme necessário
        else:
            jpg_to_tjpg(file_path, cod)
            image = Image.open(file_path)

            # Tente decodificar os dados na imagem
            try:
                decoded_data = decode_fixed_length(image, message_length)
            except Exception as e:
                # Considerar logar o erro se necessário
                pass
            else:
                if is_logical_string(decoded_data, cod):
                    # A imagem já contém dados codificados lógicos.
                    # Aqui, você pode decidir não codificar novos dados, ou informar ao usuário, etc.
                    pass
                else:
                    # Nenhum dado codificado lógico encontrado. Codificando novos dados.
                    image_with_hidden_data = hide_data_with_delimiter(image, cod)
                    image_with_hidden_data.save(file_path, format='PNG')
                    # Dados codificados na imagem.
            # Lógica adicional aqui, se necessário


def process_images(directory):
    with ThreadPoolExecutor(max_workers=4) as executor:  # Ajuste max_workers conforme necessário
        # Submeta todas as tarefas ao executor
        futures = [executor.submit(process_image, file_name, directory) for file_name in os.listdir(directory)]
        # Espere até que todas sejam concluídas
        for future in futures:
            future.result()  # Pode adicionar tratamento de exceções aqui

class InfoDialog(QDialog): #Janelinha criada quando voce cria a imagem
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

    # Aqui Carrega as informações para mostrar na janelinha ao clicar na imagem
    def show_info(self, info_text=None):
        print("NOME DA IMAGEM ESCOLHIDA: " + self.np_var)
        tjpg_path = self.np_var[:-4] + ".tjpg"
        image = Image.open(self.np_var)
        encoded_image = Image.open(self.np_var)
        decoded_data = decode_fixed_length(encoded_image, message_length)
        print("Dados decodificados:", decoded_data)

        tjpg_text = tjpg_to_jpg(tjpg_path)
        formatted_info = format_trackers_from_tjpg(tjpg_text)

        # Inicialize info_text como uma string vazia se for None
        if info_text is None:
            info_text = "CRIADOR ORIGINAL DA IMAGEM:" + decoded_data +"\n"

        info_text += formatted_info

        # Crie um texto com as informações restantes
        info_text += "\nFLAG IA = " + str(iaChecker(self.np_var)) #Puxa a flag da imagem!

        # Crie e exiba o diálogo personalizado
        info_dialog = InfoDialog(info_text, self)
        info_dialog.exec()


#Funcionamento da Galeria
class ImageGallery(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()

        # Configurações iniciais da janela principal
        self.setWindowTitle("Galeria de Imagens")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Configura um scroll area para permitir rolagem
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Cria um widget para o conteúdo rolável
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Itera sobre os caminhos das imagens
        row, col = 0, 0
        for img_path in image_paths:
            # Carrega a imagem usando QPixmap
            pixmap = QPixmap(img_path)
            image_info = os.path.basename(img_path)

            # Cria um frame para a imagem com estilo personalizado
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: #2a82da;
                    border-radius: 5px;
                }
            """)

            frame_layout = QVBoxLayout(frame)

            # Cria uma etiqueta de imagem clicável e a adiciona ao frame
            img_label = ClickableImage(pixmap.scaled(150, 150, Qt.KeepAspectRatio), image_info, "", img_path)
            frame_layout.addWidget(img_label, alignment=Qt.AlignCenter)

            # Adiciona o frame ao layout da área rolável
            self.scroll_layout.addWidget(frame, row, col)

            # Atualiza as posições de coluna e linha
            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Exibe a janela
        self.show()


#Funcao principal
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

        # Cria um rótulo (label) para o título
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 10, 721, 81))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)

        # Cria um rótulo (label) para alguma descrição
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 160, 721, 81))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_2.setFont(font1)

        # Cria um campo de entrada de texto (LineEdit)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(450, 190, 150, 25))

        # Cria um botão (PushButton)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(635, 190, 100, 25))

        # Cria uma visualização gráfica (GraphicsView) com uma imagem
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(240, 260, 358, 240))

        # Cria uma cena gráfica (GraphicsScene) e adiciona uma imagem (pixmap)
        self.scene = QGraphicsScene(self.graphicsView)
        pixmap = QPixmap("iconqT.png")
        self.scene.addPixmap(pixmap)
        self.graphicsView.setScene(self.scene)

        # Cria um rótulo (label) para algum texto
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(230, 490, 400, 51))

        # Configura o widget central na janela principal
        PVPI.setCentralWidget(self.centralwidget)

        # Cria uma barra de status (StatusBar)
        self.statusbar = QStatusBar(PVPI)
        self.statusbar.setObjectName(u"statusbar")
        PVPI.setStatusBar(self.statusbar)

        # Traduz as strings (rótulos, botões, etc.) para o idioma desejado
        self.retranslateUi(PVPI)

        # Conecta os slots e sinais automaticamente (geralmente usado para eventos)
        QMetaObject.connectSlotsByName(PVPI)
# Descricao dos Labels e Titulos
    def retranslateUi(self, PVPI):
        PVPI.setWindowTitle(QCoreApplication.translate("PVPI", u"PVPI", None))
        self.label.setText(QCoreApplication.translate("PVPI", u"     Bem-vindo a Plataforma PVPI", None))
        self.label_2.setText(QCoreApplication.translate("PVPI", u"Por favor, insira o diret\u00f3rio das imagens que deseja visualizar:", None))
        self.pushButton.setText(QCoreApplication.translate("PVPI", u"Procurar", None))
        self.label_3.setText(QCoreApplication.translate("PVPI", u"Feito com \u2764\ufe0f, Por Nicolas Sales, Wyllgner França, Jader Louis - Versao 0.0.1", None))


# Define a classe MainWindow que herda de QMainWindow e Ui_PVPI
class MainWindow(QMainWindow, Ui_PVPI):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Inicializa a interface do usuário definida em Ui_PVPI
        self.setupUi(self)

        # Define estilos CSS para elementos da interface
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

        # Conecta o evento de clique do botão a uma função
        self.pushButton.clicked.connect(self.on_buttonClick)

    # Função chamada quando o botão é clicado
    def on_buttonClick(self):
        # Abre uma janela de seleção de diretório e obtém o diretório escolhido pelo usuário
        directory = QFileDialog.getExistingDirectory(self, "Selecionar diretório")

        # Define o diretório selecionado no campo de texto
        self.lineEdit.setText(directory)

        # Processa as imagens no diretório e abre a galeria de imagens
        process_images(directory)
        self.openImageGallery(directory)

    # Função para abrir a galeria de imagens
    def openImageGallery(self, directory):
        # Converte imagens JPG para PNG no diretório selecionado
        jpg_to_png(directory)

        # Verifica se o diretório existe
        if os.path.exists(directory):
            # Lista de extensões de arquivo de imagem válidas
            valid_image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]

            # Obtém todos os arquivos no diretório e filtra por extensões de arquivo de imagem
            image_paths = [os.path.join(directory, f) for f in os.listdir(directory)
                           if os.path.isfile(os.path.join(directory, f)) and any(
                    f.lower().endswith(ext) for ext in valid_image_extensions)]

            # Verifica se há imagens para exibir
            if image_paths:
                # Cria uma instância da classe ImageGallery com os caminhos das imagens
                self.gallery = ImageGallery(image_paths)

                # Exibe a galeria de imagens
                self.gallery.show()

                # Fecha a janela principal
                self.close()
            else:
                # Exibe uma mensagem de aviso se não houver imagens no diretório
                QMessageBox.warning(self, "Sem imagens", "Não há imagens no diretório selecionado.")
        else:
            # Exibe uma mensagem de aviso se o diretório selecionado não existir
            QMessageBox.warning(self, "Diretório não encontrado", "O diretório selecionado não existe.")


# Função para formatar informações de trackers a partir de um texto em tjpg_text
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


# Bloco de código principal
if __name__ == "__main__":
    # Cria uma instância de QApplication
    app = QApplication(sys.argv)

    # Define um tema escuro para a aplicação (supondo que a função set_dark_theme exista)
    set_dark_theme(app)

    # Cria uma instância da classe MainWindow
    mainWin = MainWindow()

    # Exibe a janela principal
    mainWin.show()

    # Inicia o loop de eventos da aplicação
    sys.exit(app.exec())