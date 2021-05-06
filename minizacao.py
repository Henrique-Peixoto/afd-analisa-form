# classes
class AFD(object):
    def __init__(self,nome,alfabeto,estados,programa,estado_inicial,estados_finais):
        self.alfabeto = alfabeto
        self.estados = estados
        self.programa = programa # lista de producoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.nome = nome

class Producao(object):
    def __init__(self,estado_inicial,simbolo,proximo_estado):
        self.estado_inicial = estado_inicial
        self.simbolo = simbolo
        self.proximo_estado = proximo_estado

# objeto para guardar o automato
automato = AFD('',[],[],[],'',[])
# abrindo arquivo descritivo
with open('exemplo.txt', 'r+') as file:
    # Requisitos do algoritmo:
    # ser AFD
    # sem estados inalcançáveis
    # função programa total 

    # lê a primeira linha do arquivo texto
    linha = file.readline()
    # separa nome e descrição do AFD
    linha = linha.split('=')
    nome_AFD = linha[0]

    # separa texto da descricao em listas e elementos
    descricao = linha[1].replace('(','')
    descricao = descricao.replace(')','')
    descricao = descricao.split('}',1)
    # lista de estados
    estados = (descricao[0].strip('{')).split(',')

    descricao = descricao[1]
    descricao = descricao.strip(',')
    descricao = descricao.split('}',1)
    # alfabeto
    alfabeto = (descricao[0].strip('{')).split(',')

    descricao = descricao[1]
    descricao = descricao.strip(',')
    descricao = descricao.split(',',2)
    # estado inicial
    estado_inicial = descricao[1]

    # estados finais
    estados_finais = ((((descricao[2].strip('{')).strip('}')).replace('\n','')).replace('}', '')).split(',')
    
    # pula a linha que diz 'Prog'
    next(file)
    
    # lê as linhas restantes, são todas produções da função programa
    producoes = file.readlines()
    programa = []
    # transforma producoes numa lista de objetos, não strings
    for producao in producoes:
        producao = producao.replace('\n','')
        producao = producao.replace('(','')
        producao = producao.replace(')','')
        producao = producao.split(',')
        # estado inicial da produção
        q0 = producao[0]

        producao = producao[1]
        producao = producao.strip(',')
        producao = producao.split('=')
        # símbolo e próximo estado
        simbolo = producao[0]
        qnext = producao[1]

        # objeto Produção sendo inserido na lista de objetos Produção (programa)
        producao_obj = Producao(q0,simbolo,qnext)
        programa.append(producao_obj)

    # criação do objeto AFD
    automato = AFD(nome_AFD,alfabeto,estados,programa,estado_inicial,estados_finais)

# Equivalência de Estados
# montagem da tabela de distinções
pares_marcados = []
# percorre lista de estados finais do autômato
for i in range(len(automato.estados_finais)):
    # e a lista de estados geral
    for j in range(len(automato.estados)):
        # para cada estado na lista geral que não esteja na lista de
        # estados finais
        if (automato.estados[j] not in automato.estados_finais):
            # forma um par com esse estado e o estado final da iteração mais de fora
            # e marca este par
            par = [automato.estados_finais[i],automato.estados[j]]
            pares_marcados.append(par)

# itera a lista de estados com dois fors para saber quais
# pares de estados não foram marcados no passo anterior
nao_marcados = []
for estado1 in automato.estados:
    for estado2 in automato.estados:
        if estado1 != estado2:
            marcado = False
            for par in pares_marcados:
                if (estado1 in par) and (estado2 in par):
                    marcado = True
                    break
            if marcado == False:
                par = [estado1,estado2]
                # exclui repetições na lista de não marcados
                par_trocado = [estado2,estado1]
                if par_trocado not in nao_marcados:
                    nao_marcados.append(par)

