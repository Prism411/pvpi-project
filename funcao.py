import numpy as np
from codificar import fill_matrix_with_primes

def lu_decomposition(A):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    Li = np.zeros((n, n))
    Ui = np.zeros((n, n))

    for i in range(n):
        L[i, i] = 1.0
        
        for j in range(i, n):
            U[i, j] = A[i, j] - np.dot(L[i, :i], U[:i, j])

        for j in range(i + 1, n):
            L[j, i] = (A[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]

    return L, U

def lu_solve(L, U, b):
    n = len(L)
    
    # Resolve Ly = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
        y[i] /= L[i, i]
        
    
    # Resolve Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = y[i] - np.dot(U[i, i+1:], x[i+1:])
        x[i] /= U[i, i]
        

    return x

def binario_para_decimal(lista_binaria):
    decimais = []
    for binario in lista_binaria:
        decimal = int(binario, 2)  
        decimais.append(decimal)
    return decimais

def separar_numeros(input_str):
    resultado = []
    i = 0

    while i < len(input_str):
        tamanho = input_str[i:i+8]
        numero = input_str[i+8:i+8+int(tamanho, 2)]
        resultado.append(f'{numero}')
        i += 8 + int(tamanho, 2)

    return resultado

sequencia_binaria = return_data()
numero_decimal = separar_numeros(sequencia_binaria)
b= binario_para_decimal(numero_decimal)
print("sequencia binaria ja separada")
print(numero_decimal)
print()
print("binario para decimal")
print(b)

def result():
    return x

A= fill_matrix_with_primes()

L, U = lu_decomposition(A)
x = lu_solve(L, U, b)

#print("Solucao x:")
#print(L)
#print()
#print(U)
#print()
#print(x)

