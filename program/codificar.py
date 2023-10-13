import hashlib

import numpy as np
import subprocess
import platform

def numero_placa_mae():
    operating_system = platform.system()
    if operating_system == "Windows":
        command = 'wmic baseboard get serialnumber'

        try:
            result = subprocess.check_output(command, shell=True, text=True)
            motherboard_number = result.strip().split('\n')[2].strip()
            return motherboard_number
        except subprocess.CalledProcessError as e:
            return None
    else:
        return None

# Verifica se o número é primo
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

# Cria uma sequência de números primos
def prime_sequence(n):
    sequence = []
    num = 2
    while len(sequence) < n:
        if is_prime(num):
            sequence.append(num)
        num += 1
    return sequence

# Cria uma chave do tamanho da placa-mãe com os números primos
def fill_matrix_with_primes(tam):
    prime_numbers = prime_sequence(tam * tam)
    key = np.array(prime_numbers).reshape((tam, tam))
    return key

# Faz a multiplicação do código ASCII com a chave e cria um código criptografado
def cripto():
    vet_aux = []
    codigo = numero_placa_mae()
    tam = len(codigo)
    vet = []
    for i, v in enumerate(codigo):
        x = ord(v)
        vet.append(x)
        vet_aux.append(x)

    result_matrix = fill_matrix_with_primes(tam)
    vet_np = np.array(vet_aux)
    result_vector = np.dot(result_matrix, vet_np)
    return result_vector

# Transforma o código criptografado em uma sequência binária
def nume_binary():
    cript = cripto()
    binary_sequence = []
    for numero in cript:
        binary = bin(numero)[2:]
        len_bi = len(binary)
        rlen_bi = bin(len_bi)[2:]
        rlen_bi = rlen_bi.zfill(8)
        binary_sequence.append(rlen_bi)
        binary_sequence.append(binary)
    return binary_sequence

def seq_bin():
    binary_sequence = nume_binary()
    return ''.join(binary_sequence)

def bin_to_10_letter_word(binary_string):
    # Calcular o hash MD5 da sequência binária (pode ser usado outro algoritmo de hash)
    hash_value = hashlib.md5(binary_string.encode()).hexdigest()

    # Selecionar os primeiros 10 caracteres do hash para formar a palavra
    ten_letter_word = hash_value[:10]

    return ten_letter_word
def codificar():
    x = seq_bin()
    output_string = bin_to_10_letter_word(x)
    return output_string
