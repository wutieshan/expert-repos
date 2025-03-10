# Makefile


## reference
> - [官方文档](https://www.gnu.org/software/make/manual/make.html)
> - [在线教程](http://makefiletutorial.foofun.cn/)


## make的作用
+ 帮助确定大型程序的哪些部分需要编译
+ 更具文件更改情况运行一系列指令


## 语法
```shell
# 基本rule结构
targets: prerequisites
    commands


# targets: 目标文件名, 用空格分隔, 通常每个rule只有一个
# prerequisites: 依赖文件名, 用空格分隔
# commands: 要执行的命令, 必须用制表符缩进, 通常每个命令占一行
```


## 通配符
```shell
# % 匹配任意字符串


# * 匹配任意字符
$(wildcard *.cxx)
```


## 自动变量
```shell
# $@: 目标名称
# $?: 比目标更新的所有先决条件
# $^: 所有先决条件
```