from lark import Lark
from lark.visitors import Interpreter
from grammar import grammar
from json2html import *

p = Lark(grammar) # cria um objeto parser

string_test = """
int y; 
int x = 10 + 23; 

y = 10;
z + 10;

int x = 2;
int z = y + x;

bool t = TRUE;
bool f = FALSE;

string w = "Hello";

array a = [1,2,3];

lista l = [1,"List",TRUE];

lista vl = [];

dict d = {1: "oi", "teste" : [1,2,3]};

set s = {};

if (t) {x + 1; y-1;};

while(t){x * 2; t = FALSE;};

do{}while(x == 10);

for i in [3,5,6]{x = z + i};

for i in l {y = x / i};
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

    def start(self,tree):
        self.visit_children(tree)
        return self.symbols
    
    def expressao(self, tree): 
        self.visit_children(tree)

    def declaracao(self,tree):
        var_type = tree.children[0].children[0].value
        var_name = tree.children[1].children[0].value
        
        # tratar variavel
        if var_name in self.symbols['vars'].keys():
            self.symbols['errors']['redeclarations'] += 1
            self.symbols['vars'][var_name]['redeclaration?'] = True

        else:
            self.symbols['vars'][var_name] = {
                'type': var_type,
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': False,
                'used': 0
            }

            # tratar tipo
            if var_type in self.symbols['types'].keys():
                self.symbols['types'][var_type] += 1
            else:
                self.symbols['types'][var_type] = 1

    def inicializacao(self,tree):
        var_type = tree.children[0].children[0].value
        var_name = tree.children[1].children[0].value
        
        # tratar variavel
        if var_name in self.symbols['vars'].keys():
            self.symbols['errors']['redeclarations'] += 1
            self.symbols['vars'][var_name]['redeclaration?'] = True

        else:
            self.symbols['vars'][var_name] = {
                'type': var_type,
                'declaration?': True,
                'redeclaration?': False,
                'inicialization?': True,
                'used': 0
            }
            
            # tratar tipo
            if var_type in self.symbols['types'].keys():
                self.symbols['types'][var_type] += 1
            else:
                self.symbols['types'][var_type] = 1
            
        self.visit(tree.children[2])

    def atribuicao(self,tree):
        self.symbols['instructions']['assign'] +=1

        var_name = tree.children[0].children[0].value

        if var_name not in self.symbols['vars'].keys():
            self.symbols['errors']['not_declared'] += 1
        
        else:
            self.symbols['vars'][var_name]['used'] += 1

        self.visit(tree.children[1])

    def operacao(self, tree):
        self.symbols['instructions']['read_write'] += 1
        self.visit_children(tree)

    def condicional(self, tree):
        self.symbols['instructions']['conditional'] += 1
        self.visit_children(tree)

    def ciclo(self, tree):
        self.symbols['instructions']['cycle'] += 1
        self.visit_children(tree)
    
    def var(self, tree):
        var_name = tree.children[0].value
        if var_name not in self.symbols['vars'].keys():
            self.symbols['vars'][var_name] = {
                'type': '',
                'declaration?': False,
                'redeclaration?': False,
                'inicialization?': False,
                'used': 0
            }

            self.symbols['errors']['not_declared'] += 1
        
        self.symbols['vars'][var_name]['used'] += 1


data = InterpreterIntervalos().visit(tree)

f = open("result.html",'w')
f.write(json2html.convert(json=data))
f.close()