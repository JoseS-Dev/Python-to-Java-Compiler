import functions.sintaxis as SA
import matplotlib.pyplot as plt
import types

def default_draw(self, ax, x, y, dx, dy):
    ax.text(x, y, self.__class__.__name__, bbox=dict(facecolor='white', edgecolor='black'), ha='center')

def agregar_draw_si_falta():
    for name in dir(SA):
        obj = getattr(SA, name)
        if isinstance(obj, type) and hasattr(obj, 'accept'):
            if not hasattr(obj, 'draw'):
                setattr(obj, 'draw', default_draw)
                print(f"✔️ draw() añadido a {name}")

# Ejecutar al cargar
agregar_draw_si_falta()
