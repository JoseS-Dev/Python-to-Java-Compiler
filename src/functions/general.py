import flet as ft
from functions.lexer import proceso_lexer
from functions.parser import Parser
from functions.SemanticAnalyzer import SemanticAnalyzer
from functions.codeGen2 import PythonCodeGenerator
from components.globals import TITLE
import sys
import io
import re
from contextlib import redirect_stdout, redirect_stderr

def textPadClear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[0].value = ""
    page.controls[0].controls[0].controls[1].controls[0].update()

def clear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[1].controls[0].rows.clear()
    page.controls[0].controls[0].controls[1].controls[1].controls[0].update()
    page.controls[0].controls[0].controls[1].controls[2].controls[0].value = ""
    page.controls[0].controls[0].controls[1].controls[2].controls[1].value = ""
    page.controls[0].controls[0].controls[1].controls[3].value = ""
    page.controls[0].controls[0].controls[1].controls[4].controls[0].value = ""
    page.controls[0].controls[0].controls[1].controls[4].controls[1].value = ""
    page.controls[0].controls[0].controls[1].update()

def abrir_archivo(e: ft.FilePickerResultEvent, page: ft.Page):
    clear(page)
    if e.files:
        selected_file = e.files[0]
        file_path = selected_file.path
        if file_path.endswith(".java"):
            with open(file_path, "r") as file:
                content = file.read()
        else:
            content = "Por favor, selecciona un archivo .java"
    else:
        content= "Ningún archivo seleccionado"
    page.controls[0].controls[0].controls[1].controls[0].value = content
    page.controls[0].controls[0].controls[1].controls[0].update()

def changeSection(e):
    textButton = str(e.control.text)
    if textButton == "Léxico":
        TITLE.value = "Analizador Léxico"
        TITLE.update()
        e.control.parent.parent.controls[0].controls[1].controls[1].visible = True
        e.control.parent.parent.controls[0].controls[1].controls[2].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[3].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[4].visible = False
        
    elif textButton == "Sintáctico":
        TITLE.value = "Analizador Sintáctico"
        TITLE.update()
        e.control.parent.parent.controls[0].controls[1].controls[1].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[2].visible = True
        e.control.parent.parent.controls[0].controls[1].controls[3].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[4].visible = False
    elif textButton == "Semántico":
        TITLE.value = "Analizador Semántico"
        TITLE.update()
        e.control.parent.parent.controls[0].controls[1].controls[1].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[2].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[3].visible = True
        e.control.parent.parent.controls[0].controls[1].controls[4].visible = False
    elif textButton == "Ejecución":
        TITLE.value = "Ejecución"
        TITLE.update()
        e.control.parent.parent.controls[0].controls[1].controls[1].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[2].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[3].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[4].visible = True
    else:
        return
    e.control.parent.parent.controls[0].controls[1].update()

import sys
import io
import inspect
from contextlib import redirect_stdout, redirect_stderr

def ejecutar_codigo_python(codigo: str) -> str:
    salida_stdout = io.StringIO()
    salida_stderr = io.StringIO()

    try:
        with redirect_stdout(salida_stdout), redirect_stderr(salida_stderr):
            # Ejecutamos el código para definir las clases
            exec_globals = {}
            exec(codigo, exec_globals)
            
            # Buscamos todas las clases definidas
            for name, obj in exec_globals.items():
                if isinstance(obj, type):
                    instance = obj()
                    
                    # Ejecutamos todos los métodos que parecen ser "main" o similares
                    for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                        if not method_name.startswith('_'):  # Ignoramos métodos privados
                            try:
                                # Intentamos llamar al método de diferentes formas
                                try:
                                    method()  # Intenta como estático
                                except TypeError:
                                    try:
                                        method(instance)  # Intenta como método de instancia
                                    except TypeError:
                                        try:
                                            method(instance, None)  # Intenta con parámetro
                                        except TypeError:
                                            pass
                                        
                            except Exception as e:
                                salida_stderr.write(f"Error ejecutando {method_name}: {str(e)}\n")
    
    except Exception as e:
        salida_stderr.write(f"Error general: {str(e)}\n")

    # Procesamos la salida
    stdout_str = salida_stdout.getvalue()
    stderr_str = salida_stderr.getvalue()
    
    salida_combinada = ""
    if stdout_str:
        salida_combinada += stdout_str
    if stderr_str:
        if salida_combinada: salida_combinada += "\n"
        salida_combinada += stderr_str
    
    return salida_combinada.strip()

def ejecucion(e, page: ft.Page):
    #Lexer
    tokens = proceso_lexer(e)

    #Parser
    if tokens:
        try:
            parser = Parser(tokens)
            ast = parser.parse()
            if parser.salida == "":
                e.control.parent.parent.controls[1].controls[2].controls[0].value = "Análisis sintáctico exitoso."
            else:
                e.control.parent.parent.controls[1].controls[2].controls[0].value = parser.salida
            e.control.parent.parent.controls[1].controls[2].controls[1].value = parser.salida2
            e.control.parent.parent.controls[1].controls[2].update()
        except Exception as ex:
            e.control.parent.parent.controls[1].controls[2].controls[0].value = "Error de análisis sintáctico."
            e.control.parent.parent.controls[1].controls[2].controls[1].value = ""
            e.control.parent.parent.controls[1].controls[2].update()
    
    #Semantic Analyzer
    semantic = SemanticAnalyzer()
    semantic.analyze(ast)
    semantic_errors = f"Se encontraron {len(semantic.get_errors())} errores semánticos"
    e.control.parent.parent.controls[1].controls[3].value = semantic_errors
    e.control.parent.parent.controls[1].controls[3].update()

    #Execution
    codeGenerator = PythonCodeGenerator()
    if isinstance(ast, list):
        for nodo in ast:
            nodo.accept(codeGenerator)
    else:
        ast.accept(codeGenerator)
    generated = codeGenerator.generate(None)  # Retorna el código generado
    e.control.parent.parent.controls[1].controls[4].controls[0].value = generated
    print(f"\n{ejecutar_codigo_python(generated) }\n")
    print(generated)
    e.control.parent.parent.controls[1].controls[4].controls[1].value = ejecutar_codigo_python(generated)       
    e.control.parent.parent.controls[1].controls[4].update()

    #Graph
    parser.ast.graficar_mpl()
    

