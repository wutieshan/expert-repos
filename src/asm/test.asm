section .text
global _start ;为链接器(ld)声明入口点

_start:
    mov edx, len
    mov ecx, msg
    mov ebx, 1 ;文件描述符(stdout)
    
    mov eax, 4 ;系统调用号(sys_write)
    int 0x80 ;调用系统调用

    mov eax, 1 ;系统调用号(sys_exit)
    int 0x80


section .data
msg db 'tieshan, wu...', 0xa ;输出的字符串
len equ $ - msg ;字符串长度


; 汇编: nasm -f elf test.asm
; 链接: ld -m elf64-x86-64 -s test.o