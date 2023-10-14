import cv2
import numpy as np

def detect_inconsistent_texture(image, threshold=5000, limit=5):
    # Converter a imagem em escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar o filtro de detecção de borda (Canny)
    edges = cv2.Canny(gray_image, limit, limit * 2)

    # Calcular a porcentagem de pixels ativos nas bordas
    edge_percentage = np.sum(edges) / (image.shape[0] * image.shape[1]) * 100
    #print(edge_percentage)
    # Definir um limiar para detectar textura inconsistente
    if edge_percentage < threshold:
        return True #Da flag na IA.
    else:
        return False

def detect_lack_of_edges(image, threshold=4):
    # Converter a imagem em escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar detecção de borda (Canny)
    edges = cv2.Canny(gray_image, 50, 150)

    # Calcular a porcentagem de pixels ativos nas bordas
    edge_percentage = np.sum(edges) / (image.shape[0] * image.shape[1])

    # Se a porcentagem for maior que o limiar, considerar como padrão repetitivo
    #print(edge_percentage)
    if edge_percentage < threshold:
        return True #da flag que ela pode ser gerada por ia
    else:
        return False

def detect_vibrant_colors(image, threshold=17):
    # Converter a imagem de BGR para HSV (matiz, saturação, valor)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definir faixa de cores vibrantes (vermelho, amarelo, verde, azul)
    lower_vibrant = np.array([0, 100, 100])
    upper_vibrant = np.array([120, 255, 255])

    # Criar uma máscara para cores vibrantes
    mask = cv2.inRange(hsv_image, lower_vibrant, upper_vibrant)

    # Calcular a porcentagem de pixels vibrantes na imagem
    vibrant_percentage = np.sum(mask == 255) / (image.shape[0] * image.shape[1]) * 100
    #print(vibrant_percentage)
    # Se a porcentagem for maior que o limiar, considerar como uso intenso de cores vibrantes
    if vibrant_percentage > threshold or vibrant_percentage < 1.0:
        return True #Posivo gerada por IA!!
    else:
        return False
def resolutionChecker(image):
        width, height, _ = image.shape
        if width == 1024 and height == 1024:
            #print("1024x1024 Positivo")
            return True
        else:
            return False


import cv2


def iaChecker(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    weight = 0
    output_string = ""

    # Realizar as detecções
    inconsistent_texture = detect_inconsistent_texture(image)
    repetitive_patterns = detect_lack_of_edges(image)
    vibrant_colors = detect_vibrant_colors(image)
    resolutionAnalysis = resolutionChecker(image)

    # Imprimir resultados
    if inconsistent_texture:  # FEITO CALIBRAGEM PARA IA
        output_string += "Textura inconsistente detectada.\n"
        weight = weight + 0.25000
        # adicionar peso de probabilidade de que ela possa ser uma IA.

    if repetitive_patterns:  # FEITO CALIBRAGEM PARA IA
        output_string += "Padrões repetitivos detectados.\n"
        weight = weight + 0.2500
        # adicionar peso de probabilidade que ela pode ser uma IA.

    if vibrant_colors:  # FEITO CALIBRAGEM PARA IA
        output_string += "Uso intenso de cores vivas e contrastantes detectado.\n"
        weight = weight + 0.1500
        # adicionar peso de probabilidade que ela pode ser uma IA.

    if resolutionAnalysis:
        output_string += "Detectado Resolucao Suspeita\n"
        weight = weight + 0.5005

    output_string += f"A probabilidade da imagem ser uma IA é de aproximadamente: {weight * 100}%\n"

    if weight > 0.50:
        output_string += "A imagem provavelmente foi gerada por IA"
        return True, f"Prob. de IA: {weight * 100}%"
    else:
        output_string += "A imagem provavelmente não foi gerada por IA"
        return False,f"Prob. de IA: {weight * 100}%"

##geradaporIA = 0
##imagemNatural = 0
##i = 1

##
##for i in range(1,130):
  ##  caminho_da_imagem = "images_data_base\\real_images\\real ({0}).jpg".format(i)
    ##print("Carregando Imagem: real ({0})".format(i))

  ##  if imagem:
    ##    geradaporIA += 1
  ##  else:
   ##     imagemNatural += 1

    ##print("Imagem geradas por IA:", geradaporIA)
    ##print("Imagem Natural:", imagemNatural)

