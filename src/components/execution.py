import flet as ft

def codeOutput(boolean: bool):
    return ft.TextField(
        multiline=True,
        max_lines=999999,
        min_lines=24,
        width=550,
        border_color='#292E41',
        border_width=2,
        expand=True,
        read_only= True,
        label="Code",
        visible=boolean,
        height=300,
    )

def executionOutput(boolean: bool):
    return ft.TextField(
        multiline=True,
        max_lines=999999,
        min_lines=24,
        width=550,
        border_color='#292E41',
        border_width=2,
        expand=True,
        read_only= True,
        label="Output",
        visible=boolean,
        height=300,
    )

def executionLayout(boolean: bool):
    return ft.Column(
        controls=[
            codeOutput(True),
            executionOutput(True),
        ],
        width=550,
        height=600,
        alignment= ft.MainAxisAlignment.START,
        visible=boolean
    )