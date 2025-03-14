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

# FIRMA
class Firma(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class FirmaSimple(Firma):
    def __init__(self, visibilidad, modificador_atributo, tipo, ID, parametros_firma):
        self.visibilidad = visibilidad
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        self.parametros_firma = parametros_firma
        
    def aceptar(self, visitante):
        visitante.visitarFirmaSimple(self)
        
class FirmaMultiple(Firma):
    def __init__(self, visibilidad, modificador_atributo, tipo, expresion_corchetes, ID, parametros_firma):
        self.visibilidad = visibilidad
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.expresion_corchetes = expresion_corchetes
        self.ID = ID
        self.parametros_firma = parametros_firma
        
    def aceptar(self, visitante):
        visitante.visitarFirmaMultiple(self)
    

# PARAMETROS DE FIRMA
class ParametrosFirma(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class ParametrosFirmaId(ParametrosFirma):
    def __init__(self, tipo, ID):
        self.tipo = tipo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarParametrosFirmaId(self)

# PARAMETROS DE FIRMA
class ParametrosFirmaParametros(ParametrosFirma):
    def __init__(self, tipo, ID, parametros_firma):
        self.tipo = tipo
        self.ID = ID
        self.parametros_firma = parametros_firma
        
    def aceptar(self, visitante):
        return visitante.visitarParametrosFirmaParametros(self)
           
               
# CUERPO
class Cuerpo(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class CuerpoSentencias(Cuerpo):
    def __init__(self, sentencias):
        self.sentencias = sentencias
        
    def aceptar(self, visitante):
        return visitante.visitarCuerpoSentencias(self)
    
# SENTENCIAS
class Sentencias(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class SentenciasUnicas(Sentencias):
    def __init__(self, sentencia):
        self.sentencia = sentencia
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciasUnicas(self)
    
class SentenciasMultiples(Sentencias):
    def __init__(self, sentencia, sentencias):
        self.sentencia = sentencia
        self.sentencias = sentencias
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciasMultiples(self)

# SENTENCIA
class Sentencia(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class SentenciaExpresion(Sentencia):
    def __init__(self, expresion):
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresion(self)
    
class SentenciaExpresionWHILE(Sentencia):
    def __init__(self, expresion, cuerpo_o_sentencia):
        self.expresion = expresion
        self.cuerpo_o_sentencia = cuerpo_o_sentencia
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionWHILE(self)
    
class SentenciaExpresionDOWHILE(Sentencia):
    def __init__(self, cuerpo_o_sentencia, expresion):
        self.cuerpo_o_sentencia = cuerpo_o_sentencia
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionDOWHILE(self)
    
class SentenciaExpresionFOR(Sentencia):
    def __init__(self, expresion_para, expresion_media, expresion_final, cuerpo_o_sentencia):
        self.expresion_para = expresion_para
        self.expresion_media = expresion_media
        self.expresion_final = expresion_final
        self.cuerpo_o_sentencia = cuerpo_o_sentencia
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionFOR(self)
        
class SentenciaExpresionIF(Sentencia):
    def __init__(self, expresion, cuerpo_o_sentencia):
        self.expresion = expresion
        self.cuerpo_o_sentencia = cuerpo_o_sentencia
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionIF(self)

class SentenciaExpresionIFELSE(Sentencia):
    def __init__(self, expresion, cuerpo_o_sentencia_1, cuerpo_o_sentencia_2):
        self.expresion = expresion
        self.cuerpo_o_sentencia_1 = cuerpo_o_sentencia_1
        self.cuerpo_o_sentencia_2 = cuerpo_o_sentencia_2
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionIFELSE(self)
        
class SentenciaExpresionELSEIF(Sentencia):
    def __init__(self, expresion, cuerpo_o_sentencia_1, cuerpo_o_sentencia_2):
        self.expresion = expresion
        self.cuerpo_o_sentencia_1 = cuerpo_o_sentencia_1
        self.cuerpo_o_sentencia_2 = cuerpo_o_sentencia_2
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionELSEIF(self)
    
class SentenciaExpresionSeminColon(Sentencia):
    def __init__(self):
        pass
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionSeminColon(self)     
        
class SentenciaExpresionVariable(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariable(self)        
                
class SentenciaExpresionVariableTipo(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID, expresion):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipo(self)
    
class SentenciaExpresionVariableTipoList(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipoList(self)

class SentenciaExpresionVariableTipoListPre(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipoListPre(self)
    
class SentenciaExpresionVariableTipoListListPre(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID, expresion_llave):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        self.expresion_llave = expresion_llave
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipoListListPre(self)
    
class SentenciaExpresionVariableTipoListExpresion(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID, expresion):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipoListExpresion(self)
    
class SentenciaExpresionVariableTipoListExpresionInicializada(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID, expresion_llave):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        self.expresion_llave = expresion_llave
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipoListExpresionInicializada(self)
    
class SentenciaExpresionVariableTipoListList(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipoListList(self)

class SentenciaExpresionVariableTipoListListInicializada(Sentencia):
    def __init__(self, modificador_atributo, tipo, ID, expresion_llave):
        self.modificador_atributo = modificador_atributo
        self.tipo = tipo
        self.ID = ID
        self.expresion_llave = expresion_llave
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVariableTipoListListInicializada(self)

class SentenciaExpresionReturn(Sentencia):
    def __init__(self, expresion):
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionReturn(self)
    
class SentenciaExpresionVoidReturn(Sentencia):
    def __init__(self, retorno_vacio):
        self.retorno_vacio = retorno_vacio
        
    def aceptar(self, visitante):
        return visitante.visitarSentenciaExpresionVoidReturn(self)

# CUERPO O SENTENCIA
class CuerpoOSentencia(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class CuerpoOSentenciaCuerpo(CuerpoOSentencia):
    def __init__(self, cuerpo):
        self.cuerpo = cuerpo
        
    def aceptar(self, visitante):
        return visitante.visitarCuerpoOSentenciaCuerpo(self)
        
# EXPRESION FOR
class ExpresionFOR(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class ExpresionParaAsignarTipo(ExpresionFOR):
    def __init__(self, tipo, ID, expresion):
        self.tipo = tipo 
        self.ID = ID 
        self.expresion = expresion 
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionParaAsignarTipo(self)
    
class ExpresionAsignarFOR(ExpresionFOR):
    def __init__(self, ID, expresion):
        self.ID = ID 
        self.expresion = expresion 
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionAsignarFOR(self)

# EXPRESIÓN
class Expresion(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass

class ExpresionOperador(Expresion):
    def __init__(self, operador):
        self.operador = operador
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionOperador(self)

class ExpresionCALL(Expresion):
    def __init__(self, llamada):
        self.llamada = llamada
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionCALL(self)
    
class ExpresionNumeroFloat(Expresion):
    def __init__(self, numero_flotante):
        self.numero_flotante = numero_flotante
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionNumeroFloat(self)
        
class ExpresionNumeroDouble(Expresion):
    def __init__(self, numero_doble):
        self.numero_doble = numero_doble
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionNumeroDouble(self)
        
class ExpresionNumeroINT(Expresion):
    def __init__(self, numero_entero):
        self.numero_entero = numero_entero
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionNumeroINT(self)
    
class ExpresionSTRING(Expresion):
    def __init__(self, cadena):
        self.cadena = cadena
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionSTRING(self)

class ExpresionId(Expresion):
    def __init__(self, ID):
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionId(self)
        
class ExpresionNuevo(Expresion):
    def __init__(self, tipo, parametros_llamada):
        self.tipo = tipo
        self.parametros_llamada = parametros_llamada
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionNuevo(self)
        
class ExpresionNuevaList(Expresion):
    def __init__(self, tipo, expresion):
        self.tipo = tipo
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionNuevaList(self)
    
# OPERADOR
class Operador(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass

class OperadorAritmeticoMultiplicar(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAritmeticoMultiplicar(self)
    
class OperadorAritmeticoDividir(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAritmeticoDividir(self)
    
class OperadorAritmeticoModulo(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAritmeticoModulo(self)
    
class OperadorAritmeticoSumar(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAritmeticoSumar(self)
    
class OperadorAritmeticoRestar(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAritmeticoRestar(self)

class OperadorAsignarIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarIgual(self)
    
class OperadorAsignarMenosIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarMenosIgual(self)
    
class OperadorAsignarMultiplicarIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarMultiplicarIgual(self)

class OperadorAsignarSumarIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarSumarIgual(self)

class OperadorAsignarDividirIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarDividirIgual(self)
    
class OperadorAsignarModuloIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarModuloIgual(self)
    
class OperadorAsignarBitwiseYIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarBitwiseYIgual(self)
    
class OperadorAsignarBitwiseOIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarBitwiseOIgual(self)

class OperadorAsignarBitwiseXorIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarBitwiseXorIgual(self)
    
class OperadorAsignarDesplazamientoDerechaSinSignoIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarDesplazamientoDerechaSinSignoIgual(self)
    
class OperadorAsignarDesplazamientoIzquierdaIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarDesplazamientoIzquierdaIgual(self)

class OperadorAsignarDesplazamientoDerechaIgual(Operador):
    def __init__(self, ID, expresion):
        self.ID = ID
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorAsignarDesplazamientoDerechaIgual(self)
    
class OperadorComparadorMenorIgual(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorMenorIgual(self)

class OperadorComparadorMayorIgual(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorMayorIgual(self)
    
class OperadorComparadorMenor(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorMenor(self)

class OperadorComparadorMayor(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorMayor(self)
    
class OperadorComparadorDiferente(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorDiferente(self)
    
class OperadorComparadorIgual(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorIgual(self)
    
class OperadorComparadorY(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorY(self)
    
class OperadorComparadorO(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorO(self)

class OperadorComparadorBitwiseY(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorBitwiseY(self)

class OperadorComparadorBitwiseO(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorBitwiseO(self)
    
class OperadorComparadorBitwiseXOR(Operador):
    def __init__(self, expresion_1, expresion_2):
        self.expresion_1 = expresion_1
        self.expresion_2 = expresion_2
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorComparadorBitwiseXOR(self)

class OperadorUnarioPrefijo(Operador):
    def __init__(self, operador_unario_prefijo, ID):
        self.operador_unario_prefijo = operador_unario_prefijo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorUnarioPrefijo(self)
    
class OperadorUnarioSufijo(Operador):
    def __init__(self, ID, operador_unario_sufijo):
        self.operador_unario_sufijo = operador_unario_sufijo
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorUnarioSufijo(self)
        
class OperadorBitABit(Operador):
    def __init__(self, expresion):
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorBitABit(self)

# OPERADOR UNARIO PREFIJO
class OperadorUnarioPrefijo(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class OperadorUnarioPrefijoConcreto(OperadorUnarioPrefijo):
    def __init__(self, operador_unario_prefijo):
        self.operador_unario_prefijo = operador_unario_prefijo
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorUnarioPrefijoConcreto(self)
    

# OPERADOR UNARIO SUFIJO
class OperadorUnarioSufijo(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class OperadorUnarioSufijoConcreto(OperadorUnarioSufijo):
    def __init__(self, operador_unario_sufijo):
        self.operador_unario_sufijo = operador_unario_sufijo
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorUnarioSufijoConcreto(self)
    
# OPERADOR UNARIO BIT A BIT
class OperadorUnarioBitABit(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class OperadorUnarioBitABitConcreto(OperadorUnarioBitABit):
    def __init__(self, operador_unario_bit):
        self.operador_unario_bit = operador_unario_bit
        
    def aceptar(self, visitante):
        return visitante.visitarOperadorUnarioBitABitConcreto(self)

# EXPRESIÓN DE CORCHETES
class ExpresionDeCorchetes(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
          
class ExpresionDeCorchetesSimple(ExpresionDeCorchetes):
    def __init__(self, corchetes_por_defecto):
        self.corchetes_por_defecto = corchetes_por_defecto
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionDeCorchetesSimple(self)
          
class ExpresionDeCorchetesNumeroEntero(ExpresionDeCorchetes):
    def __init__(self, numero_entero):
        self.numero_entero = numero_entero
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionDeCorchetesNumeroEntero(self)
    
class ExpresionDeCorchetesId(ExpresionDeCorchetes):
    def __init__(self, ID):
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionDeCorchetesId(self)

# TIPO
class Tipo(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass

class TipoPrimitivo(Tipo):
    def __init__(self, tipos_primitivos):
        self.tipos_primitivos = tipos_primitivos
        
    def aceptar(self, visitante):
        return visitante.visitarTipoPrimitivo(self)
        
        
# TIPOS PRIMITIVOS
class TiposPrimitivos(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass

class TiposPrimitivosConcretos(TiposPrimitivos):
    def __init__(self, tipos_primitivos):
        self.tipos_primitivos = tipos_primitivos
        
    def aceptar(self, visitante):
        return visitante.visitarTiposPrimitivosConcretos(self)

# LLAMADA
class Llamada(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass

class CALLParams(Llamada):
    def __init__(self, ID, params_llamada):
        self.ID = ID
        self.params_llamada = params_llamada
        
    def aceptar(self, visitante):
        return visitante.visitarCALLParams(self)

class CALLPorDefecto(Llamada):
    def __init__(self, ID):
        self.ID = ID
        
    def aceptar(self, visitante):
        return visitante.visitarCALLPorDefecto(self)
    
# PARAMS LLAMADA
class ParamsCALL(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class ParamsCALLMulti(ParamsCALL):
    def __init__(self, expresion, params_llamada):
        self.expresion = expresion
        self.params_llamada = params_llamada
        
    def aceptar(self, visitante):
        return visitante.visitarParamsCALLMulti(self)

# PARAMS LLAMADA ÚNICA
class ParamsLlamadaUnica(ParamsCALL):
    def __init__(self, expresion):
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarParamsLlamadaUnica(self)

# EXPRESIÓN DE CLAVE
class ExpresionClaves(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class ExpresionClaveVacia(ExpresionClaves):
    def __init__(self):
        pass
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionClaveVacia(self)
    
class ExpresionClaveExpresion(ExpresionClaves):
    def __init__(self, expresion_clave):
        self.expresion_clave = expresion_clave
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionClaveExpresion(self)

# EXPRESIÓN CLAVE
class ExpresionClave(metaclass=ABCMeta):
    @abstractmethod
    def aceptar(self, visitante):
        pass
    
class ExpresionClaveMult(ExpresionClave):
    def __init__(self, expresion, expresion_clave):
        self.expresion = expresion
        self.expresion_clave = expresion_clave
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionClaveMult(self)
    
class ExpresionClaveUni(ExpresionClave):
    def __init__(self, expresion):
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionClaveUni(self)
    
class ExpresionClaveComa(ExpresionClave):
    def __init__(self, expresion):
        self.expresion = expresion
        
    def aceptar(self, visitante):
        return visitante.visitarExpresionClaveComa(self)