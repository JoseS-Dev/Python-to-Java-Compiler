import flet as ft

def button(page: ft.Page,Buttontext,function):
    return(
        ft.Button(
            text=Buttontext,   
            width=100,
            height=40,
            on_click= function
        )
    )

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
