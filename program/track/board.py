import subprocess

# Função básica para pegar o número serial da placa mãe
#
# OBS: só funciona em sistemas Linux

def motherboardSerialNumber():
    try:
        # Executa o comando dmidecode e captura o output
        resultado = subprocess.check_output(['sudo', 'dmidecode', '-t', 'baseboard'], universal_newlines=True)

        # Divide o output em linhas
        linhas = resultado.split('\n')

        # Procura pela linha que contém o número de série
        for linha in linhas:
            if 'Serial Number' in linha:
                # Extrai o número de série
                numero_serie = linha.split(':')[-1].strip()
                return numero_serie

    except subprocess.CalledProcessError as e:
        # Lida com erros se o comando falhar
        print(f"Erro ao executar dmidecode: {e}")
    
    return None