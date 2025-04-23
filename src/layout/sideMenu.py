import flet as ft
from components.globals import button
from functions.general import changeSection

def sideMenu(page: ft.Page):
    return(
        ft.Column(
            width=100,
            height = 600,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls=[
                button(page,changeSection,"Léxico"),
                button(page,changeSection,"Sintáctico"),
                button(page,changeSection,"Semántico"),
                ft.Text("-",size=20, font_family="Poppins-Bold"),
                button(page,changeSection,"Ejecución"),
            ],
            alignment= ft.MainAxisAlignment.CENTER
        )
    )