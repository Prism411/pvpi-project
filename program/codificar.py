import numpy as np
from codigo import numero_placa_mae

codigo = numero_placa_mae()

tam = len(codigo)
vet = []  

def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_sequence(n):
    sequence = []
    num = 2
    while len(sequence) < n:
        if is_prime(num):
            sequence.append(num)
        num += 1
    return sequence

def fill_matrix_with_primes():
    prime_numbers = prime_sequence(tam * tam)
    key = np.array(prime_numbers).reshape((tam, tam))
    return key

def cripto(): 
    vet_aux = []
    for i, v in enumerate(codigo):
        x = ord(v)
        vet.append(x)
        vet_aux.append(x)

    result_matrix = fill_matrix_with_primes()
    vet_np = np.array(vet_aux)
    result_vector = np.dot(result_matrix, vet_np)
    return result_vector


def nume_binary(lista_numeros):
    binary_sequence = []
    for numero in lista_numeros:
        binary = bin(numero)[2:]
        len_bi = len(binary)
        rlen_bi = bin(len_bi)[2:]
        rlen_bi = rlen_bi.zfill(8)
        binary_sequence.append(rlen_bi)
        binary_sequence.append(binary)
    return binary_sequence

def lista_para_string(lista):
    return ''.join(lista)

def seq_bin():
    return output_string


cript= cripto()
binary_sequence = nume_binary(cript)
output_string = lista_para_string(binary_sequence)

key = fill_matrix_with_primes()
seq_bin()

print("KEY: ")
print(key)
print()
print("Codigo ASCII")
print(vet)
print()
print("Codigo Criptografado")
print(cript)
print()
print("sequncia binaria com o tamanho")
print(binary_sequence)
print()
print("sequncia binaria STR")
print(output_string)