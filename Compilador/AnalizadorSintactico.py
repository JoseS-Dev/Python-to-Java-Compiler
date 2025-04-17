from functions.lexer import *
import ply.yacc as yacc

import io
import sys
from ply import lex, yacc
import matplotlib.pyplot as plt
from functions.arboldraw import agregar_draw_si_falta

# Precedencia de operadores
precedence = (
    ('nonassoc', 'IF', 'ELSE'),
    ('left', 'OR_LOGICO'),
    ('left', 'AND_LOGICO'),
    ('left', 'OR_BIT'),
    ('left', 'XOR_BIT'),
    ('left', 'AND_BIT'),
    ('left', 'IGUAL', 'DISTINTO'),
    ('nonassoc', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'INSTANCEOF'),
    ('left', 'DESPLAZAMIENTO_IZQUIERDO', 'DESPLAZAMIENTO_DERECHO'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'MODULO'),
    ('right', 'UMENOS', 'UMAS' ,'NOT', 'NOT_BIT'),
    ('right', 'INCREMENTO', 'DECREMENTO'),
    ('left', 'PUNTO'),
    ('left', 'CORCHETE_ABIERTO'),
    ('right', 'CORCHETE_CERRADO'),
    ('right', 'TERNARIO', 'DOSPUNTOS'),
)

def p_program(p):
    '''program : package_decl import_decls class_decls
              | import_decls class_decls
              | class_decls'''
    if len(p) == 4:
        p[0] = ('program', p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ('program', None, p[1], p[2])
    else:
        p[0] = ('program', None, None, p[1])

def p_package_decl(p):
    'package_decl : PACKAGE qualified_id PUNTO_Y_COMA'
    p[0] = ('package', p[2])

def p_import_decls(p):
    '''import_decls : import_decl import_decls
                   | import_decl'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_import_decl(p):
    'import_decl : IMPORT qualified_id PUNTO_Y_COMA'
    p[0] = ('import', p[2])

def p_class_decls(p):
    '''class_decls : class_decl class_decls
                  | class_decl'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_class_decl(p):
    'class_decl : class_header LLAVE_ABIERTA class_body LLAVE_CERRADA'
    p[0] = ('class', p[1], p[3])

def p_class_header(p):
    '''class_header : modifiers CLASS ID extends_clause implements_clause
                   | CLASS ID extends_clause implements_clause'''
    if len(p) == 6:
        p[0] = ('class_header', p[1], p[3], p[4], p[5])
    else:
        p[0] = ('class_header', None, p[2], p[3], p[4])

def p_extends_clause(p):
    '''extends_clause : EXTENDS qualified_id
                     | empty'''
    p[0] = ('extends', p[2]) if len(p) == 3 else None

def p_implements_clause(p):
    '''implements_clause : IMPLEMENTS qualified_id_list
                        | empty'''
    p[0] = ('implements', p[2]) if len(p) == 3 else None

def p_class_body(p):
    'class_body : class_members'
    p[0] = p[1]

def p_class_members(p):
    '''class_members : class_member class_members
                    | empty'''
    if len(p) == 3 and p[2]:
        p[0] = [p[1]] + p[2]
    elif len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_class_member(p):
    '''class_member : field_decl
                   | method_decl
                   | constructor_decl
                   | class_decl'''
    p[0] = ('member', p[1])

def p_field_decl(p):
    'field_decl : modifiers type variables PUNTO_Y_COMA'
    p[0] = ('field', p[1], p[2], p[3])

def p_variables(p):
    '''variables : variable COMA variables
                | variable'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_variable(p):
    '''variable : ID
               | ID ASIGNACION expression'''
    if len(p) == 2:
        p[0] = ('variable', p[1], None)
    else:
        p[0] = ('variable', p[1], p[3])

def p_method_decl(p):
    'method_decl : method_header block'
    p[0] = ('method', p[1], p[2])

def p_method_header(p):
    '''method_header : modifiers type ID PARENTESIS_ABIERTO formal_params PARENTESIS_CERRADO
                    | modifiers VOID ID PARENTESIS_ABIERTO formal_params PARENTESIS_CERRADO
                    | modifiers type ID PARENTESIS_ABIERTO PARENTESIS_CERRADO
                    | modifiers VOID ID PARENTESIS_ABIERTO PARENTESIS_CERRADO'''
    if len(p) == 7:
        p[0] = ('method_header', p[1], p[2], p[3], p[5])
    else:
        p[0] = ('method_header', p[1], p[2], p[3], [])

def p_method_call(p):
    '''method_call : ID PARENTESIS_ABIERTO arguments PARENTESIS_CERRADO
                  | THIS PARENTESIS_ABIERTO arguments PARENTESIS_CERRADO
                  | SUPER PARENTESIS_ABIERTO arguments PARENTESIS_CERRADO
                  | NEW creator PARENTESIS_ABIERTO arguments PARENTESIS_CERRADO'''
    p[0] = ('method_call', p[1], p[3])

def p_formal_params(p):
    '''formal_params : formal_param COMA formal_params
                    | formal_param
                    | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = []

def p_formal_param(p):
    '''formal_param : type ID
                   | array_type ID'''
    p[0] = ('param', p[1], p[2])

def p_array_type(p):
    '''array_type : primitive_type CORCHETE_ABIERTO CORCHETE_CERRADO
                 | reference_type CORCHETE_ABIERTO CORCHETE_CERRADO'''
    p[0] = ('array_type', p[1])

def p_constructor_decl(p):
    'constructor_decl : modifiers ID PARENTESIS_ABIERTO formal_params PARENTESIS_CERRADO block'
    p[0] = ('constructor', p[1], p[2], p[4], p[6])

def p_block(p):
    '''block : LLAVE_ABIERTA statements LLAVE_CERRADA
             | LLAVE_ABIERTA LLAVE_CERRADA'''
    if len(p) == 4:
        p[0] = ('block', p[2])
    else:
        p[0] = ('block', [])

def p_statements(p):
    '''statements : statement statements
                 | empty'''
    if len(p) == 3 and p[2]:
        p[0] = [p[1]] + p[2]
    elif len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_statement(p):
    '''statement : block
                | WHILE PARENTESIS_ABIERTO expression PARENTESIS_CERRADO statement
                | DO statement WHILE PARENTESIS_ABIERTO expression PARENTESIS_CERRADO PUNTO_Y_COMA
                | FOR PARENTESIS_ABIERTO for_init PUNTO_Y_COMA expression PUNTO_Y_COMA for_update PARENTESIS_CERRADO statement
                | SWITCH PARENTESIS_ABIERTO expression PARENTESIS_CERRADO LLAVE_ABIERTA switch_cases LLAVE_CERRADA
                | RETURN expression PUNTO_Y_COMA
                | RETURN PUNTO_Y_COMA
                | BREAK PUNTO_Y_COMA
                | CONTINUE PUNTO_Y_COMA
                | THROW expression PUNTO_Y_COMA
                | TRY block catches
                | ASSERT expression PUNTO_Y_COMA
                | TRY block catches FINALLY block
                | expression PUNTO_Y_COMA
                | local_var_decl PUNTO_Y_COMA
                | PUNTO_Y_COMA'''
    # Manejo simplificado para el ejemplo
    if len(p) == 2:
        p[0] = ('statement', p[1])
    elif p[1] == 'if' and len(p) == 6:
        p[0] = ('if', p[3], p[5])
    elif p[1] == 'if' and len(p) == 8:
        p[0] = ('if-else', p[3], p[5], p[7])
    elif p[1] == 'while':
        p[0] = ('while', p[3], p[5])
    elif p[1] == 'do':
        p[0] = ('do-while', p[2], p[5])
    elif p[1] == 'for':
        p[0] = ('for', p[3], p[5], p[7], p[9])
    elif p[1] == 'switch':
        p[0] = ('switch', p[3], p[6])
    elif p[1] in ('return', 'break', 'continue', 'throw'):
        p[0] = (p[1], p[2] if len(p) == 4 else None)
    elif p[1] == 'try' and len(p) == 4:
        p[0] = ('try-catch', p[2], p[3])
    elif p[1] == 'try' and len(p) == 6:
        p[0] = ('try-catch-finally', p[2], p[3], p[5])
    else:
        p[0] = ('expr-statement', p[1])

def p_for_init(p):
    '''for_init : local_var_decl
               | expression_list'''
    p[0] = ('for_init', p[1])

def p_for_update(p):
    'for_update : expression_list'
    p[0] = ('for_update', p[1])

def p_expression_list(p):
    '''expression_list : expression
                      | expression COMA expression_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_switch_cases(p):
    '''switch_cases : switch_case switch_cases
                   | switch_case'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_switch_case(p):
    '''switch_case : CASE expression DOSPUNTOS statements
                  | DEFAULT DOSPUNTOS statements'''
    if p[1] == 'case':
        p[0] = ('case', p[2], p[4])
    else:
        p[0] = ('default', p[3])

def p_catches(p):
    '''catches : catch catches
              | catch'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_catch(p):
    'catch : CATCH PARENTESIS_ABIERTO formal_param PARENTESIS_CERRADO block'
    p[0] = ('catch', p[3], p[5])

def p_local_var_decl(p):
    'local_var_decl : type variables'
    p[0] = ('local_var', p[1], p[2])

def p_type(p):
    '''type : primitive_type
           | reference_type'''
    p[0] = ('type', p[1])

def p_primitive_type(p):
    '''primitive_type : INT
                     | FLOAT
                     | DOUBLE
                     | CHAR
                     | BOOLEAN
                     | SHORT
                     | LONG
                     | STRING
                     | BYTE'''
    p[0] = ('primitive', p[1])

def p_reference_type(p):
    'reference_type : qualified_id'
    p[0] = ('reference', p[1])

def p_qualified_id(p):
    '''qualified_id : ID PUNTO ID
                   | ID'''
    if len(p) == 4:
        p[0] = ('qualified', p[1], p[3])
    else:
        p[0] = ('id', p[1])

def p_qualified_id_list(p):
    '''qualified_id_list : qualified_id COMA qualified_id_list
                        | qualified_id'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expression(p):
    '''expression : assignment_expression'''
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : conditional_expression
                           | ID assignment_operator expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('assign', p[1], p[2], p[3])

def p_assignment_operator(p):
    '''assignment_operator : ASIGNACION
                          | ASIGNACION_SUMA
                          | ASIGNACION_RESTA
                          | ASIGNACION_MULTIPLICACION
                          | ASIGNACION_DIVISION
                          | ASIGNACION_MODULO
                          | DESPLAZAMIENTO_IZQUIERDO_ASIGNACION
                          | DESPLAZAMIENTO_DERECHO_ASIGNACION'''
    p[0] = ('assign_op', p[1])

def p_conditional_expression(p):
    '''conditional_expression : logical_or_expression
                             | logical_or_expression TERNARIO expression DOSPUNTOS conditional_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('ternary', p[1], p[3], p[5])

def p_logical_or_expression(p):
    '''logical_or_expression : logical_and_expression
                            | logical_or_expression OR_LOGICO logical_and_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_logical_and_expression(p):
    '''logical_and_expression : inclusive_or_expression
                             | logical_and_expression AND_LOGICO inclusive_or_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_inclusive_or_expression(p):
    '''inclusive_or_expression : exclusive_or_expression
                              | inclusive_or_expression OR_BIT exclusive_or_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_exclusive_or_expression(p):
    '''exclusive_or_expression : and_expression
                              | exclusive_or_expression XOR_BIT and_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_and_expression(p):
    '''and_expression : equality_expression
                      | and_expression AND_BIT equality_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_equality_expression(p):
    '''equality_expression : relational_expression
                          | equality_expression IGUAL relational_expression
                          | equality_expression DISTINTO relational_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_relational_expression(p):
    '''relational_expression : shift_expression
                            | relational_expression MENOR shift_expression
                            | relational_expression MAYOR shift_expression
                            | relational_expression MENOR_IGUAL shift_expression
                            | relational_expression MAYOR_IGUAL shift_expression
                            | relational_expression INSTANCEOF reference_type'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_shift_expression(p):
    '''shift_expression : additive_expression
                       | shift_expression DESPLAZAMIENTO_IZQUIERDO additive_expression
                       | shift_expression DESPLAZAMIENTO_DERECHO additive_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_additive_expression(p):
    '''additive_expression : multiplicative_expression
                          | additive_expression SUMA multiplicative_expression
                          | additive_expression RESTA multiplicative_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_multiplicative_expression(p):
    '''multiplicative_expression : unary_expression
                                | multiplicative_expression MULTIPLICACION unary_expression
                                | multiplicative_expression DIVISION unary_expression
                                | multiplicative_expression MODULO unary_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary', p[2], p[1], p[3])

def p_unary_expression(p):
    '''unary_expression : postfix_expression
                       | INCREMENTO unary_expression
                       | DECREMENTO unary_expression
                       | SUMA unary_expression
                       | RESTA unary_expression
                       | UMAS unary_expression
                       | UMENOS unary_expression
                       | NOT unary_expression
                       | NOT_BIT unary_expression
                       '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('unary', p[1], p[2])

def p_if_statement(p):
    '''statement : IF PARENTESIS_ABIERTO expression PARENTESIS_CERRADO statement %prec IF
                 | IF PARENTESIS_ABIERTO expression PARENTESIS_CERRADO statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if-else', p[3], p[5], p[7])

def p_postfix_expression(p):
    '''postfix_expression : primary
                         | postfix_expression INCREMENTO
                         | postfix_expression DECREMENTO
                         | postfix_expression PUNTO member_access %prec PUNTO
                         | postfix_expression CORCHETE_ABIERTO expression CORCHETE_CERRADO'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('postfix', p[1], p[2])
    elif p[2] == '[':
        p[0] = ('array_access', p[1], p[3])
    else:
        p[0] = ('member_access', p[1], p[3])

def p_member_access(p):
    '''member_access : ID
                    | THIS
                    | SUPER
                    | NEW creator
                    | method_call'''
    if len(p) == 2:
        p[0] = ('member', p[1])
    else:
        p[0] = ('new_member', p[2])

def p_primary(p):
    '''primary : literal
              | THIS
              | SUPER
              | PARENTESIS_ABIERTO expression PARENTESIS_CERRADO
              | NEW creator
              | qualified_id'''
    if len(p) == 2:
        p[0] = ('primary', p[1])
    elif p[1] == '(':
        p[0] = p[2]
    elif p[1] == 'new':
        p[0] = ('new', p[2])

def p_literal(p):
    '''literal : NUMERO
              | CADENA
              | TRUE
              | FALSE
              | NULL
              | OCTAL_NUMERO
              | HEX_NUMERO
              | BINARIO_NUMERO'''
    p[0] = ('literal', p[1])

def p_creator(p):
    '''creator : qualified_id PARENTESIS_ABIERTO arguments PARENTESIS_CERRADO
              | qualified_id CORCHETE_ABIERTO expression CORCHETE_CERRADO
              | qualified_id CORCHETE_ABIERTO CORCHETE_CERRADO
              | primitive_type CORCHETE_ABIERTO expression CORCHETE_CERRADO
              | primitive_type CORCHETE_ABIERTO CORCHETE_CERRADO'''
    if len(p) == 5:
        p[0] = ('creator', p[1], p[3])
    else:
        p[0] = ('creator', p[1], None)

def p_arguments(p):
    '''arguments : expression_list
                | empty'''
    p[0] = ('args', p[1] if p[1] else [])

def p_modifiers(p):
    '''modifiers : modifier modifiers
                | modifier'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_modifier(p):
    '''modifier : PUBLIC
               | PRIVATE
               | PROTECTED
               | STATIC
               | FINAL
               | ABSTRACT
               | NATIVE
               | SYNCHRONIZED
               | VOLATILE
               | EXPORT
               | INTERFACE
               | TRANSIENT'''
    p[0] = ('modifier', p[1])

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en línea {p.lineno}, token '{p.value}'")
    else:
        print("Error de sintaxis: final inesperado del archivo")
def draw_ast_node(ax, node, x, y, dx, dy):
    """Dibuja el nodo y sus hijos recursivamente con separación visual"""
    label = node.__class__.__name__
    if hasattr(node, '__dict__'):
        text = label
    else:
        text = str(node)

    # Dibuja el nodo actual
    ax.text(x, y, text, bbox=dict(facecolor='white', edgecolor='black'), ha='center', fontsize=10)

    # Obtener hijos del nodo
    children = []
    for attr in vars(node).values():
        if isinstance(attr, list):
            children.extend([c for c in attr if hasattr(c, '__dict__')])
        elif hasattr(attr, '__dict__'):
            children.append(attr)

    num = len(children)
    if num == 0:
        return

    spacing = dx / max(num - 1, 1) if num > 1 else 0  # separación entre hijos
    start_x = x - (spacing * (num - 1) / 2)  # posición inicial centrada

    for i, child in enumerate(children):
        child_x = start_x + i * spacing
        child_y = y - dy
        ax.plot([x, child_x], [y, child_y], color='black')  # Línea entre padre e hijo
        draw_ast_node(ax, child, child_x, child_y, dx / 1.5, dy)

def visualize_tree(root):
    fig, ax = plt.subplots(figsize=(20, 12))  # Tamaño de la figura
    draw_ast_node(ax, root, x=0, y=0, dx=40, dy=5)  # Ajusta dx y dy para espaciamiento
    ax.axis('off')
    plt.tight_layout()
    plt.show()

def proceso_parser(e):
    text_field_value = e.control.parent.parent.controls[1].controls[0].value
    try:
        if not text_field_value.strip():
            print("La entrada está vacía.")
            return

        # Configura el lexer y el parser
        lexer.input(text_field_value)
        parser = yacc.yacc(text_field_value, lexer=lexer)

        # Limpia los controles de salida
        e.control.parent.parent.controls[1].controls[2].controls[0].value = ''
        e.control.parent.parent.controls[1].controls[2].controls[1].value = ''
        e.control.parent.parent.controls[1].controls[2].update()

        # Redirige la salida estándar y la salida de error a objetos StringIO
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        agregar_draw_si_falta()

        # Ejecuta el parser y captura la salida
        result = parser.parse(text_field_value, debug=True)  # Aquí se genera la salida de depuración

        # Recupera la salida capturada (incluyendo la salida de depuración)
        output = sys.stdout.getvalue()
        outputdebug = sys.stderr.getvalue()
        if not output.strip():
            output = "Análisis sintáctico completado sin errores."

        # Restaura la salida estándar y de error
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        # Asigna la salida capturada al control correspondiente
        e.control.parent.parent.controls[1].controls[2].controls[0].value = output
        e.control.parent.parent.controls[1].controls[2].controls[1].value = outputdebug

        # Visualiza el árbol sintáctico
        visualize_tree(result)

    except Exception as ex:
        print(f"Ocurrió un error al procesar el texto: {ex}")
    e.control.parent.parent.controls[1].controls[2].update()