import flet as ft
from components.lexer import listview
from components.parser import parserLayout
from components.interpreter import interpreterOutput
from components.execution import executionLayout
from components.globals import textpad, button, TITLE
from functions.general import clear, textPadClear, abrir_archivo, ejecucion

def mainLayout(page: ft.Page):
    file_picker = ft.FilePicker(on_result=lambda e: abrir_archivo(e, page))
    page.overlay.append(file_picker)
    return ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            TITLE,
            ft.Row(
                expand=True,
                alignment = ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    textpad(page, lambda _: clear(page)),
                    listview(True),
                    parserLayout(False),
                    interpreterOutput(False),
                    executionLayout(False),
                ],
                scroll= ft.ScrollMode.AUTO,
                height=600
            ),
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                    button(page,lambda _: file_picker.pick_files(allowed_extensions=["java"],allow_multiple=False),"Subir",ft.icons.UPLOAD),
                    button(page, lambda _: (textPadClear(page),clear(page)),"Borrar", ft.icons.DELETE),
                    button(page, lambda _: (ejecucion(_,page)),"Ejecutar"),
                    ]
            )
        ],
    )