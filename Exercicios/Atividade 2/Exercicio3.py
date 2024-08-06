def main():
    try:
        nome_arq = input('Nome do arquivo:   ')
        arq = open(nome_arq, 'r+b')
    except FileNotFoundError:
        arq = open(nome_arq, 'w+b')
        total_reg = 0
        cab = total_reg.to_bytes(4)
        arq.write(cab)
    else: 
        cab = arq.read(4)
        total_reg = int.from_bytes(cab)
        print(total_reg)

    opcao = int(input('(1)inserir (2)buscar (3)sair:   '))
    while opcao < 3:
        if opcao == 1:
            
            reg = ''
            sobrenome = input('Qual seu sobrenome:  ')
            nome = input('Qual seu nome:  ')
            endereco = input('Qual seu endereco:  ')
            cidade = input('Qual sua cidade:  ')   
            cep = input('qual seu cep:  ')
            reg = reg + '|' + sobrenome + '|' + nome + '|' + endereco + '|' + cidade + '|' + cep + '|'
            reg = reg.encode()
            reg = reg.ljust(64, b'\0')
            offset = total_reg * 64 + 4
            arq.seek(offset)
            arq.write(reg)
            total_reg += 1
            arq.seek(0)
            arq.write(total_reg.to_bytes(4))
            opcao = int(input('(1)inserir (2)buscar (3)sair:   '))
        elif opcao == 2:
            rrn = int(input('Qual o RRN:   '))
            if rrn >= total_reg:
                raise('Erro esse rrn não existe')
            else:
                offset = rrn * 64 + 4
                arq.seek(offset)
                reg = (arq.read(64)).decode()
                reg = reg.rstrip('\0')
                reg = reg.split(sep='|')
            for campo in reg:
                if campo != '':
                    print(campo)
            alterar = input('Gostaria de alterar: S/N ')
            if alterar == 'S' or alterar == 's':
                reg = ''
                sobrenome = input('Qual seu sobrenome:  ')
                nome = input('Qual seu nome:  ')
                endereco = input('Qual seu endereco:  ')
                cidade = input('Qual sua cidade:  ')   
                cep = input('qual seu cep:  ')
                reg = reg + '|' + sobrenome + '|' + nome + '|' + endereco + '|' + cidade + '|' + cep + '|'
                reg = reg.encode()
                reg = reg.ljust(64, b'\0')
                offset = rrn * 64 + 4
                arq.seek(offset)
                arq.write(reg)
            opcao = int(input('(1)inserir (2)buscar (3)sair:   '))
        elif opcao == 3:
            arq.close()

            
            


