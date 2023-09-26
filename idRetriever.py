import wmi

def get_motherboard_serial():
    # Conectando ao WMI
    c = wmi.WMI()

    # Obtendo informações da placa-mãe
    board_info = c.Win32_BaseBoard()[0]
    return board_info.SerialNumber

if __name__ == '__main__':
    # Se o script for executado diretamente, imprime o número de série
    print("Número de Série da Placa-Mãe (Windows):", get_motherboard_serial())
