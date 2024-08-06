def main():
    nome_arq = input("Qual o nome do arquivo:   ")
    saida = open(nome_arq, 'wb')
    campo = input('Qual seu sobrenome:   ')
    while campo != '':
        buffer = ''
        buffer = buffer + campo + '|' 
        campo = input('Qual seu nome:   ')
        buffer = buffer + campo + '|'
        campo = input('Qual seu endereço:   ')
        buffer = buffer + campo + '|'
        campo = input('Qual seu cidade:   ')
        buffer = buffer + campo + '|'
        campo = input('Qual seu estado:   ')
        buffer = buffer + campo + '|'
        campo = input('Qual seu cep:   ')
        buffer = buffer + campo + '|'
        buffer = buffer.encode()
        tam = len(buffer)
        tam = tam.to_bytes(2)
        saida.write(tam)
        saida.write(buffer)
        campo = input('Qual seu sobrenome:   ')
    saida.close()

def le_registros():
    try:
        nome_arq = input('Qual nome do arquivo:   ')
        entrada = open(nome_arq, 'rb')
    except FileExistsError:
        print('Arquivo não encontrado')
    else:
        buffer = leia_reg(entrada)
        while buffer != '':
            buffer = buffer.split(sep='|')
            for x in buffer:
                if x != '':
                    print('Campo: ' + x )
            buffer = leia_reg(entrada)
        entrada.close()
                

def leia_reg(entrada):
    tam = entrada.read(2)
    tam = int.from_bytes(tam)
    if tam > 0:
        buffer = entrada.read(tam)
        buffer = buffer.decode()
        return buffer
    else:
        return ''
    