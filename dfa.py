from collections import defaultdict
from disjoint_set import DisjointSet

class DFA(object):
  
  def __init__(self, filename, states=None, terminals=None, start_state=None, transitions=None, final_states=None, name_afd=None):
    self._get_data_from_file(filename)

  def _remove_unreachable_states(self):
    """
    Remove todos os estados que são inatingíveis a partir do estado inicial. 
    """

    # Dicionário de listas que será responsável por salvar, para cada estado, 
    # os outros estados que são diretamente alcançáveis a partir do estado em questão
    g = defaultdict(list)

    for k,v in self.transitions.items():
      # Criando as listas de estados alcançáveis
      # k[0] significa o primeiro componente do par ordenado (V,T), portanto k[0] é um estado
      g[k[0]].append(v)

      # Queremos, primeiramente, verificar todos os estados que 
      # são atingíveis diretamente a partir do estado inicial, # posteriormente procuramos por todos os estados que são 
      # atingíveis a partir do estado inicial de modo indireto
      stack = [self.start_state]

      # Conjunto que guarda os estados atingíveis
      reachable_states = set()

    # Inserindo os estados atingíveis
    while stack:
      # Pegando o estado que está no topo da pilha
      state = stack.pop()

      # Guardando todos os estados atingíveis a partir do estado em questão
      if state not in reachable_states:
        stack += g[state]

      # Adicionando o estado atingível em questão ao conjunto
      # de estado atingíveis, como isso é um set, elementos 
      # repetidos não são incluidos pela natureza inerente do próprio container
      reachable_states.add(state)

    # Atualizando os estados para que tenhamos somente os estados atingíveis
    self.states = [state for state in self.states if state in reachable_states]

    # Também precisamos atualizar os estados finais,
    self.final_states = [state for state in self.final_states if state in reachable_states]

    # Também precisamos atualizar as transições
    self.transitions = {k:v for k,v in self.transitions.items() if k[0] in reachable_states}

  def minimize(self):
    # Removendo os estados inatingíveis
    self._remove_unreachable_states()

    # Manter a ordem dos elementos na tuplas será importante
    # para saber quais "quadrados" já foram marcados na tabela
    def order_tuple(a,b):
      return (a,b) if a < b else (b,a)

    # Usaremos o algoritmo da tabela visto em aula para marcar
    # os estados que são distintos
    table = {}

    # Ordenamos os estados para que possamos fazer tudo em sequência,
    # do primeiro até o último estado
    sorted_states = sorted(self.states)

    # Inicializando a tabela marcando todos os quadrados onde 
    # temos um estado final e um estado não final, que são, trivialmente
    # distintos
    for i,item in enumerate(sorted_states):
      for item_2 in sorted_states[i+1:]:
        table[(item,item_2)] = (item in self.final_states) != (item_2 in self.final_states)

    flag = True

    # Preenchendo o resto da tabela
    while flag:
      flag = False

      # Vamos olhar para as cobinações de estados da seguinte maneira
      # Pegamos um estado qi, com 0 <= i < n (n = quantidade de estados), com qj, com i < j < n.
      for i, item in enumerate(sorted_states):
        for item_2 in sorted_states[i+1:]:
          
          # Verificamos se o quadrado já está marcado
          if table[(item,item_2)]:
            # Se estiver, então os estados são distintos
            continue

          # Precisamos checar as transições dos estado item e item_2 
          # para saber se eles são distinguíveis
          for w in self.terminals:
            # 'None' é para o caso em que algum estado não esteja
            # definido para algum determinado terminal
            t1 = self.transitions.get((item,w), None)
            t2 = self.transitions.get((item_2,w), None)

            if t1 is not None and t2 is not None and t1 != t2:
              # Se para pelo menos um transição os estados forem
              # distintos, então os marcamos na tabela
              marked = table[order_tuple(t1,t2)]
              flag = flag or marked
              # Se os estads t1 e t2 forem distintos, então os 
              # estados item e item_2 também serão distintos
              # então, ao invés de criar uma lista de dependências,
              # já vamos logo marcando (item,item_2) como sendo distintos
              table[(item,item_2)] = marked

              if marked:
                break

    d = DisjointSet(self.states)

    # Após analisar os estados, e descobrir aqueles que são distintos
    # e aqueles que não são, precisar fundir aquelas que são iguais
    for k,v in table.items():
      if not v:
        d.union(k[0],k[1])
  
    # Atualizando os estados após a união dos estados iguais
    self.states = [str(x) for x in range(1,1+len(d.get()))]
    new_final_states = []
    self.start_state = str(d.find_set(self.start_state))

    # Pegando os conjuntos do 'd'
    for s in d.get():
      # Pegando os elementos de 's'
      for item in s:
        if item in self.final_states:
          # Construindo uma lista de novos estados finais
          new_final_states.append(str(d.find_set(item)))
          break

    # Atualizando as transições
    self.transitions = {(str(d.find_set(k[0])), k[1]):str(d.find_set(v)) for k,v in self.transitions.items()}

    self.final_states = new_final_states
    print("AFD minimizado")

  def _get_data_from_file(self, filename):
    """
    Carrega os dados do arquivo. Esses dados são os estados,
    separados em todos os estados, os estados finais e o estado inicial, assim como as transições.
    """

    # Abrindo o arquivo e o apelidando de 'f', para facilitar seu manuseio
    with open(filename, 'r') as f:
      try:

        # Lendo a primeira linha (descrição) do arquivo
        linhas = f.readlines()

        # Temos que fazer o parsing do arquivo para pegar seus
        # valores corretamente
        linha = linhas[0].split('=')
        self.name_afd = linha[0]
        
        # Separa texto da descrição em listas e elementos
        descricao = linha[1].replace('(','')
        descricao = linha[1].replace(')','')
        descricao = descricao.split('}',1)

        # Lista de estados
        self.states = (descricao[0].strip('(').strip('{')).split(',')

        descricao = descricao[1]
        descricao = descricao.strip(',')
        descricao = descricao.split('}',1)

        # Alfabeto
        self.terminals = (descricao[0].strip('{')).split(',')

        descricao = descricao[1]
        descricao = descricao.strip(',')
        descricao = descricao.split(',',2)

        # Estado inicial
        self.start_state = descricao[1]

        descricao = descricao[2].strip('{').strip('}')

        # Estados finais
        self.final_states = descricao.replace('\n','').replace('}','').split(',')

        producoes = linhas[2:]

        self.transitions = {}
        for producao in producoes:
          # Fazendo o parsing das transições
          producao = producao.replace('\n','')
          producao = producao.replace('(','')
          producao = producao.replace(')','')
          producao = producao.split(',')

          # Estado de onde parte a produção
          current_state = producao[0]

          producao = producao[1]
          producao = producao.strip(',')
          producao = producao.split('=')

          # Terminal e próximo estado
          terminal = producao[0]
          next_state = producao[1]

          # Separando a transição em "estado de onde saímos", "símbolo que gera transição"
          # e "estado resultante"
          # As transições são representadas por um dicionário, onde as chaves são pares ordenados onde o primeiro componente
          # é um estado e o segundo componente um terminal,
          # e o valor associado a esta chave é o estado resultante
          # da transição 
          self.transitions[(current_state, terminal)] = next_state

      # Em caso de algum erro, qualquer outro erro
      except Exception as e:
        print("Erro: ", e)

  def __str__(self):
    """
    Representação do autômato
    """

    # Exibindo o autômato
    print(self.name_afd+'='+'({'+','.join(self.states)+'},{'+','.join(self.terminals)+'},Prog,'+self.start_state+',{'+','.join(self.final_states)+'})') 
    for k,v in self.transitions.items():
      print(f"({k[0]},{k[1]})={v}")

    return ''
