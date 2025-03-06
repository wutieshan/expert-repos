; org 0x7c00


; start:
;     mov edx, len
;     mov ecx, msg
;     mov ebx, 1
;     mov eax, 4
;     int 0x80

;     mov edx, 9
;     mov ecx, s2
;     mov ebx, 1
;     mov eax, 4
;     int 0x80

;     mov eax, 1
;     int 0x80


; msg db 'Displaying 9 stars', 0xa
; len equ $ - msg
; s2 times 9 db '*'
; times 510 - ($ - $$) db 0
; dw 0xaa55



section .text
    global _start


_start:
    mov r0, #10
    mov r1, #20
    add r2, r0, r1

    mov r7, #1
    swi 0x0