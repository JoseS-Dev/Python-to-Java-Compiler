from abc import abstractmethod, ABCMeta
from abc import ABCMeta, abstractmethod

# PROGRAMA
class Programa(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
        
class ProgramaConcreto(Programa):
    def __init__(self, clase):
        self.clase = clase
        
    def aceptar(self, visitante):
        return visitante.visitarProgramaConcreto(self)
        
        
# CLASE
class CClase(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class CClaseExtiende(CClase):
    def __init__(self, visibilidad, modificador_clase, ID_NOMBRECLASE, ID_NOMBREEXTIENDE, miembros):
        self.visibilidad = visibilidad
        self.modificador_clase = modificador_clase
        self.ID_NOMBRECLASE = ID_NOMBRECLASE
        self.ID_NOMBREEXTIENDE = ID_NOMBREEXTIENDE
        self.miembros = miembros
        
    def aceptar(self, visitante):
        return visitante.visitarCClaseExtiende(self)

# CLASE
class CClasePorDefecto(CClase):
    def __init__(self, visibilidad, modificador_clase, ID_NOMBRECLASE, miembros):
        self.visibilidad = visibilidad     
        self.modificador_clase = modificador_clase
        self.ID_NOMBRECLASE = ID_NOMBRECLASE
        self.miembros = miembros
        
    def aceptar(self, visitante):
        return visitante.visitarCClasePorDefecto(self)
    
class CClaseImplementa(CClase):
    def __init__(self, visibilidad, modificador_clase, ID_NOMBRECLASE, miembros):
        self.visibilidad = visibilidad
        self.modificador_clase = modificador_clase
        self.ID_NOMBRECLASE = ID_NOMBRECLASE
        self.miembros = miembros
        
    def aceptar(self, visitante):
        return visitante.visitarCClaseImplementa(self)


# VISIBILIDAD
class Visibilidad(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
    
class VisibilidadConcreta(Visibilidad):
    def __init__(self, visibilidad):
        self.visibilidad = visibilidad
        
    def aceptar(self, visitante):
        return visitante.visitarVisibilidadConcreta(self)

# MODIFICADOR DE CLASE
class ModificadorClase(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
  
class ModificadorClaseConcreto(ModificadorClase):
    def __init__(self, modificador_clase):
        self.modificador_clase = modificador_clase
        
    def aceptar(self, visitante):
        return visitante.visitarModificadorClaseConcreto(self)
    
    
# MIEMBROS
class Miembros(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class MiembrosUnico(Miembros):
    def __init__(self, miembro):
        self.miembro = miembro
        
    def aceptar(self, visitante):
        return visitante.visitarMiembrosUnico(self)
    
class MiembrosMultiples(Miembros):
    def __init__(self, miembro, miembros):
        self.miembro = miembro
        self.miembros = miembros
        
    def aceptar(self, visitante):
        return visitante.visitarMiembrosMultiples(self)
    
# MIEMBRO
class Miembro(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class MiembroAtributo(Miembro):
    def __init__(self, atributo):
        self.atributo = atributo
        
    def aceptar(self, visitante):
        return visitante.visitarMiembroAtributo(self)

class MiembroFuncion(Miembro):
    def __init__(self, funcion):
        self.funcion = funcion
        
    def aceptar(self, visitante):
        return visitante.visitarMiembroFuncion(self)


# ATRIBUTOS
class Atributo(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class AtributoPorDefecto(Atributo):
    def __init__(self, visibilidad, modificador_atributo, tipo, ID):
        self.visibilidad = visibilidad
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarAtributoPorDefecto(self)

# ATRIBUTO POR DEFECTO INICIALIZADO
class AtributoPorDefectoInicializado(Atributo):
    def __init__(self, visibilidad, modificador_atributo, tipo, ID, expresion):
        self.visibilidad = visibilidad
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarAtributoPorDefectoInicializado(self)
    
    
# MODIFICADOR DE ATRIBUTO
class ModificadorAtributo(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class ModificadorAtributoConcreto(ModificadorAtributo):
    def __init__(self, modificador_atributo):
        self.modificador_atributo = modificador_atributo
        
    def aceptar(self, visitante):
        return visitante.visitarModificadorAtributoConcreto(self)


# FUNCIONES
class Funcion(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class FuncionPorDefecto(Funcion):
    def __init__(self, firma, cuerpo):
        self.firma = firma
        self.cuerpo = cuerpo
        
    def aceptar(self, visitante):
        return visitante.visitarFuncionPorDefecto(self)