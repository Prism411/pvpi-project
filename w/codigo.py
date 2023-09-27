import subprocess
import platform

sistema_operacional = platform.system()

def numero_placa_mae():
    if sistema_operacional == "Windows":
        command = 'wmic baseboard get serialnumber'

        try:
            result = subprocess.check_output(command, shell=True, text=True)
            serial_number = result.strip().split('\n')[2].strip()
            return serial_number
        except subprocess.CalledProcessError as e:
            return None
    else:
        return None

serial_number = numero_placa_mae()

print("Codigo original: ")
print(serial_number)
print()