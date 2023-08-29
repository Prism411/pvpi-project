import wmi

# Conectando ao WMI
c = wmi.WMI()

# Obtendo informações da placa-mãe
board_info = c.Win32_BaseBoard()[0]
serial_number = board_info.SerialNumber

print("Número de Série da Placa-Mãe (Windows):", serial_number)
