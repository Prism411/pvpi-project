# Importação da biblioteca subprocess, que permite a execução de comandos do sistema operacional.
import subprocess
# Importação da biblioteca platform, que permite obter informações sobre a plataforma/sistema operacional atual.
import platform

# Obtenção do nome do sistema operacional atual (e.g., 'Windows', 'Linux').
sistema_operacional = platform.system()

# Definição de uma função que busca o número serial da placa-mãe.
def numero_placa_mae():
    # Verificação se o sistema operacional atual é Windows.
    if sistema_operacional == "Windows":
        # Definição do comando que será executado para obter o número serial da placa-mãe.
        command = 'wmic baseboard get serialnumber'

        try:
            # Execução do comando no terminal e captura da saída.
            result = subprocess.check_output(command, shell=True, text=True)
            # Processamento da string resultante para extrair o número serial. A saída é dividida em linhas e o serial é geralmente encontrado na terceira linha.
            serial_number = result.strip().split('\n')[2].strip()
            # Retorno do número serial obtido.
            return serial_number
        # Tratamento de exceção para o caso de o comando falhar.
        except subprocess.CalledProcessError as e:
            # Retorno de None (nulo) se houver um erro na execução do comando.
            return None
    # Se o sistema operacional não for Windows, a função retorna None, pois o método implementado é específico para Windows.
    else:
        return None

# Chamada da função para obter o número serial e armazenamento do valor retornado na variável 'serial_number'.
serial_number = numero_placa_mae()

# DEBUG
#print("Codigo original: ")
#print(serial_number)
#print()
