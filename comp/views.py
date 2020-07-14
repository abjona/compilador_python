from django.shortcuts import render
import ply.lex as lex
from ply import yacc

def analiselexica(request):

    template_name = "comp/compilador.html"
    context = {}

    codigo = request.POST.get('codigo', '')

    if codigo:
        context['codigo'] = codigo

    print (codigo)

    reserved = {
        'print': 'PRINT',
    }

    # TOKENS
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
    'VAR',
    'EQUALS',
    'END',
    ] + list(reserved.values())

    # TOKENS - OP, CHAVES, PARENTESES
    # t_AT = r'\:'
    # t_BEGIN = r'\{'
    # t_END = r'\}'
    t_END = r'\;'
    t_EQUALS = r'='
    t_PRINT   = r'print'
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

   
    # VERIFICA UM NÚMERO
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)    
        return t

    # VERIFICA VARIÁVEL
    def t_VAR(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'VAR')
        return t

    # VERIFICA STRING
    def t_STRING(t):
        r'"([^"]+)"'
        t.type = reserved.get(t.value, 'STRING')
        return t

    # VERIFICA DOUBLE
    def t_DOUBLE_VAL(t):
        r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
        t.type = reserved.get(t.value, 'DOUBLE_VAL')
        return t

    # VERIFICA VALOR INTEIRO
    def t_INT_VAL(t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    # IGNORA CARACTER
    t_ignore = " \r"

    def t_COMMENT(t):
        r'\#.*'
        pass
        # NÃO RETORNA VALOR

    # NOVA LINHA
    def t_newline(t):
        r'\n+'
        print ("Newline found")
        t.lexer.lineno += t.value.count("\n")

    # ENCONTRA A COLUNA EM QUE O TOKEN FOI ENCONTRADO
    def find_column(input, token):
        last_cr = input.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column
    lerror = []

    names={}

    # VERIFICA ERROS
    def t_error(t):
        lr = (t.value[0], t.lineno, t.lexpos)
        lerror.append(lr)
        t.lexer.skip(1)

    ################ ANÁLISE SINTÁTICA ######################

    def p_expression_plus(p):
        'expression : expression PLUS term'
        p[0] = p[1] + p[3]
 
    def p_expression_minus(p):
        'expression : expression MINUS term'
        p[0] = p[1] - p[3]

    def p_expression_divide(p):
        'expression : expression DIVIDE term'
        p[0] = p[1] / p[3]
 
    def p_expression_times(p):
        'expression : expression TIMES term'
        p[0] = p[1] * p[3]
    
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

    def p_statement_assignment(p):
        "statement : assignment"
        pass

    def p_statement_assignment(p):
        "statement : assignment"
        pass
    
    def p_statement_expression(p):
        "statement : expression"
        p[0] = p[1]
    

    def p_expression_name(p):
        "expression : VAR"
        p[0] = names[p[1]]
    
    def p_expression_name(p):
        "expression : NUMBER"
        p[0] = p[1]

    def p_assignment(p):
        """expression : VAR EQUALS expression END
                      | VAR EQUALS VAR END"""
        print ("Assigning variable", p[1], "to", p[3])
        names[p[1]] = p[3]
    
    def p_assignment_number(p):
        "assignment : VAR EQUALS NUMBER END"
        print ("Assigning variable", p[1], "to", p[3])
        names[p[1]] = p[3]

    # def p_print_result(p):
    #     "expression : PRINT LPAREN VAR RPAREN"
    #     p[0] = names[p[3]]

    # def p_indent(p):
    #     "expression : expression END"
    #     p[0] = p[1]

    # def p_statement_assign(t):
    #     """statement : NAME EQUALS expression.
    #             |PRINT NAME EQUALS expression """
    #     names[t[1]] = t[3]
    #     if names:
    #         names.append(t[3])

    def p_print_statement(p):
        "statement : PRINT expression END"
        p[0] = p[2]


    def p_factor_expr(p):
        'expression : LPAREN expression RPAREN'
        print('teste',p[2])
        p[0] = p[2]

        
    def p_error(p):
        print(p)
        print("Syntax error in input!")

    parser = yacc.yacc()
    lexer = lex.lex()

    lexer.input(str(codigo))
    
    llex = []

    # VERIFICA O TIPO DO TOKEN, VALOR, LINHA, COLUNA
    while 1:
        tok = lex.token()
        if not tok:
            break

        lt = (tok.type, tok.value, tok.lineno, tok.lexpos)
        llex.append(lt)
   
    def _new_token(type, lineno):
        tok = lex.LexToken()
        tok.type = type
        tok.value = None
        tok.lineno = lineno
        return tok


    context['llex'] = tuple(llex)
    context['lerror'] = tuple(lerror)

    if codigo:
        result = parser.parse(str(codigo))
        context['rsintatica'] = result
    
    print(names)
    return render(request, template_name, context)
