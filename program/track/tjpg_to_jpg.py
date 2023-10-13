# Bibliotecas usadas no script
#
# Pillow para a visualização da imagem
# io para o gerenciamento dos dados JPG da imagem em um arquivo temporário
from PIL import Image
from io import BytesIO

# Função para converter arquivo de imagem com extensão personalizada para .jpg
# Tem como objetivo mostrar a informação da imagem e voltar os dados do header
# Pode ser feito tanto pelo output pelo command line ou pelo retorno da função
# (a primeira opção deve-se ser feito tirando os comentários de teste do print)
def tjpg_to_jpg(image):
    # Abra o arquivo personalizado para leitura binária
    with open(image, 'rb') as custom_img_file:
        # Leia todo o conteúdo do arquivo personalizado
        custom_img_data = custom_img_file.read()

    # Localize o delimitador entre o cabeçalho e os dados da imagem
    delimiter = b'#\n'  # Use um delimitador adequado para separar o cabeçalho dos dados da imagem

    # Divida o conteúdo do arquivo personalizado usando o delimitador
    header_bytes, image_data = custom_img_data.split(delimiter, 1)

    # Decodifique o cabeçalho de bytes para uma string UTF-8
    header_info = header_bytes.decode('utf-8')

    # ONLY TEST: Exiba as informações do cabeçalho
    # 
    # print("Informações do Cabeçalho:")
    # print(header_info)

    # Use BytesIO para criar um objeto de arquivo temporário a partir dos dados da imagem
    # image_file = BytesIO(image_data)

    # Abra a imagem usando a biblioteca Pillow (PIL)
    # image = Image.open(image_file)

    # Exiba a imagem
    # image.show()

    # Feche o objeto de arquivo temporário
    # image_file.close()

    return header_info