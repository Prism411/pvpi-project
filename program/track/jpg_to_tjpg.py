from program.codificar import cripto, fill_matrix_with_primes, nume_binary, codificar
from program.codigo import numero_placa_mae
import hashlib

def jpg_to_tjpg(image,codigo):
    # Abra o arquivo JPG existente para leitura binária
    with open(image, 'rb') as jpg_file:
        # Leia o conteúdo do arquivo JPG
        jpg_data = jpg_file.read()

    # Crie um cabeçalho de informações adicionais
    header_info = "1" + "|" + codigo + "#\n"
    # separa o nome do arquivo imagem com a sua extensão
    image_name, _ = image.split(".")

    # Abra um novo arquivo com extensão personalizada
    with open(f'{image_name}.tjpg', 'wb') as new_file:
        # Escreva o cabeçalho no novo arquivo
        new_file.write(header_info.encode('utf-8'))
        
        # Escreva os dados do JPG original no novo arquivo
        new_file.write(jpg_data)

    #print("Arquivo personalizado criado com sucesso.")
