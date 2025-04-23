import flet as ft

def table():
    return ft.DataTable(
        columns = [
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Valor")),
            ft.DataColumn(ft.Text("Posición")),
        ],
        rows=[ft.DataRow(cells=[ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text(""))]),],
        border=ft.border.all(2, '#292E41'),
        width=550,
        height=100000,
    )

def listview(boolean: bool):
    return(ft.ListView(
        controls=[
            table()
            ],
            width=550,
            height=600,
            spacing=0,
            padding=0,
            visible=boolean,
            )
    )