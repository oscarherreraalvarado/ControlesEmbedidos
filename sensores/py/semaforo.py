import RPi.GPIO as GPIO
import time

# Configuración de los pines GPIO
RED_PIN = 17    # Pin para el LED rojo
GREEN_PIN = 27  # Pin para el LED verde
ORANGE_PIN = 22 # Pin para el LED naranja

# Configuración inicial
GPIO.setmode(GPIO.BCM)  # Usar la numeración BCM
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(ORANGE_PIN, GPIO.OUT)

# Función para apagar todas las luces
def turn_off_all():
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(ORANGE_PIN, GPIO.LOW)

# Función para cambiar de estado las luces en secuencia
def cycle_lights():
    try:
        while True:
            # Encender LED rojo
            turn_off_all()
            print("Encendiendo LED rojo")
            GPIO.output(RED_PIN, GPIO.HIGH)
            time.sleep(2)  # Mantener encendido por 2 segundos

            # Encender LED verde
            turn_off_all()
            print("Encendiendo LED verde")
            GPIO.output(GREEN_PIN, GPIO.HIGH)
            time.sleep(2)

            # Encender LED naranja
            turn_off_all()
            print("Encendiendo LED naranja")
            GPIO.output(ORANGE_PIN, GPIO.HIGH)
            time.sleep(2)

    except KeyboardInterrupt:
        # Manejar la interrupción (Ctrl+C)
        print("\nPrograma detenido. Apagando todas las luces.")
        turn_off_all()
        GPIO.cleanup()

# Ejecutar el ciclo de luces
if __name__ == "__main__":
    print("Iniciando el ciclo de luces...")
    cycle_lights()