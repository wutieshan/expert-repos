section .text
    global start
start:
    mov ax, 0x03
    int 0x10

    mov si, msg
    call print


print:
    mov ah, 0x0e

    .loop:
        lodsb
        cmp al, 0
        je .done
        int 0x10
        jmp .loop
    .done:
        ret


msg db "tieshan, wu...", 0
times 510 - ($ - $$) db 0
db 0x55, 0xaa