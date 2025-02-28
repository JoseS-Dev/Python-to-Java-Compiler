from abc import abstractmethod, ABCMeta

### Defincion de la clase Programa
class Programa(metaclass=ABCMeta):
    @abstractmethod
    def acceder(self,visitor):
        pass

class ProgramaCompilador(Programa):
    def __init__(self, clase):
        self.clase = clase
    
    def acceder(self,visitor):
        return visitor.visitarPrograma(self)

### Definicion de la clase Clase
class Class(metaclass=ABCMeta):
    @abstractmethod
    def acceder(self,visitor):
        pass

class ClassExtends(Class):
    def __init__(self,visibilidad, claseModificar, ID_NOMECLASS, ID_NOMEEXTENDS, miembros):
        self.visibilidad = visibilidad
        self.claseModificar = claseModificar
        self.ID_NOMECLASS = ID_NOMECLASS
        self.ID_NOMEEXTENDS = ID_NOMEEXTENDS
        self.miembros = miembros
    
    def acceder(self,visitor):
        return visitor.VisitCClassExtends(self)

class ClassDefault(Class):
    def __init__(self,visibilidad, claseModificar, ID_NOMECLASS, miembros):
        self.visibilidad = visibilidad
        self.claseModificar = claseModificar
        self.ID_NOMECLASS = ID_NOMECLASS
        self.miembros = miembros

    def acceder(self,visitor):
        return visitor.VisitCClassDefault(self)

class ClassImplements(Class):
    def __init__(self,visibilidad, claseModificar, ID_NOMECLASS, miembros):
        self.visibilidad = visibilidad
        self.claseModificar = claseModificar
        self.ID_NOMECLASS = ID_NOMECLASS
        self.miembros = miembros

    def acceder(self,visitor):
        return visitor.VisitCClassImplements(self)
    
### Definicion de las clase visibilidad
class visibilidad(metaclass=ABCMeta):
    
