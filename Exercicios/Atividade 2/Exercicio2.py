def main():
    try:
        nome_arq = input('Qual o nome do arquivo:   ')
        entrada = open(nome_arq, 'rb')
    except FileNotFoundError:
        print('Arquivo não existente')
    else:
        cab = entrada.read(4)
        total_reg = int.from_bytes(cab)
        rrn = int(input('Qual RRN vai ser lido:   '))
        if rrn >= total_reg:
            print('Erro')
        
        offset = rrn * 64 + 4
        entrada.seek(offset)
        reg = (entrada.read(64)).decode()
        reg = reg.rstrip('\0')
        reg = reg.split(sep='|')
        for campo in reg:
            if campo != '':
                print('Campo: ' + campo)
    entrada.close()
    
            