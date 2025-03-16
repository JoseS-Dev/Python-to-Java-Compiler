import flet as ft
from components.globals import button

def sideMenu(page: ft.Page):
    return(
        ft.Column(
            width=100,
            height = 600,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                button(page,"Léxico",lambda _: print("Hola")),
                button(page,"Sintáctico",lambda _: print("XD")),
                button(page,"Semántico",lambda _: print("Hola"))
            ],
            alignment= ft.MainAxisAlignment.CENTER
        )
    )