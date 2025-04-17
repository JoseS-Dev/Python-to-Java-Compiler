# Analizador Lexico
import flet as ft
import ply.lex as lex

# Definición de las palabras reservadas
reservadas = {
    # Condicionales
    'if': 'IF', "else": 'ELSE',
    # Ciclos
    'for': 'FOR', 'while': 'WHILE', 'do': 'DO',
    # Funciones
    'abstract': 'ABSTRACT', 'public': 'PUBLIC', 'private': 'PRIVATE', 'protected': 'PROTECTED',
    'static': 'STATIC', 'void': 'VOID', 'return': 'RETURN', 'package': 'PACKAGE',
    'import': 'IMPORT', 'class': 'CLASS', 'extends': 'EXTENDS', 'implements': 'IMPLEMENTS',
    'new': 'NEW', 'this': 'THIS', 'super': 'SUPER',

    # Tipos de datos
    'int': 'INT', 'float': 'FLOAT', 'double': 'DOUBLE', 'char': 'CHAR',
    'string': 'STRING', 'boolean': 'BOOLEAN',

    # Manipulacion de errores
    'try': 'TRY', 'catch': 'CATCH', 'finally': 'FINALLY', 'throw': 'THROW', 'assert': 'ASSERT',

    # Otros
    'export': 'EXPORT', 'native': 'NATIVE', 'synchronized': 'SYNCHRONIZED',
    'volatile': 'VOLATILE', 'transient': 'TRANSIENT',
    'default': 'DEFAULT', 'case': 'CASE','break': 'BREAK', 'continue': 'CONTINUE', 'instanceof': 'INSTANCEOF',
    'final': 'FINAL', 'short': 'SHORT', 'long': 'LONG',
    'byte': 'BYTE', 'interface': 'INTERFACE', 'switch': 'SWITCH'
}

# Lista de tokens
tokens = list(reservadas.values()) + [
    'ID', 'NUMERO', 'CADENA',
    'ASIGNACION', 'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION',
    'MODULO', 'INCREMENTO', 'DECREMENTO',
    'NOT', 'IGUAL', 'DISTINTO', 'MAYOR', 'MENOR', 'MAYOR_IGUAL',
    'MENOR_IGUAL', 'PARENTESIS_ABIERTO', 'PARENTESIS_CERRADO',
    'LLAVE_ABIERTA', 'LLAVE_CERRADA', 'CORCHETE_ABIERTO', 'CORCHETE_CERRADO',
    'PUNTO_Y_COMA', 'COMA', 'PUNTO', 'DOSPUNTOS', 'AND_LOGICO',
    'OR_LOGICO', 'OCTAL_NUMERO', 'HEX_NUMERO', 'BINARIO_NUMERO', 'TERNARIO',
    'TRUE', 'FALSE', 'NULL', 'AND_BIT', 'OR_BIT', 'XOR_BIT',
    'NOT_BIT', 'DESPLAZAMIENTO_IZQUIERDO', 'DESPLAZAMIENTO_DERECHO',
    'DESPLAZAMIENTO_IZQUIERDO_ASIGNACION', 'DESPLAZAMIENTO_DERECHO_ASIGNACION',
    'ASIGNACION_SUMA', 'ASIGNACION_RESTA','ASIGNACION_MULTIPLICACION', 'ASIGNACION_DIVISION', 'ASIGNACION_MODULO',
    'UMENOS', 'UMAS'
]

# Definición de los tokens
t_NUMERO = r'\d+(\.\d+)?'  # Números enteros y decimales
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'
t_ASIGNACION = r'='
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'
t_NOT = r'!'
t_IGUAL = r'=='
t_DISTINTO = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_PARENTESIS_ABIERTO = r'\('
t_PARENTESIS_CERRADO = r'\)'
t_LLAVE_ABIERTA = r'\{'
t_LLAVE_CERRADA = r'\}'
t_CORCHETE_ABIERTO = r'\['
t_CORCHETE_CERRADO = r'\]'
t_PUNTO_Y_COMA = r';'
t_COMA = r','
t_PUNTO = r'\.'
t_DOSPUNTOS = r':'
t_UMENOS = r'\-'
t_UMAS = r'\+'
t_AND_LOGICO = r'&&'
t_OR_LOGICO = r'\|\|'
t_TERNARIO = r'\?\:'
t_TRUE = r'true'
t_FALSE = r'false'
t_NULL = r'null'
t_AND_BIT = r'&'
t_OR_BIT = r'\|'
t_XOR_BIT = r'\^'
t_NOT_BIT = r'~'
t_DESPLAZAMIENTO_IZQUIERDO = r'<<'
t_DESPLAZAMIENTO_DERECHO = r'>>'
t_DESPLAZAMIENTO_IZQUIERDO_ASIGNACION = r'<<='
t_DESPLAZAMIENTO_DERECHO_ASIGNACION = r'>>='
t_ASIGNACION_SUMA = r'\+='
t_ASIGNACION_RESTA = r'-='
t_ASIGNACION_MULTIPLICACION = r'\*='
t_ASIGNACION_DIVISION = r'/='
t_ASIGNACION_MODULO = r'%='


def t_OCTAL_NUMBER(t):
    r'0[0-7]+'
    t.type = 'OCTAL_NUMERO'
    t.value = int(t.value, 8)
    return t

def t_HEX_NUMBER(t):
    r'0[xX][0-9a-fA-F]+'
    t.type = 'HEX_NUMERO'
    t.value = int(t.value, 16)
    return t

def t_BINARIO_NUMERO(t):
    r'0[bB][01]+'
    t.type = 'BINARIO_NUMERO'
    t.value = int(t.value, 2)
    return t

def t_INT(t):
    r'\d+'
    t.type = 'NUMERO'
    t.value = int(t.value)  # Convertir a entero
    return t

def t_MAIN(t):
    r'main'
    t.type = 'ID'
    return t


def t_FLOAT(t):
    r'\d+\.\d+'
    t.type = 'NUMERO'
    t.value = float(t.value)  # Convertir a float
    return t

def t_DOUBLE(t):
    r'\d+\.\d+[dD]'
    t.type = 'NUMERO'
    t.value = float(t.value[:-1])  # Convertir a float y eliminar la 'd' o 'D'
    return t


def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    t.type = 'CADENA'
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

def t_ID(t):
    r'[a-zA-Z_\u00A0-\uFFFF][a-zA-Z0-9_\u00A0-\uFFFF]*'
    t.type = reservadas.get(t.value, 'ID')  # Verifica si es una palabra reservada
    return t

def t_COMENTARIO_1(t):
    r'//.*\n'
    t.lexer.lineno += 1  # Aumentar el número de línea

def t_COMENTARIO_MULTILINEA(t):
    r'/\*.*?\*/'
    t.lexer.lineno += t.value.count('\n')  # Aumentar el número de línea
    t.value = t.value.replace('\n', '')  # Eliminar saltos de línea en el comentario

def t_newLine(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # Aumentar el número de línea

t_ignore = ' \t'  # Ignorar espacios y tabulaciones

def t_error(t):
    print(f"Caracter no reconocido: {t.value[0]}")
    t.lexer.skip(1)

# Define el lexer (asegúrate de que esté configurado previamente)
lexer = lex.lex()
def proceso_lexer(e):
    """
    Procesa el texto de un TextField utilizando un lexer y muestra los tokens.
    """
    text_field_value = e.control.parent.parent.controls[1].controls[0].value
    try:
        # Verifica si el texto no está vacío
        if not text_field_value.strip():
            print("El TextField está vacío.")
            return

        

        # Procesa el texto del TextField
        lexer.input(text_field_value)

        # Limpia las filas existentes en el DataTable
        e.control.parent.parent.controls[1].controls[1].controls[0].rows.clear()

        # Itera sobre los tokens y los añade al DataTable
        for token in lexer:
            e.control.parent.parent.controls[1].controls[1].controls[0].rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(token.type)),
                        ft.DataCell(ft.Text(token.value)),
                    ]
                )
            )

        # Actualiza el DataTable una vez que todas las filas han sido añadidas
        e.control.parent.parent.controls[1].controls[1].controls[0].update()

    except Exception as e:
        print(f"Ocurrió un error al procesar el texto: {e}")
        return