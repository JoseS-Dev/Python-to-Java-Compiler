import flet as ft

def textPadClear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[0].value = ""
    page.controls[0].controls[0].controls[1].controls[0].update()

def clear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[1].controls[0].rows.clear()
    page.controls[0].controls[0].controls[1].controls[1].controls[0].update()

def abrir_archivo(e: ft.FilePickerResultEvent, page: ft.Page):
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