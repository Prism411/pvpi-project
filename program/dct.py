# Importação das bibliotecas necessárias.
from PIL import Image  # Para manipular imagens.
import binascii  # Para conversões de binário para ASCII e vice-versa.
import os  # Para interação com o sistema operacional.
from multiprocessing import Pool  # Para processamento paralelo.
import re  # Para usar expressões regulares.

cod = ()  # Uma tupla vazia, a utilização não está clara sem o resto do contexto do código.

# Função que verifica se uma string é lógica baseada em várias condições.
def is_logical_string(s, keyword):
    # Tentativa de codificar e decodificar a string em UTF-8.
    try:
        s = s.encode(encoding='utf-8').decode('utf-8')
    except UnicodeDecodeError:  # Se houver um erro, a função retorna Falso.
        return False

    # Verifica se a palavra-chave fornecida está presente na string.
    if keyword.lower() in s.lower():
        return True

    # Procura por caracteres não alfanuméricos na string.
    if re.search(r'[^a-zA-Z0-9 ]', s):
        non_alphanumeric_chars = len(re.findall(r'[^a-zA-Z0-9 ]', s))
        # Se mais da metade dos caracteres são não alfanuméricos, retorna Falso.
        if non_alphanumeric_chars > len(s) / 2:
            return False

    return True  # Se passar todas as verificações, retorna Verdadeiro.

# Função para converter texto em binário.
def text_to_bin(text):
    # Converte cada caractere em sua representação binária e junta tudo em uma única string.
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

# Função para converter binário em texto.
def bin_to_text(binary_data):
    str_data = ''
    # Processa cada byte de dados binários (8 bits), converte em decimal e obtém o caractere correspondente.
    for i in range(0, len(binary_data), 8):
        temp_data = binary_data[i:i + 8]
        decimal_data = int(temp_data, 2)
        str_data = str_data + chr(decimal_data)
    return str_data

# Função para modificar o bit menos significativo do pixel.
def modify_pixel(pixel, binary_data, data_index):
    modified_pixel = []
    for i in range(0, 3):
        if data_index < len(binary_data):  # Se ainda houver dados para armazenar, modifica o pixel.
            pixel_bin = format(pixel[i], '08b')  # Converte o valor do pixel para binário.
            new_pixel_bin = pixel_bin[:-1] + binary_data[data_index]  # Substitui o LSB com o bit de dados.
            modified_pixel.append(int(new_pixel_bin, 2))  # Converte novamente para inteiro.
            data_index += 1
        else:
            modified_pixel.append(pixel[i])  # Se não houver mais dados, mantém o pixel inalterado.
    return tuple(modified_pixel), data_index

# Função para ocultar dados na imagem.
def hide_data_with_delimiter(image, data):
    # Converte os dados para binário e adiciona um delimitador.
    binary_data = text_to_bin(data) + '1111111111111110'  # O delimitador é 16 '1's seguido por '0'.

    data_index = 0

    # Percorre cada pixel da imagem.
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))[:3]  # Obtém os valores RGB do pixel (ignorando o alfa).
            modified_pixel, data_index = modify_pixel(pixel, binary_data, data_index)  # Modifica o pixel.
            # Coloca o pixel modificado de volta na imagem.
            image.putpixel((x, y), modified_pixel + (pixel[3:] if len(pixel) == 4 else ()))

            # Se todos os dados foram armazenados, retorna a imagem.
            if data_index >= len(binary_data):
                return image
    return image

# Função para decodificar dados de comprimento fixo da imagem.
def decode_fixed_length(image, length):
    binary_data = ""
    data_length = length * 8  # Cada caractere tem 8 bits.

    # Extrai os bits menos significativos dos pixels da imagem até atingir o comprimento desejado.
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))[:3]  # Obtém os valores RGB do pixel (ignorando o alfa).
            for color in pixel:
                binary_data += (format(color, '08b')[-1])  # Extrai o LSB de cada canal de cor.

            if len(binary_data) >= data_length:
                break
        if len(binary_data) >= data_length:
            break

    binary_data = binary_data[:data_length]  # Remove quaisquer dados excessivos coletados.

    return bin_to_text(binary_data)  # Converte os dados binários de volta para texto.

# Função para converter imagens.
def convert_image(args):
    directory, filename = args  # Descompacta os argumentos.

    jpg_path = os.path.join(directory, filename)  # Caminho completo para o arquivo JPG.
    png_path = os.path.join(directory, os.path.splitext(filename)[0] + ".png")  # Caminho para o novo arquivo PNG.

    try:
        with Image.open(jpg_path) as img:  # Abre a imagem JPG.
            img.save(png_path, 'PNG')  # Salva a imagem em formato PNG.
        os.remove(jpg_path)  # Remove o arquivo JPG original.
        return f"{filename} convertido e excluído com sucesso."
    except Exception as e:  # Em caso de erro, retorna uma mensagem.
        return f"Não foi possível converter {filename}: {e}"

# Função para converter todas as imagens JPG em um diretório para PNG.
def jpg_to_png(directory):
    if not os.path.isdir(directory):  # Verifica se o diretório existe.
        #print("O diretório fornecido não existe.")
        return

    # Recupera todos os arquivos .jpg no diretório especificado.
    jpg_files = [(directory, f) for f in os.listdir(directory) if f.endswith('.jpg')]  # Cada item é uma tupla.

    # Usa processamento paralelo para converter as imagens.
    with Pool() as pool:
        pool.map(convert_image, jpg_files)  # Converte as imagens.



