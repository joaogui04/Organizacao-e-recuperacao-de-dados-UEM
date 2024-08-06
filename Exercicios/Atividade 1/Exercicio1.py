def escreve_campo():
   
    nome_arq = input("Nome do arquivo:   ")
    saida = open(nome_arq,'w')
    sobrenome = input("qual seu sobrenome:   ")
   
    while sobrenome != '':
        nome = input('Qual seu nome:   ')
        endereco = input('Qual seu endereco:   ')
        cidade = input('Qual sua cidade:   ')
        estado = input('Qual seu estado:   ')
        cep = input('Qual seu cep:   ')
        saida.write( nome + '|' + endereco + '|' + cidade + '|' + estado + '|' + cep + '|')
        sobrenome = input("qual seu sobrenome:   ")
    saida.close()

def le_campo():
    try:
        nome_arq = input('Nome do arquivo:   ')
        entrada = open(nome_arq, 'r')
    except FileNotFoundError:
        print('Arquivo não encontrado')
    else:
        campo = leia_campo(entrada)
        while campo != '':
            print(campo)
            campo = leia_campo(entrada)
    entrada.close()

def leia_campo(entrada):
    campo = ''
    c = entrada.read(1)
    while c != '' and c != '|':
        campo = campo + c
        c = entrada.read(1)
    return campo

