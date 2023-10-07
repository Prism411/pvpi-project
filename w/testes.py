import cv2

def bin_to_message(binary_str):
    """Converte uma representação binária em uma string."""
    return ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))

def reveal_data(image_path):
    """Revela a mensagem secreta da imagem."""

    image = cv2.imread(image_path)
    binary_data = ""
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = list(image[i][j])
            for n in range(3):
                binary_data += format(pixel[n], '08b')[-1]

    # Encontrando o delimitador que indica o final da mensagem secreta
    message_end = binary_data.find("00100011001000110010001100100011") # Delimitador '####'
    return bin_to_message(binary_data[:message_end])

# Substitua 'teste_imagem.png' pelo caminho da imagem que você deseja decodificar
image_path = 'teste_imagem.png'
retrieved_data = reveal_data(image_path)
print("Mensagem recuperada:", retrieved_data)
