from lark import Lark

grammar = """
//Regras Semanticas
start: (expressao SC)+
expressao: atribuicao 
         |declaracao
         | inicializacao
         | operacao 
         | condicional 
         | ciclo

declaracao: tipo var
inicializacao: tipo var "=" [objeto|operacao]
atribuicao: var "=" [objeto|operacao]
operacao: termo operador termo
        | termo operador (operacao)+ 

condicional: alternativa 
           | casos
alternativa: IF PE condicao PD CE expressao+ CD 
		   | IF PE condicao PD CE expressao+ CD ELSE CE expressao+ CD
casos: "match" PE var PD CE "case" objeto DP expressao* "case" "_" DP expressao* CD

ciclo: enquanto 
     | repete 
     | percorre
enquanto: "while" PE condicao PD CE expressao* CD 
repete: "do" CE expressao* CD "while" PE condicao PD
percorre: "for" var "in" conjunto CE expressao* CD

condicao: int 
        | bool 
        | operacao 
bool: "TRUE" 
    | "FALSE"

int : NUMBER

string: STR

tuplo: PE objeto [VIR objeto]* PD

array: PRE  PRD 
     | PRE objeto PRD 
     | PRE objeto (VIR objeto)* PRD

lista: PRE PRD 
     | PRE objeto lista* PRD

set: CE CD 
   | CE objeto CD 
   | CE objeto VIR set* CD

dict: CE key DP objeto (VIR key DP objeto)* CD
key: int
   | string

objeto: int
    | bool 
    | string 
    | tuplo 
    | array 
    | lista 
    | set
    | dict

var: /[a-zA-Z]\w*/ 

termo: var
     | int

conjunto: array 
        | set 
        | lista
        | dict
     
operador: PLUS 
        | MINUS 
        | MULT
        | DIV
        | MOD 
        | EQUAL 
        | DIFF 
        | LESS 
        | GREAT 
        | LEQUAL 
        | GEQUAL

tipo: INT
    | BOOL
    | STRING
    | TUPLO 
    | ARRAY 
    | LISTA 
    | SET
    | DICT

//Regras Lexicograficas
DP: ":"
PE: "("
PD: ")"
PRE: "["
PRD: "]"
VIR: ","
CE: "{"
CD: "}"
IF: "if"
ELSE: "else"
CASE: "case"
INT: "int"
BOOL: "bool" 
STRING: "string"
TUPLO: "tuplo" 
ARRAY: "array" 
LISTA: "lista" 
SET: "set"
DICT: "dict"
PLUS: "+" 
MINUS: "-" 
MULT: "*" 
DIV: "/" 
MOD: "%" 
EQUAL: "==" 
DIFF: "!=" 
LESS: "<" 
GREAT: ">" 
LEQUAL:"<=" 
GEQUAL:">="
NUMBER: /\-?\d+/
STR: /\"\w+\"/
SC: ";" 

%import common.WS_INLINE
%ignore WS_INLINE
%ignore "\\n"
"""

frase = """
int y; 
int x = 10 + 23; 
x = 10;
dict d = {1: "oi", "teste" : [1,2,3]};
"""

p = Lark(grammar)

tree = p.parse(frase)
print(tree)
print(tree.pretty())