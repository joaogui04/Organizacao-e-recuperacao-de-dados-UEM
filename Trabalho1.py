from dataclasses import dataclass
import sys

@dataclass
class Regs:
    offset : int
    tamanho: int
    offset_prox : int

# -------------- MAIN ---------------------------------------------------------------- 
def main(lista_exe:str):
    try: 
        ARQ = open('dados.dat', 'r+b')
    except:
        raise Exception('O arquivo não foi encontrado')
    
    arq = open(lista_exe, 'r')
    exec = arq.readlines()
    exec = remove_esp(exec)
    for x in exec:
        if x[0] == 'b':
            print(f'Busca pelo registro de chave {x[2:]} ')
            BuscaRegistroPorID(ARQ,x[2:])
            print('')
        elif x[0] == 'r':
            RemoveRegistroPorID(ARQ,x[2:])
            print('')
        elif x[0] == 'i':
            ARQ.close()
            InsereRegristro('dados.dat',x[2:])
            ARQ = open('dados.dat', 'r+b')
            print('')
        else:
            raise ValueError('Ação não identificada')
            
#Remove os todos '\n' de uma lista de str.
def remove_esp(lista):
  return [item.replace('\n', '') for item in lista]

# -------------- BUSCA ----------------------------------------------------------------
def BuscaRegistroPorID(arquivo, ID: str):
    offset = OffsetRegistroPorID(arquivo, ID)
    if offset == -1:
        print(f'ERRO: Registro de ID:{ID} não encontrado')
    else:
        arquivo.seek(offset)
        tamanho = int.from_bytes(arquivo.read(2), byteorder='big', signed=True)
        print('Registro encontrado: ')
        print(arquivo.read(tamanho).decode(), f'  ({tamanho} bytes)')


# -------------- Funções Auxiliares da Busca ------------------------------------------

def OffsetRegistroPorID(arquivo, ID_buscado: str):
    # inicializando variáveis importantes
    ID_encontrado = False
    EOF = False
    retorno = -1

    # pulamos o cabeçalho do arquivo
    arquivo.seek(4)

    while (not ID_encontrado) and (not EOF):
        # guardamos o offset do registro atual
        offset_reg_atual = arquivo.tell()

        # lemos o campo "tamanho" do registro atual
        tam = arquivo.read(2)
        # convertemos o campo "tamanho" para inteiro
        tamanho_reg = int.from_bytes(tam, byteorder='big', signed=True)
        # verificamos se chegamos no fim do arquivo
        # calculamos o offset do próximo registro
        offset_prox_reg = offset_reg_atual + tamanho_reg + 2

        # lemos o primeiro caractere do campo ID
        caractere = arquivo.read(1).decode()
        # verificamos se o caractere lido é o especial "*", se for, pulamos para o próximo, se não, continuamos lendo o ID atual
        if caractere == '':
            EOF = True
        else:
            # verificamos se o caractere lido é o especial "*", se for, pulamos para o próximo registro,
            # se não, continuamos lendo o ID atual
            if caractere == '*':
                arquivo.seek(offset_prox_reg)
            else:
                ID_atual = ''
                while caractere != '|':
                    ID_atual = ID_atual + caractere
                    caractere = arquivo.read(1).decode()

                arquivo.seek(offset_prox_reg)

                #verificamos se o ID do registro atual é o ID que estávamos buscando
                if ID_atual == ID_buscado:
                    ID_encontrado = True
                    retorno = offset_reg_atual
    return retorno

# -------------- REMOÇÃO --------------------------------------------------------------
def RemoveRegistroPorID(arquivo, ID: str):
    offset = OffsetRegistroPorID(arquivo, ID)
    if offset == -1:
        print(f'ERRO: Registro de ID:{ID} não foi encontrado')
    else:
        reg = RecupDados(arquivo, offset)
        RemocaoLogicaRegistro(arquivo, offset)
        insercao = InsereOrdLED(arquivo, 0, offset)
        if insercao == 1:
            print(f'Registro removido com sucesso!  ({reg.tamanho} bytes)')
            print(f'Local: offset = {offset} bytes  ({hex(offset)})')
        else:
            print('Erro ao inserir registro na LED')

# -------------- Funções Auxiliares da Remoção --------------------------------------
def RemocaoLogicaRegistro(arquivo, offset: int):
    # edição do campo ID
    caractere_especial = '*'
    caractere_especial_binario = caractere_especial.encode()
    arquivo.seek(offset + 2)
    arquivo.write(caractere_especial_binario)

    # adição de um campo de 4 bytes numéricos
    proximo = -2
    proximo_binario = proximo.to_bytes(4, byteorder='big', signed=True)
    arquivo.seek(offset + 3)
    arquivo.write(proximo_binario)

    # essa função não possui retorno

def InsereOrdLED(arquivo, cabeca:int, registro:int):
    resp = 0
    # primeiro passo é recuperar as informações cruciais da cabeça da LED
    # e do registro que será inserido

    cabeca_LED = RecupDados(arquivo, cabeca)
    espaco_disponivel = RecupDados(arquivo, registro)
    proximo_LED = RecupDados(arquivo, cabeca_LED.offset_prox)

    # o segundo passo é comparar as informações para saber onde o registro será
    # inserido na LED
    if espaco_disponivel.tamanho >= proximo_LED.tamanho:
        espaco_disponivel.offset_prox = proximo_LED.offset
        cabeca_LED.offset_prox = espaco_disponivel.offset
        AtualizaRegistros(arquivo, cabeca_LED)
        AtualizaRegistros(arquivo, espaco_disponivel)
        resp = 1

    elif espaco_disponivel.tamanho < proximo_LED.tamanho:
        resp = InsereOrdLED(arquivo, cabeca_LED.offset_prox, registro)

    return resp

def RecupDados(arquivo, offset:int):
    if offset == 0: # offset do cabeçalho do arquivo
        tamanho = 0
        arquivo.seek(offset)
        offset_proximo = int.from_bytes(arquivo.read(4), byteorder='big', signed=True)
    elif offset == -1: # caso não exista próximo
        tamanho = 0
        offset_proximo = -1
    else:
        arquivo.seek(offset)
        tamanho = int.from_bytes(arquivo.read(2), byteorder='big', signed=True)
        arquivo.seek(offset + 3)
        offset_proximo = int.from_bytes(arquivo.read(4), byteorder='big', signed=True)

    return Regs(offset=offset, tamanho=tamanho, offset_prox=offset_proximo)

def AtualizaRegistros(arquivo, registro:Regs):
    offset_registro = registro.offset
    offset_prox = registro.offset_prox
    if offset_registro == 0:
        arquivo.seek(0)
        arquivo.write(offset_prox.to_bytes(4, byteorder='big', signed=True))
    else:
        arquivo.seek(offset_registro + 3)
        arquivo.write(offset_prox.to_bytes(4, byteorder='big', signed=True))

# -------------- INSERÇÃO -------------------------------------------------------------
def InsereRegristro(ARQ: str, registro:str):
    arquivo = open(ARQ, 'r+b')
    SOBRA_MINIMA = 15
    # codificando o registro em binário
    registro_binario = registro.encode()
    tamanho_registro = len(registro_binario)
    tamanho_registro_binario = tamanho_registro.to_bytes(2, byteorder='big', signed=True) # converte o tamanho do registro para binário

    # verificar o tamanho do topo da LED
    arquivo.seek(0)
    offset_topo_LED = int.from_bytes(arquivo.read(4), byteorder='big', signed=True)
    topo = RecupDados(arquivo, offset_topo_LED)
    tamanho_topo_LED = topo.tamanho

    # cálculo do espaço que sobra
    sobra_espaco = tamanho_topo_LED - tamanho_registro

    # verificar se o registro cabe no topo da LED
    if tamanho_registro <= tamanho_topo_LED:
        # atualizando o topo da LED
        offset_novo_topo = topo.offset_prox # o novo topo será o próximo espaço da LED
        offset_novo_topo_binario = offset_novo_topo.to_bytes(4, byteorder='big', signed=True) # converte o offset do novo topo para binário
        arquivo.seek(0)
        arquivo.write(offset_novo_topo_binario) # atualiza a cabeça da LED

        # gravando o registro no espaço disponível que estava no topo
        arquivo.seek(offset_topo_LED + 2)
        arquivo.write(registro_binario) # sobreescreve o registro anterior

        print(f'Inserção concluída!  ({tamanho_registro} bytes)')
        print(f'Tamanho do espaço reutilizado: {tamanho_topo_LED} bytes (sobra de {sobra_espaco} bytes)')
        print(f'Local da Inserção: offset {offset_topo_LED} bytes  ({hex(offset_topo_LED)})')
        # cálculo do offset da sobra de espaço
        offset_sobra = offset_topo_LED + 2 + tamanho_registro

        if sobra_espaco >= SOBRA_MINIMA:
            arquivo.seek(offset_topo_LED)
            arquivo.write(tamanho_registro_binario) # sobreescreve o tamanho do registro anterior
            InsereSobraLED(arquivo, offset_sobra, sobra_espaco)
        else:
            arquivo.seek(offset_sobra - 1)
            i = 0
            while i < sobra_espaco:
                arquivo.write(b' ')
                i += 1
            arquivo.write(b'|')
    else:
        arquivo.close()
        nova_abertura = open(ARQ, 'ab')
        nova_abertura.write(tamanho_registro_binario)
        nova_abertura.write(registro_binario)
        nova_abertura.close()
        print('Inserção concluída!')
        print('Local da Inserção: Fim do arquivo')

# -------------- Funções Auxiliares da Inserção ------------------------------------------
def InsereSobraLED(arquivo, offset_da_sobra: int, tamanho_da_sobra: int):
    # preparamos o espaço de sobra
    sobra_real = tamanho_da_sobra - 2 # 2 bytes são para o tamanho do registro
    tamanho_sobra_binario = sobra_real.to_bytes(2, byteorder='big', signed=True) # convertemos o tamanho da sobra para binário
    arquivo.seek(offset_da_sobra)
    arquivo.write(tamanho_sobra_binario) # criamos o campo "tamanho" na sobra de espaço
    RemocaoLogicaRegistro(arquivo, offset_da_sobra)
    insercao = InsereOrdLED(arquivo, 0, offset_da_sobra)
    if insercao == 1:
        print('Espaço inserido com sucesso')
    else:
        raise ValueError('Erro ao inserir o espaço na LED')


# -------------- Funções Da Impressão da LED ------------------------------------------
def impressaoLED():
    contador = 0
    lista = 'LED'
    arquivo = open('dados.dat', 'rb')
    arquivo.seek(0)
    tam = int.from_bytes(arquivo.read(4), byteorder='big', signed='True')
    reg = RecupDados(arquivo,tam)
    while reg.offset != -1:
        contador +=1
        lista = lista + ' -> [offset: '+str(reg.offset) + ', tam: '+ str(reg.tamanho) +']'
        reg = RecupDados(arquivo,reg.offset_prox)      
    lista = lista + ' -> [offset: -1]'
    print(lista)
    print(f'Total: {str(contador)} espacos disponiveis')

# -------------- Flags -p -e ------------------------------------------
if __name__ == '__main__':
    if sys.argv[1] == '-e':
        arquivo_operacoes = sys.argv[2]
        main(arquivo_operacoes)
    elif sys.argv[1] == '-p':
        impressaoLED()
    else:
        raise ValueError('Erro')