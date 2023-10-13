import numpy as np
from scipy.linalg import lu
import base64

from idRetriever import get_motherboard_serial
from program.model import iaChecker


def getSerialNumber():
    return get_motherboard_serial()

def string_to_ascii_matrix(s):
    ascii_vals = [ord(c) for c in s]
    size = int(np.ceil(len(ascii_vals) ** 0.5))
    total_elements = size * size
    while len(ascii_vals) < total_elements:
        ascii_vals.append(0)
    return np.array(ascii_vals).reshape(size, size)

def ascii_matrix_to_string(matrix):
    flat_list = matrix.flatten().tolist()
    char_list = [chr(int(i)) for i in flat_list if int(i) != 0]
    return ''.join(char_list)

def encode_to_unique_identifier(L, U):
    # Convert matrix to string
    L_string = ','.join(map(str, L.flatten()))
    U_string = ','.join(map(str, U.flatten()))

    # Concatenate with delimiter and encode
    combined_string = L_string + "|" + U_string
    encoded_string = base64.b64encode(combined_string.encode()).decode()

    return encoded_string

def decode_from_unique_identifier(identifier):
    decoded_string = base64.b64decode(identifier).decode()
    L_string, U_string = decoded_string.split('|')  # Use '|' as delimiter

    L_list = list(map(float, L_string.split(',')))
    U_list = list(map(float, U_string.split(',')))

    size = int(np.sqrt(len(L_list)))
    L = np.array(L_list).reshape(size, size)
    U = np.array(U_list).reshape(size, size)

    return L, U

def get_original_from_LU(P, L, U):
    return np.dot(P, np.dot(L, U))

def getIaFlag(image_path):
    imagem = iaChecker(image_path)
    print(imagem)

def naturalIdentifier(identifier, image_path):
    flag = iaChecker(image_path)
    truncated_identifier = identifier[:10]  # pega as 10 primeiras letras do identifier
    return f"{truncated_identifier}-{flag}"


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
L_decoded, U_decoded = decode_from_unique_identifier(identifier)
reconstructed_matrix = get_original_from_LU(P, L_decoded, U_decoded)
reconstructed_string = ascii_matrix_to_string(reconstructed_matrix)
print("Reconstructed string:", reconstructed_string)
image_path = "teste_imagem.png"
print(naturalIdentifier(identifier, image_path))