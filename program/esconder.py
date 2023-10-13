import cv2
import numpy as np

def encode_string_into_image(image_path, secret_message):
    # Certifique-se de que a mensagem não é muito longa para esta abordagem
    if len(secret_message) > 255:
        print("Mensagem muito longa!")
        return False

    # Carregue a imagem
    image = cv2.imread(image_path)

    # Escolha um canto da imagem para codificar a mensagem (por exemplo, os primeiros 10 pixels do canto superior esquerdo)
    corner = image[:10, :1]  # Isso seleciona uma pequena seção da imagem

    # Codifique o comprimento da mensagem no primeiro pixel
    corner[0, 0, :3] = len(secret_message)

    # Codifique a mensagem nos pixels restantes
    for i in range(len(secret_message)):
        char = secret_message[i]
        corner[i+1, 0, :3] = ord(char)

    # Grave a imagem modificada
    cv2.imwrite("encoded_image.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    return True

def decode_string_from_image(image_path):
    print("Decodificando...")

    # Carregue a imagem
    image = cv2.imread(image_path)

    # Selecione o mesmo canto que você usou para codificação
    corner = image[:10, :1]

    # Decodifique o comprimento da mensagem
    message_length = int(corner[0, 0, :3][0])

    # Decodifique a mensagem
    message = ""
    for i in range(message_length):
        code = corner[i+1, 0, :3]
        char = chr(int(code[0]))
        message += char

    return message

# Teste as funções
secret_message = "fddkkakak"  # A mensagem deve ter 10 caracteres ou menos para este exemplo
path_to_image = "teste_imagem.jpg"  # Coloque o caminho da sua imagem original aqui

#success = encode_string_into_image(path_to_image, secret_message)
#if success:
decoded_message = decode_string_from_image("encoded_image.jpg")
print(decoded_message)
#else:
    #print("Não foi possível codificar a mensagem.")
