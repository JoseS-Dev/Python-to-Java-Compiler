import flet as ft
from components.lexer_components import mainTitle, textarea, table, button

def lexer_page():
    return ft.Column(
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            mainTitle(),
            ft.Row(
                expand=True,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    textarea(),
                    ft.ListView(
                        controls=[
                            table()
                        ],
                        width=600,
                        height=600,
                        spacing=0,
                        padding=0,
                    ),
                ],
                scroll= ft.ScrollMode.AUTO,
            ),
            button()
        ]
    )