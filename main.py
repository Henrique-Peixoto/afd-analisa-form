from dfa import DFA

# Nome do arquivo contendo o AFD a ser lido
filename = 'exemplo2.txt'

# Nome do arquivo contendo a lista de palavras
listname = "lista_exemplo.txt"

# Cria o DFA baseado no arquivo
dfa = DFA(filename)
print(dfa)

# Minimiza o dfa
dfa.minimize()
print(dfa)

# Pede uma palavra para verificar se ela faz parte do AFD minimizado
word = input("Insira uma palavra para verificar se ela faz parte de ACEITA(M min): ")

# Verifica se a plavra é aceita ou rejeitada
dfa.verify_word(word)

# Verifica uma lista de palavras
dfa.verify_list(listname)