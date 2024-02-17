from pathlib import Path
from tkinter import *
from .Coleccion_Cubos import Coleccion, resource_path
import ast


def Seleccion(name, estados):
    def mostrar2(posicion):
        if estados[posicion]:
            estados[posicion] = 0
            cubos[posicion].config(bg='white', bd=0)
        else:
            estados[posicion] = 1
            cubos[posicion].config(bg='green', bd=5)

    def coleccion():
        with open(resource_path('codex/res/usuarios.txt'), 'r+') as file:
            lines = [ast.literal_eval(line) for line in file]

            for line in lines:
                if name in line:
                    line['Estado'] = estados

            file.seek(0)
            file.truncate()
            file.writelines([str(line) + '\n' for line in lines])

        root.destroy()
        Coleccion(carpeta, estados, name)
        

    root = Tk()
    root.geometry('560x550+10+10')
    root.iconbitmap(resource_path('codex/res/icono.ico'))
    if name == 'rubik':
        Label(root, text=f'BIENVENIDO ADMIN', font=('bauhaus 93', 40, 'italic'), fg='red').pack(expand=True, padx=10)
    else:
        Label(root, text=f'BIENVENIDO {name.upper()}', font=('bauhaus 93', 40, 'italic'), fg='red').pack(expand=True, padx=10)
    fr2 = Frame(root)
    fr2.pack(fill='x')
    Label(fr2, text=f'Que cubo deseas: ', font=('impact', 20), fg='black').pack(side=LEFT, pady=5)

    carpeta = Path(resource_path('codex/res/cubos'))
    cantidad_archivos = len(list(carpeta.glob('*')))

    #file.name  Nombre con Extension
    #file.stem  Nombre
    #file.suffix Extension

    frame = Frame(root)
    frame.pack()
    
    imagenes_cubos = [PhotoImage(file=f'{carpeta}/{file.name}') for file in carpeta.iterdir()]
    cubos = [Button(frame, image=imagenes_cubos[posicion], command=lambda pos=posicion: mostrar2(pos)) 
                                for posicion in range(cantidad_archivos)] # El problema al usar lambda dentro de un bucle es que solo captura el ultimo valor de la variable

    row = 0
    columna = 0
    for i,j in enumerate(carpeta.iterdir()):
        cubos[i].grid(row=row, column=columna, padx=15)
        Label(frame, text=j.stem).grid(row=row+1, column=columna)

        columna += 1
        if (i+5) % 4 == 0: #Para que hayan solo 4 imagenes en cada fila
            row += 2
            columna = 0
            
    Button(root, text='Aceptar', font=('bauhaus 93', 20), bg='blue', fg='white', command=coleccion).pack()

    for posicion in range(len(estados)):
        if estados[posicion]:
                cubos[posicion].config(bg='green', bd=5)
        else:
            cubos[posicion].config(bg='white', bd=0)
            

    root.mainloop()