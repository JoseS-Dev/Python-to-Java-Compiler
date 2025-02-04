import ply.lex as lex

#Valores Reservados
reservados = {
    #Tipos de datos
    "boolean": 'TYPE_BOOLEAN',
    "int": 'TYPE_INT',
    "float": 'TYPE_FLOAT',
    "double": 'TYPE_DOUBLE',
    "char": 'TYPE_CHAR',
    "String": 'TYPE_STRING',
    "void": 'TYPE_VOID',

    #Metodos
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

#Tokens
tokens = ['INT_NUMBER','FLOAT_NUMBER','BYTE_NUMBER','DOUBLE_NUMBER',
'CHAR','STRING','LONG_NUMBER','BITWISE_XOR_EQ','BITWISE_OR_EQ','BITWISE_AND_EQ',
'BITWISE_XOR','BITWISE_NOT','BITWISE_OR','BITWISE_AND','EQUAL','POT','LPAREN','RPAREN',
'COMMA','DOT','LCHAV','RCHAV','SEMICOLON','PLUS','MINUS','TIMES','DIVIDE','EQ','NEQ',
'LT','GT','LEQ','GEQ','AND','OR','NOT','LSHIFT_EQ','RSHIFT_EQ','URSHIFT_EQ','ID','RBRACKET',
'LBRACKET','HEXA_NUMBER','OCTAL_NUMBER','BIN_NUMBER','INCREMENT','DECREMENT','TERNARY','MODULE'
]