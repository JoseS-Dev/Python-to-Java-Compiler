import flet as ft
from functions.general import clear

def title(texto):
    return ft.Text(
        texto,
        size=28,
        font_family= "Poppins-Bold",
        weight=ft.FontWeight.BOLD
        )

def textpad(page: ft.Page):
    return ft.TextField(
        multiline=True,
        max_lines=9999,
        min_lines=24,
        label="Escribe tu código aquí",
        width=550,
        border_color='#292E41',
        border_width=2,
        height=600,
        on_change=lambda _: clear(page)
    )

def button(page: ft.Page,function,Buttontext="",icono=None):
    return ft.Button(
        text=Buttontext,
        width=100,
        height=40,
        on_click=function,
        icon=icono
    )

TITLE = title("Analizador Léxico")