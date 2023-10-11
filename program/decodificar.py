import numpy as np
from funcao import result

matriz_b = result()

print()
print("Resultado da descriptografia LU:")
print(matriz_b)


ascii_string = ""
for value in matriz_b:
    rounded_value = int(round(value))
    ascii_char = chr(rounded_value)
    ascii_string += ascii_char
    
print()
print("Mensagem descriptografiado:")
print(ascii_string)

