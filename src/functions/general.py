import flet as ft

def textPadClear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[0].value = ""
    page.controls[0].controls[0].controls[1].controls[0].update()

def clear(page: ft.Page):
    page.controls[0].controls[0].controls[1].controls[1].controls[0].rows.clear()
    page.controls[0].controls[0].controls[1].controls[1].controls[0].update()