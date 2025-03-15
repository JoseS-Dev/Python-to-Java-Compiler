import flet as ft
from pages.lexer_page import lexer_page

def main(page: ft.Page):
    page.fonts = {
        "Poppins": "fonts/Poppins-Regular.ttf",
        "Poppins-Bold": "fonts/Poppins-Bold.ttf",
        "Poppins-SemiBold": "fonts/Poppins-SemiBold.ttf",
    }
    page.title = "Compilador"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.maximizable = False
    page.window.width = 1024,
    page.window.height = 768,
    page.add(lexer_page(page))

ft.app(main, assets_dir="assets")
