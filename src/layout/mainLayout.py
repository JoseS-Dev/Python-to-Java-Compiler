import flet as ft
from components.lexer import listview
from components.globals import TEXT_PAD, button, TITLE
from functions.lexer import proceso_lexer, abrir_archivo

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
                    TEXT_PAD,
                    listview(),
                ],
                scroll= ft.ScrollMode.AUTO,
            ),
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                    button(page,"Ejecutar", proceso_lexer),
                    button(page,"Abrir Doc",lambda _: file_picker.pick_files(allowed_extensions=["java"],allow_multiple=False))
                ]
            )
        ]
    )