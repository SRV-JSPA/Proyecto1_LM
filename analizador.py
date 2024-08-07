import sys
import io
import ply.lex as lex
import ply.yacc as yacc

# Redefinir la salida para permitir caracteres especiales
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Definición de tokens
tokens = (
    'VARIABLES',   
    'NOT',        
    'AND',        
    'OR',        
    'IF',    
    'IFF',        
    'PAREN_I',     
    'PAREN_D',     
    'CONST_CERO', 
    'CONST_UNO',  
)

t_NOT = r'∼'
t_AND = r'∧'
t_OR = r'o'
t_IF = r'=>'
t_IFF = r'<=>'
t_PAREN_I = r'\('
t_PAREN_D = r'\)'
t_CONST_CERO = r'0'
t_CONST_UNO  = r'1'
t_VARIABLES = r'[p-z]'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Definición de precedencia
precedence = (
    ('left', 'IFF'),
    ('left', 'IF'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

# Definición de reglas gramaticales
def p_formula_binaria(p):
    '''formula : formula AND formula
               | formula OR formula
               | formula IF formula
               | formula IFF formula'''
    p[0] = (p[2], p[1], p[3])

def p_formula_unaria(p):
    'formula : NOT formula'
    p[0] = ('NOT', p[2])

def p_formula_parens(p):
    'formula : PAREN_I formula PAREN_D'
    p[0] = p[2]

def p_formula_constante(p):
    '''formula : CONST_CERO
               | CONST_UNO'''
    p[0] = p[1]

def p_formula_variable(p):
    'formula : VARIABLES'
    p[0] = p[1]

def p_error(p):
    print(f"Error de sintaxis en '{p.value if p else 'EOF'}'")

parser = yacc.yacc()

# Función para probar el parser y guardar resultados en un archivo
def test_parser(input_string, file):
    lexer.input(input_string)
    file.write(f"Tokens para: '{input_string}'\n")
    for token in lexer:
        file.write(f"{token}\n")
    
    file.write(f"Resultado para: '{input_string}'\n")
    result = parser.parse(input_string)
    file.write(f"{result}\n")
    file.write("\n")

# Crear o abrir el archivo respuesta.txt en modo escritura
with open('respuesta.txt', 'w', encoding='utf-8') as file:
    # Ejemplos de prueba
    test_parser('p', file)
    test_parser('∼∼∼ q', file)
    test_parser('(p ∧ q)', file)
    test_parser('(0 => (ros))', file)
    test_parser('∼(p ∧ q)', file)
    test_parser('(p <=> ∼p)', file)
    test_parser('((p => q) ∧ p)', file)
    test_parser('(∼(p ∧ (q o r)) o s)', file)
