# classes
class AFD(object):
    def __init__(self,alfabeto,estados,programa,estado_inicial,estados_finais):
        self.alfabeto = alfabeto
        self.estados = estados
        self.programa = programa # lista de producoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

class Producao(object):
    def __init__(self,estado_inicial,simbolo,proximo_estado):
        self.estado_inicial = estado_inicial
        self.simbolo = simbolo
        self.proximo_estado = proximo_estado

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
    automato = AFD(alfabeto,estados,programa,estado_inicial,estados_finais)
    print(automato.alfabeto)