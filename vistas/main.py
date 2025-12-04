from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import os
import time
import subprocess
import re
import atexit

v0 = Tk()
v0.title("Control de Sensores")

#sudo pkill -f 'nombreDelProceso o  archivo'

#gcc saludo.c -o nombredelcompilado
#./nombredelcompilado

#python3 
# Al finalizar un &

DIRECTORIO_ESTADOS = "/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados"

# Obtener ancho y alto de la pantalla
ancho_pantalla = v0.winfo_screenwidth()
alto_pantalla = v0.winfo_screenheight()

# Definir tamanio de la ventana
ancho_ventana = 800
alto_ventana = 500

# Calculo de coordenadas para centrar la ventana
x = (ancho_pantalla - ancho_ventana) // 2
y = (alto_pantalla - alto_ventana) // 2

# Establecer geometría centrada
v0.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# Crear un Canvas y agregarlo como widget de fondo
canvas = Canvas(v0, width=ancho_ventana, height=alto_ventana)
canvas.pack(fill="both", expand=True)

# Variables de fuentes para texto
text1 = font.Font(family="Arial", size=18)
text2 = font.Font(family="Arial", size=12)
text3 = font.Font(family="Arial", size=100)

# Cargar la imagen de fondo
imagen_fondo = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/fondo-v0.png")  # Cambia la ruta a tu imagen

img_off = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/radiobutton-gris.png")
img_on = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/radiobutton-negro.png")

img_onluzverde = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/off-luzverde.png")
img_offluzverde = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/on-luzverde.png")

img_onluzamarilla = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/off-luzamarilla.png")
img_offluzamarilla = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/on-luzamarilla.png")

img_onluzroja = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/off-luzroja.png")
img_offluzroja = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/on-luzroja.png")

img_temporizador = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/temporizador.png")

estados = {"verde": 0, "amarillo": 0, "rojo": 0}

# Diccionario para almacenar los botones
botones = {}

# Crear frames y botones
config_luces = {
    "verde": {"frame": (390, 251), "on": img_onluzverde, "off": img_offluzverde, "gpio": 0},
    "amarillo": {"frame": (655, 251), "on": img_onluzamarilla, "off": img_offluzamarilla, "gpio": 3},
    "rojo": {"frame": (523, 368), "on": img_onluzroja, "off": img_offluzroja, "gpio": 2}
}

radiobuttons = {}

config_lenguaje = {
    "py": {"frame": (257, 36), "value": 1},
    "bash": {"frame": (400, 36), "value": 2},
    "c": {"frame": (542, 36), "value": 3},
    "asm": {"frame": (684, 36), "value": 4}
}

selected_value = IntVar()

lenguaje = 'bash'
extension = 'sh'

# ZONA DE FUNCIONES
def encender(color):
    os.system(f"sudo /home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/on-lucesita-{color}.sh")
    
def apagar(color):
    os.system(f"sudo /home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/off-lucesita-{color}.sh")

def actualizarhora(): 
    # Obtener la hora actual en formato "HH:MM:SS"
    hora_actual = time.strftime("%H:%M:%S")
    
    lbl_hora.config(text=hora_actual)
    
    v0.after(1000, actualizarhora)

def leer_estado(color):
    ruta = os.path.join(DIRECTORIO_ESTADOS, f"estado-{color}.txt")
    gpio = config_luces[color]["gpio"]
    os.system(f"sudo gpio read {gpio} > {ruta}")
    with open(ruta, "r") as pf:
        estado = pf.readline().strip()
        return int(estado)

def cambiar_estado(color):
    estado_actual = leer_estado(color)
    if estado_actual == 0:
        apagar(color)
    else:
        encender(color)
    actualizar_luz(color)

def actualizar_luz(color):
    estado = leer_estado(color)
    if estado == 1:
        botones[color]["on"].lift()
    else:
        botones[color]["off"].lift()

def leer_distancia():
    try:
        with open("/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-ultrasonico.txt", "r") as file:
            lines = file.readlines()
            if lines:
                # Leer la última línea
                return lines[-1].strip()  # Quitar los espacios y saltos de línea
            else:
                return "No data"
    except Exception as e:
        return f"Error: {e}"

def leer_movimiento():
    try:
        with open("/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-pir.txt", "r") as file:
            lines = file.readlines()
            if lines:
                # Leer la última línea
                return lines[-1].strip()  # Quitar los espacios y saltos de línea
            else:
                return "No data"
    except Exception as e:
        return f"Error: {e}"

def leer_temperatura():
    try:
        with open("/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-dht11.txt", "r") as file:
            lines = file.readlines()
            if lines:
                # Leer la última línea
                ultima_linea = lines[-1].strip()
                # Buscar la temperatura usando una expresión regular
                match = re.search(r"Temp: ([\d.]+)C", ultima_linea)
                if match:
                    temperatura = match.group(1)  # Obtener el valor de la temperatura
                    return f"{temperatura}C"
                else:
                    return "Temperatura no encontrada"
            else:
                return "No data"
    except Exception as e:
        return f"Error: {e}"

def leer_humedad():
    try:
        with open("/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-dht11.txt", "r") as file:
            lines = file.readlines()
            if lines:
                # Leer la última línea
                ultima_linea = lines[-1].strip()
                # Buscar la humedad usando una expresión regular
                match = re.search(r"Humedad: (\d+)%", ultima_linea)
                if match:
                    humedad = match.group(1)  # Obtener el valor de la humedad
                    return f"{humedad}%"
                else:
                    return "Humedad no encontrada"
            else:
                return "No data"
    except Exception as e:
        return f"Error: {e}"

def actualizar_todos():
    for color in config_luces.keys():
        actualizar_luz(color)

    distancia = leer_distancia()
    lbl_distancia.config(text=f"{distancia}")

    movimiento = leer_movimiento()
    lbl_movimiento.config(text=f"{movimiento}")

    temperatura = leer_temperatura()
    lbl_temperatura.config(text=f"Temperatura: {temperatura}")
    
    humedad = leer_humedad()
    lbl_humedad.config(text=f"Humedad: {humedad}")
    
    v0.after(1000, actualizar_todos)  # Actualiza cada segundo

def lenguajePython():
    print("cambiar a python")
    kill_sensor_processes()
    process1 = subprocess.Popen(['python3', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/py/sensor-ultrasonico.py'])  # Cambia 'script1.py' con tu archivo
    process2 = subprocess.Popen(['python3', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/py/sensor-pir.py'])  # Cambia 'script2.py' con tu archivo
    proceso3 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/sensor-dht11.sh'])
    #os.system('python /home/uth/Desktop/ProyectoFinalEmbebida/sensores/py/sensor-dht11.py')  # Cambia 'script3.py' con tu archivo

    #process1.wait()
    #process2.wait()
    #process3.wait()
    
    print("Los procesos se están ejecutando en lenguaje PYTHON.")

def on_closing():
    kill_sensor_processes()
    v0.destroy()

def lenguajeBash():
    print("cambiar a bash")
    kill_sensor_processes()
    process1 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/sensor-pir.sh'])  # Cambia 'script1.py' con tu archivo
    process2 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/sensor-ultrasonico.sh'])  # Cambia 'script2.py' con tu archivo
    process3 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/sensor-dht11.sh'])  # Cambia 'script3.py' con tu archivo

    print("Los procesos se están ejecutando en lenguaje BASH.")

def lenguajeC():
    print("cambiar a C")
    kill_sensor_processes()
    process1 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/c/sensor-pir'])  # Cambia 'script1.py' con tu archivo
    process2 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/c/sensor-ultrasonico'])  # Cambia 'script2.py' con tu archivo
    process3 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/sensor-dht11.sh'])
    print("Los procesos se están ejecutando en lenguaje C.")

def lenguajeASM():
    print("cambiar a ASM")
    kill_sensor_processes()
    process1 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/asm/sensor-pir'])  # Cambia 'script1.py' con tu archivo
    process2 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/asm/sensor-ultrasonico'])  # Cambia 'script2.py' con tu archivo
    process3 = subprocess.Popen(['sudo', '/home/uth/Desktop/ProyectoFinalEmbebida/sensores/asm/sensor-dht11'])
    print("Los procesos se están ejecutando en lenguaje ASM.")

def cronometro():
    imagen_fondo = PhotoImage(file="/home/uth/Desktop/ProyectoFinalEmbebida/img/fondo-v1.png")
    v1=Toplevel()
    v1.title("Conometro de Luces")
    ancho_pantalla = v1.winfo_screenwidth()
    alto_pantalla = v1.winfo_screenheight()

    # Definir tamanio de la ventana
    ancho_ventana = 600
    alto_ventana = 430

    # Calculo de coordenadas para centrar la ventana
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2

    # Establecer geometría centrada
    v1.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    canvas = Canvas(v1, width=ancho_ventana, height=alto_ventana)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, anchor=NW, image=imagen_fondo)

    global horarios
    horarios = {
        "horai": {"rojo": StringVar(), "amarillo": StringVar(), "verde": StringVar()},
        "minini": {"rojo": StringVar(), "amarillo": StringVar(), "verde": StringVar()},
        "horaf": {"rojo": StringVar(), "amarillo": StringVar(), "verde": StringVar()},
        "minf": {"rojo": StringVar(), "amarillo": StringVar(), "verde": StringVar()},
    }

    colores = ["rojo", "amarillo", "verde"]

    # Posicionamiento inicial
    y_offset = 105  # Posición inicial en el eje Y
    x_offset = 60  # Posición inicial en el eje X
    espacio_vertical = 80  # Espaciado vertical entre las líneas de cada campo
    espacio_horizontal = 185  # Espaciado horizontal entre los colores

    # Definimos las posiciones Y para cada tipo de campo
    y_horai = y_offset
    y_minini = y_offset + espacio_vertical
    y_horaf = y_offset + 2 * espacio_vertical
    y_minf = y_offset + 3 * espacio_vertical

    def validar_numero(entrada):
        return entrada.isdigit() or entrada == ""

    validacion_numero = v1.register(validar_numero)

    for i, color in enumerate(colores):
        x_pos = x_offset + i * espacio_horizontal

        Entry(v1, textvariable=horarios["horai"][color], width=10, font=("Arial", 13), highlightthickness=0, bd=0,
          validate="key", validatecommand=(validacion_numero, '%P')).place(x=x_pos, y=y_horai)

        Entry(v1, textvariable=horarios["minini"][color], width=10, font=("Arial", 13), highlightthickness=0, bd=0,
          validate="key", validatecommand=(validacion_numero, '%P')).place(x=x_pos, y=y_minini)

        Entry(v1, textvariable=horarios["horaf"][color], width=10, font=("Arial", 13), highlightthickness=0, bd=0,
          validate="key", validatecommand=(validacion_numero, '%P')).place(x=x_pos, y=y_horaf)

        Entry(v1, textvariable=horarios["minf"][color], width=10, font=("Arial", 13), highlightthickness=0, bd=0,
          validate="key", validatecommand=(validacion_numero, '%P')).place(x=x_pos, y=y_minf)
    
    boton_y = y_minf + 44
    for i, color in enumerate(colores):
        x_pos = (x_offset - 10) + i * espacio_horizontal
        Button(v1, text=f"Guardar {color.capitalize()}", font=("Arial", 13),bg="white",highlightthickness=0, bd=0, cursor="hand2", command=lambda c=color: save1(c)).place(
            x=x_pos, y=boton_y
        )

    v1.mainloop()

def save1(color):
    hi = str(horarios["horai"][color].get())
    mi = str(horarios["minini"][color].get())
    hf = str(horarios["horaf"][color].get())
    mf = str(horarios["minf"][color].get())
    
    tab = " "
    dia = "*"
    mes = "*"
    aa = "*"
    user = "root"
    path1 = f"/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/on-lucesita-{color}.sh"
    path2 = f"/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/off-lucesita-{color}.sh"

    cadena1 = f"{mi}{tab}{hi}{tab}{dia}{tab}{mes}{tab}{aa}{tab}{user}{tab}{path1}"
    cadena2 = f"{mf}{tab}{hf}{tab}{dia}{tab}{mes}{tab}{aa}{tab}{user}{tab}{path2}"

    # Permisos
    os.system(f"sudo chmod -R 777 /etc/cron.d/task1-{color}")
    os.system(f"sudo chmod -R 777 /etc/cron.d/task2-{color}")
    
    # Abrir archivo
    with open(f"/etc/cron.d/task1-{color}", "w") as pf1:
        pf1.write(cadena1 + "\n")

    with open(f"/etc/cron.d/task2-{color}", "w") as pf2:
        pf2.write(cadena2 + "\n")

    # Tiempo estratégico
    time.sleep(0.5)
    
    os.system(f"sudo chmod -R 755 /etc/cron.d/task1-{color}")
    os.system(f"sudo chmod -R 755 /etc/cron.d/task2-{color}")

    # Reiniciar servicios
    os.system("sudo /./etc/init.d/cron restart")

    # Mostrar mensaje de éxito
    exito = "Tiempo Grabado con Éxito."
    dospuntos = ":"
    mensajecompleto = (
        f"{exito}{tab}Enciende luz {color.upper()} a las: {hi}{dospuntos}{mi}{tab}"
        f"Apaga luz {color.upper()} a las: {hf}{dospuntos}{mf}"
    )
    messagebox.showinfo("INFO", message=mensajecompleto)

def kill_sensor_processes():
    # Ejecutar el comando 'sudo pkill' para matar todos los procesos llamados 'sensor-*'
    try:
        subprocess.run(['sudo', 'pkill', '-f', 'sensor-'], check=True)
        print("Se han terminado los procesos que comienzan con 'sensor-'")
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar matar los procesos: {e}")

# Evaluación del radiobutton
def EvaluarRadiobutton():
    r = selected_value.get()  # Obtener el valor de la variable asociada a los radiobuttons
    if r == 1:
        os.system("sudo /./home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/matar_todos-py.sh")
        lenguajePython()
    elif r == 2:
        os.system("sudo /./home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/matar_todos-sh.sh")
        lenguajeBash()
    elif r == 3:
        os.system("sudo /./home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/matar_todos-c.sh")
        lenguajeC()
    elif r == 4: #bash
        os.system("sudo /./home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/matar_todos-asm.sh")
        lenguajeASM()

for lenguaje, config in config_lenguaje.items():
    x, y = config["frame"]

    # Crear frame
    frame = Frame(v0, bg="white", bd=0, width=24, height=24, cursor="hand2")
    frame.place(x=x, y=y)

    # Crear radiobuttons
    radio_btn = Radiobutton(frame, image=img_off, selectimage=img_on, indicatoron=False,variable=selected_value, value=config["value"], bg="white", bd=0, command=EvaluarRadiobutton)
    radio_btn.image = img_off
    radio_btn.selectimage = img_on
    radio_btn.pack(fill="both", expand=True)  # Empaquetar el botón en el frame
    
    # Guardar botones en el diccionario
    radiobuttons[lenguaje] = radio_btn
    
selected_value.set(1)

canvas.create_image(0, 0, anchor=NW, image=imagen_fondo)

frame = Frame(v0, bg="#545454", width=51, height=51, cursor="hand2")
frame.place(x=554,y=281)

btn_cronometro=Button(frame,image=img_temporizador, bg="#545454", bd=0, width=51, height=51, command=cronometro)
btn_cronometro.place(x=-1,y=-1)

lbl_hora=Label(v0,text="",font=("Arial",18,"bold"),bg="#77b1ff",fg="#2c3179")
lbl_hora.place(x=390,y=460)

lbl_distancia = Label(v0, text="Distancia", font=("Arial", 18, "bold"), bg="white", fg="#2c3179")
lbl_distancia.place(x=120, y=420)

lbl_temperatura = Label(v0, text="Temperatura", font=("Arial", 18, "bold"), bg="white", fg="#2c3179")
lbl_temperatura.place(x=120, y=290)

lbl_humedad = Label(v0, text="Humedad", font=("Arial", 18, "bold"), bg="white", fg="#2c3179")
lbl_humedad.place(x=120, y=170)

lbl_movimiento = Label(v0, text="Movimiento detectado", font=("Arial", 18, "bold"), bg="white", fg="#2c3179")
lbl_movimiento.place(x=400, y=170)

for color, config in config_luces.items():
    x, y = config["frame"]

    # Crear frame
    frame = Frame(v0, bg="white", bd=0, width=114, height=114, cursor="hand2")
    frame.place(x=x, y=y)

    # Crear botones superpuestos
    btn_encender = Button(frame, image=config["on"], bd=0, bg="white", width=114, height=114, command=lambda c=color: cambiar_estado(c))
    btn_apagar = Button(frame, image=config["off"], bd=0, bg="white", width=114, height=114, command=lambda c=color: cambiar_estado(c))
    
    btn_encender.place(x=0, y=0)
    btn_apagar.place(x=0, y=0)
    
    botones[color] = {"on": btn_encender, "off": btn_apagar}
    actualizar_luz(color)

EvaluarRadiobutton()
actualizarhora()
actualizar_todos()

v0.protocol("WM_DELETE_WINDOW", on_closing)

#atexit.register(kill_sensor_processes)

v0.mainloop()
