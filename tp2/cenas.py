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

string_test = ""
tree = p.parse(string_test)  # retorna uma tree


class InterpreterIntervalos(Interpreter):
    def __init__(self):
        symbols = {
            'vars' : {},
            'types' : {},
            'instructions' : {
                'assign' : 0,
                'read_write' : 0,
                'conditional' : 0,
                'cycle' : 0
            },
            'functions' : {

            },
            'errors': {
                'redeclarations' : 0,
                'not_declared' : 0
            }
        }

    def declaracao(self,tree):
        # tratar tipo
        if tree[0] in self.symbols["types"].keys():
            self.symbols["types"][tree[0]] += 1
        else:
            self.symbols["types"][tree[0]] = 1
        
        # tratar variavel
        if tree[1] in vars["name"]:
            self.symbols['errors']["redeclarations"] += 1
            self.symbols["vars"][tree[1]]['redeclaration?'] = True

        else:
            self.symbols['vars'][tree[1]] = {
                'type': tree[0],
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': False,
                'used': False
        }

    def inicializacao(self,tree):
        # tratar tipo
        if tree[0] in self.symbols["types"].keys():
            self.symbols["types"][tree[0]] += 1
        else:
            self.symbols["types"][tree[0]] = 1
        
        # tratar variavel
        if tree[1] in vars["name"]:
            self.symbols['errors']["redeclarations"] += 1
            self.symbols["vars"][tree[1]]['redeclaration?'] = True

        else:
            self.symbols['vars'][tree[1]] = {
                'type': tree[0],
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': True,
                'used': 0
        }

    def atribuicao(self,tree):
        if tree[1] not in vars["name"]:
            self.symbols['errors']['not_declared'] += 1
        self.symbols['vars'][tree[1]]['used'] = True

    def var(self, tree):
        if tree not in self.symbols['vars'].keys():
            self.symbols['vars'][tree] = [tree, "", False, False, False, 0]
        else:
            self.symbols['vars'][tree]['used'] += 1

    def expressao(self, tree, args):
        if args[0] == "atribuicao":    
            self.symbols['instructions']['assign'] +=1
        elif args[0] == "operacao":
            self.symbols['instructions']['read_write'] += 1
        elif args[0] == "condicional":
            self.symbols['instructions']['conditional'] += 1
        elif args[0] == "ciclo":
            self.symbols['instructions']['cycle'] += 1

data = InterpreterIntervalos().visit(tree)


