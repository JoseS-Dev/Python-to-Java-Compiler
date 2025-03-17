import flet as ft
from components.globals import button

def sideMenu(page: ft.Page):
    return(
        ft.Column(
            width=100,
            height = 600,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                button(page,lambda _: print("Hola"),"Léxico"),
                button(page,lambda _: print("XD"),"Sintáctico"),
                button(page,lambda _: print("Hola"),"Semántico")
            ],
            alignment= ft.MainAxisAlignment.CENTER
        )
    )