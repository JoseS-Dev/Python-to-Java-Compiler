from AnalizadorLexico import *
import ply.yacc as yacc
from Arbol_sintactico import sintaxis as SA

predendencias = (
    ('left', 'EQUAL','MINUS_EQ','TIMES_EQ','PLUS_EQ','DIVIDE_EQ','MOD_EQ','BITWISE_AND_EQ','BITWISE_OR_EQ','BITWISE_XOR_EQ','URSHIFT_EQ','LSHIFT_EQ','RSHIFT_EQ'),
    ('left','OR'),
    ('left','AND'),
    ('left','BITWISE_OR'),
    ('left','BITWISE_XOR'),
    ('left','BITWISE_AND'),
    ('left','EQ','NEQ'),
    ('left','LT','GT','LEQ','GEQ'),
    ('left','LSHIFT','RSHIFT','URSHIFT'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MODULE'),
    ('left','INCREMENT','DECREMENT'),
)

### Definicion de la gramatica
def p_program(p):
    ''' program : class'''
    p[0] = SA.ProgramCompiler(p[1])

### clases
def p_class_extends(p):
    ''' class : visibility ClassModifier ID EXTENDS ID ID LCHAV members RCHAV '''
    p[0] = SA.ClassExtends(p[1],p[2],p[4],p[6],p[8])

def p_class_default(p):
    ''' class : visibility ClassModifier ID LCHAV members RCHAV '''
    p[0] = SA.ClassDefault(p[1],p[2],p[4], p[6])

def p_class_implements(p):
    ''' class : visibility ClassModifier ID IMPLEMENTS ID LCHAV members RCHAV'''
    p[0] = SA.ClassImplements(p[1],p[2],p[4],p[7])

### Visibilidad
def p_visibility_public(p):
    '''visibility : PUBLIC'''
    p[0] = SA.visibilityConcrete(p[1])

def p_visibility_private(p):
    '''visibility : PRIVATE'''
    p[0] = SA.visibilityConcrete(p[1])

def p_visibility_protected(p):
    '''visibility : PROTECTED'''
    p[0] = SA.visibilityConcrete(p[1])

def p_visibility_default(p):
    '''visibility : '''
    p[0] = SA.visibilityConcrete(None)

### Modificador de clase
def p_classModifier_default(p):
    '''classmodifer : '''
    p[0] = SA.ClassModifyConcrete(None)

def p_classModifier_abstract(p):
    '''classmodifer : ABSTRACT'''
    p[0] = SA.ClassModifyConcrete(p[1])

def p_classModifier_final(p):
    '''classmodifer : FINAL'''
    p[0] = SA.ClassModifyConcrete(p[1])

def p_classModifier_package(p):
    '''classmodifer : PACKAGE'''
    p[0] = SA.ClassModifyConcrete(p[1])

### Miembros de la clase
def p_member(p):
    '''members : member'''
    p[0] = SA.MembersUni(p[1])

def p_members(p):
    '''members : member members'''
    p[0] = SA.MembersMult(p[1],p[2])

### Miembro
def p_membro_atribute(p):
    '''miembro : atribute'''
    p[0] = SA.MemberAtribute(p[1])

def p_membrofunction(p):
    '''miembro : function'''    
    p[0] = SA.MemberFunction(p[1])

# Atributos
def p_atribute(p):
    '''atributo : visibility atributemodifier type ID SEMICOLON'''
    p[0] = SA.AtributeDefault(p[1], p[2], p[3], p[4])

def p_atribute_inicialized_type(p):
    '''atributo : visibility atributemodifier type ID EQUAL expression SEMICOLON'''
    p[0] = SA.AtributeDefaultInicializedType(p[1], p[2], p[3], p[4], p[6])

### Modificador de atributo
def p_atributemodifier_default(p):
    '''ModificadorAtributo : '''
    p[0] = SA.AtributeModifierConcrete(None)

def p_atributemodifier_static(p):
    '''ModificadorAtributo : STATIC'''
    p[0] = SA.AtributeModifierConcrete(p[1])


def p_atributemodifier_final(p):
    '''ModificadorAtributo : FINAL'''
    p[0] = SA.AtributeModifierConcrete(p[1])

### Funciones
def p_function(p):
    '''function : signature body'''
    p[0] = SA.FunctionDefault(p[1], p[2])

### Signature (firma)
def p_signature_simple(p):
    '''signature : visibility atributemodifier type ID LPAREN sigparams RPAREN '''
    p[0] = SA.SignatureSimple(p[1], p[2], p[3], p[4], p[6])

def p_signature_list(p):
    '''signature : visibility atributemodifier type brackets_expression ID LPAREN sigparams RPAREN '''
    p[0] = SA.SignatureMult(p[1], p[2], p[3], p[4], p[5], p[7])

### Parametros de la firma
def p_sigparams_id(p):
    '''sigparams : type ID  '''
    p[0] = SA.SigparamsId(p[1], p[2])

def p_sigparams_sigparams(p):
    '''sigparams : type ID COMMA sigparams'''
    p[0] = SA.SigparamsSigparams(p[1], p[2], p[4])

### Cuerpo de la funcion
def p_body(p):
    '''body : LCHAV stms RCHAV'''
    p[0] = SA.BodyStms(p[2])

### Sentencias
def p_stms(p):
    '''stms : stm '''
    p[0] = SA.StmsUni(p[1])

def p_multistms(p):
    '''stms : stm stms '''
    p[0] = SA.StmsMulti(p[1], p[2])

### Sentencia
def p_stm_exp(p):
    '''stm : expression SEMICOLON'''
    p[0] = SA.StmExpression(p[1])

def p_stm_while(p):
    '''stm : WHILE LPAREN expression RPAREN bodyorstm'''
    p[0] = SA.StmExpressionWhile(p[3], p[5])

def p_stm_dowhile(p):
    '''stm : DO bodyorstm WHILE LPAREN expression RPAREN SEMICOLON '''
    p[0] = SA.StmExpressionDoWhile(p[2], p[5])

def p_stm_for(p):
    '''stm : FOR LPAREN expression_for SEMICOLON expression SEMICOLON expression RPAREN bodyorstm'''
    p[0] = SA.StmExpressionFor(p[3], p[5], p[7], p[9])

def p_stm_if(p):
    '''stm : IF LPAREN expression RPAREN bodyorstm'''
    p[0] = SA.StmExpressionIf(p[3], p[5])

def p_stm_ifelse(p):
    '''stm : IF LPAREN expression RPAREN bodyorstm ELSE bodyorstm'''
    p[0] = SA.StmExpressionIfElse(p[3], p[5], p[7])

def p_stm_elseif(p):
    '''stm : IF LPAREN expression RPAREN bodyorstm ELSE IF bodyorstm'''
    p[0] = SA.StmExpressionElseIf(p[3], p[5], p[8])

def p_stm_semicollon(p):
    '''stm : SEMICOLON '''
    p[0] = SA.StmExpressionSemicolon(None)

def p_stm_variable(p):
    '''stm : atributemodifier type ID SEMICOLON'''
    p[0] = SA.StmExpressionVariable(p[1], p[2], p[3])

def p_stm_variable_type(p):
    '''stm : atributemodifier type ID EQUAL expression SEMICOLON'''
    p[0] = SA.StmExpressionVariableType(p[1], p[2], p[3], p[5])
    

def p_stm_variable_type_list(p):
    '''stm : atributemodifier type ID LBRACKET RBRACKET SEMICOLON'''
    p[0] = SA.StmExpressionVariableTypeList(p[1], p[2], p[3])

def p_stm_variable_type_list_pre(p):
    '''stm : atributemodifier type LBRACKET RBRACKET ID SEMICOLON'''
    p[0] = SA.StmExpressionVariableTypeListPre(p[1], p[2], p[5])	

def p_stm_variable_type_list_list_pre(p):
    '''stm : atributemodifier type LBRACKET RBRACKET ID EQUAL chav_exp SEMICOLON'''
    p[0] = SA.StmExpressionVariableTypeListListPre(p[1], p[2], p[5], p[7])

def p_stm_variable_type_list_expression(p):
    '''stm : atributemodifier type ID LBRACKET RBRACKET EQUAL expression SEMICOLON'''
    p[0] = SA.StmExpressionVariableTypeListExpression(p[1], p[2], p[3], p[7])

def p_stm_variable_type_list_expression_inicialized(p):
    '''stm : atributemodifier type ID LBRACKET RBRACKET EQUAL chav_exp SEMICOLON'''
    p[0] = SA.StmExpressionVariableTypeListExpressionInicialized(p[1], p[2], p[3], p[7])

def p_stm_variable_type_list_list(p):
    '''stm : atributemodifier type LBRACKET RBRACKET ID LBRACKET RBRACKET SEMICOLON'''
    p[0] = SA.StmExpressionVariableTypeListList(p[1], p[2], p[5])

def p_stm_variable_type_list_list_inicialized(p):
    '''stm : atributemodifier type LBRACKET RBRACKET ID LBRACKET RBRACKET EQUAL chav_exp SEMICOLON'''
    p[0] = SA.StmExpressionVariableTypeListListInicialized(p[1], p[2], p[5], p[9])

def p_stm_return(p):
    '''stm : RETURN expression SEMICOLON'''
    p[0] = SA.StmExpressionReturn(p[2])

def p_stm_void_return(p):
    '''stm : RETURN SEMICOLON'''
    p[0] = SA.StmExpressionVoidReturn(None)

### Cuerpo o sentencia
def p_bodyorstm_body(p):
    '''bodyorstm : body'''
    p[0] = SA.BodyOrStmBody(p[1])

### Expresion for
def p_expression_assign_for_type(p):
    ''' expression_for : type ID EQUAL expression  '''
    p[0] = SA.ExpressionForAssignForType(p[1], p[2], p[4])

def p_expression_assign_for(p):
    ''' expression_for : ID EQUAL expression  '''
    p[0] = SA.ExpressionForAssignFor(p[1], p[3])

### Expresiones
def p_expression_operator(p):
    ''' expression : operator '''
    p[0] = SA.ExpressionOperator(p[1])

def p_expression_call(p):
    ''' expression : call '''
    p[0] = SA.ExpressionCall(p[1])

def p_expression_FLOAT_NUMBER(p):
    ''' expression : FLOAT_NUMBER '''
    p[0] = SA.ExpressionFloatNumber(p[1])

def p_expression_DOUBLE_NUMBER(p):
    ''' expression : DOUBLE_NUMBER '''
    p[0] = SA.ExpressionDoubleNumber(p[1])

def p_expression_INT_NUMBER(p):
    ''' expression : INT_NUMBER '''
    p[0] = SA.ExpressionIntNumber(p[1])

def p_expression_STRING(p):
    ''' expression : STRING '''
    p[0] = SA.ExpressionString(p[1])

def p_expression_ID (p):
    ''' expression : ID  '''
    p[0] = SA.ExpressionId(p[1])

def p_expression_new(p):
    '''expression : NEW type LPAREN params_call RPAREN '''
    p[0] = SA.ExpressionNew(p[2], p[4])

def p_expression_new_list(p):
    '''expression : NEW type LBRACKET expression RBRACKET '''
    p[0] = SA.ExpressionNewList(p[2], p[4])

### Operadores
def p_operator_arithmetic_times(p):
    '''operator : expression TIMES expression'''
    p[0] = SA.OperatorArithmeticTimes(p[1], p[3])

def p_operator_arithmetic_divide(p):
    '''operator : expression DIVIDE expression'''
    p[0] = SA.OperatorArithmeticDivide(p[1], p[3])

def p_operator_arithmetic_module(p):
    '''operator : expression MODULE expression'''
    p[0] = SA.OperatorArithmeticModule(p[1], p[3])

def p_operator_arithmetic_plus(p):
    '''operator : expression PLUS expression'''
    p[0] = SA.OperatorArithmeticPlus(p[1], p[3])

def p_operator_arithmetic_minus(p):
    '''operator : expression MINUS expression'''
    p[0] = SA.OperatorArithmeticMinus(p[1], p[3])

def p_operator_assign_EQUAL(p):
    '''operator : ID EQUAL expression'''
    p[0] = SA.OperatorAssignEqual(p[1], p[3])

def p_operator_assign_MINUS_EQ(p):
    '''operator : ID MINUS_EQ expression'''
    p[0] = SA.OperatorAssignMinusEQ(p[1], p[3])

def p_operator_assign_TIMES_EQ(p):
    '''operator : ID TIMES_EQ expression'''
    p[0] = SA.OperatorAssignTimesEQ(p[1], p[3])

def p_operator_assign_PLUS_EQ(p):
    '''operator : ID PLUS_EQ expression'''
    p[0] = SA.OperatorAssignPlusEQ(p[1], p[3])

def p_operator_assign_DIVIDE_EQ(p):
    '''operator : ID DIVIDE_EQ expression'''
    p[0] = SA.OperatorAssignDivideEQ(p[1], p[3])

def p_operator_assign_MOD_EQ(p):
    '''operator : ID MOD_EQ expression'''
    p[0] = SA.OperatorAssignModuleEQ(p[1], p[3])

def p_operator_assign_BITWISE_AND_EQ(p):
    '''operator : ID BITWISE_AND_EQ expression'''
    p[0] = SA.OperatorAssignBitwiseAndEQ(p[1], p[3])

def p_operator_assign_BITWISE_OR_EQ(p):
    '''operator : ID BITWISE_OR_EQ expression'''
    p[0] = SA.OperatorAssignBitwiseOrEQ(p[1], p[3])

def p_operator_assign_BITWISE_XOR_EQ(p):
    '''operator : ID BITWISE_XOR_EQ expression'''
    p[0] = SA.OperatorAssignBitwiseXorEQ(p[1], p[3])

def p_operator_assign_URSHIFT_EQ(p):
    '''operator : ID URSHIFT_EQ expression'''
    p[0] = SA.OperatorAssignUrshiftEQ(p[1], p[3])

def p_operator_assign_LSHIFT_EQ(p):
    '''operator : ID LSHIFT_EQ expression'''
    p[0] = SA.OperatorAssignLshiftEQ(p[1], p[3])

def p_operator_assign_RSHIFT_EQ(p):
    '''operator : ID RSHIFT_EQ expression'''
    p[0] = SA.OperatorAssignRshiftEQ(p[1], p[3])

def p_operator_comparator_LEQ(p):
    '''operator : expression LEQ expression'''
    p[0] = SA.OperatorComparatorLeq(p[1], p[3])

def p_operator_comparator_GEQ(p):
    '''operator : expression GEQ expression'''
    p[0] = SA.OperatorComparatorGeq(p[1], p[3])

def p_operator_comparator_LT(p):
    '''operator : expression LT expression'''
    p[0] = SA.OperatorComparatorLt(p[1], p[3])

def p_operator_comparator_GT(p):
    '''operator : expression GT expression'''
    p[0] = SA.OperatorComparatorGt(p[1], p[3])

def p_operator_comparator_NEQ(p):
    '''operator : expression NEQ expression'''
    p[0] = SA.OperatorComparatorNeq(p[1], p[3])

def p_operator_comparator_EQ(p):
    '''operator : expression EQ expression'''
    p[0] = SA.OperatorComparatorEq(p[1], p[3])

def p_operator_comparator_AND(p):
    '''operator : expression AND expression'''
    p[0] = SA.OperatorComparatorAnd(p[1], p[3])

def p_operator_comparator_OR(p):
    '''operator : expression OR expression'''
    p[0] = SA.OperatorComparatorOr(p[1], p[3])

def p_operator_comparator_BITWISE_AND(p):
    '''operator : expression BITWISE_AND expression'''
    p[0] = SA.OperatorComparatorBitwise_And(p[1], p[3])

def p_operator_comparator_BITWISE_OR(p):
    '''operator : expression BITWISE_OR expression'''
    p[0] = SA.OperatorComparatorBitwise_OR(p[1], p[3])

def p_operator_comparator_BITWISE_XOR(p):
    '''operator : expression BITWISE_XOR expression'''
    p[0] = SA.OperatorComparatorBitwise_XOR(p[1], p[3])

def p_operator_unaryoperatorprefix(p):
    '''operator : unaryoperatorprefix ID'''
    p[0] = SA.OperatorUnaryPrefix(p[1], p[2])

def p_operator_unaryoperatorsufix(p):
    '''operator : ID unaryoperatorsufix'''
    p[0] = SA.OperatorUnarySufix(p[1], p[2])

def p_operator_operatorbittobit(p):
    '''operator : expression operatorbittobit'''
    p[0] = SA.OperatorBitToBit(p[1], p[2])

### Operador de unario prefijo
def p_unaryoperatorprefx(p):
    '''
    unaryoperatorprefx : INCREMENT 
                        | DECREMENT 
                        | MINUS 
                        | PLUS
                        | NOT
    '''
    p[0] = SA.UnaryOperatorPrefixConcrete(p[1])

### Operador de unario sufijo
def p_unaryoperatorsufx(p):
    '''
    unaryoperatorsufx : INCREMENT 
                        | DECREMENT
    '''
    p[0] = SA.UnaryOperatorSufixConcrete(p[1])

### Operador de bit a bit
def p_operatorbittobit(p):
    '''
    operatorbittobit : URSHIFT
                        | LSHIFT
                        | RSHIFT
    
    '''
    p[0] = SA.UnaryOperatorBitToBitConcrete(p[1])

### Operador de brackets
def p_brackets_expression_default(p):
    ''' brackets_expression : LBRACKET RBRACKET'''
    p[0] = SA.BracketsExpressionSimple(None)

def p_brackets_expression_int(p):
    ''' brackets_expression : LBRACKET INT_NUMBER RBRACKET'''
    p[0] = SA.BracketsExpressionIntNumber(p[2])


def p_brackets_expression_id(p):
    ''' brackets_expression : LBRACKET ID RBRACKET'''
    p[0] = SA.BracketsExpressionId(p[2])

### Tipos primitivos
def p_type(p):
    ''' type : primitivetypes
               '''
    p[0] = SA.TypePrimitive(p[1])


def p_primitivetypes(p):
    '''primitivetypes : TYPE_INT
                        | TYPE_FLOAT
                        | TYPE_DOUBLE
                        | TYPE_BYTE
                        | TYPE_BOOLEAN
                        | TYPE_CHAR
                        | TYPE_STRING
                        | TYPE_LONG
                        | TYPE_VOID

    '''
    p[0] = SA.PrimitiveTypesConcrete(p[1])

### Llamada a la funcion
def p_call(p):
    ''' call : ID LPAREN params_call RPAREN'''
    p[0] = SA.CallParams(p[1], p[3])

def p_call_default(p):
    ''' call : ID LPAREN RPAREN'''
    p[0] = SA.CallDefault(p[1])

### Parametros de la llamada
def p_params_multi(p):
    ''' params_call : expression COMMA params_call'''
    p[0] = SA.ParamsCallMulti(p[1], p[3])

def p_params_unique(p):
    ''' params_call : expression'''
    p[0] = SA.ParamsLlamadaUnica(p[1])

### Chav_vacia
def p_chav_exp(p):
    '''chav_exp : LCHAV RCHAV'''
    p[0] = SA.ExpresionClaveVacia(None)

def p_chav_exp_expchav(p):
    '''chav_exp : LCHAV expression_chav
    '''
    p[0] = SA.ExpresionClaveExpresion(p[2])

### Expresion chav
def p_expression_chav_mult(p):
    '''expression_chav : expression COMMA expression_chav'''
    p[0] = SA.ExpresionClaveMult(p[1], p[3])

def p_expression_chav_expression_uni(p):
    '''expression_chav : expression RCHAV'''
    p[0] = SA.ExpresionClaveUni(p[1])

def p_expression_chav_expression_comma(p):
    '''expression_chav :  expression COMMA RCHAV'''
    p[0] = SA.ExpresionClaveComa(p[1])

def p_error(p):
    print("Error de sintaxis en la linea: ", p.lineno(0))
    print("Error de sintaxis en el token: ", p.value)
    print("Error de sintaxis en el tipo: ", p.type)
### Funcion main
def main():
    try:
        with open('Test/Test-1.java', 'r') as directorio:
            lexer = lex.lex()
            lexer.input(directorio.read())
            parser = yacc.yacc()
            for tok in lexer:
                print(tok)
            result = parser.parse(lexer=lexer)
            print(result)
    except Exception as e:
        print(e)
        print("Error al abrir el archivo")

main()