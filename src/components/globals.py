import flet as ft

def title(texto):
    return ft.Text(
        texto,
        size=28,
        font_family= "Poppins-Bold",
        weight=ft.FontWeight.BOLD
        )

def textpad(page: ft.Page,function):
    return ft.TextField(
        multiline=True,
        max_lines=9999,
        min_lines=24,
        label="Escribe tu código aquí",
        width=550,
        border_color='#292E41',
        border_width=2,
        height=600,
        on_change=function
    )

def button(page: ft.Page,function,Buttontext="",icono=None, disabled=False):
    return ft.Button(
        text=Buttontext,
        width=100,
        height=40,
        on_click=function,
        icon=icono,
        disabled=disabled
    )

TITLE = title("Analizador Léxico")