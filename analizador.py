import sys
import io
import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
import matplotlib.pyplot as plt


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


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

precedence = (
    ('left', 'IFF'),
    ('left', 'IF'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

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

def probar_parser(cadena_entrada, archivo):
    lexer.input(cadena_entrada)
    archivo.write(f"Tokens para: '{cadena_entrada}'\n")
    for token in lexer:
        archivo.write(f"{token}\n")
    
    archivo.write(f"Resultado para: '{cadena_entrada}'\n")
    resultado = parser.parse(cadena_entrada)
    archivo.write(f"{resultado}\n")
    archivo.write("\n")
    return resultado

def jerarquia_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _jerarquia_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _jerarquia_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
        
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)
        
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _jerarquia_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    
    return pos

def dibujar_y_guardar_arbol_expresion(arbol, nombre_archivo):
    G = nx.DiGraph()
    etiquetas = {}
    idx = 0

    def agregar_aristas(nodo, padre=None):
        nonlocal idx
        nodo_actual = f"{nodo}_{idx}"
        idx += 1
        G.add_node(nodo_actual)
        if padre:
            G.add_edge(padre, nodo_actual)
        etiquetas[nodo_actual] = nodo
        
        if isinstance(nodo, tuple):
            if len(nodo) == 3:
                op, izquierda, derecha = nodo
                etiquetas[nodo_actual] = op
                agregar_aristas(izquierda, nodo_actual)
                agregar_aristas(derecha, nodo_actual)
            elif len(nodo) == 2:
                op, operando = nodo
                etiquetas[nodo_actual] = op
                agregar_aristas(operando, nodo_actual)
        else:
            etiquetas[nodo_actual] = nodo

    agregar_aristas(arbol)
    
    pos = jerarquia_pos(G, root='{}_0'.format(arbol))
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=etiquetas, node_size=3000, node_color='orange', font_size=10, font_weight='bold', arrowsize=20)
    plt.savefig(nombre_archivo)
    plt.close()

with open('respuesta.txt', 'w', encoding='utf-8') as archivo:
    expresiones = [
        'p',
        '∼∼∼ q',
        '(p ∧ q)',
        '(0 => (ros))',
        '∼(p ∧ q)',
        '(p <=> ∼p)',
        '((p => q) ∧ p)',
        '(∼(p ∧ (q o r)) o s)',
        '((p o q) ∧ (r o s))'
    ]

    for i, expr in enumerate(expresiones):
        resultado = probar_parser(expr, archivo)
        nombre_archivo = f"arbol_{i + 1}.png"
        dibujar_y_guardar_arbol_expresion(resultado, nombre_archivo)
