import flet as ft
from layout.mainLayout import mainLayout
from layout.sideMenu import sideMenu

def main(page: ft.Page):
    page.fonts = {
        "Poppins": "fonts/Poppins-Regular.ttf",
        "Poppins-Bold": "fonts/Poppins-Bold.ttf",
        "Poppins-SemiBold": "fonts/Poppins-SemiBold.ttf",
    }
    page.title = "Compilador // Alejandro Chávez & José Santana"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.maximizable = False
    page.window.width = 1300
    page.window.height = 800
    page.add(
        ft.Row(
            expand=True,
            controls=[
                mainLayout(page),
                sideMenu(page)
                ]
            )
        )

ft.app(main, assets_dir="assets")
