import flet as ft

def stateOutput():
    return ft.TextField(
        width = 550,
        border_color='#292E41',
        border_width=2,
        label="Output",
        read_only=True,
    )

def textarea():
    return ft.TextField(
        multiline=True,
        max_lines=999999,
        min_lines=24,
        width=550,
        border_color='#292E41',
        border_width=2,
        expand=True,
        read_only= True,
        label="Debug Output"
    )

def parserLayout(boolean: bool):
    return ft.Column(
        controls=[
            stateOutput(),
            textarea(),
        ],
        width=550,
        height=600,
        alignment= ft.MainAxisAlignment.START,
        visible=boolean
    )