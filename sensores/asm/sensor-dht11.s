.global _start

.section .data
script_path:
    .asciz "/home/uth/Desktop/ProyectoFinalEmbebida/sensores/bash/sensor-dht11.sh"

argv:
    .word script_path     // argv[0] = script_path
    .word 0               // argv[1] = NULL (fin de argumentos)

envp:
    .word 0               // sin variables de entorno

.section .text

_start:
    ldr r0, =script_path  // const char *filename
    ldr r1, =argv         // const char *argv[]
    ldr r2, =envp         // const char *envp[]

    mov r7, #11           // syscall execve
    swi 0                 // ejecutar el script

    // Si execve falla, salimos con error
    mov r0, #1
    mov r7, #1
    swi 0
