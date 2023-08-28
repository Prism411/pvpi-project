import cv2
import numpy as np
def detect_inconsistent_texture(image):
    # Carregar a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Aplicar o filtro de detecção de borda (por exemplo, Canny)
    edges = cv2.Canny(image, threshold, threshold * 2)

    # Calcular a porcentagem de pixels ativos nas bordas
    edge_percentage = np.sum(edges) / (image.shape[0] * image.shape[1]) * 100

    # Definir um limiar para detectar textura inconsistente
    if edge_percentage > 10:  # Ajuste o limiar conforme necessário
        return True
    else:
        return False

def detect_repetitive_patterns(image_path, threshold=0.8):
    # Carregar a imagem em escala de cinza
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Aplicar detecção de borda (Canny)
    edges = cv2.Canny(image, 50, 150)

    # Calcular a porcentagem de pixels ativos nas bordas
    edge_percentage = np.sum(edges) / (image.shape[0] * image.shape[1])

    # Se a porcentagem for maior que o limiar, considerar como padrão repetitivo
    if edge_percentage > threshold:
        return True
    else:
        return False

image = cv2.imread(image_path)

    # Converter a imagem de BGR para HSV (matiz, saturação, valor)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir faixa de cores vibrantes (vermelho, amarelo, verde, azul)
    lower_vibrant = np.array([0, 100, 100])
    upper_vibrant = np.array([120, 255, 255])

    # Criar uma máscara para cores vibrantes
    mask = cv2.inRange(hsv_image, lower_vibrant, upper_vibrant)

    # Calcular a porcentagem de pixels vibrantes na imagem
    vibrant_percentage = np.sum(mask == 255) / (image.shape[0] * image.shape[1]) * 100

    # Se a porcentagem for maior que o limiar, considerar como uso intenso de cores vibrantes
    if vibrant_percentage > threshold:
        return True
    else:
        return False


def main(image_path):
    # Carregar a imagem
    image = carregar_imagem(image_path)

    # Realizar as detecções
    inconsistent_texture = detect_inconsistent_texture(image)
    repetitive_patterns = detect_repetitive_patterns(image)
    vibrant_colors = detect_vibrant_colors(image)

    # Imprimir resultados
    if inconsistent_texture:
        print("Textura inconsistente detectada.")
    if repetitive_patterns:
        print("Padrões repetitivos detectados.")
    if vibrant_colors:
        print("Uso intenso de cores vivas e contrastantes detectado.")

# Caminho da imagem a ser analisada
caminho_da_imagem = "caminho/para/sua/imagem.png"
main(caminho_da_imagem)
