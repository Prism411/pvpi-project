# Bibliotecas usadas no script
#
# Pillow para a visualização da imagem
# io para o gerenciamento dos dados JPG da imagem em um arquivo temporário
from program.codificar import codificar



# Função para adicionar um novo número serial da placa mãe no track da imagem
# com formato personalizado
#
# Eventos captados: adicionar um novo track com o número, caso esse já exista,
# não adiciona-o
def addTrack(image):

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

    number = int(header_info[0])

    track = header_info.split("|")

    track.pop(0)

    motherboardNumber = codificar()

    # Se o número serial da placa mãe já estiver no tracking, não inserir-lo
    for t in track:
        if t == motherboardNumber:
           # print("MESMO DONO, ENCERRANDO APLICACAO!")
            return


    #print("Dono Diferente, Colocando dentro!")
    # Número inicial igual 5, volta para número 2, recomeçando o tracking
    if number == 5:
        number = 1
        track[number] = motherboardNumber

        newHeader = f"{number + 1}"

        for t in track:
            newHeader += "|" + t

        newHeader += "#\n"

        # Abra um novo arquivo com extensão personalizada
        with open(image, 'wb') as new_file:
            # Escreva o cabeçalho no novo arquivo
            new_file.write(newHeader.encode('utf-8'))
                
            # Escreva os dados do JPG original no novo arquivo
            new_file.write(image_data)
            
        return

    elif number >= len(track):

        track.append(motherboardNumber)
        newHeader = f"{number + 1}"

        for t in track:
            newHeader += "|" + t
        
        newHeader += "#\n"

        # Abra um novo arquivo com extensão personalizada
        with open(image, 'wb') as new_file:
            # Escreva o cabeçalho no novo arquivo
            new_file.write(newHeader.encode('utf-8'))
            
            # Escreva os dados do JPG original no novo arquivo
            new_file.write(image_data)

            # Se o número serial da placa mãe já estiver no tracking, não inserir-lo
        for t in track:
            if t == motherboardNumber:
                return
            
    else:
        
        track[number] = motherboardNumber
        newHeader = f"{number + 1}"

        for t in track:
            newHeader += "|" + t
        
        newHeader += "#\n"

        # Abra um novo arquivo com extensão personalizada
        with open(image, 'wb') as new_file:
            # Escreva o cabeçalho no novo arquivo
            new_file.write(newHeader.encode('utf-8'))
            
            # Escreva os dados do JPG original no novo arquivo
            new_file.write(image_data)