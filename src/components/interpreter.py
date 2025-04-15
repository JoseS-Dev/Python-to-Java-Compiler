import flet as ft

def interpreterOutput(boolean: bool):
    return ft.TextField(
        multiline=True,
        max_lines=999999,
        min_lines=24,
        width=550,
        border_color='#292E41',
        border_width=2,
        expand=True,
        read_only= True,
        label="Semantic Analysis Output",
        visible=boolean
    )