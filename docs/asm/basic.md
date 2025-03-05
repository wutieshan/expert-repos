# ASM基础知识


## reference
- [汇编语言在线参考手册](https://cankaoshouce.com/assembly/assembly-course.html)


## environment
- [nasm](https://nasm.us/)
- [cygwin](https://cygwin.com/)


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
