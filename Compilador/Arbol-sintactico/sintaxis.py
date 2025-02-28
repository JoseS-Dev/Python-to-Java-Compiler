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

