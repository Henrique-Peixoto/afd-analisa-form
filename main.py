from dfa import DFA
filename = 'exemplo.txt'
dfa = DFA(filename)
print(dfa)
dfa.minimize()
print(dfa)
