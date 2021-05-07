from dfa import DFA
filename = 'exemplo2.txt'
dfa = DFA(filename)
print(dfa)
dfa.minimize()
print(dfa)