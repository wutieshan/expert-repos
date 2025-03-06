# ASM基础知识


## reference
- [汇编语言在线参考手册](https://cankaoshouce.com/assembly/assembly-course.html)


## environment
- [nasm](https://nasm.us/)
- [cygwin](https://cygwin.com/)
- [bochs](https://github.com/bochs-emu/Bochs)


## 语法
### 段
汇编程序可以分为3个段: data, bss, text;
- data: 即数据段, 用于声明初始化的数据或常数, 在运行时不会更改, 格式如下:
```asm
section .data
```
- bss: 用于声明变量, 格式如下:
```asm
section .bss
```
- text: 即代码段, 用于编写程序的指令, 必须以全局声明`_start`开头, 标识内核程序的入口, 格式如下:
```asm
section .text
global _start
_start:
```


### 注释
汇编程序的注释以分号`;`开头, 可以包含任何可打印字符, 属于单行注释.


### 语句类型
- 可执行指令或说明: 指示处理器如何做, 会生成相应的机器语言指令
- 汇编程序指令或伪操作: 设置汇编器关于程序的各个方面, 不可执行, 也不会生成机器指令
- 宏: 一种代码替换机制


### 基本语法格式
```asm
[label] mnemonic [operands] [;comment]
```


### helloworld示例程序
```asm
org 0x7c00


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
```


## 内存段
## 寄存器
寄存器用于存储待处理的数据, 而无需访问内存; 处理器芯片内置有限数量的寄存器.
- 通用寄存器
    + 数据寄存器
    + 指针寄存器
    + 索引寄存器
    + 数据寄存器
- 控制寄存器
- 段寄存器


### 数据寄存器
4个32位的数据寄存器可用于算术, 逻辑和其它操作, 如下:
- 作为完整的32位数据寄存器: EAX, EBX, ECX, EDX
- 取低位作为4个16位寄存器:
    + AX: 累加
    + BX: 基址
    + CX: 计数
    + DX: 数据
- 分别取4个16位寄存器的高位和低位作为8个8位寄存器: AL, AH, BL, BH, CL, CH, DL, DH


### 指针寄存器
3个32位指针寄存器用于存放内存地址, 如下:
- 作为完整的32位指针寄存器: EIP, ESP, EBP
- 取相应的低位作为16位指针寄存器:
    + IP: 指令指针寄存器
    + SP: 堆栈指针寄存器
    + BP: 基址指针寄存器


### 索引寄存器
2个32位的索引寄存器用于存放内存地址偏移量, 如下:
- 作为完整的32位索引寄存器: ESI, EDI
- 取相应的低位作为16位索引寄存器:
    + SI: 源变址寄存器
    + DI: 目标变址寄存器


### 控制寄存器
控制寄存器是32位指令寄存器与32位标志寄存器的合称, 通用标志位如下:
- OF: 溢出标志
- DF: 方向标志
- IF: 中断标志
- TF: 陷阱标志(单步标志)
- SF: 符号标志
- ZF: 零标志
- AF: 辅助进位标志
- PF: 奇偶校验标志
- CF: 进位标志


### 段寄存器
段是程序中定义的特定区域, 包含数据, 代码和堆栈, 如下:
- CS寄存器: 存储代码段的起始地址
- DS寄存器: 存储数据段的起始地址
- SS寄存器: 存储堆栈段的起始地址
- ES/FS/GS寄存器: 存储附加段的起始地址


## 系统调用
### 执行系统调用的步骤
1. 将系统呼叫号放入eax寄存器
2. 将参数保存到系统调用中的寄存器ebx, ecx, edx, esi, edi
3. 调用中断: `int 0x80`
4. 结果通常在eax寄存器中返回