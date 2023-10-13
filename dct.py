from PIL import Image
import binascii
import os
from multiprocessing import Pool
import re

cod = ()
def is_logical_string(s, keyword):
    # Verifica se a string pode ser codificada e decodificada em UTF-8 sem erros
    try:
        s = s.encode(encoding='utf-8').decode('utf-8')
    except UnicodeDecodeError:
        return False

    # Verifica a presença de uma palavra-chave específica
    if keyword.lower() in s.lower():
        return True

    # Verifica se a string contém um número excessivo de caracteres não alfanuméricos
    if re.search(r'[^a-zA-Z0-9 ]', s):
        non_alphanumeric_chars = len(re.findall(r'[^a-zA-Z0-9 ]', s))
        if non_alphanumeric_chars > len(s) / 2:  # Se mais da metade dos caracteres são não alfanuméricos
            return False

    return True  # A string passou em todas as verificações

# Function to convert text to binary
def text_to_bin(text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

# Function to convert binary to text
def bin_to_text(binary_data):
    str_data = ''
    for i in range(0, len(binary_data), 8):
        temp_data = binary_data[i:i + 8]
        decimal_data = int(temp_data, 2)
        str_data = str_data + chr(decimal_data)
    return str_data

# Function to modify the least significant bit of the pixel
def modify_pixel(pixel, binary_data, data_index):
    modified_pixel = []
    for i in range(0, 3):
        if data_index < len(binary_data):  # if there is still data to store, modify the pixel
            pixel_bin = format(pixel[i], '08b')  # convert the pixel value to binary
            new_pixel_bin = pixel_bin[:-1] + binary_data[data_index]  # replace the LSB with the data bit
            modified_pixel.append(int(new_pixel_bin, 2))  # convert back to integer
            data_index += 1
        else:
            modified_pixel.append(pixel[i])  # no more data to store, leave the pixel as it is
    return tuple(modified_pixel), data_index

# Function to hide data within the image
def hide_data_with_delimiter(image, data):

    # Convert the data to binary and add the delimiter
    binary_data = text_to_bin(data) + '1111111111111110'  # Delimiter is 16 '1's followed by '0'

    data_index = 0

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))[:3]  # get the RGB values of the pixel (ignoring alpha)
            modified_pixel, data_index = modify_pixel(pixel, binary_data, data_index)  # modify the pixel
            image.putpixel((x, y), modified_pixel + (pixel[3:] if len(pixel) == 4 else ()))  # put the modified pixel back in the image

            if data_index >= len(binary_data):  # if all data has been stored, return the image
                return image
    return image

# Function to decode data of a fixed length from the image
def decode_fixed_length(image, length):
    binary_data = ""
    data_length = length * 8  # Each character is 8 bits

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))[:3]  # get the RGB values of the pixel (ignoring alpha)
            for color in pixel:
                binary_data += (format(color, '08b')[-1])  # extract the LSB of each color channel

            # If we've extracted the amount of data we want, break from the loop
            if len(binary_data) >= data_length:
                break
        if len(binary_data) >= data_length:
            break

    binary_data = binary_data[:data_length]  # Trim any excess data we've collected

    return bin_to_text(binary_data)

# Usage
def main():
    # Carregue a imagem
    #img_path = 'real8.png'  # especifique o caminho para sua imagem PNG
    #image = Image.open(img_path)

    # Os dados a serem ocultados
    #data_to_hide = "123456789"

    # Oculte os dados na imagem
    #image_with_hidden_data = hide_data_with_delimiter(image, data_to_hide)

    # Salve a nova imagem no formato PNG
    output_image_path = 'real8_steganografed.png'  # especifique o caminho para a imagem de saída
    #image_with_hidden_data.save(output_image_path, format='PNG')

    # Carregue a imagem com dados ocultos
    encoded_image = Image.open(output_image_path)

    # Sabemos que o comprimento da mensagem original é de 9 caracteres
    message_length = 9

    # Decodifique os dados na imagem
    decoded_data = decode_fixed_length(encoded_image, message_length)

    #print("Dados decodificados:", decoded_data)


def convert_image(args):
    directory, filename = args  # Desempacotando os argumentos

    jpg_path = os.path.join(directory, filename)
    png_path = os.path.join(directory, os.path.splitext(filename)[0] + ".png")

    try:
        with Image.open(jpg_path) as img:
            img.save(png_path, 'PNG')
        os.remove(jpg_path)
        return f"{filename} convertido e excluído com sucesso."
    except Exception as e:
        return f"Não foi possível converter {filename}: {e}"

def jpg_to_png(directory):
    if not os.path.isdir(directory):
        #print("O diretório fornecido não existe.")
        return

    # Recupera todos os arquivos .jpg no diretório
    jpg_files = [(directory, f) for f in os.listdir(directory) if f.endswith('.jpg')]  # Agora, cada item é uma tupla

    # Usa um pool de processos para converter as imagens em paralelo
    with Pool() as pool:
        pool.map(convert_image, jpg_files)
        #for result in results:
        #print(result)


#jpg_to_png("C:\\Users\\jader\\Desktop\\estudos\\PROJETOALGEBRA\\pvpi-project\\program\\testeimg")
if __name__ == "__main__":
    main()



## a função asyncio.run() foi introduzida no Python 3.7, então você precisará de
## Python 3.7 ou mais recente para usar este código como está.