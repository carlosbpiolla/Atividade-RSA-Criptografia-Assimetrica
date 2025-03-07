import random
import math
from socket import *

# Função para verificar se um número é primo
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Função para gerar um número primo aleatório
def gerar_primo():
    while True:
        num = random.randint(2**12, 2**13)  # Número grande, mas não tão grande quanto 4096 bits
        if is_prime(num):
            return num

# Função para calcular o MDC (Máximo Divisor Comum)
def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

# Função para calcular o inverso modular
def inverso_modular(a, m):
    for i in range(2, m):
        if (a * i) % m == 1:
            return i
    return None

# Função para gerar as chaves pública e privada RSA
def gerar_chaves():
    p = gerar_primo()
    q = gerar_primo()

    while p == q:
        q = gerar_primo()

    # Calculando n e a função totiente
    n = p * q
    totiente = (p - 1) * (q - 1)

    # Escolher e tal que 1 < e < totiente e mdc(e, totiente) = 1
    e = 65537  # Usamos 65537 porque é um número comum e eficiente para e
    while mdc(e, totiente) != 1:
        e = random.randint(2, totiente)

    # Calcular d tal que (e * d) % totiente = 1
    d = inverso_modular(e, totiente)

    return (e, n), (d, n)  # Retorna a chave pública (e, n) e a chave privada (d, n)

# Função de criptografia RSA
def criptografar(mensagem, chave_publica):
    e, n = chave_publica
    return [pow(ord(char), e, n) for char in mensagem]

# Função de decriptação RSA
def decriptografar(mensagem_criptografada, chave_privada):
    d, n = chave_privada
    return ''.join([chr(pow(char, d, n)) for char in mensagem_criptografada])


# Código do Cliente (Alice) com Criptografia RSA
def cliente():
    # Gerando chaves pública e privada
    chave_publica, chave_privada = gerar_chaves()

    # Conectando ao servidor
    serverName = '10.1.70.15'
    serverPort = 1300
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    # Enviando a chave pública para o servidor
    clientSocket.send(str(chave_publica).encode())
    print(f"Chave pública do cliente enviada para o servidor: {chave_publica}")

    # Recebendo a chave pública do servidor
    chave_publica_servidor = eval(str(clientSocket.recv(65000), 'utf-8'))
    print(f"Chave pública do servidor recebida: {chave_publica_servidor}")

    # O cliente digita a mensagem
    mensagem = input("Digite a mensagem para enviar ao servidor: ")

    # Criptografando a mensagem com a chave pública do servidor
    mensagem_criptografada = criptografar(mensagem, chave_publica_servidor)

    # Enviando a mensagem criptografada para o servidor
    clientSocket.send(str(mensagem_criptografada).encode())

    # Recebendo a mensagem criptografada do servidor
    mensagem_criptografada_do_servidor = eval(str(clientSocket.recv(65000), 'utf-8'))
    print(f"Mensagem criptografada recebida do servidor: {mensagem_criptografada_do_servidor}")

    # Descriptografando a mensagem recebida usando a chave privada do cliente
    mensagem_decriptografada = decriptografar(mensagem_criptografada_do_servidor, chave_privada)
    print(f"Mensagem decriptografada recebida do servidor: {mensagem_decriptografada}")

    # Fechando a conexão
    clientSocket.close()

# Executando o cliente
cliente()
 