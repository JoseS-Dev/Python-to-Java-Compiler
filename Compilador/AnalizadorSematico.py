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
        self.errors.append(f"Error at line {line}: {message}")


    
    # Visitas especificas para cada nodo del AST
    def VisitProgramConcrete(self, node):
        self.visit(node.cclass)
    
    def VisitCClassExtends(self, node):
        self.current_class = node.ID_NOMECLASS
        self.symbol_table.enter_scope()

        # Se verifica la herencia 
        if node.ID_NOMEEXTENDS not in self.symbol_table.classes:
            self.add_error(f'Class {node.ID_NOMEEXTENDS} not found', getattr(node, 'lineno', None))
        
        else:
            self.symbol_table.add_class(node.ID_NOMECLASS, node)
            self.visit(node.membros)
            self.symbol_table.exit_scope()
            self.current_class = None
        
    def VisitCClassDefault(self, node):
        
        self.current_class = node.ID_NOMECLASS
        self.symbol_table.enter_scope()
    
    # Add the class to the symbol table
        self.symbol_table.add_class(node.ID_NOMECLASS, node)
    
    # Verify class modifiers
        self.visit(node.visibility)
        self.visit(node.classmodifier)
    
    # Check for invalid modifier combinations
        if isinstance(node.classmodifier, ClassModifierConcrete) and hasattr(node.classmodifier, 'classmodifier'):
            if node.classmodifier.classmodifier == 'abstract' and node.classmodifier.classmodifier == 'final':
                self.add_error("Class cannot be both 'abstract' and 'final'", getattr(node, 'lineno', None))
    
        
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

    def VisitMembrosUni(self,node):
        self.visit(node.membro)
    
    def VisitMembrosMult(self,node):
        self.visit(node.membro)
        self.visit(node.membros)
    
    def VisitMembroAtribute(self, node):
        self.visit(node.atribute)

    def VisitMembroFunction(self, node):
        self.visit(node.function)
    
    def VisitAtributeDefault(self, node):
        # Se verifica el tipo de la variable
        self.visit(node.visibility)
    
        # Verificar modificadores
        self.visit(node.atributemodifier)
    
        # un atributo final debe ser inicializado
        if (isinstance(node.atributemodifier, AtributeModifierConcrete) and 
        node.atributemodifier.atributemodifier == 'final' and 
        not isinstance(self, AtributeDefaultInicializedType)):
            self.add_error("Final attribute must be initialized", getattr(node, 'lineno', None))
    
        # Verificar tipo
        if not self.is_valid_type(node.type):
            self.add_error(f"Invalid type '{node.type}' for attribute '{node.ID}'", getattr(node, 'lineno', None))
    
        # Registrar atributo
        if not self.symbol_table.add_variable(node.ID, node.type, node.atributemodifier, node.visibility):
            self.add_error(f"Duplicate attribute '{node.ID}' in class '{self.current_class}'", getattr(node, 'lineno', None))
        
    def VisitAtributeDefaultInicializedType(self,node):
        self.VisitAtributeDefault(node) # Se verifica la declaracion de la variable

        # Se verifica tipo de la expresion de inicialización
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(node.type, expr_type):
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {node.type} , got {expr_type}', getattr(node, 'lineno', None))

    def VisitAtributeModifierConcrete(self,node):
        pass # Ya esta verificada en la sintaxis

    def VisitFunctionDefault(self, node):
        # Verificar visibilidad
        self.visit(node.signature.visibility)
    
        # Verificar modificadores
        self.visit(node.signature.atributemodifier)
    
        # Verificar combinaciones inválidas
        if (isinstance(node.signature.atributemodifier, AtributeModifierConcrete) and
        node.signature.atributemodifier.atributemodifier == 'abstract' and
        node.signature.atributemodifier.atributemodifier == 'static'):
            self.add_error("Method cannot be both 'abstract' and 'static'", getattr(node, 'lineno', None))
    
    def VisitSignatureSimple(self, node):
        pass # Se verifica en FunctionDefault

    def VisitSignatureMult(self, node):
        pass # Se verifica en FunctionDefault
    
    def VisitSigparamsId(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} in method {self.current_method}', getattr(node, 'lineno', None))
        
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
            self.add_error(f'Condition of while must be boolean, got {cond_type}', getattr(node, 'lineno', None))
        
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
            self.add_error(f'Condition of do-while must be boolean, got {cond_type}', getattr(node, 'lineno', None))
    
    def VisitStmExpressionFor(self,node):
        self.visit(node.expression_for)
        if node.expression_mid is not None:
            cond_type = self.visit(node.expression_mid)
            if cond_type != 'boolean':
                self.add_error(f'Condition of for must be boolean, got {cond_type}', getattr(node, 'lineno', None))
        
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
            self.add_error(f'Condition of if must be boolean, got {cond_type}', getattr(node, 'lineno', None))
        
        # Analizamos el cuerpo del if
        self.visit(node.bodyorstm)
    
    def VisitStmExpressionIfElse(self, node):
        cond_type = self.visit(node.expression)
        if cond_type != 'boolean':
            self.add_error(f'Condition of if must be boolean, got {cond_type}', getattr(node, 'lineno', None))
        
        # Analizamos ambos cuerpos tanto del if y else
        self.visit(node.bodyorstm_1)
        self.visit(node.bodyorstm_2)
    
    def VisitStmExpressionElseIf(self,node):
        self.VisitStmExpressionIfElse(node) # Se verifica la condicion del if
    
    def VisitStmExpressionSemicolon(self, node):
        pass # No se requiere verificacion
    
    def VisitStmExpressionVariable(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}', getattr(node, 'lineno', None))
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, node.type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}', getattr(node, 'lineno', None))
    
    def VisitStmExpressionVariableType(self, node):
        self.VisitStmExpressionVariable(node)

        # Se verifica el tipo de la expresion de inicialización
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(node.type, expr_type):
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {node.type} , got {expr_type}', getattr(node, 'lineno', None))

    def VisitStmExpressionVariableTypeList(self, node):
        array_type = node.type + '[]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}', getattr(node, 'lineno', None))
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}', getattr(node, 'lineno', None))
    
    def VisitStmExpressionVariableTypeListPre(self, node):
        self.VisitStmExpressionVariableTypeList(node)
    
    def VisitStmExpressionVariableTypeListListPre(self, node):
        array_type = node.type + '[][]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}', getattr(node, 'lineno', None))
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}', getattr(node, 'lineno', None))
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.chav_exp)
        if expr_type != array_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {array_type} , got {expr_type}', getattr(node, 'lineno', None))
        
    def VisitStmExpressionVariableTypeListExpression(self, node):
        array_type = node.type + '[]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}', getattr(node, 'lineno', None))
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}', getattr(node, 'lineno', None))
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.expression)
        expected_type = f'new {node.type}[int]'
        
        if not isinstance(node.expression, ExpressionNewList) or expr_type != expected_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {expected_type} , got {expr_type}', getattr(node, 'lineno', None))
        
    def VisitStmExpressionVariableTypeListExpressionInicialized(self,node):
        array_type = node.type + '[]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}', getattr(node, 'lineno', None))
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}', getattr(node, 'lineno', None))
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.chav_exp)
        
        if expr_type != array_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {array_type} , got {expr_type}', getattr(node, 'lineno', None))
        
    def VisitStmExpressionVariableTypeListList(self, node):
        array_type = node.type + '[][]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}', getattr(node, 'lineno', None))
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}', getattr(node, 'lineno', None))

    def VisitStmExpressionVariableTypeListListInicialized(self, node):
        array_type = node.type + '[][]'
        if not self.is_valid_type(node.type):
            self.add_error(f'Invalid type {node.type} for variable {node.ID}', getattr(node, 'lineno', None))
        
        # Se registra la variable local
        if not self.symbol_table.add_variable(node.ID, array_type, node.atributemodifier):
            self.add_error(f'Duplicate variable {node.ID} in method {self.current_method}', getattr(node, 'lineno', None))
        
        # Se verifica la expresion de inicialización
        expr_type = self.visit(node.chav_exp)
        
        if expr_type != array_type:
            self.add_error(f'Type mismatch in initialization of {node.ID}. Expected {array_type} , got {expr_type}', getattr(node, 'lineno', None))

    def VisitStmExpressionReturn(self, node):
        if self.current_method is None:
            self.add_error('Return statement outside of method', getattr(node, 'lineno', None))
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
            self.add_error(f"Return type mismatch in method {self.current_method} Expected {return_type}, found {expr_type}", getattr(node, 'lineno', None))
    
    def VisitStmExpressionVoidReturn(self,node):
        if self.current_method is None:
            self.add_error("Return statement outside method", getattr(node, 'lineno', None))
            return
        method_info = self.symbol_table.lookup_method(self.current_method, self.current_class)
        
        if method_info is None:
            return
        
        if method_info['type'] != 'void':
            self.add_error(f"Non-void method '{self.current_method}' must return a value", getattr(node, 'lineno', None))

    def VisitBodyOrStmBody(self, node):
        self.visit(node.body)
    
    def VisitExpressionForAssignForType(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f"Invalid type '{node.type}' for variable '{node.ID}'", getattr(node, 'lineno', None))
        
        # Registrar variable local del for
        if not self.symbol_table.add_variable(node.ID, node.type):
            self.add_error(f"Duplicate variable '{node.ID}' in for loop", getattr(node, 'lineno', None))
        
        # Verificar expresión de inicialización
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(node.type, expr_type):
            self.add_error(f"Type mismatch in for loop initialization. Expected '{node.type}', found '{expr_type}'", getattr(node, 'lineno', None))
    
    def VisitExpressionForAssignFor(self, node):
        # Verificar que la variable existe
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}' in for loop", getattr(node, 'lineno', None))
            return
        
        # Verificar expresión de asignación
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(var_info['type'], expr_type):
            self.add_error(f"Type mismatch in for loop assignment. Expected '{var_info['type']}', found '{expr_type}'", getattr(node, 'lineno', None))
    
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
            self.add_error(f"Undeclared variable '{node.ID}'", getattr(node, 'lineno', None))
            return 'unknown'
        return var_info['type']

    def VisitExpressionNew(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f"Invalid type {node.type} in new expression", getattr(node, 'lineno', None))
            return 'unknown'

        # Verificar los parametros del constructor
        if node.params_call is not None:
            self.visit(node.params_call)
        
        return node.type
    
    def VisitExpressionNewList(self, node):
        if not self.is_valid_type(node.type):
            self.add_error(f"Invalid type '{node.type}' in array creation", getattr(node, 'lineno', None))
            return 'unknown'

        size_type = self.visit(node.expression)
        if size_type != 'int':
            self.add_error(f"Array size must be int, found '{size_type}'", getattr(node, 'lineno', None))
        
        return node.type + '[]'
    
    ### Falta los demas operadores

    def VisitOperatorArithmeticTimes(self,node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for multiplication: '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return self.get_numeric_result_type(left_type, right_type)

    def VisitOperatorArithmeticDivide(self,node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for division: {left_type} and {right_type}", getattr(node, 'lineno', None))
            return 'unknown'

        return self.get_numeric_result_type(left_type, right_type)

    def VisitOperatorArithmeticPlus(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for addition: {left_type} and {right_type}", getattr(node, 'lineno', None))
            return 'unknown'
        
        return self.get_numeric_result_type(left_type, right_type)


    def VisitOperatorArithmeticMinus(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Invalid operands for subtraction: {left_type} and {right_type}", getattr(node, 'lineno', None))
            return 'unknown'

        return self.get_numeric_result_type(left_type, right_type)
    
    def VisitOperatorComparatorLeq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '<='", getattr(node, 'lineno', None))
            return 'unknown'
        
        return 'boolean'


    def VisitOperatorComparatorGeq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '>='", getattr(node, 'lineno', None))
            return 'unknown'
        
        return 'boolean'
    

    def VisitOperatorComparatorLt(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '<'", getattr(node, 'lineno', None))
            return 'unknown'

        return 'boolean'


    def VisitOperatorComparatorGt(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '>'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return 'boolean'
    

    def VisitOperatorComparatorEq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_comparable_types(left_type) or not self.are_comparable_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '=='", getattr(node, 'lineno', None))
            return 'unknown'

        return 'boolean'


    def VisitOperatorComparatorNeq(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_numeric_types(left_type) or not self.are_numeric_types(right_type):
            self.add_error(f"Cannot compare types: {left_type} and {right_type} with '!='", getattr(node, 'lineno', None))
            return 'unknown'

        return 'boolean'


    def VisitOperatorLogicalAND(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if left_type != 'boolean' or right_type != 'boolean':
            self.add_error(f"Logical AND requires boolean operands, found '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'

        return 'boolean'


    def VisitOperatorLogicalOR(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if left_type != 'boolean' or right_type != 'boolean':
            self.add_error(f"Logical OR requires boolean operands, found '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return 'boolean'


    def VisitOperatorComparatorBitwise_AND(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Bitwise AND requires integral operands, found '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return self.get_integral_result_type(left_type, right_type)


    def VisitOperatorComparatorBitwise_OR(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Bitwise OR requires integral operands, found '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return self.get_integral_result_type(left_type, right_type)
    

    def VisitOperatorComparatorBitwise_XOR(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Bitwise XOR requires integral operands, found '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
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
    
    def VisitOperatorAssignBitwiseNotEQ(self, node):
        vars_info = self.symbol_table.lookup_variable(node.ID)
        if vars_info is None:
            self.add_error(f"Undeclared variable '{node.ID}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        if not self.are_integral_types(vars_info['type']):
            self.add_error(f"Invalid operand for bitwise NOT operator: '{vars_info['type']}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return vars_info['type']

    def visit_compound_assignment(self, node, op):
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}'", getattr(node, 'lineno', None))
            return 'unknown'

        expr_type = self.visit(node.expression)

        #Verificacion de tipos
        if op == '+' and var_info['type'] == 'String':
            if expr_type != 'String':
                self.add_error(f"Type mismatch in compound assignment. Expected 'String', found '{expr_type}'", getattr(node, 'lineno', None))
            return 'String'
        
        if not self.are_types_compatible(var_info['type'], expr_type, op):
            self.add_error(f"Type mismatch in compound assignment. Expected '{var_info['type']}', found '{expr_type}'", getattr(node, 'lineno', None))
        
        return var_info['type']


    def VisitOperatorUnaryPrefix(self, node):
        operator_type = self.visit(node.ID)
        if node.unaryoperatorprefx in ['++', '--', '+', '-']:
            if not self.are_numeric_types(operator_type):
                self.add_error(f"Invalid operand for unary operator '{node.unaryoperatorprefx}': '{operator_type}'", getattr(node, 'lineno', None))
                return 'unknown'
            return operator_type
        elif node.unaryoperatorprefx == '!':
            if operator_type != 'boolean':
                self.add_error(f"Invalid operand for unary operator '{node.unaryoperatorprefx}': '{operator_type}'", getattr(node, 'lineno', None))
                return 'unknown'
            return 'boolean'
        else:
            self.add_error(f"Unknown unary operator '{node.unaryoperatorprefx}'", getattr(node, 'lineno', None))
            return 'unknown'
        
    def VisitOperatorUnarySufix(self, node):
        operator_type = self.visit(node.ID)
        if node.unaryoperatorsufix in ['++', '--']:
            if not self.are_numeric_types(operator_type):
                self.add_error(f"Invalid operand for unary operator '{node.unaryoperatorsufix}': '{operator_type}'", getattr(node, 'lineno', None))
                return 'unknown'
            return operator_type
        else:
            self.add_error(f"Unknown unary operator '{node.unaryoperatorsufix}'", getattr(node, 'lineno', None))
            return 'unknown'
    

    def VisitUnaryOperatorPrefixConcrete(self, node):
        return node.unaryoperatorprefx # Retorna el operador para que el padre lo use

    def VisitUnaryOperatorSufixConcrete(self, node):
        return node.unaryoperatorsufix # Retorna el operador para que el padre lo use


    def VisitOperatorBitToBit(self, node):
        expr_type = self.visit(node.expression)

        if not self.are_integral_types(expr_type):
            self.add_error(f"Invalid operand for bitwise operator: '{expr_type}'", getattr(node, 'lineno', None))
            return 'unknown'

        return expr_type
    
    def VisitUnaryOperatorBitToBitConcrete(self, node):
        return node.unaryoperatorbit
            
    def VisitOperatorBitwiseLshift(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Invalid operands for left shift: '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return left_type
    
    def VisitOperatorBitwiseRshift(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Invalid operands for right shift: '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return left_type
    
    def VisitOperatorBitwiseURshift(self, node):
        left_type = self.visit(node.expression_1)
        right_type = self.visit(node.expression_2)

        if not self.are_integral_types(left_type) or not self.are_integral_types(right_type):
            self.add_error(f"Invalid operands for unsigned right shift: '{left_type}' and '{right_type}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        return left_type

    def VisitOperatorAssignEqual(self, node):
        var_info = self.symbol_table.lookup_variable(node.ID)
        if var_info is None:
            self.add_error(f"Undeclared variable '{node.ID}'", getattr(node, 'lineno', None))
            return 'unknown'
        
        expr_type = self.visit(node.expression)
        if not self.are_types_compatible(var_info['type'], expr_type):
            self.add_error(f"Type mismatch in assignment. Expected '{var_info['type']}', found '{expr_type}'", getattr(node, 'lineno', None))
        
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
            self.add_error(f"Undeclared variable '{node.ID}' in array size declaration", getattr(node, 'lineno', None))
            return "[unknown]"
        if var_info['type'] != 'int':
            self.add_error(f"Array size must be int, found '{var_info['type']}'", getattr(node, 'lineno', None))
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


    def VisitClassModifierConcrete(self, node):
        valid_class_modifiers = {'public', 'private', 'protected', 'static'}
        if node.classmodifier not in valid_class_modifiers:
            self.add_error(f"Invalid class modifier {node.classmodifier}", getattr(node, 'lineno', None))
            return False
        return True

    def VisitAttributeModifierConcrete(self, node):
        valid_attr_modifiers = {'public', 'private', 'protected', 'static', 'final'}
        if node.atributemodifier not in valid_attr_modifiers:
            self.add_error(f"Invalid attribute modifier {node.atributemodifier}", getattr(node, 'lineno', None))
            return False
        return True
    
    def VisitVisibilityConcrete(self, node):
        valid_visibilities = {'public', 'private', 'protected', None}
        if node.visibilidade not in valid_visibilities:
            self.add_error(f"Invalid visibility '{node.visibilidade}'", getattr(node, 'lineno', None))
            return False
        return True

    
    # Métodos auxiliares

    def is_valid_type(self, type_name):
        # Verificar arrays
        if type_name.endswith('[]'):
            base_type = type_name[:-2]
            return self.is_valid_type(base_type)
        
        primitive_types = {'int', 'float', 'double', 'byte', 'boolean', 'char', 'String', 'long', 'void', 'short'}
        return type_name in primitive_types or self.symbol_table.lookup_class(type_name) is not None
    
    
    def are_types_compatible(self, expected, actual, operator=None):
        primitive_types = {'int', 'float', 'double', 'byte', 'boolean', 'char', 'String', 'long', 'void', 'short'}
        if expected == actual:
            return True
        
        # Compatibilidad numérica
        numeric_types = {'byte', 'short', 'int', 'long', 'float', 'double'}
        if expected in numeric_types and actual in numeric_types:
            if operator in ['+', '-', '*', '/', '%']:
                return True
            if operator in ['==', '!=']:
                return True
            
        # Strings solo con +
        if expected == 'String' and actual == 'String' and operator == '+':
            return True
        
        # null puede asignarse a cualquier objeto
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
        # Buscar en ámbitos anidados
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
    
        # Buscar en variables de clase
        if self.current_class:
            class_node = self.symbol_table.lookup_class(self.current_class)
            if class_node:
                for member in class_node.membros:
                    if isinstance(member, MembroAtribute) and member.atribute.ID == name:
                        return {
                            'type': member.atribute.type,
                            'modifier': member.atribute.atributemodifier,
                            'visibility': member.atribute.visibility
                        }
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
    file = open("Test/Test-2.java", "r")
    lexer = lex.lex()
    lexer.input(file.read())
    parser = yacc.yacc()
    ast = parser.parse()

    semantico = SemanticAnalyzer()
    semantico.visit(ast)
    print('\n\n# Errores encontrados:')

    for error in semantico.errors:
        print(error)
    if not semantico.errors:
        print("No hay errores en el analizador sematico.")

Main()