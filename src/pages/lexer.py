import flet as ft
from components.lexer import mainTitle, textarea, table, button
from functions.lexer import proceso_lexer, abrir_archivo

def lexer_page(page: ft.Page):
    file_picker = ft.FilePicker(on_result=lambda e: abrir_archivo(e, page))
    page.overlay.append(file_picker)
    return ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            mainTitle(),
            ft.Row(
                expand=True,
                alignment = ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    textarea(),
                    ft.ListView(
                        controls=[
                            table()
                        ],
                        width=550,
                        height=600,
                        spacing=0,
                        padding=0,
                    ),
                ],
                scroll= ft.ScrollMode.AUTO,
            ),
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                    button("Ejecutar", proceso_lexer),
                    button("Abrir Doc",lambda _: file_picker.pick_files(allowed_extensions=["java"],allow_multiple=False))
                ]
            )
        ]
    )