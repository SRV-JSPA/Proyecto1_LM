import ply.lex as lex
import ply.yacc as yacc

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
