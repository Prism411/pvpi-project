import cv2
import numpy as np
from scipy.linalg import lu

from luFactor import encode_to_unique_identifier, string_to_ascii_matrix, getSerialNumber, naturalIdentifier


def message_to_bin(message):
    """Converte uma string em uma representação binária."""
    return ''.join(format(ord(i), '08b') for i in message)

def bin_to_message(binary_str):
    """Converte uma representação binária em uma string."""
    return ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))

def hide_data(image, secret_message):
    """Esconde a mensagem secreta na imagem usando LSB."""

    n_bytes = image.shape[0] * image.shape[1] * 3 // 8

    if len(secret_message) > n_bytes:
        raise ValueError("Erro: bytes insuficientes! Use uma imagem maior ou menos dados.")

    secret_message += "####"  # Usado como delimitador
    data_index = 0
    binary_secret_msg = message_to_bin(secret_message)
    data_len = len(binary_secret_msg)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = list(image[i][j])
            for n in range(3):
                if data_index < data_len:
                    pixel[n] = int(format(pixel[n], '08b')[:-1] + binary_secret_msg[data_index], 2)
                    data_index += 1
            image[i][j] = tuple(pixel)

    return image

def reveal_data(image):
    """Revela a mensagem secreta da imagem."""

    binary_data = ""
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = list(image[i][j])
            for n in range(3):
                binary_data += format(pixel[n], '08b')[-1]

    # Encontrando o delimitador que indica o final da mensagem secreta
    message_end = binary_data.find("00100011001000110010001100100011") # Delimitador '####'
    return bin_to_message(binary_data[:message_end])

# Testando o código
serial = getSerialNumber()
print("Serial = ", serial)
matrix = string_to_ascii_matrix(serial)
print("Matriz = ", matrix)
P, L, U = lu(matrix)
print("P = ", P)
print("L = ", L)
print("U = ", U)

identifier = encode_to_unique_identifier(L, U)
print("Unique Identifier:", identifier)

image_path = 'teste_imagem.png'
image = cv2.imread(image_path)
secret_data = identifier

# Escondendo os dados
#image_with_hidden_data = hide_data(image.copy(), secret_data)
#cv2.imwrite('teste_imagem.png', image_with_hidden_data)

# Recuperando os dados
image_with_hidden_data = cv2.imread('teste_imagem.png')
retrieved_data = reveal_data(image_with_hidden_data)
print("Mensagem recuperada:", retrieved_data)

print("Mensagem recuperada:", retrieved_data)
print("Natural Identifier = ", naturalIdentifier(retrieved_data, image_path))
print("Original Identifier = ", naturalIdentifier(identifier, image_path))
