import flet as ft
from functions.parser import proceso_parser
from functions.lexer import proceso_lexer
from components.globals import TITLE

def textPadClear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[0].value = ""
    page.controls[0].controls[0].controls[1].controls[0].update()

def clear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[1].controls[0].rows.clear()
    page.controls[0].controls[0].controls[1].controls[1].controls[0].update()
    page.controls[0].controls[0].controls[1].controls[2].controls[0].value = ""
    page.controls[0].controls[0].controls[1].controls[2].controls[1].value = ""
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
    elif textButton == "Sintáctico":
        TITLE.value = "Analizador Sintáctico"
        TITLE.update()
        e.control.parent.parent.controls[0].controls[1].controls[1].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[2].visible = True
        e.control.parent.parent.controls[0].controls[1].controls[3].visible = False
    elif textButton == "Semántico":
        TITLE.value = "Analizador Semántico"
        TITLE.update()
        e.control.parent.parent.controls[0].controls[1].controls[1].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[2].visible = False
        e.control.parent.parent.controls[0].controls[1].controls[3].visible = True
    else:
        return
    e.control.parent.parent.controls[0].controls[1].update()

def ejecucion(e):
    proceso_lexer(e)
    proceso_parser(e)