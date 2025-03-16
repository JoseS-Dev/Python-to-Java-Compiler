import flet as ft

def mainTitle():
    return ft.Text(
        "Analizador Léxico",
        size=28,
        font_family= "Poppins-Bold",
        weight=ft.FontWeight.BOLD
        )

def textarea():
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

def table():
    return ft.DataTable(
        columns = [
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Valor")),
        ],
        rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(""))]),],
        border=ft.border.all(2, '#292E41'),
        width=550,
        height=100000,
    )

def button(Buttontext,function):
    return ft.Button(
        text=Buttontext,
        width=100,
        height=40,
        on_click=function
    )