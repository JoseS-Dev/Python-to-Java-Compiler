from abc import ABC, abstractmethod
from sintaxis import *
from AnalizadorLexico import *
from AnalizadorSintactico import *

## Clase de visitante para el analizador semántico
class SemanticVisitor(ABC):
    @abstractmethod
    def visit(self, node):
        pass

## Clase para el analizador semántico
class SemanticAnalyzer(SemanticVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_class = None
        self.current_method = None
        self.errors = []
        self.loop_depth = 0
    
    def visit(self, node):
        if node is not None:
            return node.accept(self)
        return None

    def add_error(self, message, line):
        self.errors.append(f'Semantic error {str(line)} : {message}')

    
    # Visitas especificas para cada nodo del AST
    def VisitProgramConcrete(self, node):
        self.visit(node.cclass)
    
    def VisitCClassExtends(self, node):
        self.current_class = node.ID_NOMECLASS
        self.symbol_table.enter_scope()

        # Se verifica la herencia 
        if node.ID_NOMEEXTENDS not in self.symbol_table.classes:
            self.add_error(f'Class {node.ID_NOMEEXTENDS} not found')
        
        else:
            self.symbol_table.add_class(node.ID_NOMECLASS, node)
            self.visit(node.membros)
            self.symbol_table.exit_scope()
            self.current_class = None
        
    def VisitCClassDefault(self, node):
        self.current_class = node.ID_NOMECLASS
        self.symbol_table.enter_scope()
        self.symbol_table.add_class(node.ID_NOMECLASS, node)
        self.visit(node.membros)
        self.symbol_table.exit_scope()
        self.current_class = None
    
    def VisitCClassImplements(self, node):
        self.current_class = node.ID_NOMECLASS
        self.symbol_table.enter_scope()
        self.symbol_table.add_class(node.ID_NOMECLASS, node)
        self.visit(node.membros)
        self.symbol_table.exit_scope()
        self.current_class = None
    
    def VisitVisibilityConcrete(self,node):
        pass # Ya esta verificada en la sintaxis

    def VisitClassModifierConcrete(self, node):
        pass # Ya esta verificada en la sintaxis

    def VisitMembroUni(self,node):
        self.visit(node.membro)
    
    def VisitMembroMult(self,node):
        self.visit(node.membro)
        self.visit(node.membros)
    
    def VisitMembroAtribute(self, node):
        self.visit(node.atribute)

    def VisitMembroFunction(self, node):
        self.visit(node.function)
    
    def VisitAtributeDefault(self, node):
        # Se verifica el tipo de la variable
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for attribute {node.ID}')
        
        if not self.symbol_table.add_variable(node.ID, node.type, node.atributemodifier, node.visibility):
            self.add_error(f'Duplicate variable {node.ID} in class {self.current_class}')
        
    def VisitAtributeDefaultInicializedType(self,node):
        self.VisitAtributeDefault(node) # Se verifica la declaracion de la variable

        # Se verifica tipo de la expresion de inicialización
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(node.type, expr_type):
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {node.type} , got {expr_type}')

    def VisitAtributeModifierConcrete(self,node):
        pass # Ya esta verificada en la sintaxis

    def VisitFunctionDefault(self, node):
        self.current_method = node.signature.ID if hasattr(node.signature, 'ID') else None
        self.symbol_table.enter_scope()

        #Registramos los paraemetros de la funcion
        if hasattr(node.signature, 'sigparams'):
            self.visit(node.signature.sigparams)
        
        # Se verifica el tipo de retorno de la funcion
        if not self.is_valid_type(node.signature.type):
            self.add_error(f'Invalid return type {node.signature.type} for function {node.signature.ID}')
        
        # Analizar el cuerpo de la funcion
        self.visit(node.body)

        # Verifica si el tipo de retorno es para metodos no void
        if(hasattr(node.signature, 'type') and node.signature.type != 'void' and not self.has_return_statement(node.body)):
            self.add_error(f'Method {node.signature.ID} must return a value')
        
        self.symbol_table.exit_scope()
        self.current_method = None
    
    def VisitSignatureSimple(self, node):
        pass # Se verifica en FunctionDefault

    def VisitSignatureMult(self, node):
        pass # Se verifica en FunctionDefault
    
    def VisitSigparamsId(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} in method {self.current_method}')
        
        self.symbol_table.add_variable(node.ID, node.type)
    
    def VisitSigparamsSigparams(self, node):
        self.visit(node.sigparams)
        self.visit(node.sigparam)
    
    def VisitBodyStms(self, node):
        self.visit(node.stms)
    
    def VisitStmsUni(self, node):
        self.visit(node.stm)
    
    def VisitStmsMult(self, node):
        self.visit(node.stm)
        self.visit(node.stms)
    
    def VisitStmExpression(self, node):
        self.visit(node.expression)
    
    def VisitStmExpressionWhile(self,node):
        cond_type = self.visit(node.expression)
        if cond_type != 'boolean':
            self.add_error(f'Condition of while must be boolean, got {cond_type}')
        
        #Analizar el cuerpo del while
        self.loop_depth += 1
        self.visit(node.bodyorstm)
        self.loop_depth -= 1
    
    def VisitStmExpressionDoWhile(self,node):
        self.loop_depth += 1
        self.visit(node.bodyorstm)
        self.loop_depth -= 1

        cond_type = self.visit(node.expression)
        if cond_type != 'boolean':
            self.add_error(f'Condition of do-while must be boolean, got {cond_type}')
    
    def VisitStmExpressionFor(self,node):
        self.visit(node.expression_for)
        if node.expression_mid is not None:
            cond_type = self.visit(node.expression_mid)
            if cond_type != 'boolean':
                self.add_error(f'Condition of for must be boolean, got {cond_type}')
        
        # Analizamos el incremento del for
        if node.expression_final is not None:
            self.visit(node.expression_final)
        
        # Analizamos el cuerpo del for
        self.loop_depth += 1
        self.visit(node.bodyorstm)
        self.loop_depth -= 1
    
    def VisitStmExpressionIf(self, node):
        cond_type = self.visit(node.expression)
        if cond_type != 'boolean':
            self.add_error(f'Condition of if must be boolean, got {cond_type}')
        
        # Analizamos el cuerpo del if
        self.visit(node.bodyorstm)
    
    def VisitStmExpressionIfElse(self, node):
        cond_type = self.visit(node.expression)
        if cond_type != 'boolean':
            self.add_error(f'Condition of if must be boolean, got {cond_type}')
        
        # Analizamos ambos cuerpos tanto del if y else
        self.visit(node.bodyorstm_1)
        self.visit(node.bodyorstm_2)
    
    def VisitStmExpressionElseIf(self,node):
        self.VisitStmExpressionIfElse(node) # Se verifica la condicion del if
    
    def VisitStmExpressionSemicolon(self, node):
        pass # No se requiere verificacion
    
    def VisitStmExpressionVariable(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}')
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, node.type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}')
    
    def VisitStmExpressionVariableType(self, node):
        self.VisitStmExpressionVariable(node)

        # Se verifica el tipo de la expresion de inicialización
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(node.type, expr_type):
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {node.type} , got {expr_type}')

    def VisitStmExpressionVariableTypeList(self, node):
        array_type = node.type + '[]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}')
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}')
    
    def VisitStmExpressionVariableTypeListPre(self, node):
        self.VisitStmExpressionVariableTypeList(node)
    
    def VisitStmExpressionVariableTypeListListPre(self, node):
        array_type = node.type + '[][]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}')
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}')
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.chav_exp)
        if expr_type != array_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {array_type} , got {expr_type}')
        
    def VisitStmExpressionVariableTypeListExpression(self, node):
        array_type = node.type + '[]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}')
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}')
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.expression)
        expected_type = f'new {node.type}[int]'
        
        if not isinstance(node.expression, ExpressionNewList) or expr_type != expected_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {expected_type} , got {expr_type}')
        
    def VisitStmExpressionVariableTypeListExpressionInicialized(self,node):
        array_type = node.type + '[]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}')
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}')
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.chav_exp)
        
        if expr_type != array_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {array_type} , got {expr_type}')
        
    def VisitStmExpressionVariableTypeListList(self, node):
        array_type = node.type + '[][]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}')
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}')

    def VisitStmExpressionVariableTypeListListInicialized(self, node):
        array_type = node.type + '[][]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}')
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}')
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.chav_exp)
        
        if expr_type != array_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {array_type} , got {expr_type}')

    def VisitStmExpressionReturn(self, node):
        if self.current_method is None:
            self.add_error('Return statement outside of method')
            return
        
        # Obtenemos el tipo de retorno
        method_info = self.symbol_table.lookup_method(self.current_method, self.current_class)
        if method_info is None:
            return
        
        return_type = method_info['type']
        expr_type = self.visit(node.expression) if node.expression is not None else 'void'

        if return_type == 'void':
            self.add_error(f"Void method {self.current_method} cannot return a value")
        elif not self.are_types_compatible(return_type, expr_type):
            self.add_error(f"Return type mismatch in method {self.current_method} Expected {return_type}, found {expr_type}")
    
    def VisitStmExpressionVoidReturn(self,node):
        if self.current_method is None:
            self.add_error("Return statement outside method")
            return
        method_info = self.symbol_table.lookup_method(self.current_method, self.current_class)
        
        if method_info is None:
            return
        
        if method_info['type'] != 'void':
            self.add_error(f"Non-void method '{self.current_method}' must return a value")

    def VisitBodyOrStmBody(self, node):
        self.visit(node.body)
    
    def VisitExpressionForAssignForType(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f"Invalid type '{node.type}' for variable '{node.ID}'")
        
        # Registrar variable local del for
        if not self.symbol_table.add_variable(node.ID, node.type):
            self.add_error(f"Duplicate variable '{node.ID}' in for loop")
        
        # Verificar expresión de inicialización
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(node.type, expr_type):
            self.add_error(f"Type mismatch in for loop initialization. Expected '{node.type}', found '{expr_type}'")
    
    def VisitExpressionForAssignFor(self, node):
        # Verificar que la variable existe
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}' in for loop")
            return
        
        # Verificar expresión de asignación
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(var_info['type'], expr_type):
            self.add_error(f"Type mismatch in for loop assignment. Expected '{var_info['type']}', found '{expr_type}'")
    
    def VisitExpressionperator(self, node):
        return self.visit(node.operator)

    def VisitExpressionCall(self, node):
        return self.visit(node.call)

    def VisitExpressionFloatNumber(self, node):
        return 'float'
    
    def VisitExpressionDoubleNumber(self, node):
        return 'double'
    
    def VisitExpressionIntNumber(self, node):
        return 'int'
    
    def VisitExpressionString(self, node):
        return 'String'

    def VisitExpressionId(self,node):
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}'")
            return 'unknown'
        return var_info['type']

    def VisitExpressionNew(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f"Invalid type {node.type} in new expression")
            return 'unknown'

        # Verificar los parametros del constructor
        if node.params_call is not None:
            self.visit(node.params_call)
        
        return node.type
    
    def VisitExpressionNewList(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f"Invalid type '{node.type}' in array creation")
            return 'unknown'

        size_type = self.visit(node.expression)
        if size_type != 'int':
            self.add_error(f"Array size must be int, found '{size_type}'")
        
        return node.type + '[]'
    
    ### Falta los demas operadores

    def VisitOperatorArithmeticTimes(self,node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for multiplication: '{left_type}' and '{right_type}'")
            return 'unknown'
        
        return self.get_numeric_result_type(left_type, right_type)

    def VisitOperatorArithmeticDivide(self,node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for division: {left_type} and {right_type}")
            return 'unknown'

        return self.get_numeric_result_type(left_type, right_type)

    def VisitOperatorArithmeticPlus(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for addition: {left_type} and {right_type}")
            return 'unknown'
        
        return self.get_numeric_result_type(left_type, right_type)


    def VisitOperatorArithmeticMinus(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for subtraction: {left_type} and {right_type}")
            return 'unknown'

        return self.get_numeric_result_type(left_type, right_type)
    
    def VisitOperatorComparatorLeq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '<='")
            return 'unknown'
        
        return 'boolean'


    def VisitOperatorComparatorGeq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '>='")
            return 'unknown'
        
        return 'boolean'
    

    def VisitOperatorComparatorLt(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '<'")
            return 'unknown'

        return 'boolean'


    def VisitOperatorComparatorGt(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '>'")
            return 'unknown'
        
        return 'boolean'
    

    def VisitOperatorComparatorEq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '=='")
            return 'unknown'

        return 'boolean'


    def VisitOperatorComparatorNeq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '!='")
            return 'unknown'

        return 'boolean'


    def VisitOperatorLogicalAND(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if left_type != 'boolean' or right_type != 'boolean':
            self.add_error(f"Logical AND requires boolean operands, found '{left_type}' and '{right_type}'")
            return 'unknown'

        return 'boolean'


    def VisitOperatorLogicalOR(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if left_type != 'boolean' or right_type != 'boolean':
            self.add_error(f"Logical OR requires boolean operands, found '{left_type}' and '{right_type}'")
            return 'unknown'
        
        return 'boolean'


    def VisitOperatorComparatorBitwise_AND(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Bitwise AND requires integral operands, found '{left_type}' and '{right_type}'")
            return 'unknown'
        
        return self.get_integral_result_type(left_type, right_type)


    def VisitOperatorComparatorBitwise_OR(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Bitwise OR requires integral operands, found '{left_type}' and '{right_type}'")
            return 'unknown'
        
        return self.get_integral_result_type(left_type, right_type)
    

    def VisitOperatorComparatorBitwise_XOR(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Bitwise XOR requires integral operands, found '{left_type}' and '{right_type}'")
            return 'unknown'
        
        return self.get_integral_result_type(left_type, right_type)


    def VisitOperatorAssignMinusEQ(self, node):
        return self.visit_compound_assignment(node, '-')

    def VisitOperatorAssignTimesEQ(self, node):
        return self.visit_compound_assignment(node, '*')

    def VisitOperatorAssignPlusEQ(self, node):
        return self.visit_compound_assignment(node, '+')

    def VisitOperatorAssignDivideEQ(self, node):
        return self.visit_compound_assignment(node, '/')

    def VisitOperatorAssignModuleEQ(self, node):
        return self.visit_compound_assignment(node, '%')

    def VisitOperatorAssignBitwiseAndEQ(self, node):
        return self.visit_compound_assignment(node, '&')

    def VisitOperatorAssignBitwiseOrEQ(self, node):
        return self.visit_compound_assignment(node, '|')

    def VisitOperatorAssignBitwiseXorEQ(self, node):
        return self.visit_compound_assignment(node, '^')

    def VisitOperatorAssignUrshiftEQ(self, node):
        return self.visit_compound_assignment(node, '>>>')

    def VisitOperatorAssignLshiftEQ(self, node):
        return self.visit_compound_assignment(node, '<<')

    def VisitOperatorAssignRshiftEQ(self, node):
        return self.visit_compound_assignment(node, '>>')

    def visit_compound_assignment(self, node, op):
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}'")
            return 'unknown'

        expr_type = self.visit(node.expression)

        #Verificacion de tipos
        if op == '+' and var_info['type'] == 'String':
            if expr_type != 'String':
                self.add_error(f"Type mismatch in compound assignment. Expected 'String', found '{expr_type}'")
            return 'String'
        
        if not self.are_types_compatible(var_info['type'], expr_type, op):
            self.add_error(f"Type mismatch in compound assignment. Expected '{var_info['type']}', found '{expr_type}'")
        
        return var_info['type']


    def VisitOperatorUnaryPrefix(self, node):
        operator_type = self.visit(node.ID)
        if node.unaryoperatorprefx in ['++', '--', '+', '-']:
            if not self.are_numeric_types(operator_type):
                self.add_error(f"Invalid operand for unary operator '{node.unaryoperatorprefx}': '{operator_type}'")
                return 'unknown'
            return operator_type
        elif node.unaryoperatorprefx == '!':
            if operator_type != 'boolean':
                self.add_error(f"Invalid operand for unary operator '{node.unaryoperatorprefx}': '{operator_type}'")
                return 'unknown'
            return 'boolean'
        else:
            self.add_error(f"Unknown unary operator '{node.unaryoperatorprefx}'")
            return 'unknown'
        
    def VisitOperatorUnarySufix(self, node):
        operator_type = self.visit(node.ID)
        if node.unaryoperatorsufix in ['++', '--']:
            if not self.are_numeric_types(operator_type):
                self.add_error(f"Invalid operand for unary operator '{node.unaryoperatorsufix}': '{operator_type}'")
                return 'unknown'
            return operator_type
        else:
            self.add_error(f"Unknown unary operator '{node.unaryoperatorsufix}'")
            return 'unknown'
    

    def VisitUnaryOperatorPrefixConcrete(self, node):
        return node.unaryoperatorprefx # Retorna el operador para que el padre lo use

    def VisitUnaryOperatorSufixConcrete(self, node):
        return node.unaryoperatorsufix # Retorna el operador para que el padre lo use


    def VisitOperatorBitToBit(self, node):
        expr_type = self.visit(node.expression)

        if not self.are_integral_types(expr_type):
            self.add_error(f"Invalid operand for bitwise operator: '{expr_type}'")
            return 'unknown'

        return expr_type
    
    def VisitUnaryOperatorBitToBitConcrete(self, node):
        return node.unaryoperatorbit
            


    def VisitOperatorAssignEqual(self, node):
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}'")
            return 'unknown'
        
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(var_info['type'], expr_type):
            self.add_error(f"Type mismatch in assignment. Expected '{var_info['type']}', found '{expr_type}'")
        
        return var_info['type']
    
    def VisitBracketsExpressionSimple(self, node):
    # Para el caso de [] en declaraciones de arrays
        return "[]"  # Indica que es un tipo array

    def VisitBracketsExpressionIntNumber(self, node):
        # Para el caso de [int_number] en declaraciones de arrays
        return f"[{node.int_number}]"

    def VisitBracketsExpressionId(self, node):
        # Para el caso de [ID] en declaraciones de arrays
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}' in array size declaration")
            return "[unknown]"
        if var_info['type'] != 'int':
            self.add_error(f"Array size must be int, found '{var_info['type']}'")
            return f"[{node.ID}]"

    def VisitChavExpEmpty(self, node):
        # Para el caso de {} - array vacío
        return "[]"  # Tipo array sin especificar elementos

    def VisitChavExpExpressionChav(self, node):
        # Para el caso de {expresiones} - inicialización de array
        return self.visit(node.expression_chav)

    def VisitExpressionChavMult(self, node):
        # Para el caso de {expr, expr, ...}
        first_type = self.visit(node.expression)
        self.visit(node.expression_chav)  # Verificar el resto de expresiones
        return f"{first_type}[]"  # Retorna el tipo del array

    def VisitExpressionChavUni(self, node):
        # Para el caso de {expr}
        expr_type = self.visit(node.expression)
        return f"{expr_type}[]"

    def VisitExpressionChavComma(self, node):
        # Para el caso de {expr,}
        expr_type = self.visit(node.expression)
        return f"{expr_type}[]"
    
    # Métodos auxiliares
    
    def is_valid_type(self, type_name):
        primitive_types = {'int', 'float', 'double', 'byte', 'boolean', 'char', 'String', 'long', 'void'}
        return type_name in primitive_types or self.symbol_table.lookup_class(type_name) is not None
    
    def are_types_compatible(self, expected, actual):
        if expected == actual:
            return True
        primitive_types = {'int', 'float', 'double', 'byte', 'boolean', 'char', 'String', 'long', 'void'}
        # Reglas de compatibilidad de tipos
        numeric_types = {'byte', 'short', 'int', 'long', 'float', 'double'}
        if expected in numeric_types and actual in numeric_types:
            return True
        
        # Compatibilidad con null para objetos
        if actual == 'null' and expected not in primitive_types:
            return True
        
        return False
    
    def are_numeric_types(self, type_name):
        return type_name in {'byte', 'short', 'int', 'long', 'float', 'double'}
    
    def get_numeric_result_type(self, type1, type2):
        # Reglas para determinar el tipo resultante de operaciones aritméticas
        numeric_priority = ['double', 'float', 'long', 'int', 'short', 'byte']
        for t in numeric_priority:
            if t == type1 or t == type2:
                return t
        return 'int'  # Default

    def are_integral_types(self, type_name):
        return type_name in {'int', 'short', 'byte', 'long'}
    
    def are_comparable_types(self, type_name):
        # Tipos que se pueden comparar entre sí
        comparable_types = {'int', 'float', 'double', 'boolean', 'char', 'String'}
        return type_name in comparable_types

    def get_integral_result_type(self, type1, type2):
        # Reglas para determinar el tipo resultante de operaciones bitwise
        integral_priority = ['long', 'int', 'short', 'byte']
        for t in integral_priority:
            if t == type1 or t == type2:
                return t
        return 'int'
    
    def has_return_statement(self, body):
        # Recorrer el cuerpo del método buscando return statements
        # Implementación simplificada - en realidad necesitaría un análisis más completo
        if isinstance(body, BodyStms):
            if isinstance(body.stms, StmsMulti):
                last_stmt = body.stms
                while isinstance(last_stmt, StmsMulti):
                    last_stmt = last_stmt.stms
                if isinstance(last_stmt.stm, (StmExpressionReturn, StmExpressionVoidReturn)):
                    return True
        return False



## Tabla de Simbolos 

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Pila de ámbitos
        self.classes = {}   # Diccionario de clases
        
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        self.scopes.pop()
    
    def add_variable(self, name, var_type, modifier=None, visibility=None):
        if name in self.scopes[-1]:
            return False
        self.scopes[-1][name] = {
            'type': var_type,
            'modifier': modifier,
            'visibility': visibility
        }
        return True
    
    def add_class(self, name, class_node):
        if name in self.classes:
            return False
        self.classes[name] = class_node
        return True
    
    def lookup_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def lookup_class(self, name):
        return self.classes.get(name, None)
    
    def lookup_method(self, method_name, class_name):
        class_node = self.lookup_class(class_name)
        if class_node is None:
            return None
        
        # Buscar el método en la clase
        for member in class_node.membros:
            if isinstance(member, MembroFunction) and member.function.signature.ID == method_name:
                return {
                    'type': member.function.signature.type,
                    'params': member.function.signature.sigparams if hasattr(member.function.signature, 'sigparams') else []
                }
        
        return None

def Main():
    file = open("Test/Test-3.java", "r")
    lexer = lex.lex()
    lexer.input(file.read())
    parser = yacc.yacc()
    ast = parser.parse()

    semantico = SemanticAnalyzer()
    semantico.visit(ast)

    if semantico.errors:
        print("\n".join(semantico.errors))
    else:
        print("No hay errores en el analisis semantico")

Main()