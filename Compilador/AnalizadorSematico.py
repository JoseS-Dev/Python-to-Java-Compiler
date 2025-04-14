from abc import ABC, abstractmethod
from sintaxis import *

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
        self.errors.append(f'Semantic error {'at line' + str(line) if line else ''}: {message}')

    
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
    
    


## Tabla de Simbolos 
class SymbolTable:
    pass