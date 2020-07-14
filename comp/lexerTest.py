import ply.lex as lex
from ply import yacc
# List of token names.   This is always required

reserved = {
        'print': 'PRINT',
}

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'INT_VAL',
    'STRING',
    'DOUBLE_VAL',
    'VAR'
] + list(reserved.values())


def mylex(inp):
    lexer.input(str(inp))
    print(lexer.token())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'



# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'"([^"]+)"'
    t.type = reserved.get(t.value, 'STRING')
    return t

# VERIFICA DOUBLE
def t_DOUBLE_VAL(t):
    r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    t.type = reserved.get(t.value, 'DOUBLE_VAL')
    return t

def t_COMMENT(t):
        r'\#.*'
        pass
        # NÃO RETORNA VALOR

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# VERIFICA VALOR INTEIRO
def t_INT_VAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'VAR')
    return t

    # NÃO RETORNA VALOR
# Define a rule so we can track line numbers
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer from my environment and return it    
    return lex.lex()

# def p_expression_equals(p):
#     """assignment : VAR EQUALS NUMBER
#                   | VAR EQUALS expression"""
#     p[0] = p[3]

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]
 
def p_expression_minus(p):
     'expression : expression MINUS term'
     p[0] = p[1] - p[3]
    
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]
 
def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]
 
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

    # Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

    # Build the parser
parser = yacc.yacc()
lexer = lex.lex()

while True:
    try:
        s = input('calc > ')
        mylex(s)
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)