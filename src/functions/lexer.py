import flet as ft
import ply.lex as lex

# Valores Reservados
reservados = {
    # Tipos de datos
    "boolean": 'TYPE_BOOLEAN',
    "int": 'TYPE_INT',
    "float": 'TYPE_FLOAT',
    "double": 'TYPE_DOUBLE',
    "char": 'TYPE_CHAR',
    "String": 'TYPE_STRING',
    "void": 'TYPE_VOID',
    # Métodos
    "public": 'PUBLIC',
    "private": 'PRIVATE',
    "default": 'DEFAULT',
    "protected": 'PROTECTED',
    # Identificadores
    "abstract": 'ABSTRACT',
    "assert": 'ASSERT',
    "break": 'BREAK',
    "case": 'CASE',
    "catch": 'CATCH',
    "class": 'CLASS',
    "var": 'VAR',
    "continue": 'CONTINUE',
    "do": 'DO',
    "else": 'ELSE',
    "enum": 'ENUM',
    "extends": 'EXTENDS',
    "final": 'FINAL',
    "finally": 'FINALLY',
    "for": 'FOR',
    "goto": 'GOTO',
    "if": 'IF',
    "implements": 'IMPLEMENTS',
    "import": 'IMPORT',
    "instanceof": 'INSTANCEOF',
    "interface": 'INTERFACE',
    "native": 'NATIVE',
    "new": 'NEW',
    "package": 'PACKAGE',
    "return": 'RETURN',
    "short": 'SHORT',
    "static": 'STATIC',
    "strictfp": 'STRICTFP',
    "super": 'SUPER',
    "switch": 'SWITCH',
    "synchronized": 'SYNCHRONIZED',
    "this": 'THIS',
    "throw": 'THROW',
    "throws": 'THROWS',
    "transient": 'TRANSIENT',
    "try": 'TRY',
    "volatile": 'VOLATILE',
    "while": 'WHILE'  
}

# Tokens
tokens = ['INT_NUMBER', 'FLOAT_NUMBER', 'BYTE_NUMBER', 'DOUBLE_NUMBER',
          'CHAR', 'STRING', 'LONG_NUMBER', 'BITWISE_XOR_EQ', 'BITWISE_OR_EQ', 'BITWISE_AND_EQ',
          'BITWISE_XOR', 'BITWISE_NOT', 'BITWISE_OR', 'BITWISE_AND', 'EQUAL', 'POT', 'LPAREN', 'RPAREN',
          'COMMA', 'DOT', 'LCHAV', 'RCHAV', 'SEMICOLON', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQ', 'NEQ',
          'LT', 'GT', 'LEQ', 'GEQ', 'AND', 'OR', 'NOT', 'LSHIFT_EQ', 'RSHIFT_EQ', 'URSHIFT_EQ', 'ID', 'RBRACKET',
          'LBRACKET', 'HEXA_NUMBER', 'OCTAL_NUMBER', 'BIN_NUMBER', 'INCREMENT', 'DECREMENT', 'TERNARY', 'MODULE',
'URSHIFT','PLUS_EQ','TIMES_EQ','LSHIFT','RSHIFT','MINUS_EQ','DIVIDE_EQ','MOD_EQ'
] + list(reservados.values())

# Expresiones regulares para los tokens
t_URSHIFT_EQ = r'>>>='
t_LSHIFT_EQ  = r'<<='
t_RSHIFT_EQ  = r'>>='
t_URSHIFT  = r'>>>'
t_LSHIFT  = r'<<'
t_RSHIFT = r'>>'
t_LEQ = r'<='
t_GEQ = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_PLUS_EQ = r'\+='
t_MINUS_EQ = r'-='
t_TIMES_EQ = r'\*='
t_DIVIDE_EQ = r'/='
t_MOD_EQ = r'%='
t_MODULE = r'%'
t_BITWISE_AND_EQ = r'&='
t_BITWISE_OR_EQ = r'\|='
t_BITWISE_XOR_EQ = r'^='
t_EQ = r'=='
t_NEQ = r'!='
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_LCHAV = r'{'
t_RCHAV = r'}'
t_SEMICOLON = r';'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_NOT = r'!'
t_TERNARY = r'\?'
t_BITWISE_AND = r'&'
t_BITWISE_OR = r'\|'
t_BITWISE_XOR = r'\^'
t_BITWISE_NOT = r'~'
t_ignore = ' \t'

# Función para comentarios
def t_comments_1(t):
    r'//.*\n'
    t.lexer.lineno += 1

def t_comments_2(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += len(t.value)

# Función que identifica números binarios
def t_BIN_NUMBER(t):
    r'0b[01]+'
    t.value = int(t.value, base=2)
    return t

# Función que identifica números octales
def t_OCTAL_NUMBER(t):
    r'0[0-7]+'
    t.value = int(t.value, base=8)
    return t

# Función que identifica números hexadecimales
def t_HEXA_NUMBER(t):
    r'0(x|X)[a-fA-F0-9]+'
    t.value = int(t.value, base=16)
    return t

# Función que identifica datos tipo Float
def t_FLOAT_NUMBER(t):
    r'\d+\.\d+(f|F)'
    t.value = float(t.value)
    return t

# Función que identifica datos tipo double
def t_DOUBLE_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Función que identifica datos tipo int
def t_INT_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Función que identifica datos tipo char
def t_CHAR(t):
    r"'([^'\\]|\\.)'"
    return t

# Función que identifica datos tipo String  
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    return t

# Función que identifica un identificador reservado
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservados.get(t.value, 'ID')
    return t

# Función para realizar un nuevo salto de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función para detectar un carácter ilegal
def t_error(t):
    print("Caracter Ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

def proceso_lexer(e):
    """
    Procesa el texto de un TextField utilizando un lexer y muestra los tokens.

    Parámetros:
        text_field_value (str): El texto obtenido de un TextField.
    """
    text_field_value = e.control.parent.controls[1].controls[0].value
    try:
        # Verifica si el texto no está vacío
        if not text_field_value.strip():
            print("El TextField está vacío.")
            return

        # Define el lexer (asegúrate de que esté configurado previamente)
        lexer = lex.lex()

        # Procesa el texto del TextField
        lexer.input(text_field_value)

        # Limpia las filas existentes en el DataTable
        e.control.parent.controls[1].controls[1].controls[0].rows.clear()

        # Itera sobre los tokens y los añade al DataTable
        for token in lexer:
            e.control.parent.controls[1].controls[1].controls[0].rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(token.type)),
                        ft.DataCell(ft.Text(token.value)),
                    ]
                )
            )

        # Actualiza el DataTable una vez que todas las filas han sido añadidas
        e.control.parent.controls[1].controls[1].controls[0].update()

    except Exception as e:
        print(f"Ocurrió un error al procesar el texto: {e}")
        return