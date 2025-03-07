# Criptografia Assimétrica usando RSA

Este repositório apresenta uma implementação simples da criptografia assimétrica usando o algoritmo RSA em Python. O projeto consiste em dois programas: um cliente e um servidor que se comunicam de forma segura trocando mensagens criptografadas.

## Visão Geral
O cliente (Alice) e o servidor (Bob) geram pares de chaves RSA (pública e privada) e trocam suas chaves públicas. Em seguida, o cliente envia uma mensagem criptografada para o servidor. O servidor decripta a mensagem, a converte para maiúsculas, criptografa novamente e a envia de volta ao cliente.

## Tecnologias Utilizadas
- Python 3
- Biblioteca `socket` para comunicação em rede
- Algoritmo RSA para criptografia e decriptação

## Como Funciona
1. **Geração de Chaves RSA**:
   - Cada parte gera um par de chaves RSA (pública e privada).
   - A chave pública é compartilhada com a outra parte.
2. **Troca de Mensagens**:
   - O cliente digita uma mensagem.
   - A mensagem é criptografada usando a chave pública do servidor e enviada.
   - O servidor decripta a mensagem com sua chave privada.
   - A mensagem é convertida para maiúsculas e criptografada novamente com a chave pública do cliente.
   - O cliente recebe a mensagem criptografada e a decripta com sua chave privada.

## Executando o Projeto
### 1. Configurar o Servidor
Execute o seguinte comando para iniciar o servidor:
```bash
python servidor.py
```
O servidor ficará aguardando conexões na porta 1300.

### 2. Executar o Cliente
Em outro terminal, execute:
```bash
python cliente.py
```
Digite a mensagem que deseja enviar ao servidor.

### 3. Exemplo de Saída
**No Cliente:**
```
Chave pública do cliente enviada para o servidor: (e, n)
Chave pública do servidor recebida: (e, n)
Digite a mensagem para enviar ao servidor: hello
Mensagem criptografada recebida do servidor: [numeros]
Mensagem decriptografada recebida do servidor: HELLO
```

**No Servidor:**
```
Servidor TCP (RSA) aguardando conexões na porta 1300...
Conexão recebida de ('IP', PORTA)
Chave pública recebida do cliente: (e, n)
Mensagem decriptografada do cliente: hello
Mensagem em maiúsculas: HELLO
Mensagem criptografada (maiúsculas) enviada ao cliente: [numeros]
```

## Melhorias Futuras
- Implementar tamanhos de chaves maiores para maior segurança.
- Utilizar bibliotecas como `pycryptodome` para otimização.
- Adicionar suporte a mensagens mais longas.

## Autor
- Carlos Baroni Piolla - 082200013
- Thiago Cardoso Hanna - 082200021
- Guilherme Silveira Cavinato - 082200032
- Bruna dos Santos Freitas - 082200015

