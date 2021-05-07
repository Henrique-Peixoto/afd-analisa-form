from dfa import DFA
filename = 'exemplo3.txt'
dfa = DFA(filename)
print(dfa)
dfa.minimize()
print(dfa)