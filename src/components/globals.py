import flet as ft

def title(texto):
    return ft.Text(
        texto,
        size=28,
        font_family= "Poppins-Bold",
        weight=ft.FontWeight.BOLD
        )

def textpad():
    return ft.TextField(
        multiline=True,
        max_lines=9999,
        min_lines=23,
        height=600,
        label="Escribe tu código aquí",
        width=550,
        border_color='#292E41',
        border_width=2,
    )

def button(page: ft.Page,Buttontext,function):
    return ft.Button(
        text=Buttontext,
        width=100,
        height=40,
        on_click=function
    )

TEXT_PAD = textpad()
TITLE = title("Analizador Léxico")