from collections import defaultdict
from disjoint_set import DisjointSet

class DFA(object):
  
  def __init__(self, filename, states=None, terminals=None, start_state=None, transitions=None, final_state=None):
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

  def _get_data_from_file(self, filename):
    """
    Carrega os dados do arquivo. Esses dados são os estados,
    separados em todos os estados, os estados finais e o estado inicial, assim como as transições.
    """

    # Abrindo o arquivo e o apelidando de 'f', para facilitar seu manuseio
    with open(filename, 'r') as f:
      try:
        # A ordem de leitura do arquivo é a seguinte:
        # Primeira linha: os estados
        # Segunda linha: os terminais
        # Terceira linha: o estado inicial
        # Quarta linha: os estados finais
        # Linhas seguintes: as transições

        # Lendo o conteúdo do arquivo
        lines = f.readlines()
        states, terminals, start_state, final_states = lines[:4]

        # Fazendo o parsing dos símbolos lidos 
        # Sempre checando para ver se o formato do arquivo está correto

        if states:
          self.states = states.split()
        else:
          raise Exception('Formato de arquivo inválido: estados não puderam ser lidos')

        if terminals: 
          self.terminals = terminals.split()
        else:
          raise Exception('Formato de arquivo inválido: terminais não puderam ser lidos')

        if start_state:
          self.start_state = start_state
        else:
          raise Exception('Formato de arquivo inválido: estado inicial não pode ser lido')

        if final_states:
          self.final_states = final_states.split()
        else:
          raise Exception('Formato de arquivo inválido: estados finais não puderam ser lidos')

        # Pegando as transições
        lines = lines[:4]
        self.transitions = {}
        for line in lines:
          # Separando a transição em "estado de onde saímos", "símbolo que gera transição"
          # e "estado resultante"
          # As transições são representadas por um dicionário, onde as chaves são pares ordenados onde o primeiro componente
          # é um estado e o segundo componente um terminal,
          # e o valor associado a esta chave é o estado resultante
          # da transição 
    
          current_state, terminal, next_state = line.split()
          self.transitions[(current_state, terminal)] = next_state

      # Em caso de algum erro, qualquer outro erro
      except Exception as e:
        print("Erro: ", e)