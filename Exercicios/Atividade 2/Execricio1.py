def main():
    try:
        nome_arq = input('Qual o nome do arquivo:')
        entrada = open(nome_arq, 'rb')
    except FileNotFoundError:
        print('Arquivo não existente')
    else:
        chave = input('Fale um sobrenome:   ')
        achou = False
        buffer = leia_reg(entrada)
        while buffer != '' and achou != True:
            sobrenome = buffer.split(sep='|')[0]
            if chave == sobrenome:
                achou = True
            else:
                buffer = leia_reg(entrada)
        if achou == True:
            buffer = buffer.split(sep='|')
            print('registro encontrado:')
            for x in buffer:
                if x != '':
                    print('Campo: ' + x )
        else:
            print('Sobrenome não encontrado')
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