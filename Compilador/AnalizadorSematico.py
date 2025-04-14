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



## Tabla de Simbolos 
class SymbolTable:
    pass