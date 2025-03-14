from abc import abstractmethod, ABCMeta 

#PROGRAM
class Program(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
        pass
        
class ProgramConcrete(Program):
    def __init__(self, cclass):
        self.cclass = cclass
    def accept(self, visitor):
        return visitor.VisitProgramConcrete(self)
        
        
#CLASS
class CClass(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
        pass
    
class CClassExtends(CClass):
    def __init__(self,visibility, classmodifier,  ID_NOMECLASS, ID_NOMEEXTENDS, membros):
        self.visibility = visibility
        self.classmodifier = classmodifier
        self.ID_NOMECLASS = ID_NOMECLASS
        self.ID_NOMEEXTENDS = ID_NOMEEXTENDS
        self.membros = membros
    def accept(self, visitor):
        return visitor.VisitCClassExtends(self)
        
class CClassDefault(CClass):
    def __init__(self, visibility, classmodifier, ID_NOMECLASS,  membros):
        self.visibility = visibility     
        self.classmodifier = classmodifier
        self.ID_NOMECLASS = ID_NOMECLASS
        self.membros = membros
    def accept(self, visitor):
        return visitor.VisitCClassDefault(self)
    
class CClassImplements(CClass):
    def __init__(self, visibility, classmodifier, ID_NOMECLASS, membros):
        self.visibility = visibility
        self.classmodifier = classmodifier
        self.ID_NOMECLASS = ID_NOMECLASS
        self.membros = membros
    def accept(self, visitor):
        return visitor.VisitCClassImplements(self)


#VISIBILIDADE
class Visibility(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
        pass
    
    
class VisibilityConcrete(Visibility):
    def __init__(self,visibilidade):
        self.visibilidade = visibilidade
    def accept(self, visitor):
        return visitor.VisitVisibilityConcrete(self)

    
#CLASSMODIFIER
class ClassModifier(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
        pass
  
class ClassModifierConcrete(ClassModifier):
    def __init__(self, classmodifier):
        self.classmodifier = classmodifier
    def accept(self, visitor):
        return visitor.VisitClassModifierConcrete(self)
    
    
#MEMBROS
class Membros(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
        pass
    
class MembrosUni(Membros):
    def __init__(self, membro):
        self.membro = membro
    def accept(self, visitor):
        return visitor.VisitMembrosUni(self)
    
class MembrosMult(Membros):
    def __init__(self, membro, membros):
        self.membro = membro
        self.membros = membros
    def accept(self, visitor):
        return visitor.VisitMembrosMult(self)
    
    
#MEMBRO
class Membro(metaclass=ABCMeta):
    @abstractmethod
    def accept(self,visitor):
        pass
    
class MembroAtribute(Membro):
    def __init__(self,atribute):
        self.atribute = atribute
    def accept(self, visitor):
        return visitor.VisitMembroAtribute(self)

class MembroFunction(Membro):
    def __init__(self, function):
        self.function = function
    def accept(self, visitor):
        return visitor.VisitMembroFunction(self)


#ATRIBUTOS
class Atribute(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class AtributeDefault(Atribute):
    def __init__(self, visibility, atributemodifier, type, ID):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitAtributeDefault(self)
    
class AtributeDefaultInicializedType(Atribute):
    def __init__(self, visibility, atributemodifier, type, ID, expression):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitAtributeDefaultInicializedType(self)
    
    
#ATRIBUTEMODIFIER
class AtributeModifier(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class AtributeModifierConcrete(AtributeModifier):
    def __init__(self,atributemodifier):
        self.atributemodifier = atributemodifier
    def accept(self, visitor):
        return visitor.VisitAtributeModifierConcrete(self)


#FUNÇÕES
class Function(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class FunctionDefault(Function):
    def __init__(self, signature, body):
        self.signature = signature
        self.body = body
    def accept(self, visitor):
        return visitor.VisitFunctionDefault(self)
    

#SIGNATURE
class Signature(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class SignatureSimple(Signature):
    def __init__(self, visibility, atributemodifier, type, ID, sigparams):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.sigparams = sigparams
    def accept(self, visitor):
        visitor.VisitSignatureSimple(self)
        
class SignatureMult(Signature):
    def __init__(self, visibility, atributemodifier, type, brackets_expression, ID, sigparams):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.brackets_expression = brackets_expression
        self.ID = ID
        self.sigparams = sigparams
    def accept(self, visitor):
        visitor.VisitSignatureMult(self)
    

#SIGPARAMS
class Sigparams(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class SigparamsId(Sigparams):
    def __init__(self, type, ID):
        self.type = type
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitSigparamsId(self)
    
class SigparamsSigparams(Sigparams):
    def __init__(self, type, ID, sigparams):
        self.type = type
        self.ID = ID
        self.sigparams = sigparams
    def accept(self, visitor):
        return visitor.VisitSigparamsSigparams(self)
           
               
#BODY
class Body(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class BodyStms(Body):
    def __init__(self, stms):
        self.stms = stms
    def accept(self, visitor):
        return visitor.VisitBodyStms(self)
    
#STMS
class Stms(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class StmsUni(Stms):
    def __init__(self, stm):
        self.stm = stm
    def accept(self, visitor):
        return visitor.VisitStmsUni(self)
    
class StmsMulti(Stms):
    def __init__(self, stm, stms):
        self.stm = stm
        self.stms = stms
    def accept(self, visitor):
        return visitor.VisitStmsMulti(self)


#STM
class Stm(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class StmExpression(Stm):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitStmExpression(self)
    
class StmExpressionWhile(Stm):
    def __init__(self, expression, bodyorstm):
        self.expression = expression
        self.bodyorstm = bodyorstm
    def accept(self, visitor):
        return visitor.VisitStmExpressionWhile(self)
    
class StmExpressionDoWhile(Stm):
    def __init__(self, bodyorstm, expression):
        self.bodyorstm = bodyorstm
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitStmExpressionDoWhile(self)
    
class StmExpressionFor(Stm):
    def __init__(self, expression_for, expression_mid, expression_final, bodyorstm):
        self.expression_for = expression_for
        self.expression_mid = expression_mid
        self.expression_final = expression_final
        self.bodyorstm = bodyorstm
    def accept(self, visitor):
        return visitor.VisitStmExpressionFor(self)
        
class StmExpressionIf(Stm):
    def __init__(self, expression, bodyorstm):
        self.expression = expression
        self.bodyorstm = bodyorstm
    def accept(self, visitor):
        return visitor.VisitStmExpressionIf(self)
        
class StmExpressionIfElse(Stm):
    def __init__(self, expression, bodyorstm_1,bodyorstm_2):
        self.expression = expression
        self.bodyorstm_1 = bodyorstm_1
        self.bodyorstm_2 = bodyorstm_2
    def accept(self, visitor):
        return visitor.VisitStmExpressionIfElse(self)
        
class StmExpressionElseIf(Stm):
    def __init__(self, expression, bodyorstm_1,bodyorstm_2):
        self.expression = expression
        self.bodyorstm_1 = bodyorstm_1
        self.bodyorstm_2 = bodyorstm_2
    def accept(self, visitor):
        return visitor.VisitStmExpressionElseIf(self)
    
class StmExpressionSemicolon(Stm):
    def __init__(self):
        pass
    def accept(self, visitor):
        return visitor.VisitStmExpressionSemicolon(self)     
        
class StmExpressionVariable(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariable(self)        
                
class StmExpressionVariableType(Stm):
    def __init__(self, atributemodifier, type, ID, expression):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableType(self)
    
class StmExpressionVariableTypeList(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableTypeList(self)
    
class StmExpressionVariableTypeListPre(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListPre(self)
    
class StmExpressionVariableTypeListListPre(Stm):
    def __init__(self, atributemodifier, type, ID, chav_exp):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.chav_exp = chav_exp
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListListPre(self)
    
class StmExpressionVariableTypeListExpression(Stm):
    def __init__(self, atributemodifier, type, ID, expression):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListExpression(self)
    
class StmExpressionVariableTypeListExpressionInicialized(Stm):
    def __init__(self, atributemodifier, type, ID, chav_exp):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.chav_exp = chav_exp
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListExpressionInicialized(self)
    
class StmExpressionVariableTypeListList(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListList(self)
    
class StmExpressionVariableTypeListListInicialized(Stm):
    def __init__(self, atributemodifier, type, ID, chav_exp):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.chav_exp = chav_exp
    def accept(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListListInicialized(self)

class StmExpressionReturn(Stm):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitStmExpressionReturn(self)
    
class StmExpressionVoidReturn(Stm):
    def __init__(self, void_return):
        self.void_return = void_return
    def accept(self, visitor):
        return visitor.VisitStmExpressionVoidReturn(self)

#BODYORSTM
class BodyOrStm(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class BodyOrStmBody(BodyOrStm):
    def __init__(self, body):
        self.body = body
    def accept(self, visitor):
        return visitor.VisitBodyOrStmBody(self)
        
#EXPRESSIONFOR
class ExpressionFor(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class ExpressionForAssignForType(ExpressionFor):
    def __init__(self, type, ID, expression):
        self.type = type 
        self.ID = ID 
        self.expression = expression 
    def accept(self, visitor):
        return visitor.VisitExpressionForAssignForType(self)
    
class ExpressionForAssignFor(ExpressionFor):
    def __init__(self, ID, expression):
        self.ID = ID 
        self.expression = expression 
    def accept(self, visitor):
        return visitor.VisitExpressionForAssignFor(self)
    
    
    
#EXPRESSION
class Expression(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass

class ExpressionOperator(Expression):
    def __init__(self, operator):
        self.operator = operator
    def accept(self, visitor):
        return visitor.VisitExpressionOperator(self)

class ExpressionCall(Expression):
    def __init__(self, call):
        self.call = call
    def accept(self, visitor):
        return visitor.VisitExpressionCall(self)
    
class ExpressionFloatNumber(Expression):
    def __init__(self, float_number):
        self.float_number = float_number
    def accept(self, visitor):
        return visitor.VisitExpressionFloatNumber(self)
        
class ExpressionDoubleNumber(Expression):
    def __init__(self, double_number):
        self.double_number = double_number
    def accept(self, visitor):
        return visitor.VisitExpressionDoubleNumber(self)
        
class ExpressionIntNumber(Expression):
    def __init__(self, int_number):
        self.int_number = int_number
    def accept(self, visitor):
        return visitor.VisitExpressionIntNumber(self)
    
class ExpressionString(Expression):
    def __init__(self, string):
        self.string = string
    def accept(self, visitor):
        return visitor.VisitExpressionString(self)
        
class ExpressionId(Expression):
    def __init__(self, ID):
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitExpressionId(self)
        
class ExpressionNew(Expression):
    def __init__(self, type, params_call):
        self.type = type
        self.params_call = params_call
    def accept(self, visitor):
        return visitor.VisitExpressionNew(self)
        
class ExpressionNewList(Expression):
    def __init__(self, type, expression):
        self.type = type
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitExpressionNewList(self)   
        

#OPERATOR
class Operator(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass

class OperatorArithmeticTimes(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorArithmeticTimes(self)
    
class OperatorArithmeticDivide(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorArithmeticDivide(self)
    
class OperatorArithmeticModule(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorArithmeticModule(self)
    
class OperatorArithmeticPlus(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorArithmeticPlus(self)
    
class OperatorArithmeticMinus(Operator):
    def __init__(self,expression_1, expression_2):
            self.expression_1 = expression_1
            self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorArithmeticMinus(self)

class OperatorAssignEqual(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignEqual(self)
    
class OperatorAssignMinusEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignMinusEQ(self)
    
class OperatorAssignTimesEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignTimesEQ(self)

class OperatorAssignPlusEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignPlusEQ(self)

class OperatorAssignDivideEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignDivideEQ(self)
    
class OperatorAssignModuleEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignModuleEQ(self)
    
class OperatorAssignBitwiseAndEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignBitwiseAndEQ(self)
    
class OperatorAssignBitwiseOrEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignBitwiseAndEQ(self)
    
class OperatorAssignBitwiseXorEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignBitwiseXorEQ(self)
    
class OperatorAssignUrshiftEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignUrshiftEQ(self)
    
class OperatorAssignLshiftEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignLshiftEQ(self)

class OperatorAssignRshiftEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorAssignRshiftEQ(self)
    
class OperatorComparatorLeq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorLeq(self)

class OperatorComparatorGeq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorGeq(self)
    
class OperatorComparatorLt(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorLt(self)

class OperatorComparatorGt(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorGt(self)
    
class OperatorComparatorNeq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorNeq(self)
    
class OperatorComparatorEq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorEq(self)
    
class OperatorComparatorAnd(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorAnd(self)
    
class OperatorComparatorOr(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorOr(self)
    
class OperatorComparatorBitwise_And(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorBitwise_And(self)

class OperatorComparatorBitwise_OR(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorBitwise_OR(self)
    
class OperatorComparatorBitwise_XOR(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def accept(self, visitor):
        return visitor.VisitOperatorComparatorBitwise_XOR(self)
    
class OperatorUnaryPrefix(Operator):
    def __init__(self, unaryoperatorprefx, ID):
        self.unaryoperatorprefx = unaryoperatorprefx
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitOperatorUnaryPrefix(self)
    
class OperatorUnarySufix(Operator):
    def __init__(self, ID, unaryoperatorsufix):
        self.unaryoperatorsufix = unaryoperatorsufix
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitOperatorUnarySufix(self)
        
class OperatorBitToBit(Operator):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitOperatorBitToBit(self)


#UNARYOPERATORPREFIX
class UnaryOperatorPrefix(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class UnaryOperatorPrefixConcrete(UnaryOperatorPrefix):
    def __init__(self, unaryoperatorprefx):
        self.unaryoperatorprefx = unaryoperatorprefx
    def accept(self, visitor):
        return visitor.VisitUnaryOperatorPrefixConcrete(self)
    

#UNARYOPERATORSUFIX
class UnaryOperatorSufix(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class UnaryOperatorSufixConcrete(UnaryOperatorSufix):
    def __init__(self, unaryoperatorsufix):
        self.unaryoperatorsufix = unaryoperatorsufix
    def accept(self, visitor):
        return visitor.VisitUnaryOperatorSufixConcrete(self)
    
#UNARYOPERATORBITTOBIT
class UnaryOperatorBitToBit(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class UnaryOperatorBitToBitConcrete(UnaryOperatorBitToBit):
    def __init__(self, unaryoperatorbit):
        self.unaryoperatorbit = unaryoperatorbit
    def accept(self, visitor):
        return visitor.VisitUnaryOperatorBitToBitConcrete(self)
        
#BRACKETSEXPRESSION       
class BracketsExpression(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
          
class BracketsExpressionSimple(BracketsExpression):
    def __init__(self, brackets_default):
        self.brackets_default = brackets_default
    def accept(self, visitor):
        return visitor.VisitBracketsExpressionSimple(self)
          
class BracketsExpressionIntNumber(BracketsExpression):
    def __init__(self, int_number):
        self.int_number = int_number
    def accept(self, visitor):
        return visitor.VisitBracketsExpressionIntNumber(self)
    
class BracketsExpressionId(BracketsExpression):
    def __init__(self, ID):
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitBracketsExpressionId(self)
    

    
#TYPE
class Type(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass

class TypePrimitive(Type):
    def __init__(self, primitivetypes):
        self.primitivetypes = primitivetypes
    def accept(self, visitor):
        return visitor.VisitTypePrimitive(self)
        
        
#PRIMITIVETYPES
class PrimitiveTypes(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass

class PrimitiveTypesConcrete(PrimitiveTypes):
    def __init__(self, primitivetypes):
        self.primitivetypes = primitivetypes
    def accept(self, visitor):
        return visitor.VisitPrimitiveTypesConcrete(self)

# class PrimitiveTypesInt(PrimitiveTypes):
#     def __init__(self, _int):
#         self._int = _int
#     def accept(self, visitor):
#         pass
    
# class PrimitiveTypes(PrimitiveTypes):
#     def __init__(self, _float):
#         self._float = _float
#     def accept(self, visitor):
#         pass

# class PrimitiveTypesDouble(PrimitiveTypes):
#     def __init__(self, _double):
#         self._double = _double
#     def accept(self, visitor):
#         pass
    
# class PrimitiveTypesByte(PrimitiveTypes):
#     def __init__(self, _byte):
#         self._byte = _byte
#     def accept(self, visitor):
#         pass

# class PrimitiveTypesBoolean(PrimitiveTypes):
#     def __init__(self, _boolean):
#         self._boolean = _boolean
#     def accept(self, visitor):
#         pass
    
# class PrimitiveTypesChar(PrimitiveTypes):
#     def __init__(self, _char):
#         self._char = _char
#     def accept(self, visitor):
#         pass
    
# class PrimitiveTypesString(PrimitiveTypes):
#     def __init__(self, _string):
#         self._string = _string
#     def accept(self, visitor):
#         pass
        
# class PrimitiveTypesLong(PrimitiveTypes):
#     def __init__(self, _long):
#         self._long = _long
#     def accept(self, visitor):
#         pass

# class PrimitiveTypesVoid(PrimitiveTypes):
#     def __init__(self, _void):
#         self._void = _void
#     def accept(self, visitor):
#         pass
  
    
#CALL    
class Call(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass

class CallParams(Call):
    def __init__(self,ID , callparams):
        self.ID = ID
        self.callparams = callparams
    def accept(self, visitor):
        return visitor.VisitCallParams(self)

class CallDefault(Call):
    def __init__(self, ID):
        self.ID = ID
    def accept(self, visitor):
        return visitor.VisitCallDefault(self)
    
#PARAMSCALL
class ParamsCall(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class ParamsCallMulti(ParamsCall):
    def __init__(self, expression, params_call):
        self.expression = expression
        self.params_call = params_call
    def accept(self, visitor):
        return visitor.VisitParamsCallMulti(self)
    
class ParamsCallUnique(ParamsCall):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitParamsCallUnique(self)

#CHAVEXPRESSION
class ChavExp(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class ChavExpEmpty(ChavExp):
    def __init__(self):
        pass
    def accept(self, visitor):
        return visitor.VisitChavExpEmpty(self)
    
class ChavExpExpressionChav(ChavExp):
    def __init__(self, expression_chav):
        self.expression_chav = expression_chav
    def accept(self, visitor):
        return visitor.VisitChavExpExpressionChav(self)
    
#EXPRESSIONCHAV
class ExpressionChav(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class ExpressionChavMult(ExpressionChav):
    def __init__(self, expression, expression_chav):
        self.expression = expression
        self.expression_chav = expression_chav
    def accept(self, visitor):
        return visitor.VisitExpressionChavMult(self)
    
class ExpressionChavUni(ExpressionChav):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitExpressionChavUni(self)
    
class ExpressionChavComma(ExpressionChav):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.VisitExpressionChavComma(self)