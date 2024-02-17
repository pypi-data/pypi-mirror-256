from tkinter import messagebox
from tkinter import *
from pathlib import Path
import ast
from .Seleccion_Cubos import Seleccion, resource_path


def Login():
    def IN(e): #Usuario
        user.delete(0,END)

    def OUT(e):
        if not user.get():
            user.insert(0, 'Usuario')

    def ingreso():
        name = user.get() 
        passw = passw_entry.get()
        label_registrar.config(text='', fg='red', font=('stika small', 1))

        with open(resource_path('codex/res/usuarios.txt'), 'r') as file:
            numero_lineas = len(file.readlines())
            file.seek(0)
            lines = [ast.literal_eval(file.readline()) for i in range(numero_lineas)]

            for i in range(numero_lineas):
                if name in lines[i].keys():
                    passtwt = lines[i][name]
                    estados = lines[i]['Estado'] #Pieza clave para poner y quitar imagenes
                    
        try:
            if passw == passtwt:
                root.destroy()
                Seleccion(name, estados)
            else:
                messagebox.showerror('Error', 'Contraseña incorrecta!')
        except UnboundLocalError:
            messagebox.showerror('Error', 'Usuario o Contraseña incorrectos!')
    
    global registrando
    registrando = False
    def registrar():
        global registrando
        if registrando:
            registrando = False
            with open(resource_path('codex/res/usuarios.txt'), 'r+') as file:
                numero_lineas = len(file.readlines())
                file.seek(0) #Puntero regrese al inicio
                lines = [ast.literal_eval(file.readline()) for i in range(numero_lineas)]

                name = user.get().strip()
                passw = passw_entry.get().strip()
                exist = False

                if name=='' or passw.strip()=='':
                    messagebox.showerror('Error', 'COMPLETE LOS CAMPOS!')
                else: 
                    for i in range(numero_lineas):
                        if name in lines[i].keys():
                            exist = True
                            label_registrar.config(text='Ingrese usuario nuevo', fg='red', font=('stika small', 30))
                            messagebox.showerror('Error', 'USUARIO YA EXISTE!')
                            break
                    if not exist:
                        file.write(f"{{'{name}':'{passw}', 'Estado': {[0]*cantidad_archivos}}}\n")
                        label_registrar.config(text='Registrado', fg='green', font=('stika small', 30))
        else:
            registrando = True
            label_registrar.config(text='Registrando...', fg='red', font=('stika small', 30))

            user.delete(0,END)
            user.insert(0,'Usuario')

            passw_entry.delete(0,END)
            passw_entry.insert(0,'Password')
            passw_entry.config(show='')
                    

    root = Tk()
    root.title('Inicio de sesion')
    root.geometry('500x430+10+10')
    root.iconbitmap(resource_path('codex/res/icono.ico'))
    carpeta = Path(resource_path('codex/res/cubos'))
    cantidad_archivos = len(list(carpeta.glob('*')))

    Label(root, text='INICIE SESION', fg='dark blue', font=('showcard gothic', 40)).pack()

    user = Entry(root, text='Usuario', width= 30, font=('Arial', 40))
    user.insert(0, 'Usuario')
    user.bind('<FocusIn>', IN)
    user.bind('<FocusOut>', OUT)
    user.pack()

    Frame(root, bg='black', height=10).place(y=130, relwidth=1) #Fill no existe en Place, asi que se usa Relwidth
    Frame(root).pack(pady=20) #Separador

    def IN(e): #Password
        if registrando:
            passw_entry.delete(0,END)
            passw_entry.config(show='')
        else:
            passw_entry.delete(0,END)
            passw_entry.config(show='*')

    def OUT(e):
        if not passw_entry.get():
            passw_entry.insert(0, 'Password')
            passw_entry.config(show='')
        
    passw_entry = Entry(root, width=30, font=('Arial', 40))
    passw_entry.insert(0, 'Password')
    passw_entry.bind('<FocusIn>', IN) #Evento de click/tabulacion en el widget
    passw_entry.bind('<FocusOut>', OUT)   #Evento de que se salio del widget
    passw_entry.pack()

    Frame(root, bg='black', height=10).place(y=235, relwidth=1) 
    Frame(root).pack(pady=30) #Separador

    frame_label_registrar = Frame(root)
    frame_label_registrar.pack(fill='x')
    
    label_registrar = Label(root, font=('stika small', 1))
    label_registrar.place(y=245)

    ingresar = Button(root, border=3, text='Ingresar', command=ingreso, font=('Arial', 30))
    ingresar.pack()

    frame = Frame(root)
    frame.pack()
    Label(frame, text='No tiene cuenta?', font=('Arial', 20)).grid(row=0, column=0)
    registro = Button(frame, text='Registrarse', fg='blue', font=('Arial', 20), border=0, command=registrar)
    registro.grid(row=0, column=1)

    root.mainloop()

if __name__ == "__main__":
    Login()