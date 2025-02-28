from abc import abstractmethod, ABCMeta

### Defincion de la clase Programa
class Program(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class ProgramCompiler(Program):
    def __init__(self, clase):
        self.clase = clase
    
    def access(self,visitor):
        return visitor.visitarPrograma(self)

### Definicion de la clase Clase
class Class(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class ClassExtends(Class):
    def __init__(self,visibility, claseModificar, ID_NOMECLASS, ID_NOMEEXTENDS, members):
        self.visibility = visibility
        self.claseModificar = claseModificar
        self.ID_NOMECLASS = ID_NOMECLASS
        self.ID_NOMEEXTENDS = ID_NOMEEXTENDS
        self.members = members
    
    def access(self,visitor):
        return visitor.VisitCClassExtends(self)

class ClassDefault(Class):
    def __init__(self,visibility, claseModificar, ID_NOMECLASS, members):
        self.visibility = visibility
        self.claseModificar = claseModificar
        self.ID_NOMECLASS = ID_NOMECLASS
        self.members = members

    def access(self,visitor):
        return visitor.VisitCClassDefault(self)

class ClassImplements(Class):
    def __init__(self,visibility, claseModificar, ID_NOMECLASS, members):
        self.visibility = visibility
        self.claseModificar = claseModificar
        self.ID_NOMECLASS = ID_NOMECLASS
        self.members = members

    def access(self,visitor):
        return visitor.VisitCClassImplements(self)
    
### Definicion de las clase visibilidad
class visibility(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class visibilityConcrete(visibility):
    def __init__(self,visibilitys):
        self.visibilitys = visibilitys
    
    def access(self, visitor):
        return visitor.VisitVisibilityConcrete(self)

### definicion de la clase ClaseModificar
class ClassModify(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class ClassModifyConcrete(ClassModify):
    def __init__(self, classModifys):
        self.classModifys = classModifys
    
    def access(self, visitor):
        return visitor.VisitClassModifyConcrete(self)

### Definiciond de la clase Miembros
class Members(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class MembersUni(Members):
    def __init__(self, member):
        self.member = member
    
    def access(self,visitor):
        return visitor.VisitMembersUni(self)

class MembersMult(Members):
    def __init__(self, member, members):
        self.member = member
        self.members = members
    
    def access(self,visitor):
        return visitor.VisitMembersMult(self)

### Definicion de la clase Miembro
class Member(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class MemberAtribute(Member):
    def __init__(self,atribute):
        self.atribute = atribute
    
    def access(self, visitor):
        return visitor.VisitMemberAtribute(self)

class MemberFunction(Member):
    def __init__(self, function):
        self.function = function
    
    def access(self, visitor):
        return visitor.VisitMemberFunction(self)

### Definicion de la clase Atributo
class Atribute(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class AtributeDefault(Atribute):
    def __init__(self,visibility, atributemodifier, type, ID):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    
    def access(self,visitor):
        return visitor.VisitAtributeDefault(self)

class AtributeDefaultInicializedType(Atribute):
    def __init__(self, visibility, atributemodifier, type, ID, expression):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.expression = expression
    
    def access(self,visitor):
        return visitor.VisitAtributeDefaultInicializedType(self)

### dEfinicion de la clase AtributoModificador
class AtributeModifier(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class AtributeModifierConcrete(AtributeModifier):
    def __init__(self, atributeModifiers):
        self.atributeModifiers = atributeModifiers
    
    def access(self, visitor):
        return visitor.VisitAtributeModifierConcrete(self)

### Definicion de la clase funcion
class Function(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class FunctionDefault(Function):
    def __init__(self, signature, body):
        self.signature = signature
        self.body = body
    
    def access(self, visitor):
        return visitor.VisitFunctionDefault(self)

### Definicion de la clase Signature
class Signature(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class SignatureSimple(Signature):
    def __init__(self, visibility, atributemodifier, type, ID, sigparams):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.sigparams = sigparams
    
    def access(self, visitor):
        return visitor.VisitSignatureSimple(self)

class SignatureMult(Signature):
    def __init__(self, visibility, atributemodifier, type, bracket_expression, ID, sigparams):
        self.visibility = visibility
        self.atributemodifier = atributemodifier
        self.type = type
        self.bracket_expression = bracket_expression
        self.ID = ID
        self.sigparams = sigparams
    
    def access(self, visitor):
        return visitor.VisitSignatureMult(self)

### Definicion de la clase SignatureParams
class SigParams(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class SigparamsId(SigParams):
    def __init__(self, type, ID):
        self.type = type
        self.ID = ID
    
    def access(self, visitor):
        return visitor.VisitSigparamsId(self)
    
class SigparamsSigparams(SigParams):
    def __init__(self, type, ID, sigparams):
        self.type = type
        self.ID = ID
        self.sigparams = sigparams
    
    def access(self, visitor):
        return visitor.VisitSigparamsSigparams(self)

### Definicion de la clase Cuerpo
class Body(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass
class BodyStms(Body):
    def __init__(self, stms):
        self.stms = stms
    
    def access(self, visitor):
        return visitor.VisitBodyStms(self)

### Definicion de la clase stms
class Stms(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class StmsUni(Stms):
    def __init__(self, stm):
        self.stm = stm
    
    def access(self, visitor):
        return visitor.VisitStmsUni(self)
    
class StmsMulti(Stms):
    def __init__(self, stm, stms):
        self.stm = stm
        self.stms = stms
    
    def access(self, visitor):
        return visitor.VisitStmsMulti(self)

### Definicion de la clase stm
class Stm(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class StmExpression(Stm):
    def __init__(self, expression):
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitStmExpression(self)
    
class StmExpressionWhile(Stm):
    def __init__(self, expression, bodyorstm):
        self.expression = expression
        self.bodyorstm = bodyorstm
    
    def access(self, visitor):
        return visitor.VisitStmExpressionWhile(self)
    
class StmExpressionDoWhile(Stm):
    def __init__(self, bodyorstm, expression):
        self.bodyorstm = bodyorstm
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitStmExpressionDoWhile(self)
    
class StmExpressionFor(Stm):
    def __init__(self, expression_for, expression_mid, expression_final, bodyorstm):
        self.expression_for = expression_for
        self.expression_mid = expression_mid
        self.expression_final = expression_final
        self.bodyorstm = bodyorstm
    
    def access(self, visitor):
        return visitor.VisitStmExpressionFor(self)
        
class StmExpressionIf(Stm):
    def __init__(self, expression, bodyorstm):
        self.expression = expression
        self.bodyorstm = bodyorstm
    
    def access(self, visitor):
        return visitor.VisitStmExpressionIf(self)
        
class StmExpressionIfElse(Stm):
    def __init__(self, expression, bodyorstm_1,bodyorstm_2):
        self.expression = expression
        self.bodyorstm_1 = bodyorstm_1
        self.bodyorstm_2 = bodyorstm_2
    
    def access(self, visitor):
        return visitor.VisitStmExpressionIfElse(self)
        
class StmExpressionElseIf(Stm):
    def __init__(self, expression, bodyorstm_1,bodyorstm_2):
        self.expression = expression
        self.bodyorstm_1 = bodyorstm_1
        self.bodyorstm_2 = bodyorstm_2
    
    def access(self, visitor):
        return visitor.VisitStmExpressionElseIf(self)
    
class StmExpressionSemicolon(Stm):
    def __init__(self):
        pass
    def access(self, visitor):
        return visitor.VisitStmExpressionSemicolon(self)     
        
class StmExpressionVariable(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def access(self, visitor):
        return visitor.VisitStmExpressionVariable(self)        
                
class StmExpressionVariableType(Stm):
    def __init__(self, atributemodifier, type, ID, expression):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableType(self)
    
class StmExpressionVariableTypeList(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableTypeList(self)
    
class StmExpressionVariableTypeListPre(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListPre(self)
    
class StmExpressionVariableTypeListListPre(Stm):
    def __init__(self, atributemodifier, type, ID, chav_exp):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.chav_exp = chav_exp
    
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListListPre(self)
    
class StmExpressionVariableTypeListExpression(Stm):
    def __init__(self, atributemodifier, type, ID, expression):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListExpression(self)
    
class StmExpressionVariableTypeListExpressionInicialized(Stm):
    def __init__(self, atributemodifier, type, ID, chav_exp):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.chav_exp = chav_exp
    
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListExpressionInicialized(self)
    
class StmExpressionVariableTypeListList(Stm):
    def __init__(self, atributemodifier, type, ID):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
    
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListList(self)
    
class StmExpressionVariableTypeListListInicialized(Stm):
    def __init__(self, atributemodifier, type, ID, chav_exp):
        self.atributemodifier = atributemodifier
        self.type = type
        self.ID = ID
        self.chav_exp = chav_exp
    
    def access(self, visitor):
        return visitor.VisitStmExpressionVariableTypeListListInicialized(self)

class StmExpressionReturn(Stm):
    def __init__(self, expression):
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitStmExpressionReturn(self)
    
class StmExpressionVoidReturn(Stm):
    def __init__(self, void_return):
        self.void_return = void_return
    
    def access(self, visitor):
        return visitor.VisitStmExpressionVoidReturn(self)

### Definicion de la clase bodyorstm
class BodyOrStm(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class BodyOrStmBody(BodyOrStm):
    def __init__(self, body):
        self.body = body
    
    def access(self, visitor):
        return visitor.VisitBodyOrStmBody(self)

### Definicion de la clase expressionFor
class ExpressionFor(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class ExpressionForAssignForType(ExpressionFor):
    def __init__(self, type, ID, expression):
        self.type = type 
        self.ID = ID 
        self.expression = expression 
    
    def access(self, visitor):
        return visitor.VisitExpressionForAssignForType(self)
    
class ExpressionForAssignFor(ExpressionFor):
    def __init__(self, ID, expression):
        self.ID = ID 
        self.expression = expression 
    
    def access(self, visitor):
        return visitor.VisitExpressionForAssignFor(self)

### Definicion de la clase expression
class Expression(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class ExpressionOperator(Expression):
    def __init__(self, operator):
        self.operator = operator
    
    def access(self, visitor):
        return visitor.VisitExpressionOperator(self)

class ExpressionCall(Expression):
    def __init__(self, call):
        self.call = call
    
    def access(self, visitor):
        return visitor.VisitExpressionCall(self)
    
class ExpressionFloatNumber(Expression):
    def __init__(self, float_number):
        self.float_number = float_number
    
    def access(self, visitor):
        return visitor.VisitExpressionFloatNumber(self)
        
class ExpressionDoubleNumber(Expression):
    def __init__(self, double_number):
        self.double_number = double_number
    
    def access(self, visitor):
        return visitor.VisitExpressionDoubleNumber(self)
        
class ExpressionIntNumber(Expression):
    def __init__(self, int_number):
        self.int_number = int_number
    
    def access(self, visitor):
        return visitor.VisitExpressionIntNumber(self)
    
class ExpressionString(Expression):
    def __init__(self, string):
        self.string = string
    
    def access(self, visitor):
        return visitor.VisitExpressionString(self)
        
class ExpressionId(Expression):
    def __init__(self, ID):
        self.ID = ID
    
    def access(self, visitor):
        return visitor.VisitExpressionId(self)
        
class ExpressionNew(Expression):
    def __init__(self, type, params_call):
        self.type = type
        self.params_call = params_call
    
    def access(self, visitor):
        return visitor.VisitExpressionNew(self)
        
class ExpressionNewList(Expression):
    def __init__(self, type, expression):
        self.type = type
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitExpressionNewList(self)

### Definicion de la clase Operador
class Operator(metaclass=ABCMeta):
    @abstractmethod
    def access(self,visitor):
        pass

class OperatorArithmeticTimes(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def access(self, visitor):
        return visitor.VisitOperatorArithmeticTimes(self)
    
class OperatorArithmeticDivide(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def access(self, visitor):
        return visitor.VisitOperatorArithmeticDivide(self)
    
class OperatorArithmeticModule(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def access(self, visitor):
        return visitor.VisitOperatorArithmeticModule(self)
    
class OperatorArithmeticPlus(Operator):
    def __init__(self,expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    def access(self, visitor):
        return visitor.VisitOperatorArithmeticPlus(self)
    
class OperatorArithmeticMinus(Operator):
    def __init__(self,expression_1, expression_2):
            self.expression_1 = expression_1
            self.expression_2 = expression_2
    def access(self, visitor):
        return visitor.VisitOperatorArithmeticMinus(self)

class OperatorAssignEqual(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitOperatorAssignEqual(self)
    
class OperatorAssignMinusEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitOperatorAssignMinusEQ(self)
    
class OperatorAssignTimesEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitOperatorAssignTimesEQ(self)

class OperatorAssignPlusEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitOperatorAssignPlusEQ(self)

class OperatorAssignDivideEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitOperatorAssignDivideEQ(self)
    
class OperatorAssignModuleEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitOperatorAssignModuleEQ(self)
    
class OperatorAssignBitwiseAndEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    def access(self, visitor):
        return visitor.VisitOperatorAssignBitwiseAndEQ(self)
    
class OperatorAssignBitwiseOrEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitOperatorAssignBitwiseAndEQ(self)
    
class OperatorAssignBitwiseXorEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitOperatorAssignBitwiseXorEQ(self)
    
class OperatorAssignUrshiftEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitOperatorAssignUrshiftEQ(self)
    
class OperatorAssignLshiftEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitOperatorAssignLshiftEQ(self)

class OperatorAssignRshiftEQ(Operator):
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitOperatorAssignRshiftEQ(self)
    
class OperatorComparatorLeq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorLeq(self)

class OperatorComparatorGeq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorGeq(self)
    
class OperatorComparatorLt(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorLt(self)

class OperatorComparatorGt(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorGt(self)
    
class OperatorComparatorNeq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorNeq(self)
    
class OperatorComparatorEq(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorEq(self)
    
class OperatorComparatorAnd(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorAnd(self)
    
class OperatorComparatorOr(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorOr(self)
    
class OperatorComparatorBitwise_And(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorBitwise_And(self)

class OperatorComparatorBitwise_OR(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorBitwise_OR(self)
    
class OperatorComparatorBitwise_XOR(Operator):
    def __init__(self, expression_1, expression_2):
        self.expression_1 = expression_1
        self.expression_2 = expression_2
    
    def access(self, visitor):
        return visitor.VisitOperatorComparatorBitwise_XOR(self)
    
class OperatorUnaryPrefix(Operator):
    def __init__(self, unaryoperatorprefx, ID):
        self.unaryoperatorprefx = unaryoperatorprefx
        self.ID = ID
    
    def access(self, visitor):
        return visitor.VisitOperatorUnaryPrefix(self)
    
class OperatorUnarySufix(Operator):
    def __init__(self, ID, unaryoperatorsufix):
        self.unaryoperatorsufix = unaryoperatorsufix
        self.ID = ID
    
    def access(self, visitor):
        return visitor.VisitOperatorUnarySufix(self)
        
class OperatorBitToBit(Operator):
    def __init__(self, expression):
        self.expression = expression
    
    def access(self, visitor):
        return visitor.VisitOperatorBitToBit(self)
