##################### HELP DO ENUNCIADO #####################
###### Vars
# Redeclaração
# Não-Declaração
# Usada mas não inicializada
# Declarada mas nunca mencionada
# var -> name, type, declaration?, redeclaration?, inicialization?, used

###### Types
# Total de vars declaradas por cada tipo
# type -> nr_variables

###### Instructions
# Nr de instrucoes de cada tipo
# Atribuicao | Leitura e Escrita | Condicional | Ciclico
# inst_type -> nr_instructions

from lark import Lark
from lark.visitors import Interpreter
from grammar import grammar

p = Lark(grammar) # cria um objeto parser

string_test = """
int y; 
int x = 10 + 23; 
x = 10;
dict d = {1: "oi", "teste" : [1,2,3]};
"""

tree = p.parse(string_test) # retorna uma tree

class InterpreterIntervalos(Interpreter):
    def __init__(self):
        self.symbols = {
            'vars' : {},
            'types' : {},
            'instructions' : {
                'assign' : 0,
                'read_write' : 0,
                'conditional' : 0,
                'cycle' : 0
            },
            'errors': {
                'redeclarations' : 0,
                'not_declared' : 0
            }
        }

    def declaracao(self,tree):
        # tratar tipo
        if tree.children[0] in self.symbols['types'].keys():
            self.symbols['types'][tree.children[0]] += 1
        else:
            self.symbols['types'][tree.children[0]] = 1
        
        # tratar variavel
        if tree.children[1] in self.symbols['vars']['name']:
            self.symbols['errors']['redeclarations'] += 1
            self.symbols['vars'][tree.children[1]]['redeclaration?'] = True

        else:
            self.symbols['vars'][tree.children[1]] = {
                'type': tree.children[0],
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': False,
                'used': False
        }

    def inicializacao(self,tree):
        # tratar tipo
        if tree.children[0] in self.symbols['types'].keys():
            self.symbols['types'][tree.children[0]] += 1
        else:
            self.symbols['types'][tree.children[0]] = 1
        
        # tratar variavel
        if tree.children[1] in self.symbols['vars']['name']:
            self.symbols['errors']['redeclarations'] += 1
            self.symbols['vars'][tree.children[1]]['redeclaration?'] = True

        else:
            self.symbols['vars'][tree.children[1]] = {
                'type': tree.children[0],
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': True,
                'used': 0
        }

    def atribuicao(self,tree):
        if tree.children[1] not in self.symbols['vars']['name']:
            self.symbols['errors']['not_declared'] += 1
        self.symbols['vars'][tree.children[1]]['used'] = True

    def var(self, tree):
        if tree not in self.symbols['vars'].keys():
            self.symbols['vars'][tree] = [tree, '', False, False, False, 0]
        else:
            self.symbols['vars'][tree]['used'] += 1

    def expressao(self, tree):
        if tree.data == 'atribuicao':    
            self.symbols['instructions']['assign'] +=1
        elif tree.data == 'operacao':
            self.symbols['instructions']['read_write'] += 1
        elif tree.data == 'condicional':
            self.symbols['instructions']['conditional'] += 1
        elif tree.data == 'ciclo':
            self.symbols['instructions']['cycle'] += 1

data = InterpreterIntervalos().visit(tree)
print(data)

# estrutura para ser imprimida no html:

# variáveis do programa: var1, var2, var3, var4
# variáveis declaradas mais do que uma vez: var1 -> 2x; var2 -> 3x
# variáveis usadas mas nunca inicializadas: var3, var4
# variáveis declaradas mas nunca usadas: var1

# tipos usados no programa
# int: 3 
# char: 2

# total de instruções
# atribuições: 4
# leitura e escrita: 15
# condicional: 7
# ciclos: 2
# total: 28

# ...