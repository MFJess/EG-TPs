# Analisador de Código para a Linguagem de Programação Imperativa
Escrever em Python uma ferramenta que analise programas e gere um HTML, e um relatório com resultados, usando o Parser e os Visitors do módulo para geração de processadores de linguagens Lark.

A Linguagem deve permitir declarar:
- variáveis atómicas;
- variáveis estruturadas (conjunto, lista, tuplo, dicionario);
- instruções de seleção (condicionais);
- pelo menos 3 variantes de ciclos.

Deve registar:
- lista de todas as variaveis do programa, indicando:
    - os que são redeclaração;
    - os que não são redeclaração;
    - variáveis usadas mas que não foram inicializadas;
    - variáveis declaradas nunca usadas.
- total de variáveis declaradas por cada tipo de dados;
- total de instruções que formam o corpo do programa, agrupadas por tipo:
    - atribuições;
    - leitura e escrita;
    - condicionais;
    - cíclicas.
- total de situações em que as estruturas surgem aninhadas a outras de controlo, do mesmo tipo, ou tipos diferentes;
- situações em que existem ifs aninhados que possam ser substituidos por um só if