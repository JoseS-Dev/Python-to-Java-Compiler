import flet as ft
from components.lexer import listview
from components.parser import parserLayout
from components.globals import textpad, button, TITLE
from functions.lexer import proceso_lexer, abrir_archivo
from functions.general import clear, textPadClear

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
                    textpad(page),
                    listview(True),
                    parserLayout(False),
                ],
                scroll= ft.ScrollMode.AUTO,
                height=600
            ),
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                    button(page,lambda _: file_picker.pick_files(allowed_extensions=["java"],allow_multiple=False),"Subir",ft.icons.UPLOAD),
                    button(page, lambda _: (textPadClear(page),clear(page)),"Borrar", ft.icons.DELETE),
                    button(page, proceso_lexer,"Ejecutar"),
                    ]
            )
        ],
    )