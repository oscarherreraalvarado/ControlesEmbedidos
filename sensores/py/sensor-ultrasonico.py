import time as Time
import RPi.GPIO as GPIO  # Usar la biblioteca RPi.GPIO

TRIG = 23
ECHO = 24

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def medir_distancia():
    GPIO.output(TRIG, GPIO.HIGH)
    Time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == GPIO.LOW:
        inicio = Time.time()

    while GPIO.input(ECHO) == GPIO.HIGH:
        fin = Time.time()

    duracion = fin - inicio
    distancia = duracion * 17150
    distancia = round(distancia, 2)
    return distancia

def actualizar_distancia():
    try:
        while True:
            
            distancia = medir_distancia()

            archivo = "/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-ultrasonico.txt"
            with open(archivo, "w") as f:
                f.write(f"Distancia: {distancia} cm\n")
    
            Time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

actualizar_distancia()
