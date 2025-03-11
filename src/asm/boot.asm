start:
    mov ax, 0x07
    mov ah, 0x0e
    int 0x10


times 510 - ($ - $$) db 0
dw 0xaa55