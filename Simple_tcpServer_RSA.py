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

# Função de decriptação RSA
def decriptografar(mensagem_criptografada, chave_privada):
    d, n = chave_privada
    return ''.join([chr(pow(char, d, n)) for char in mensagem_criptografada])

# Função para criptografar a mensagem
def criptografar(mensagem, chave_publica):
    e, n = chave_publica
    return [pow(ord(char), e, n) for char in mensagem]

# Código do Servidor (Bob) com Criptografia RSA
def servidor():
    # Gerando chaves pública e privada
    chave_publica, chave_privada = gerar_chaves()

    # Definindo a porta do servidor
    serverPort = 1300
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(5)
    print("Servidor TCP (RSA) aguardando conexões na porta 1300...\n")

    # Aceitando uma conexão do cliente
    connectionSocket, addr = serverSocket.accept()
    print(f"Conexão recebida de {addr}")

    # Recebendo a chave pública do cliente
    chave_publica_cliente = eval(str(connectionSocket.recv(65000), 'utf-8'))
    print(f"Chave pública recebida do cliente: {chave_publica_cliente}")

    # Enviando a chave pública do servidor para o cliente
    connectionSocket.send(str(chave_publica).encode())
    print(f"Chave pública do servidor enviada para o cliente: {chave_publica}")

    # Recebendo a mensagem criptografada do cliente
    sentence = connectionSocket.recv(65000)

    # Decriptografando a mensagem recebida (com a chave privada do servidor)
    mensagem_criptografada = eval(str(sentence, 'utf-8'))
    print(f"Mensagem Criptografada recebida do cliente: {mensagem_criptografada}")

    mensagem_decriptografada = decriptografar(mensagem_criptografada, chave_privada)
    print(f"Mensagem decriptografada do cliente: {mensagem_decriptografada}")

    # Convertendo a mensagem decriptografada para maiúsculas
    mensagem_maiuscula = mensagem_decriptografada.upper()
    print(f"Mensagem em maiúsculas: {mensagem_maiuscula}")

    # Criptografando novamente a mensagem maiúscula para enviar de volta ao cliente
    mensagem_criptografada_resposta = criptografar(mensagem_maiuscula, chave_publica_cliente)

    # Enviando a mensagem criptografada de volta para o cliente
    connectionSocket.send(str(mensagem_criptografada_resposta).encode())
    print(f"Mensagem criptografada (maiúsculas) enviada ao cliente: {mensagem_criptografada_resposta}")

    # Fechando a conexão
    connectionSocket.close()

# Executando o servidor
servidor()