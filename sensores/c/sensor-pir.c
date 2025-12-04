#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

int main() {
    // Configuración inicial del pin GPIO 12 como entrada
    if (wiringPiSetupGpio() == -1) {
        printf("Error al inicializar wiringPi\n");
        return 1;
    }

    pinMode(12, INPUT);

    int movement_count = 0;
    int prev_status = 0;

    FILE *file = NULL;
    char message[100];

    while (1) {
        int current_status = digitalRead(12);

        
        if (current_status == HIGH && prev_status == LOW) {
            movement_count++;
            
            file = fopen("/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-pir.txt", "w");
            if (file == NULL) {
                printf("Error al abrir el archivo\n");
                return 1;
            }
            
            snprintf(message, sizeof(message), "Movimiento detectado: %d \n", movement_count);
            fputs(message, file);

            fclose(file);
            prev_status = HIGH;
        } else if (current_status == LOW && prev_status == HIGH) {
            printf("¡Listo para detectar más movimientos!\n");
            prev_status = LOW;
        }

        delay(10); // Espera 10 ms
    }

    fclose(file);

    return 0;
}
