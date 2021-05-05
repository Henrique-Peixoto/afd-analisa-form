from collections import defaultdict
from disjoint_set import DisjointSet

class DFA(object):
  
  def __init__(self, filename, states=None, terminals=None, start_state=None, transitions=None, final_state=None):
    self._get_data_from_file(filename)

  

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
          current_state, terminal, next_state = line.split()
          self.transitions[(current_state, terminal)] = next_state

      # Em caso de algum erro, qualquer outro erro
      except Exception as e:
        print("Erro: ", e)