.global _start


_start:
    mov r0, 10
    mov r1, 20
    add r2, r0, r1

    mov r7, 1
    swi 0x0
