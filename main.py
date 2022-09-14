# B. CSV: Comma separated values
from tabulate import tabulate
import ply.lex as plex

tokens = ("COMENTARIO", "ASPAS", "SEMASPAS")
t_ignore = ','

filename = "Ficheiro.csv"
colunas = []
dados = None

def t_COMENTARIO(t):
    r"\#[^\n+]+\n?"     #Expressão regular destinada a identificar que palavras existem depois de um #. Faz com que estes comentários não sejam lidos pelo programa
    pass

def t_ASPAS(t):
    r"\"([^\"]+)[\"]"       #Expressão regular destinada a identificar que palavras existem entre 2 aspas
    return t

def t_SEMASPAS(t):
    r"[^,\n]+"      #Expressão regular destinada a identificar que palavras existem entre 2 aspas
    return t

def t_NOVALINHA(t):
    r"\n+"
    pass

def t_error(t):
    print(f"Unexpected token: {t} ")
    exit(1)

def lerColunas(filename):
    global colunas
    firstLine = None
    with open(filename) as f:
        firstLine = f.readline()
    colunas = firstLine.split(",")
    colunas[3] = colunas[3][:1]

def criarMatriz(filename):
    global dados
    file = open(filename, "rt")
    linhas = sum(1 for line in file)-1
    dados = [[0 for x in range(len(colunas))] for y in range(linhas)]

def slurp(filename):
    with open(filename, "rt") as fh:
        contents = fh.read()
    return contents

def escreverLATEX(dados):
    tabela = "\documentclass{article}\n\\usepackage{pdflscape}\n\\title{Tabela CSV em Latex}\n\\author{Andre e Diogo}\n\\begin{document}\n\\begin{landscape}\n\\begin{center}\n\maketitle Tabela\n\\bigbreak\n"
    tabulate.PRESERVE_WHITESPACE = True
    tabela += tabulate(dados, tablefmt="latex", stralign="left")
    tabela += "\n\end{center}\n\end{landscape}\n\end{document}"
    ficheirodeoutput = open("TabelaLatex.tex", "w")
    ficheirodeoutput.writelines(tabela)
    ficheirodeoutput.close()


def escreverHTML(colunas, dados):
    ficheiro = "<!DOCTYPE html>\n<html>\n"
    style = "\n<head>\n<style>\n"
    style += "table {\n font-family: rebuchet MS, sans-serif;\n border-collapse: collapse;\n width: 100%;\n}"
    style += "td, th {\n border: 5px solid black;\n text-align: center;\n padding:10px;\n}"
    style += "tr:nth-child(1) {\n background-color: #00bf07;\n}"
    style += "tr:nth-child(even) {\n background-color: white;\n}"
    style += "h2 {\n font-family: Trebuchet MS, sans-serif;\n color: black;\n  text-align: center;\n}\n</head>\n</style>\n"
    ficheiro += style
    ficheiro += "<body>\n\n  <h2>Tabela CSV</h2>\n"

    tabela = " <table>\n"

    tabela += "    <tr>\n"
    for colunas in cabecalho:
        tabela += "      <th>{0}</th>\n".format(colunas.strip())
    tabela += "    </tr>\n"

    for nrLinha, linhas in enumerate(dados):
        if nrLinha:
            tabela += "    <tr>\n"
            for colunas in linhas:
                tabela += "      <td>{0}</td>\n".format(colunas)
            tabela += "    </tr>\n"

    tabela += "    </table>\n"
    ficheiro += tabela
    ficheiro += "  </body>\n"
    ficheiro += "</html>\n<br><br><br>"

    ficheirooutput = open("TabelaHTML.html", "w")
    ficheirooutput.writelines(ficheiro)
    ficheirooutput.close()

lerColunas(filename)
criarMatriz(filename)

contents = slurp(filename)
lexer = plex.lex()
lexer.input(contents)

cabecalho = []
contador = 0

lenghtX = 0
lenghtY = 0

for token in iter(lexer.token, None):
    if token is not None and contador < len(colunas):
        cabecalho.append(token.value)
        contador += 1
    if token is not None:
        dados[lenghtX][lenghtY] = token.value
        lenghtY += 1
        if lenghtY == len(colunas):
            lenghtX += 1
            lenghtY = 0

print(dados)
escreverHTML(colunas, dados)
escreverLATEX(dados)