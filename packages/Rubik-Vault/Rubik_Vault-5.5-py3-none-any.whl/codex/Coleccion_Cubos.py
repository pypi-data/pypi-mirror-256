from tkinter import *
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def Coleccion(carpeta, estados, name):
    def agregar():
        root.destroy()
        from .Seleccion_Cubos import Seleccion
        
        Seleccion(name, estados)

    def inicio():
        from .Inicio_de_sesion import Login
        root.destroy()
        Login()
    root = Tk()
    root.geometry('560x500+10+10')
    root.iconbitmap(resource_path('codex/res/icono.ico'))
    
    Label(root, text='MI COLECCION', font=('STENCIL', 40), fg='white', bg='black').pack(fill='x', pady=10)

    frame = Frame(root)
    frame.pack()

    imagenes=[]

    cont = -1
    row = 0
    columna = 0
    for i,j in enumerate(carpeta.iterdir()):
        if estados[i]:
            cont += 1
            imagenes.append(PhotoImage(file=f'{carpeta}/{j.name}'))
            Label(frame, image=imagenes[cont]).grid(row=row, column=columna, padx=15)
            Label(frame, text=j.stem).grid(row=row+1, column=columna)
            columna += 1

            if (cont+5) % 4 == 0:
                row += 2
                columna = 0

    frame2 = Frame(root)
    frame2.pack(side="bottom", anchor="se")
    Button(frame2, text='Inicio', font=('STENCIL', 15), bg='black', fg='white',command=inicio).grid(row=0, column=0, padx=10)
    Button(frame2, text='Agregar', font=('STENCIL', 15), bg='Dark Green', fg='white',command=agregar).grid(row=0, column=1, padx=10)

    root.mainloop()