# C++ 学习笔记


## 参考
> - 《C++_primer_plus_E6.pdf》


## 开发环境搭建
### vscode
1. [vscode官网](https://code.visualstudio.com/)
2. [minGW-w64](https://sourceforge.net/projects/mingw-w64/files/)
   - 解压, 并添加bin目录到环境变量即可
3. vscode安装C/C++插件
4. 配置c_cpp_properties.json
   - compilerPath: C:/wutieshan/software/devenv/mingw64/bin/g++.exe
   - intelliSenseMode: windows-gcc-x64
```json
{
    "configurations": [
        {
            "name": "cppwin32",
            "includePath": [
                "${workspaceFolder}/**",
                "${workspaceFolder}/include/**"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "windowsSdkVersion": "10.0.22621.0",
            "compilerPath": "C:/wutieshan/software/devenv/mingw64/bin/g++.exe",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "windows-gcc-x64"
        }
    ],
    "version": 4
}
```
5. 配置task.json
```json
{
    "tasks": [
        {
            "type": "cppbuild",
            "label": "C/C++: g++.exe 生成活动文件",
            "command": "C:\\wutieshan\\software\\devenv\\mingw64\\bin\\g++.exe",
            "args": [
                "-fdiagnostics-color=always",
                "-g", //需要编译的源代码文件
                "${workspaceFolder}\\*.cpp",
                "${workspaceFolder}\\source\\*.cpp",
                "-I", //头文件
                "${workspaceFolder}\\include",
                "-o",
                "${workspaceFolder}\\${workspaceRootFolderName}.exe"
            ],
            "options": {
                "cwd": "${fileDirname}"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "detail": "调试器生成的任务。"
        }
    ],
    "version": "2.0.0"
}
```
6. 配置launch.json
```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) 启动",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}\\${workspaceRootFolderName}.exe",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "miDebuggerPath": "C:\\wutieshan\\software\\devenv\\mingw64\\bin\\gdb.exe",
            "setupCommands": [
                {
                    "description": "为 gdb 启用整齐打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "将反汇编风格设置为 Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }
            ]
        }

    ]
}
```


## Book-No-1: [C++_primer_plus_E6.pdf](#)
### 第一章: 预备知识
#### 1.1 C++简介
1. C++继承了C的优点: 高效, 简洁, 快速, 可移植性
2. C++融合了3种不同的编程方式
   - C语言代表的过程式编程
   - 面向对象编程
   - C++模板支持的泛型编程


#### 1.2 C++简史
1. 20世纪70年代, Dennis Ritchie 开发了C语言, 致力于将低级语言的效率, 硬件访问能力和高级语言的通用性, 可移植性融合到一起
2. C语言编程原理
   1. 过程性编程: 强调算法
   2. 结构化编程: 使用for, while等词汇组织语言, 提高了程序的清晰度, 可靠性, 可维护性
   3. 自顶向下设计: 将大型程序分解成小型, 便于管理的任务, 持续该过程直到程序变成小型的, 易于编写的模块; 这还是体现了过程性编程的思想
   4. (C++)OOP: 强调数据, 理念是设计与问题本质特性相对应的数据格式(i.e. 类)
   5. 自底向上设计: 根据OOP理念, 从低级组织(类)到高级组织(程序)的过程
3. 在C++中, 类是一种规范, 它描述了OOP中的数据格式, 根据这种规范构造出的特定数据结构被称为对象
4. OOP的优势
   1. 将数据和方法组织到一起
   2. 有助于创建可重用的代码
   3. 保护私有数据
   4. 多态为运算符和函数创建多个定义, 通过上下文确定究竟使用哪一个
   5. 继承可以从旧类派生出新类
5. 泛型(generic): 提供执行常见任务(如排序)的工具, 创建独立于特定数据类型的代码
6. C++与C的关系: C++是C的超集
7. C++的二重性: 利用OOP对问题进行抽象, 利用C来访问硬件


#### 1.3 可移植性和标准
1. 可移植性的两个难题
   1. 特定硬件的程序是不可移植的
   2. 语言的多个版本之间可能不兼容


#### 1.4 程序创建的技巧
1. 编写源代码 -> 编译(得到目标代码) -> 将目标代码与其使用的库和一些必要的启动代码链接(得到最终的可执行代码)
2. 源文件的扩展名根据不同的C++实现略有不同, 通常是cpp, cxx, cc,...


### 第二章: 开始学习C++
#### 2.1 进入C++
```c++
// C++风格的单行注释, 推荐使用
/* C风格的多行注释 */

// 预处理器编译指令
// #include指令效果: 指定内容的源代码替换该行, 形成一个复合文件, 随后编译时一起发送给编译器
// 这里的iostream叫做包含(include)文件, 也叫头(header)文件
// 命名规则
//     1. 对于C语言头文件, 保留其带扩展名的风格, 如: stdio.h
//     2. 对于C++自己的头文件, 则没有后缀名, 如: iostream
//     3. 对于从C头文件转换过来的C++头文件, 被重新命名(去掉扩展名, 并前缀c), 如: math.h => cmath
#include "iostream"

// C++标准main函数头
// 等效于: `int main (viod)`
// 在C中, 让括号空着意味着对是否接收参数保持沉默
// 对于一个常规的独立程序, 必须定义入口函数, 并且函数名必须是main; 对于编写DLL模块则不需要
int main()
{
    // 使用命名空间std
    // C++使用分号作为语句的终止符, 不能省略
    // 对于C++风格的头文件, 使用using编译指令来使命名空间std中的定义直接可用, 而不用添加前缀 `std::`
    // using namespace std;

    // 上述方式让std中所有的定义都可用, 存在一个潜在的问题, 就是多个命名空间中的同名定义会冲突, 更好的方式如下
    using std::cout;
    using std::endl;

    // cout/cin是C++的输出/输入工具
    // 它相较于C的printf/scanf有很大的变动
    // C++中使用双引号括起来的一系列字符是字符串
    // << 操作符将字符串发送给cout, 它表示了信息的流向
    // 从概念上讲, cout表示输出流, 而插入运算符(<<)将右侧的信息插入到该输出流
    // 插入运算符(<<)也是一个运算符重载的例子, 它还可以表示按位左移运算; 同一个运算符可以有多个功能, 具体的功能由编译器根据上下文确定
    cout << "Come up and C++ me some time.";

    // endl表示重起一行, C++还支持C风格的换行方式"\n"
    // endl与"\n"的一个重要区别是: endl保证程序继续执行前刷新(flush)输出
    // 祥endl一样对cout由特殊含义的符号被称为控制符(manipulator)
    cout << endl;

    // C++源代码的格式化
    // 有些语言是面向行的(即每条语句占一行), 对于它们来说, Enter的作用就是将语句分开
    // 而在C++中, 分号标识了语句的结尾, Enter的作用就和空格和制表符相同, 即可以通过换行格式化代码
    // 标记(token): 代码中不可分隔的元素叫做token, 通常必须使用空白符(空格/制表符/回车)将两个token分开
    // 推荐风格:
    //     1. 每条语句占一行
    //     2. 每个函数的开始和结束花括号各占一行
    //     3. 函数中的语句都相对于花括号进行缩进
    //     4. 与函数名称相关的圆括号周围没有空白  ==>  有助于区分函数和C++内置的使用圆括号的结构, 如: for, wihle,...  ==>  虽然IDE有代码颜色提示
    cout << "You won't"
         << " regret it!"
         << endl;

    // ANSI/ISO C++标准的妥协: 如果编译器到达main函数末尾没有遇到return语句, 则默认是`return 0;`
    return 0;
}
```


#### 2.2 C++语句
#### 2.3 其它C++语句
```c++
#include "iostream"

int main()
{
    using namespace std;

    // 声明一个变量  ==>  ps: "声明"是"定义声明"的简称
    // 该声明完成2项任务: 指出需要足够的内存空间; 赋予对应内存空间一个名称  ==>  具体细节信息由编译器负责
    // 为什么变量必须声明?
    //     1. 某些语言不需要显式的声明变量, 而是在变量首次出现的时候, 自动创建新的变量;
    //     2. 这种方式虽然看起来对用户比较友好, 但是如果错误的拼写了变量, 那么将在不知情的情况下创建新的变量;
    //     3. 因为没有违反语法规则, 是比较难以发现这类错处的;
    //     4. 如果是C++, 那么就违反了变量使用前必须声明的规则, 会报语法错误
    // 变量声明的位置
    //     1. C++: 在变量首次使用的地方
    //     2. C: 通常位于函数或过程的开始位置  ==>  对于函数使用了哪些变量一目了然
    int carrots;
    // 变量赋值
    // C++支持连续赋值(赋值将从右向左依次进行): x = y = z = 1
    carrots = 25;
    cout << "I have ";
    cout << carrots; // cout自动将carrots转换为字符串, 这种行为源自面向对象特性, 也是运算符重载的例子
    cout << " carrots.";
    cout << endl;

    int eats;
    cout << "How many carrots do you wanna eat?" << endl;
    // 通过cin读取键盘输入
    // 注意操作符(>>)的方向, 表示信息从cin流向eats
    // 同cout类似, cin表示输入流, 操作符(>>)表示从输入流中提取字符, 通常需要在右侧提供一变量以接收信息
    // 同时cin会根据右侧变量的类型将输入自动转换
    cin >> eats;
    carrots = carrots - eats;
    cout << "Now I have " << carrots << " carrots." << endl; // 将4条输出语句组合

    return 0;

    // 类简介
    // 类是用户定义的一种数据类型, 它描述了该数据类型的全部属性(数据格式 + 可执行的操作)
    // 对象是基于类创建的实体
    // 就像函数有函数库一样, 类也有类库
    // C++提供了两种向对象发送消息的方式
    //     1. 使用类方法(本质上是函数调用)
    //     2. 运算符重载
}
```


#### 2.4 函数
```c++
// 函数原型(function prototype)
// 函数原型之于函数, 就像变量声明之于变量, 指出了函数的参数和返回值
// 函数原型是一条语句, 结尾的分号表明它是不是函数头
// 在每个函数使用之前应当为其提供原型, 有两种方式
//     1. 在源代码文件中直接提供, 如: `int increment(int);`
//     2. 通过头文件简介提供, 如cmath中就包含sqrt的函数原型  ==>  推荐方式
// 函数原型和函数定义的区别
//     1. 原型只描述接口, 定义包含了具体代码
//     2. C/C++将库函数的原型和定义分开了, 头文件中包含了原型, 库文件中包含了函数的编译代码

// 函数变体
//     1. 多个参数: double pow(double, double);
//     2. 不接受任何参数: int random(void);
//         1. void关键字明确指出函数不接受任何参数, 如果省略void, C++将其解释为一个不接受任何参数的隐式声明
//         2. 注意C++中的函数调用必须包含括号, 即便它不接受参数
//     3. 没有返回值: void hello();
//         1. 因为不返回值, 所以不能将这种函数调用放在表达式, 而应该使用一条纯粹的函数调用语句
//         2. 某些语言中, 没有返回值的函数被称为过程(procedure)或子程序(subroutine), 而C/C++将这些函数变体统一称为函数

// 用户自定义函数
// C++不允许将函数定义嵌套在另一个函数中
#include "cmath"
#include "iostream"
void hello(int);

// 如果多个函数共享同一个命名空间, 则可以将using编译指令放在外面
// 总结
//     1. 将`using namespace std;`放在函数定义之前, 让文件中所有函数都能使用std中的元素
//     2. 将`using namespace std;`放在特定函数定义的开头, 只让该函数使用std中的元素
//     3. 在特定函数中使用类似`using std::cout;`的编译指令, 让该函数使用指定的std中的元素
//     4. 不使用using编译指令, 而是而是在访问std中的元素之前加上`std::`
using namespace std;

int main()
{

    hello(2);

    double area;
    cout << "Enter the floor area, in square feet, of your home: ";
    cin >> area;
    double side = sqrt(area); // C++允许声明变量的同时赋值, 这个过程叫做初始化(initialization)
    cout << "That the equivalent of a square "
         << side
         << " feet to the side." << endl;
    cout << "How fancilating!" << endl;

    // main函数的返回值交给操作系统
    // 通常返回0表示程序正常运行; 返回非0值则表示存在问题
    return 0;
}

void hello(int n)
{

    cout << "hello, I got a int: " << n << endl;
}
```


### 第三章: 处理数据
#### 3.1 简单变量
```c++
// 程序通常需要存储信息, 且必须记录3个基本属性
//     1. 存储的位置
//     2. 存储的数据类型
//     3. 存储的值

// C++变量命名规则
//     1. 只能由字母, 数字, 下划线组成
//     2. 第一个字符不能是数字
//     3. 大小写敏感
//     4. 不能使用C++关键字
//     5. 以两个下划线或下划线开头的名称保留给实现使用
//     6. C++对于变量名的长度没有限制, 但是某些平台由限制
//     7. 具体命名风格因人而定, 但最重要的一点是要保证风格的统一

// 整型
// C++基本整型
//     1. char, short, int, long, long long
//     2. 其中每种类型又分为有符号和无符号版本, 所以一共有10种
//     3. 因为不可能保证所有系统中, 同一种类型的宽度总是相同, 所以C++保证了最小宽度(借鉴自C)
//     4. 位数规则
//         1. short <= int <= long <= long long
//         2. short >= 16bit
//         2. long >= 32bit
//         2. long long >= 64bit
// C++对字节的定义: 由至少能容纳实现的基本字符集的相邻位组成, 依赖于实现, 可能是8bit, 16bit, 32bit
// sizeof运算符返回类型或变量的长度, 单位为字节
// 究竟选择使用哪一种整型?
//     1. int通常被设置为对计算机最"自然"的长度, 即处理起来效率最高; 默认情况下应该使用它
//     2. 如果变量表示的值不可能为负数, 则应该使用对应的unsigned版本
//     3. 如果明确知道变量表示的整数值大于16bit, 应该使用long(即便系统上的int是32bit)  ==>  为了保证程序移植到16位系统时依然能正常工作
//     4. 如果要存储的值大于20亿, 则应该使用long long
//     5. 当使用大规模的整型数组时, 使用short可以节省内存(前提是short表示的范围已经足够使用)
//     6. 如果只需要一个字节, 可以使用char
// 整型字面量
// C++以三种不同的记数方式表示整型字面量: 10进制, 8进制, 16进制
//     1. 如果第一位是1~9, 则表示十进制
//     2. 如果第一位是0, 第二为是1~7, 则表示8进制
//     3. 如果前两位是0x或0X, 则表示16进制
// 值得注意的是这些方式只是为了表示方便, 在底层它们都以相同的方式存储
// 如果需要以不同的方式显示, 可以使用cout的控制符: dec(默认), hex, oct
//     1. cout << hex;  ==>  改变当前显示整型为16进制
// 后缀(推荐使用大写)
//     1. l/L: long
//     1. ll/LL: long long
//     3. u/U: unsigned
// C++如何确定常量的类型
//     1. 除非有理由(特殊的后缀, 值太大)存储为其它类型, 否则储存为int
//     2. 对于不带后缀的十进制整数: 将使用如下能够存储的最小类型: int, long, long long
//     3. 对于不带后缀的16进制或8进制整数: 将使用如下能够存储的最小类型: int, unsigned int, long, unsigned long, long long, unsigned long long
// char类型
//     1. 可用来表示单个字符或比short更小的整数
//     2. 字面量
//         1. 将字符用单引号括起来, 代表字符的数值编码: 'A'
//         2. 使用转义序列: '\b' 或 '0x1a'  ==>  如果既可以使用数字转义序列, 也可以使用符号转义序列, 优先使用符号转义序列, 因为可读性更强, 并且是独立于编码方式的
//         3. 通用字符名: (\u + 8位16进制数) 或 (\U + 16位16进制数)
// unsigned/signed
// 与int不同的是, char默认情况下既不是signed也不是unsigned, 而是取决于具体实现, 如此编译器开发者能够最大程度的将这种类型与硬件属性匹配
//     1. 如果需要用char存储整数(如200), 则必须显式的指定unsigned
//     2. 如果需要用char存储字符, 则是否有符号不重要

// #define是一个预处理器指令, 用于定义符号常量, 这是C遗留下来的; C++使用const关键字
#include "iostream"
#include "climits"

int main()
{
    using namespace std;

    // 变量初始化
    // 不同的初始化风格
    //     1. C: int age = 25;
    //     2. C++: int age(25);
    //     3. C++11: int age = {25};  ==>  主要用于数组和结构, 但也可用于单值变量, 有如下特点
    //         1. 等号是可选的: int age{25};
    //         2. 花括号内可以为空, 表示将变量初始化为0: int age{};
    //         3. 有助于防范类型转换错误
    //         4. 使初始化常规变量和类变量的方式统一
    // 如果知道变量的初始值, 则应该将其初始化
    short n_short = SHRT_MAX;
    int n_int = INT_MAX;
    long n_long = LONG_MAX;
    long long n_llong(LLONG_MAX);

    // 可以对类型名和变量使用sizeof运算符
    // 但是对类型名使用的时候, 括号是必须的
    cout << "short max value is " << n_short << " with size " << sizeof(n_short) << " bytes." << endl;
    cout << "int max value is " << n_int << " with size " << sizeof n_int << " bytes." << endl;
    cout << "long max value is " << n_long << " with size " << sizeof(long) << " bytes." << endl;
    cout << "long long max value is " << n_llong << " with size " << sizeof(long long) << " bytes." << endl;

    cout << "bits per bytes: " << CHAR_BIT << endl;

    // 以不同的进制显示整型
    int n_100 = 100;
    cout << "100 in decimal: " << n_100 << endl;
    cout << hex << "100 in hex: " << n_100 << endl;
    cout << oct << "100 in oct: " << n_100 << endl;

    // wchar_t: 宽字符类型
    // 程序需要处理的字符可能无法用一个8位的字节表示, 这种情况下有两种处理方式
    //     1. 如果大型字符集是实现的基本字符集, 则编译器厂商可以将char定义为一个16位或更大的字节
    //     2. 用8位char表示基本字符集, 用wchar_t(一种整型)表示扩展字符集
    // cin和cout将输入和输出看做char流, 因此不适合用来处理wchar_t, 相应的, iostream提供了类似的工具: wcin/wcout
    // wchar_t常量: 通过前缀L表示, 如: L'A', L"Hello"
    wchar_t suffix = L'!';
    wcout << L"Hello, World" << suffix << endl;

    // char16_t/char32_t
    // 因为wchat_t的长度和符号特征是依赖于实现的, 无法满足特定的开发需求, 所以出现了char16_t/char32_t
    // char16_t: 无符号, 16位; 字面量使用前缀u, 如: u"so good"  ==>  匹配\u版本的通用字符名
    // char32_t: 无符号, 32位; 字面量使用前缀U, 如: U"so good"  ==>  匹配\U版本的通用字符名

    // bool类型
    // 字面量: true, false
    // 可以通过提升转换为int类型: true -> 1; false -> 0
    // 任何数字值和指针值都可以被隐式转换为bool: 非0值 -> true; 0 -> false

    return 0;
}
```


#### 3.2 const限定符
1. 语法: `const double PI = 3.1415926;`
2. 常量一旦初始化, 其值就固定了, 如果尝试修改, 将引发错误
3. 应该在声明的同时进行初始化
4. 常见命名约定
   1. 首字母大写
   2. 整个名称大写(类似于#define)
   3. 以字母k开头
5. 相较于#define, const的优势
   1. 能够明确指定类型
   2. 可以通过作用域规则将定义限定在特定函数或文件
   3. 可以用于定义更复杂的类型


#### 3.3 浮点数
```c++
// 浮点数
// "浮点"一词的由来: 计算机将小数表示为两个部分, 即数值部分 + 小数点位置(缩放因子), 如3.14和31.4的数值部分都是一样的, 区别在于小数点位置不同, 故称为浮点
// 表示浮点数
//     1. 常规的小数点表示法
//     2. E表示法  ==>  适合非常大或非常小的数
// 浮点类型(按可表示的有效位数和允许的指数最小范围来描述, 可以在cfloat中查看)
//     1. float: 有效位数至少32
//     2. double: 有效位数至少48且不少于float
//     3. long double: 有效位数不少于double
// 浮点常量的类型
//     1. 默认情况下, 都是double
//     2. 指定float: 后缀f/F
//     3. 指定long double： 后缀l/L
// 浮点数的优缺点
//     1. 优点: 可以表示小数值, 表示数值的范围比整数大
//     2. 缺点: 运算速度比整数更慢, 并且精度更低

#include "iostream"
#include "cfloat"

int main()
{
    using namespace std;

    float f_result = 10.0 / 3.0;
    double d_result = 10.0 / 3.0;
    const float million = 1.0e6;
    cout.setf(ios_base::fixed, ios_base::floatfield); // 强制输出使用顶点表示法, 以便更好的了解精度
    cout << "f_result = " << f_result << endl;
    cout << "f_result * million = " << f_result * million << endl;
    cout << "d_result = " << d_result << endl;
    cout << "d_result * million = " << d_result * million << endl;

    // float精度演示
    float a = 2.34e22f;
    float b = a + 1.0f;
    cout << "a = " << a << endl;
    cout << "b - a = " << b - a << endl; // 数学上, b - a应该等于1.0f, 可是由于float的精度问题, b无法精确到1.0f, 所以导致b - a的结果为0.0f

    return 0;
}
```


#### 3.4 C++算术运算符
```c++
// 算术运算符
// 5种基本的算术运算符: +, -, *, /, %
// 对于运算符/, 如果两个操作数都是整数, 则结果取整数部分, 小数部分丢弃; 如果其中一个操作数为浮点数, 则结果为浮点数
// 对于操作符%, 两个操作数都必须是整数, 如果其中一个操作数为负数, 则结果的符号满足 (a / b) * b + a % b == a
// 当两个运算符应用于同一个操作数时, 运算符的优先级和结合性决定了先执行哪种操作
// C++类型转换
//     1. 将一种算数类型的值赋给另一种算数类型
//         1. 将一个值赋给范围更小的类型时, 存在安全问题(精度丢失)
//         2. C++列表初始化不允许narrowing
//     2. 表达式中包含不同的类型
//         1. 整型提升: bool, char, unsigned char, signed char, short  ==>  int
//         2. 当运算涉及多种类型时, 较小的类型会被转换为较大的类型
//     3. 将参数传递给函数时
//     4. 强制类型转换(不会修改变量本身, 而是创建一个新的, 指定类型的变量)
//         1. int(x)  ==>  C++风格, 看起来像函数调用
//         2. (int)x  ==>  C风格
//         3. C++引入的4个强制类型转换运算符

// C++中的auto声明
//     1. 编译器把变量的类型设置成与初始值相同
//     2. auto设计的初衷是为了简化处理复杂类型, 如: std::vector<double>::iterator pv = scores.begin();  ==>  auto pv = scores.begin();
//     3. 如果将auto应用于简单情况, 可能会引起歧义
#include "iostream"

int main()
{
    using namespace std;

    int auks, bats, coots;

    // 先做两个double的加法, 然后将结果转换为int
    // ps: C++的int转换是直接截断
    auks = 19.99 + 11.99;
    // 先将double转换为int, 然后再做加法
    bats = (int)19.99 + (int)11.99;
    coots = int(19.99) + int(11.99);
    cout << "auks = " << auks << endl;
    cout << "bats = " << bats << endl;
    cout << "coots = " << coots << endl;

    // 使用强制类型转换查看字符编码
    char ch = 'Z';
    cout << "the code for " << ch << " is " << int(ch) << endl;
    cout << "yes, the code is " << static_cast<int>(ch) << endl;

    return 0;
}
```


### 第四章: 复合类型
#### 4.1 数组
```c++
// 数组
// 数组是一种数据格式, 它可以存储多个同类型的值
// 声明数组需要指出: 数组的名称, 元素的类型, 元素的个数  ==>  short months[12];
// C++数组的索引从0开始
// 编译器不会检查数组索引是否有效, 但是在运行时可能会引发错误
#include "iostream"

int main()
{
    using namespace std;

    int yams[3];
    yams[0] = 7;
    yams[1] = 8;
    yams[2] = 6;

    // 初始化
    // 初始化规则
    //     1. 只有在定义数组的时候才能初始化, 其它时候不能使用, 也不能将一个数组赋值给另一个数组
    //     2. 可以使用下标(索引)分别给数组中的元素赋值
    //     3. 初始化数组的时候, 提供的值可以少于数组的长度, 此时编译器将把剩下的元素设置为0
    //     4. 基于第3点, 将数组中的所有元素初始化为0, 只需要显式的将第一个元素初始化为0即可
    //     5. 如果初始化数组的时候, 方括号内为空, 则编译器将计算元素个数  ==>  对于将字符数组初始化为字符串来说比较有用
    //     6. C++11初始化数组的方法
    //         1. 可以省略等号
    //         2. 可以不在花括号内包含任何内容, 这将把所有元素都初始化为0
    //         3. 列表初始化禁止缩窄(narrowing)
    int yamcosts[3] = {20, 30, 5};
    cout << "total yams = " << yams[0] + yams[1] + yams[2] << endl;
    cout << "the package with " << yams[1] << " yams costs " << yamcosts[1] << " cents per yam.\n";
    int total = yams[0] * yamcosts[0] + yams[1] * yamcosts[1] + yams[2] * yamcosts[2];
    cout << "the total yam expense is " << total << " cent.\n";

    cout << endl;
    cout << "size of yams array is " << sizeof(yams) << " bytes.\n";
    cout << "size of yams array element is " << sizeof(yams[0]) << " bytes.\n";

    return 0;
}
```


#### 4.2 字符串
```c++
// 字符串
// 字符串是存储在内存连续字节中的一系列字符
// C++处理字符串的方式有两种: C风格字符串, 基于string类库的方法
// C++的字符串没有长度限制
// 字符常量's'和字符串常量"s"的区别
//     1. 字符常量是字符编码的一种简写, 实际上是整型
//     2. 字符串常量"s"实际上是两个字符's'和'\0'组成的字符串
//     3. 另外字符串常量"s"表示的是一个地址
#include "iostream"
#include "cstring"

int main()
{
    using namespace std;

    // C风格字符串初始化
    // C风格字符串的一个特点是以空字符('\0')结尾
    // 第一种方式为列表初始化, 比较繁琐
    // 第二种方式为字符串常量, 将自动添加末尾的'\0'
    // 第三种方式为第二种方式的进一步优化, 让编译器自动计算长度
    // 应该确保数组的长度足够大(包括'\0'), 需要明确的是, 这没有太大的坏处(除了浪费一点空间), 因为处理字符串的函数是根据空字符的位置来进行处理的
    // char greetings[20] = {'H', 'e', 'l', 'l', 'o', ' ', 'M', 'r', '.', ' ', 'L', 'e', 'e', '!', '\0'};
    // char greetings[20] = "Hello Mr. Lee!";
    char greetings[] = "Hello Mr. Lee!";

    // 字符串拼接
    // 任何两个由空白符分隔的字符串常量都将自动拼接成一个
    cout << "Hello "
            "Mr. Lee!\n";

    // 将字符串存储到数组中的两种方法
    //     1. 将数组初始化为字符串常量
    //     2. 将键盘或文件输入读到数组中
    const int SIZE = 20;
    char name[SIZE];
    cout << "what's your name?\n";
    // 面向行的输入
    // getline读取指定数目的字符或遇到换行符时停止
    // get可以实现更精细的控制
    cin.getline(name, SIZE); // 最多读取(SIZE-1)个字符, 剩下一个留给空字符'\0'
    // cin.get(name, SIZE).get();
    cout << "your name is " << name << " with " << strlen(name) << " letters.\n";

    // 混合输入字符串和数字
    cout << "what year was your house built?\n";
    int year;
    cin >> year; // 用户输入年份, 将回车键生成的换行符留在了输入队列, 如果不加以处理, 会影响后面的getline()
    cin.get();
    cout << "what's its street address?\n";
    char address[80];
    cin.getline(address, 80);
    cout << "built year: " << year << endl;
    cout << "street address: " << address << endl;

    return 0;
}
```


#### 4.3 string类简介
```c++
// string类
// string类隐藏了字符串的数组性质

#include "iostream"
#include "string"

int main()
{
    using namespace std;

    // string的使用方式与C-string相似
    //     1. 可以使用字符串字面量初始化
    //     2. 可以将键盘输入存储到string对象中
    //     3. 可以使用索引访问元素
    // C++11列表初始化
    //     1. string msg{"hello world"}
    //     2. char msg[]{"hello world"}
    // 不能将一个数组赋值给另一个数组, 但是可以将一个string对象赋值给另一个string对象
    // 可以使用运算符+对string进行合并操作; 也可以使用+=将字符串附加到string对象的末尾
    string name = "Wu Tieshan";
    cout << "my name is " << name << " with " << name[0] << " as the first letter.\n";

    // 其他形式的字符串字面量
    //     1. wchar_t: 前缀L
    //     2. char16_t: 前缀u
    //     3. char32_t: 前缀U
    //     4. UTF-8: 前缀u8
    //     5. 原始字符串: 前缀R并使用"(和)“作为界定符, 如: R"(hello world)"  ==>  同时原始字符串语法还允许在界定符中间添加其它字符, 如: R"+(haha, "( can exist here)+"
    //     6. 可以将原始字符串与其他前缀结合

    return 0;
}
```


#### 4.4 结构简介
```c++
// 结构(struct)
// 结构是一种比数组更灵活的数据格式, 因为同一个结构中可以存储多种类型的数据
// 结构是用户自定义的数据类型, 而结构的声明定义了这种类型的数据属性

#include "iostream"
#include "string"

// 声明一个结构
// 末尾的分号表示这是一条语句
// 声明结构的位置可以是
//     1. 在函数内部
//     2. 在函数外部
// 还可以同时完成结构声明和创建结构变量的操作, 只需要将变量名放在结束括号后面即可, 然而将它们分开是更好的实践
// 还可以声明一种没有名称的结构类型, 此时必须要在末尾指定一个该类型的变量, 有点像一次性的结构
struct person
{
    // 每一项都是一条声明语句, 被称为结构成员
    // 成员也可以使用非基本类型
    std::string name;
    int age;
    std::string job;

    // 位字段: 同C一样C++也可以指定占用特定位数的成员  ==>  可以方便地创建与硬件设备上寄存器对应的数据结构
    // 这一般用在低级编程中
    // unsigned int SN: 4;
};

int main()
{
    using namespace std;

    // 声明结构变量
    // 在C中需要关键字struct, 而在C++中关键字struct可以省略
    // C++11声明
    //     1. 如果花括号内未包含任何内容, 各个成员将被设置为对应的0值
    //     2. 同样不允许缩窄
    // 可以创建结构数组, 方法与创建基本类型数组完全相同
    struct person zhangsan = {
        "张三",
        18,
        "teacher",
    };
    // 可以通过成员运算符访问各个成员
    zhangsan.name = "张三QAQ";
    cout << zhangsan.name << endl;

    // 成员赋值
    person zhangsan_copy = zhangsan;
    cout << zhangsan_copy.name << endl;

    return 0;
}
```


#### 4.5 共用体
```c++
// 共用体(union)
// 共用体是一种数据格式, 它能够存储不同的数据类型, 但是只能同时存储其中一种

#include "iostream"

// 定义共用体
// 由于共用体每次只能存储一个值, 所以必须要有足够大的空间(最大成员的长度)
// 用途: 当数据项(不同时)使用两种或多种格式时, 可以节省空间(通常是嵌入式系统); 另外也用于操作系统和硬件的数据结构
union oneforall
{
    int int_value;
    float float_value;
    double double_value;
};

int main()
{
    using namespace std;

    // 声明一个共用体变量
    oneforall result;

    // 向共用体中存入一个int
    result.int_value = 3;
    cout << result.int_value << endl;
    // 向共用体中存入一个float, 此时前面的int消失
    result.float_value = 3.14;
    cout << result.float_value << endl;
    cout << result.int_value << endl; // 显示为一个不确定的数字

    return 0;
}
```


#### 4.6 枚举
```c++
// 枚举(enumeration)

#include "iostream"

// 定义一个枚举类型
enum spectrum
{
    // 每一项都是符号常量
    // 默认情况下对应从0开始的整数值
    // 可以使用赋值运算符来显式的指定枚举量的值, 并且可以只指定其中的一部分, 甚至可以给多个枚举量设置相同的值
    // 在C++的早期版本中, 只能将int赋给枚举量, 但后来取消了这种限制, 可以long甚至long long了
    red = 0,
    orange,
    yellow,
    green,
    blue,
    violet,
    indigo,
    ultraviolet,
};

int main()
{
    using namespace std;

    // 声明一个枚举变量
    // 在不进行强制类型转换到的情况下只能将枚举值赋给这种变量
    // 对于枚举, 只定义了赋值运算符
    // 枚举值是整型, 可以被提升为int, 但是int不能自动转换为枚举类型
    spectrum band = orange;

    // 通过强制类型转换, 可以将取值范围内的任何整数值赋给枚举量
    // 取值范围的定义(联系底层的2进制存储就好理解了)
    //     1. 上限: 大于枚举量最大值的2的幂 - 1
    //     2. 下限: 如果枚举量的最小值不小于0, 则下限等于0; 否则计算方式同上限, 只是加上了负号
    band = spectrum(5);
    cout << band << endl;

    return 0;
}
```


#### 4.7 指针和自由存储空间
```c++
// 使用常规变量时, 值是指定的量, 而地址是派生量, 可以通过对变量应用地址运算符&, 获取地址
// 使用指针变量时, 地址是指定的量, 而值是派生量, 可以通过对变量应用间接值(解除引用)运算符*, 获取值
// 指针的危险
//     1. 创建指针时, 计算机会分配存储地址的内存, 但是不会分配用来存储指针所指向数据的内存
//     2. 一定要在对指针应用解除引用运算符(*)之前, 将指针初始化为一个明确的, 适当的地址

// 指针和数字
// 从概念上来讲, 指针和整数是两个完全不同的类型; 如, 将两个地址相乘/除是完全没有意义的
// 因此不能简单的将整数赋给指针, 要将数值作为地址来使用, 应该使用强制类型转换  ==>  pt = (int*)0xb8000000;

// 使用new分配内存
// 指针真正的用武之地是, 在运行时分配未命名的内存以存储值; 这种情况下, 只能通过指针来访问内存
// C语言中, 可以通过malloc()分配内存, C++同样可以, 担忧更好的方式new
// 用法: int* pt = new int;  ==>  new int告诉程序需要申请一块适合存储int类型的内存, 并返回其地址
// 常规变量被存储在栈(stack)内存区域, 而new分配的内存在堆(heap)内存区域(自由存储区域)

// 使用delete释放内存
// 用法: delete pt;  ==>  将释放pt所指向的内存, 但不会删除pt本身, 可以将pt重新指向另一个新分配的内存
// delete和new要成对使用
//     1. 如果new之后不使用delete释放, 则会发生内存泄漏(memory leak), 即被分配的内存再也无法使用了
//     2. 如果delete已经释放的内存, 则结果是不确定的(什么都有可能发生)
//     3. delte只能用来释放new分配的内存, 而不能对常规声明的变量使用
//     4. 使用new []为数组分配内存, 相应的需要用delete []来释放
//     5. 使用new []为一个实体分配内存, 则应该使用delete(没有方括号)来释放
// 值得注意的是: 对空指针使用delete是安全的
// delete的关键在于, 释放new分配的一块内存, 这意味着如果有两个指针指向同一块内存地址, 对任何一个指针使用delete均可, 但是通常情况下不建议创建两个指向统一地址的指针, 因为这会增加对同一地址多次使用delete的概率

// 使用new创建动态数组
// 通常, 对于大型数据(数组, 结构, 字符串), 应该使用new
// 在编译时给数组分配内存被称为静态联编(static binding)  ==>  不管最终是否需要, 数组都已经在那里, 它占用了内存
// 在运行时通过new创建数组被称为动态联编(dynamic binding), 相应的数组被称为动态数组

#include "iostream"

int main()
{
    using namespace std;

    int year = 2023;
    // 声明指针时, 必须明确指定它所指向数据的类型, 因为不同的类型的存储格式不尽相同
    // *运算符两边的空格是可选的
    //     1. C风格: int *ptr;  ==>  强调*ptr是一个int类型
    //     2. C++风格: int* ptr;  ==>  强调ptr是一个int*类型, 即指向int的指针
    //     3. 甚至可以不要空格: int*ptr;
    //     4. 但是需要注意的是: int *p1, p2;  ==>  声明了一个指针p1和一个int类型的变量
    // 初始化时, 被初始化的是指针而不是它指向的值
    int *p_year = &year; // 这种方式的用法只是声明了一个&year的别名, 其实没有太大的用处

    cout << "year: " << year << "\t || &year: " << &year << endl;
    cout << "p_year: " << p_year << "\t || *p_year: " << *p_year << endl;

    // 通过指针操作
    // 在这里year和p_year就像是一枚硬币的正反两面
    //     1. year表示值, 使用&运算符可以获得地址
    //     2. p_year表示地址, 使用运算符*可以获得值
    // 因此&year和p_year完全等价, year和*p_year也完全等价
    *p_year += 1;
    cout << "year: " << year << endl;

    // 使用new分配内存
    int *p_month = new int;
    *p_month = 10;
    cout << endl;
    cout << "p_month: " << p_month << "\t || *p_month: " << *p_month << endl;
    cout << "address of p_month: " << &p_month << endl;
    cout << "size of p_month: " << sizeof(p_month) << endl;
    cout << "size of *p_month: " << sizeof(*p_month) << endl;

    // 创建动态数组
    // psome指向第一个元素
    // 程序会自动跟踪分配的内存量, 以便之后使用delete []释放
    // 但是这种信息不是公开的, 如, 不能通过sizeof来确定动态数组的字节数
    // 访问数组元素只需要将指针当成数组名即可, 原因是: C/C++内部都使用指针来处理数组, 数组名和指针基本是等价的
    double *psome = new double[3];
    psome[0] = 0.2;
    psome[1] = 0.5;
    psome[2] = 0.8;
    cout << endl;
    cout << "psome[1] is " << psome[1] << endl;
    // 这里是指针和数组名的一个区别: 指针是变量, 因此可以修改它到的值
    // 这里将指针+1, 实际上是将指针向右移动, 指向了下一个元素
    psome += 1;
    cout << "now, psome[1] is " << psome[1] << endl;
    psome -= 1; // 将指针指向原来的位置, 以便给delete[]提供正确的地址
    cout << "now, psome[1] is " << psome[1] << endl;
    delete[] psome; // 释放内存

    return 0;
}
```


#### 4.8 指针、数组和指针算数
```c++
// 指针算数
// 指针和数组名基本等价的原因在于, 指针算数和C++内部处理数组的方式(将数组名解释为地址)
// 将指针变量+1, 增加的值等于它指向类型的字节数

// 指针和字符串
// 指针和数组的关系可以扩展到C风格字符串
// 对于数组中的字符串, 用引号括起来的字符串, 指针所描述的字符串, 处理方式是一样的, 都将传递它们第一个字符的地址

// C++管理数据内存的方式: 自动存储, 静态存储, 动态存储, (C++11)线程存储
//     1. 自动存储: 再函数内部定义的常规变量使用自动存储空间, 实际上是一个局部变量, 作用域为包含它的代码块, 再作用域自动创建自动释放; 自动变量通常存储在栈中
//     2. 静态存储: 在整个程序执行期间都存在的存储方式, 定义方法有两种
//         1. 在函数外面定义它
//         2. 声明变量是使用关键字static, 如`static double fee = 56.00;`
//     3. 动态变量: new和delete管理一个内存池(被称为堆或自由存储空间), 使得程序员对程序如何使用内存有更大的控制权; 同时也使得内存管理更复杂了, 因为分配的堆内存并不连续

#include "iostream"
#include "string"
#include "cstring"

struct person
{
    int id;
    std::string name;
    int age;
};

int main()
{
    using namespace std;

    double wages[3] = {1000.0, 2000.0, 3000.0};
    short stacks[3] = {3, 2, 1};
    double *pw = wages;     // C++将数组名解释为第一个元素的地址
    short *ps = &stacks[0]; // 显式的说明指针指向数组的第一个元素

    cout << "pw = " << pw << ", *pw = " << *pw << endl;
    cout << "ps = " << ps << ", *ps = " << *ps << endl;
    // 对指针+1
    pw += 1;
    ps += 1;
    cout << "pw = " << pw << ", *pw = " << *pw << endl;
    cout << "ps = " << ps << ", *ps = " << *ps << endl;
    // 访问元素
    // 使用方括号表示法等同于对指针解除引用
    cout << "stacks[0] = " << stacks[0] << endl;
    cout << "*stacks = " << *stacks << endl;
    cout << "*(stacks+1) = " << *(stacks + 1) << endl; // 通常使用数组表示法时, C++执行转换: arr[i] => *(arr + i)
    // 大小
    // 指针和数组名的区别
    //     1. 指针是变量, 可以修改它的值
    //     2. 对数组使用sizeof, 得到的是数组的长度; 而对指针使用sizeof, 得到的是指针的长度
    cout << "size of stacks: " << sizeof(stacks) << endl;
    cout << "size of ps: " << sizeof(ps) << endl;

    // 对数组名取地址和数组名本身(对数组的第一个元素取地址), 虽然从数字上看, 这两个值相同, 但从概念上讲, 它们是不同的
    //     1. stacks(&stacks[0]): 是一个2字节内存块的地址  ==>  short*
    //     2. &stacks: 是一个6字节内存块的地址  ==>  short(*)[3]
    cout << "stacks = " << stacks << endl;
    cout << "&stacks = " << &stacks << endl;

    // 创建动态结构
    // 因为动态结构没有名称, 所以不能使用成员运算符(.), 针对这种情况, C++提供了箭头成员运算符(->), 用于指向结构的指针
    // 另一种访问方法是同过解除引用将指针转换为结构本身, 再使用句点成员运算符: (*p_zhangsan).name, 优先级要求必须有括号, 显然这种方式比较麻烦
    person *p_zhangsan = new person;
    p_zhangsan->id = 1;
    p_zhangsan->name = "张三";
    p_zhangsan->age = 18;
    cout << endl;
    cout << "info of zhangsan:\n  name: " << p_zhangsan->name << "\n  age: " << p_zhangsan->age << endl;
    delete p_zhangsan;

    return 0;
}

char *getname(void)
{
    // 演示创建动态字符串
    // 已知输入字符串最大长度为79, 并且大部分时候, 用不了这么大的空间
    // 这里有一点需要注意的是: 将new和delete放在了不同的函数中, 这通常不是一个好的办法, 但确实也是可以的

    using namespace std;
    char temp[80];
    cout << "please enter your last name: ";
    cin >> temp;
    char *pt = new char[strlen(temp) + 1];
    strcpy(pt, temp);
    return pt;
}
```


#### 4.9 类型组合
```c++
// 结构, 数组, 指针的组合

#include "iostream"
#include "string"

struct person
{
    int id;
    std::string name;
};

int main()
{
    using namespace std;

    // 声明person结构类型的变量
    person p1{1, "张三"}, p2{2, "李四"}, p3{3, "王五"};
    cout << "p1.name: " << p1.name << endl;

    // 声明一个指向person结构类型的指针
    person *pa = &p1;
    cout << "\npa->name: " << pa->name << endl;
    cout << "(*pa).name: " << (*pa).name << endl;

    // 声明一个person结构类型的数组
    person pb[3] = {p1, p2, p3};
    cout << "\npb[0].name: " << pb[0].name << endl;
    cout << "pb->name: " << pb->name << endl;

    // 声明一个指向person结构类型指针的数组
    const person *pc[3] = {&p1, &p2, &p3};
    cout << "\npc[0]->name: " << pc[0]->name << endl;
    cout << "(*pc[0]).name: " << (*pc[0]).name << endl;
    cout << "(*pc)->name: " << (*pc)->name << endl;

    // 定义一个指向pc的指针
    // 在这里pd本身的类型可以看成是person**
    // 也可以使用C++11提供的auto
    // auto pd = pc;
    const person **pd = pc;
    cout << "\n(*pd)->name: " << (*pd)->name << endl;
    cout << "(*(pd+1))->name: " << (*(pd + 1))->name << endl;

    return 0;
}
```


#### 4.10 数组的替代品
```c++
#include "iostream"
#include "vector"
#include "array"

int main()
{
    using namespace std;

    // 原始数组
    double a1[4] = {1.2, 2.4, 3.6, 4.8};

    // 模板类vector - 动态数组的替代品
    // vector对象在插入值的时候自动调整长度, 使用动态内存, 代价是效率低
    vector<int> vi;       // 声明一个int数组, 初始长度为0
    vector<double> vd(4); // 声明一个double数组, 初始长度为3
    vd[0] = 1.2;

    // 模板类array - 定长数组的替代品
    // 和数组一样, array对象的长度是固定的, 使用静态内存(栈), 效率与数组爹同, 但使用起来更方便, 安全
    array<int, 5> ai; // 创建一个包含5个int值的array对象
    array<double, 4> ad = {1.2, 2.4, 3.6, 4.8};

    // 访问成员
    cout << "a1[0] = " << a1[0] << endl;
    cout << "vd[0] = " << vd[0] << endl;
    cout << "ad[0] = " << ad[0] << endl;

    // C/C++不检查越界错误
    cout << "a1[-1] = " << a1[-1] << endl;
    cout << "vd[-1] = " << vd[-1] << endl;
    cout << "ad[-1] = " << ad[-1] << endl;

    // 也可以使用at成员函数在运行时捕获非法索引, 代价是运行时间更长, 这也是C/C++允许使用任意一种表示方法的原因
    cout << "vd.at(0) = " << vd.at(0) << endl;
    cout << "ad.at(0) = " << ad.at(0) << endl;

    return 0;
}
```


### 第五章: 循环和关系表达式
#### 5.1 for循环
```c++
// for循环
// for循环是入口条件循环, 即每轮循环之前都将计算条件表达式的值
// C++通常在for, while, if等关键字与后面的圆括号之间插入空格, 强调这是控制语句, 而不是函数调用

// 表达式和语句
// C++中每个表达式都有值, 如
//     1. 赋值表达式的值为左侧成员的值, 即表达式x=10的值为10
//     2. 关系表达式的值为bool
// 为判定表达是x=10的值, C++必须将10赋值给x, 像这种判定表达式的值的操作改变了内存中的值, 我们说表达式有副作用(side effect)
// 在任何表达式的末尾加上分号, 即可将其转变为语句; 然而反过来却不一定, 如, return语句, 声明语句, for语句,...

// 在C++中, for语句的句法如下
// for (for-init-statment condition; expression) statement
// 因为老式的C风格的for循环的控制体中, 只能是3条语句表达式, 不能包含声明; 而C++的这项改动, 使得可以在for中初始化变量, 乍一看只有一个分号, 但事实上init-statment可以包含一个分号, 它既可以是表达式语句, 也可以是声明

// ++和--
// 前缀和后缀版本的区别
//     1. 前缀: 先修改, 再使用
//     2. 后缀: 先使用, 再修改
// 两个概念
//     1. 副作用(side effect): 在计算表达式时对某些东西（如变量中的值）进行了修改
//     2. 顺序点(sequence point): 程序执行过程中的一个点, 在这里, 在进入下一步之前, 将确保对所有副作用都进行了评估
//         1. 在C++中语句的分号就是一个顺序点
//         2. 任何完整表达式的后面都有一个顺序点  ==>  何谓"完整表达式"? 即不是另一个更大表达式的子表达式
// 得注意的是: 不要在同一条语句中对同一个值进行多次递增或递减操作, 这会产生不确定的结果
//     1. 例如 y = (4 + x++) - (6 + x++);
//     2. 由于(4 + x++)和(6 + x++)都不是完整的表达式, 因此C++并不保证在执行完(4 + x++)之后立即对x递增
//     3. C++只保证在执行完整个表达式之后, 对x递增2次1, 因此将导致结果不确定
// 在C++11中, 不再使用术语"顺序点"了, 而是使用术语"顺序", 主要是为了能更好地描述多线程执行
// 对于前面缀和后缀两种格式来说, 如果表达式的只没有被使用, 那么对程序的执行(最终效果)是没有影响的, 然而在执行速度上可能存在细微的差别
//     1. 对于内置类型来说, 不会有差别
//     2. 对于用户定义的类型, 如果定义了递增和递减运算符, 则前缀格式效率更高(?)
// 允许对指针进行递增和递减操作
// 如果递增/减运算符同时和解除引用运算符作用于指针, 规则如下
//     1. 前缀格式和*的优先级相同, 以从右到左的方式进行结合  ==>  *++pt等价于*(++pt)
//     2. 后缀格式比前缀格式优先级高, 以从左到右的方式进行结合  ==>  *pt++等价于*(pt++)

// 组合赋值运算符: +=, -=, *=, /=, %=

// 复合语句(语句块): 通过两个花括号来构造
// 语句块在句法上被视为一条语句
// 语句块中定义的变量仅在该语句块中生效

// 逗号运算符: 将多个表达式合并, 在句法上视为一个表达式
// 逗号运算符的一个应用场景是for循环, for (int x=0, y=1; condition; x++, y++;) {}
// 注意逗号并不总是逗号运算符, 还可能只是单纯的分隔符, 如: int x, y;
// 逗号运算符的两个特性
//     1. 本身是一个顺序点, 即确保先计算第一个表达式, 然后计算第二个表达式
//     2. C++规定逗号表达式的值, 是第二部分的值
// 在所有的运算符中, 逗号运算符的优先级是最低的

// 关系表达式
// 关系运算符: >, <, ==, >=, <=, !=

// C风格的字符串比较
// 因为数组名和字符串常量都是地址, 所以类似`str == "hello"`的比较必能如预想的方式工作
// 而应该是使用库函数strcmp()
// 因为C风格的字符串是通过结尾的'\0'来定义的, 所以即便两个字符数组的长度不同等, strcmp()的比较结果也可能相等
// 虽然不能用关系运算符来比较字符串, 但是却可以用来比较字符, 因为字符实际上是整型

// string字符串的比较
// 类函数重载使得该比较可以使用关系运算符

#include "iostream"

int main()
{
    using namespace std;

    const int SIZE = 16;
    long long factorials[SIZE];
    factorials[0] = factorials[1] = 1LL;

    // 计算
    // 值得一提的是, 检测不等式条件通常比检测相等条件要好
    for (int i = 2; i < SIZE; i++)
    {
        factorials[i] = factorials[i - 1] * i;
        cout << i << "! = " << factorials[i] << endl;
    }

    return 0;
}
```


#### 5.2 while循环
```c++
// while循环
// while循环是没有初始化和更新部分的for循环
// while循环也是一种入口条件循环
// 由于for和while循环几乎是等效的, 所以究竟使用哪个只是风格上的问题
//

#include "iostream"
#include "ctime"

int main()
{
    using namespace std;
    char name[] = "wutieshan";
    int i = 0;
    while (name[i] != '\0')
    {
        cout << name[i] << ": " << int(name[i]) << endl;
        i++;
    }

    // 延时
    // clock_t是一个类型别名, C++创建类型别名的方式有两种
    //     1. 使用预处理器: #define BYTE char
    //     2. 使用关键字typedef: typedef char BYTE;  ==>  推荐
    float secs = 1.5;
    clock_t delay = secs * CLOCKS_PER_SEC;
    clock_t start = clock();
    while (clock() - start < delay)
    {
        // 循环体为空
    }
    cout << "times up!";

    return 0;
}
```


#### 5.3 do while循环
```c++
// do while循环
// do while循环是出口条件循环, 即首先执行循环体, 然后再判断测试表达式, 决定是否继续
// 通常情况下, 入口条件循环比出口条件循环更好, 但是有时使用do while更合理, 例如, 先获取用户输入, 然后再对其进行测试

#include "iostream"

int main()
{
    using namespace std;

    cout << "Enter numbers in the range 1-10 to find my favorite number\n";
    int favorite_num = 7;
    int guess_num;
    do
    {
        cin >> guess_num;
    } while (guess_num != favorite_num);

    return 0;
}
```


#### 5.4 基于范围的for循环 (C++11)
```c++
#include "iostream"

int main()
{
    using namespace std;
    double prices[5] = {4.99, 10.99, 6.87, 7.99, 8.49};

    for (double price : prices)
    {
        cout << price << endl;
    }

    // 如果要修改元素, 语法稍有不同
    for (double &price : prices)
    {
        price *= 0.80;
    }
    cout << "now, prices[0] = " << prices[0] << endl;

    return 0;
}
```


#### 5.5 循环和文本输入
```c++
#include "iostream"

int main()
{
    using namespace std;

    // cin对象支持3种不同的输入模式

    // 1. 使用原始的cin进行输入
    // 程序必须要知道何时停止读取, 一种方法是选择某个特殊字符(哨兵, sentinel)作为停止标记
    // 特点
    //     1. cin读取char值时, 将忽略空格和换行
    //     2. 发送给cin的输入被缓冲, 即只有当用户按下Enter键之后, 输入的内容才会被发送给程序, 因此用户可以在哨兵字符后面继续输入
    char ch;
    int count = 0;
    char sentinel = '#';

    cout << "1. cin >> ch\n";
    cout << "Enter characters; enter " << sentinel << " to quit:\n";
    cin >> ch;
    while (ch != sentinel)
    {
        cout << ch; // 回显
        ++count;
        cin >> ch;
    }
    cout << endl;
    cout << count << " characters read\n\n";

    // 2. 使用cin.get()读取输入中的每一个元素, 包括空白符
    // 该版本仍然存在输入被缓冲的问题
    cin.clear();
    count = 0;
    cout << "2. cin.get(ch)\n";
    cout << "Enter characters; enter " << sentinel << " to quit:\n";
    cin.get(ch);
    while (ch != sentinel)
    {
        cout << ch;
        ++count;
        cin.get(ch);
    }
    cout << endl;
    cout << count << " characters read\n\n";

    // 3. eof
    // 使用哨兵字符的一个缺陷是: 哨兵字符本身可能也是有效的输入
    // 如果输入来自于文件, 则可以使用一种更为强大的技术: EOF
    // 在Unix系统中, 可以使用Ctrl+D来模拟EOF, 在Windows系统中可以使用Ctrl+Z来模拟EOF
    // 在检测到EOF之后, cin将eofbit和failbit都设置为1, 可以通过成员函数eof()和fail()来查看其值
    cin.clear();
    count = 0;
    cout << "3. eof\n";
    cout << "Enter characters\n";
    cin.get(ch);
    while (!cin.fail())
    {
        cout << ch;
        ++count;
        cin.get(ch);
    }
    cout << endl;
    cout << count << " characters read\n\n";

    // 4. 简化
    // 因为cin.get(char)返回cin对象, 而istream类提供了一个自动将istream对象转换为bool的成员函数
    // 因此可以简化while测试条件, 表示是否成功读取, 这比eof更为通用, 因为它可以检测到其它失败的原因(如磁盘故障)
    // 同时此方法不需要在循环前调用一次cin.get()进行初始化, 使得代码更简洁
    cin.clear();
    count = 0;
    cout << "4. simplify\n";
    cout << "Enter characters\n";
    while (cin.get(ch))
    {
        cout << ch;
        ++count;
    }
    cout << endl;
    cout << count << " characters read\n\n";

    return 0;
}
```


#### 5.6 嵌套循环和二维数组
```c++
// C++没有提供二维数组类型, 但是用户可以自己创建每个元素本身都是数组的数组

#include "iostream"

int main()
{
    using namespace std;
    const int CITIES = 5;
    const int YEARS = 4;
    // 也可以使用二维数组: const char cities[CITIES][25];
    // 也可以使用string: const string cities[CITIES];
    const char *cities[CITIES] = {
        "Gribble City",
        "Gribble Town",
        "New Gribble",
        "San Gribble",
        "Gribble Vista",
    };
    int maxtemps[YEARS][CITIES] = {
        {96, 100, 87, 101, 105},
        {96, 98, 91, 107, 104},
        {97, 101, 93, 108, 107},
        {98, 103, 95, 109, 108},
    };

    cout << "Maximum temperatures for 2008 - 2011\n\n";
    for (int j = 0; j < CITIES; ++j)
    {
        cout << cities[j] << ":\t";
        for (int i = 0; i < YEARS; ++i)
        {
            cout << maxtemps[i][j] << "\t";
        }
        cout << endl;
    }

    return 0;
}
```


### 第六章: 分支语句和逻辑运算符
#### 6.1 if语句
```c++
// if语句
// 因为C++的自由格式, if-else if-else结构只是if-else中包含了另一个if-else
// 为了防止错误的将相等测试写成赋值语句, 可以将`x == 3`改写成`3 == x`; 此时, 如果少写了一个等号, 编译器会报错提示

#include "iostream"

int main()
{
    using namespace std;

    // 猜数字游戏
    const int favorite_num = 27;
    int guess_num;

    cout << "Enter a number in the range 1-100 to find my favorite nunmber: ";
    do
    {
        cin >> guess_num;
        if (guess_num > favorite_num)
            cout << "too high, guess again: ";
        else if (guess_num < favorite_num)
            cout << "too low, guess again: ";
        else
            cout << "that's right!";
    } while (guess_num != favorite_num);

    return 0;
}
```


#### 6.2 逻辑表达式
```c++
// 逻辑表达式
// 与: &&
// 或: ||
// 非: !

// ||和&&都是顺序点, 即运算符左边的子表达式优先于右边的子表达式
// ||和&&都有短路特性

// C++不支持连续的关系运算符
// 如: 17 < age < 35
// 这个表达式在语法上不会报错, 但是根据运算符<从左到右的结合性, 等价于(17 < age) < 35
// 而括号内表达式的结果要么为0(false), 要么为1(true), 因此整个表达式恒等于true

// 对于NOT操作!, 通常不在关系表达式中使用(因为可以做等价变换), 而是用在可被解释为true/false值的对象或函数返回值

// 在C++中逻辑运算符有另一个表达方式
//     1. && -> and
//     2. || -> or
//     3. !  -> not

#include "iostream"
#include "climits"

bool is_intable(double);

int main()
{
    using namespace std;
    const int SIZE = 6;
    float naaq[SIZE];
    cout << "Enter the NAAQs of your neighbors\n"
         << "program terminates when you make "
         << SIZE << " entries or enter a negative value\n";

    int i = 0;
    float temp;
    cout << "first value: ";
    cin >> temp;
    while (i < SIZE && temp >= 0)
    {
        naaq[i] = temp;
        ++i;
        if (i < SIZE)
        {
            cout << "next value: ";
            cin >> temp;
        }
    }

    if (i == 0)
        cout << "no data -- bye!\n";
    else
    {
        cout << "Enter your NAAQ: ";
        float you;
        cin >> you;
        int count = 0;
        for (int j = 0; j < i; ++j)
        {
            if (naaq[j] > you)
                ++count;
        }
        cout << count << " of your neighbors have greater NAAQ that you do.\n";
    }

    return 0;
}

bool is_intable(double x)
{
    if (x <= INT_MAX && x >= INT_MIN)
        return true;
    else
        return false;
}
```


#### 6.3 字符函数库cctype
```c++
// cctype中常用的函数
// isalnum
// isalpha
// iscntrl
// isdigit
// isgraph: 除空格之外的打印字符
// islower
// isprint
// ispunct
// isspace: 标准空白字符
// isupper
// isxdigit
// tolower
// toupper

#include "iostream"
#include "cctype"

int main()
{
    using namespace std;
    cout << "Enter text for analysis, and type @ to terminate input.\n";
    char ch;
    int chars = 0;
    int whitespace = 0;
    int digits = 0;
    int punct = 0;
    int others = 0;

    while ((ch = cin.get()) != '@')
    {
        if (isalpha(ch))
            ++chars;
        else if (isspace(ch))
            ++whitespace;
        else if (isdigit(ch))
            ++digits;
        else if (ispunct(ch))
            ++punct;
        else
            ++others;
    }
    cout << "chars: " << chars << endl;
    cout << "whitespace: " << whitespace << endl;
    cout << "digits: " << digits << endl;
    cout << "punct: " << punct << endl;
    cout << "others: " << others << endl;

    return 0;
}
```


#### 6.4 条件运算符
```c++
// 条件运算符
// 这是C++中唯一一个需要3个操作数的运算符, 常用来替代简单的if-else结构
// 语法: expr1 ? expr2 : expr3

#include "iostream"

int main()
{
    using namespace std;
    cout << "Enter two integers: ";
    int a, b;
    cin >> a >> b;
    cout << "the larger of " << a << " and " << b << " is " << (a > b ? a : b) << endl;

    return 0;
}
```


#### 6.5 switch语句
```c++
// switch语句
// 原理: 类似于指路牌, 根据switch后面括号中表达式的值, 跳到对应的case子句, 如果没有对应的case, 则跳到default子句, 如果也没有default, 就结束继续执行后面的代码
// C++中的case标签只是行标签, 而不是选项之间的界限, 即程序跳到特定的代码行后, 将依次执行之后所有的语句; 因此如果不想执行后面的行, 需要显式的使用break语句
// switch与if-else比较
//     1. if-else更通用, 它可以处理取值范围
//     2. switch中每一个case标签都必须是一个单独的值, 并且还必须是整数常量
//     3. 因为switch是专门为"整数常量"而设计的, 所以它的执行效率更高

// 结论: 当两者(switch和if-else)都能使用并且选项个数不少于3时, 应该使用switch

#include "iostream"

enum color
{
    red,
    orange,
    yellow,
    green,
    blue,
    violet,
    indigo
};

int main()
{
    using namespace std;

    int code;
    cout << "Enter color code(0-6): ";
    cin >> code;
    while (code >= red && code <= indigo)
    {
        switch (code)
        {
        case red:
            cout << "her lips were red.\n";
            break;
        case orange:
            cout << "her hair was orange.\n";
            break;
        case yellow:
            cout << "her shoes were yellow.\n";
            break;
        case green:
            cout << "her nails were green.\n";
            break;
        case blue:
            cout << "her sweatsuit was blue.\n";
            break;
        case violet:
            cout << "her eyes were violet.\n";
            break;
        case indigo:
            cout << "her mood was indigo.\n";
            break;
        }
        cout << "Enter color code(0-6): ";
        cin >> code;
    }
    cout << "Bye!\n";

    return 0;
}
```


#### 6.6 break和continue语句
```c++
// break
// 应用场景: 循环, switch
// 作用: 跳出循环或switch, 执行后面的语句

// continue
// 应用场景: 循环
// 作用: 跳过本轮循环中后面的代码, 开始新一轮的循环

// C++也有goto语句, 然而使用它可能导致结构混乱的代码

#include "iostream"

int main()
{
    using namespace std;
    const int SIZE = 80;
    char line[SIZE];
    int spaces = 0;
    cout << "Enter a line of text:\n";
    cin.get(line, SIZE);
    cout << "Complete line:\n"
         << line << endl;
    cout << "Line through first period:\n";
    for (int i = 0; line[i]; ++i)
    {
        cout << line[i] << endl;
        if (line[i] == '.')
            break;
        if (line[i] != ' ')
            continue;

        ++spaces;
    }
    cout << "\nspaces: " << spaces << endl;

    return 0;
}
```


#### 6.7 读取数字的循环
```c++
// 使用`cin >> x`时出现类型不匹配, 将产生的影响
//     1. x的值保持不变
//     2. 不匹配的输入被保留在输入队列
//     3. cin对象的一个错误标记被设置  ==>  必须重置cin.clear()
//     4. 对cin方法的调用返回false  ==>  可以用非数字输入结束循环

#include "iostream"

int main()
{
    using namespace std;
    const int Max = 5;
    double fish[Max];
    cout << "Enter the weights of your fish.\n";
    cout << "You may enter up to " << Max << "fish, <q to terminate.\n";
    cout << "fish #1: ";
    for (int i = 0; i < Max;)
    {
        cout << "fish #" << i + 1 << ": ";
        if (cin >> fish[i])
        {
            // 成功取得输入
            ++i;
            continue;
        }

        // 获取输入失败
        cin.clear();
        while (cin.get() != '\n') // 忽略整个错误行, 也可以读取到下一个空白符
            continue;
        cout << "Bad input, try it again!\n";
    }

    // average
    double total = 0.0;
    for (int i = 0; i < Max; ++i)
    {
        total += fish[i];
    }

    // result
    cout << total / Max << " average weights of " << Max << " fish.\n";

    return 0;
}
```


#### 6.8 简单文件输入/输出
```c++
// 文本I/O
// 在使用cin进行输入时, 程序将输入视为一系列字节, 其中每个字节都被解释为字符编码
// 对于不同的目标类型, 进行不同的处理
//     1. char: 读取输入中的第一个字符
//     2. int: 一直读取, 直到第一个非数字字符
//     3. double: 一直读取, 直到第一个不属于浮点数的字符
//     4. char[]: 一直读取, 直到第一个空白符

#include "iostream"
#include "fstream"
#include "cstdlib"

int main()
{
    using namespace std;
    const char filepath[] = "info.txt";

    // fout
    // 第一步: 声明一个ofstream对象, 并通过open方法将其与要操作的文件关联
    ofstream fout;
    fout.open(filepath);

    // 第二步: 像使用cout一样使用fout
    // 所有可用于cout的操作和方法都可以用于ofstream对象
    fout << "red\norange\nyellow\ngreen\nblue\nviolet\nindigo\n";

    // 第三步: 使用完之后, 通过close方法关闭文件
    // 如果忘记了, 程序终止时也会自动关闭文件
    fout.close();

    // fin
    // 第一步: 声明一个ifstream对象, 并通过open方法将其与要操作的文件关联
    ifstream fin;
    fin.open(filepath);

    // 第二步: 检查文件是否被成功打开
    // 可能无法正常打开文件: 不存在, 权限不够,...
    if (!fin.is_open())
        exit(EXIT_FAILURE);

    // 第三步: 像使用cint一样使用fin
    // 所有可用于cin的操作和方法都可以用于ifstream对象
    char color[10];
    while (fin >> color)
    {
        cout << color << endl;
    }
    // fin.good()指出最后一次读取操作是否成功
    if (fin.eof())
        cout << "End of file reached.\n";
    else if (fin.fail())
        cout << "Input terminated by data mismatch.\n";
    else
        cout << "Input terminated for unknown reason.\n";

    // 第四步: 关闭文件
    fin.close();

    return 0;
}
```


### 第七章: 函数--C++的编程模块
#### 7.1 复习函数的基本知识
```c++
// 要使用C++函数, 必须完成如下工作
//     1. 提供函数定义
//     2. 提供函数原型
//     3. 调用函数

// 根据有无返回值分类
//     1. 无返回值
//         1. `return;`是可选的
//         2. 相当于某些语言的procedure或subroutine
//     2. 有返回值
//         1. 必须使用return语句, 并且返回值的类型必须为指定的类型或者可以强制转换为该类型
//         2. C++对于返回值有一定的限制: 不能直接返回数组, 但可以是其它任意类型

// C++函数是如何返回值的?
//     1. 将返回值复制到指定的CPU寄存器或内存单元
//     2. 调用程序查看该内存单元
//     3. 调用函数和返回函数就对该内存单元中存储数据的格式进行统一
//         1. 函数原型将返回值类型告知调用程序
//         2. 函数定义指定被调函数应该返回的数据类型

// C++为什么需要原型
// 原型描述了函数到编译器的接口
//     1. 如果函数调用传入类型不匹配的参数, 编译器将捕获错误
//     2. 将返回值存入CPU寄存器或内存中时, 编译器知道需要多少空间来存储
// 原型的功能
//     1. 使编译器正确处理函数返回值
//     2. 使编译器检查传参个数是否正确
//     3. 使编译器检查传参类型是否正确, 如果不正确, 尝试自动转换

// 函数原型的语法
// 1. 函数原型是一条语句, 必须要以分号结束  ==>  获取原型的方式: 函数头, 添加分号, 删除变量名
// 2. 函数原型中可以包含变量名, 但他只是一个占位符, 不必与函数定义中的变量保持一致  ==>  然而提供变量名将使原型更容易理解
// 3. C++中函数原型的参数列表为空和显式的指定为void是等效的
// 4. C中参数列表为空表示不指出参数, 即将在后面定义; 而在C++中不指定参数列表时, 应当使用省略号(...)

// 在编译阶段进行的原型化被称为静态类型检查(static type checking), 它可以发现很多在运行时难以发现的错误
```


#### 7.2 函数参数和按值传递
```c++
// C++函数通常按值传递参数  ==>  即将数值参数传递给函数, 而函数将其赋给一个新的变量, 这样在被调函数中的操作将不会影响调用函数
// 用于接收传递值的变量叫做形参(parameter), 传递给函数的值叫做实参(argument)
// 在函数中声明的变量是局部变量(为该函数私有), 也是自动变量(自动分配和释放)
// 函数定义时, 如果多个参数的类型相同, 则必须分别指定每个参数的类型, 而不能将它们"组合"

#include "iostream"

long double probability(unsigned, unsigned);

int main()
{
    using namespace std;
    unsigned total = 51, choices = 6;
    cout << "you have one chance in " << probability(total, choices) << " of winning.\n";

    return 0;
}

long double probability(unsigned numbers, unsigned picks)
{
    long double result = 1.0;
    for (unsigned n = numbers, p = picks; p > 0; --n, --p)
        result *= n / p;
    return result;
}
```


#### 7.3 函数和数组
```c++
// 在C++中, 当且仅当在函数头或函数原型中, `int arr[]`与`int *arr`的含义才相同, 它们都表示arr是一个指针
// 两个恒等式
//     1. arr[i] = *(arr + i)
//     2. &arr[i] = arr + i

// 将数组作为参数意味着什么?
// 传递常规变量时, 函数使用该变量的拷贝; 而传递数组时, 函数将使用原来的数组
// 但是这种区别并不违反C++按值传递的规则, 仍然向函数传递了一个值, 只不过这个值是一个指针
// 将数组地址作为参数传递, 一方面, 可以节省复制整个数组所需的时间和内存; 另一方面, 也增加了破坏原始数据的风险

// 数组处理函数的常用编写方式
// int fill_arr(double *arr, int maxsize);  ==>  传递两个参数(数组名和个数), 可以处理任意长度的数组, 但是不能通过sizeof获取原始数组的长度, 而必须依赖传入正确的size值

// 使用数组区间的函数
// 传递两个指针: 一个指针标识数组的开头, 另一个指针标识数组的结尾  ==>  C++STL中使用"超尾"的概念定义区间, 即表示元素结尾的参数是指向最后一个元素后面的指针

// 指针和const
// 将const用于指针的两种场景
//     1. 让指针指向一个常量对象  ==>  防止使用该指针修改它所指向的值
//     2. 将指针本身声明为常量  ==>  防止改变指针所指向的位置
// const int *pt = &age;  ==>  *pt是常量, 但pt不是  ==>  指向const对象(只是对于指针pt而言, 不能修改*pt的值, 并不意味着这个对象age本身是常量)
// int* const pt = &age;  ==>  pt是常量, 但*pt不是  ==>  const指针
// const int* const pt = &age;  ==>  pt和*pt都是常量  ==>  指向const对象的const指针
// 通常, 将指针作为函数形参时, 可以使用指向const的指针来保护数据
// 另外使用指向const的指针使得函数能够接受const和非const实参, 否则将只能接受非const实参  ==>  只有一层间接关系, 即数组元素是基本类型

#include "iostream"
int sum_arr(int *arr, int n); // 省略变量名: int sum_arr(int *, int);
// int sum_arr(int arr[], int n); // 省略变量名: int sum_arr(int[], int);
int fill_arr(double *arr, int maxsize);
void show_arr(const double *arr, int size);
void show_arr_by_range(const double *begin, const double *end);
void modify_arr(double *arr, int size, double factor);

using namespace std;

int main()
{
    const int Size = 8;
    int cookies[Size] = {1, 2, 4, 8, 16, 32, 64, 128};
    int total = sum_arr(cookies, Size);
    cout << "cookies address: " << cookies << endl;
    // 这里的cookies是数组名, sizeof将获取整个数组的长度
    cout << "sizeof cookies: " << sizeof(cookies) << endl;
    cout << "total cookies eaten: " << total << endl;
    total = sum_arr(&cookies[4], 4);
    cout << "last 4 eaters eaten: " << total << endl;

    // 数组操作
    cout << endl;
    const int Max = 5;
    double properties[Max];
    int size = fill_arr(properties, Max);
    // show_arr(properties, size);
    show_arr_by_range(properties, properties + size);
    if (size > 0)
    {
        cout << "Enter revaluation factor: ";
        double factor;
        while (!(cin >> factor))
        {
            cin.clear();
            while (cin.get() != '\n')
                continue;
            cout << "Bad input, try it again: ";
        }
        modify_arr(properties, size, factor);
        show_arr(properties, size);
    }

    return 0;
}

// 计算数组元素的和
int sum_arr(int *arr, int size)
{
    cout << "arr address: " << arr << endl;
    // 这里的arr其实是一个指针(无论形参是`int arr[]`形式, 还是`int *arr`形式`), sizeof将返回指针变量的长度
    // 这也是必须显式传递数组长度size的原因, 因为指针arr并不能指出数组的长度
    // 因此可以对函数说谎, 不告诉函数真正的数组元素个数和起始位置
    cout << "sizeof arr: " << sizeof(arr) << endl;
    int total = 0;
    for (int i = 0; i < size; ++i)
    {
        total += arr[i];
    }
    return total;
}

// 构建数组
// 因为接受数组名参数的函数访问的是原始数组, 所以可以通过函数给数组赋值
int fill_arr(double *arr, int maxsize)
{
    double temp;
    int i;
    for (i = 0; i < maxsize; ++i)
    {
        cout << "Enter value #" << i + 1 << ": ";
        cin >> temp;
        if (!cin) // bad input
        {
            cin.clear();
            while (cin.get() != '\n')
                continue;
            cout << "Bad input, process terminated.\n";
            break;
        }
        else if (temp < 0)
        {
            break;
        }
        arr[i] = temp;
    }

    return i;
}

// 显示数组元素
// 此函数在设计上是不需要修改原始数组的, 所以为了防止意外修改, 可以在声明形参时使用关键字const
// 注意, 此处的const并不意味着原始数据必须是常量, 只是表明在该函数中不能修改这些数据
void show_arr(const double *arr, int size)
{
    cout << "** show arr **\n";
    for (int i = 0; i < size; ++i)
    {
        cout << "property #" << i + 1 << ": $" << arr[i] << endl;
    }
}

// show_arr使用数组区间的版本
void show_arr_by_range(const double *begin, const double *end)
{
    cout << "** show arr by range **\n";
    for (const double *pt = begin; pt != end; ++pt)
    {
        cout << "property #" << pt - begin + 1 << ": $" << *pt << endl;
    }
}

// 修改数组
// 将数组中的每一个元素与同一个因子相乘
void modify_arr(double *arr, int size, double factor)
{
    for (int i = 0; i < size; ++i)
    {
        arr[i] *= factor;
    }
}
```


#### 7.4 函数和二维数组
```c++
// 为编写将二维数组作为参数的函数, 该如何正确的声明指针?

#include "iostream"
void show_2d_arr(int data[][4], int size); // 省略变量名: void show_2d_arr(int[][4], int);

using namespace std;

int main()
{
    // 分析
    // data是一个数组名, 有3个元素, 而每个元素又是由4个int组成的数组
    // 所以data的类型是: int (*data)[4]
    // 另一种格式: int data[][4]
    int data[3][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12},
    };
    show_2d_arr(data, 3);

    return 0;
}

// 此处不能使用const, 因为data是指向指针的指针
void show_2d_arr(int data[][4], int size)
{
    // 第二个参数size指出了data的第一维长度; 而第二维的长度一直是固定的4
    for (int i = 0; i < size; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            cout << data[i][j] << "\t";
        }
        cout << endl;
    }
}
```


#### 7.5 函数和C风格字符串
```c++
// 假设要将字符串作为参数传递给函数, 则表示字符串的方式如下
//     1. char数组
//     2. 字符串字面量
//     3. 对应字符串地址的char指针
// 但是上述3种表达方式再本质上都是char指针, 所以可以将char*作为字符串处理函数的参数

// C风格字符串与常规char数组之间的一个重要区别是: C风格字符串有内置的结束符'\0'
// 这意味着不必将字符串长度作为参数传递给处理函数

#include "iostream"
unsigned int ch_in_str(const char *str, char ch);
char *build_str(char ch, int repeat);

int main()
{
    using namespace std;

    // 将C风格字符串作为函数参数
    char str[] = "maximum & minimum";
    char ch = 'm';
    cout << ch_in_str(str, ch) << " '" << ch << "' counted in '" << str << "'.\n";

    // 返回C风格字符串
    ch = '+';
    char *ps = build_str(ch, 5);
    cout << "\nbuilt_str: " << ps << endl;
    delete[] ps;

    return 0;
}

// 将C风格字符串作为函数参数
// 计算在str中ch出现的次数
unsigned int ch_in_str(const char *str, char ch)
{
    unsigned count = 0;
    while (*str)
    {
        if (*str == ch)
        {
            ++count;
        }
        ++str;
    }
    return count;
}

// 返回C风格字符串
// 在C++中, 函数无法返回字符串, 但是可以返回字符串的指针, 并且这样做效率更高
char *build_str(char ch, int repeat)
{
    // build_str函数结束之后, pstr变量就被回收, 但是使用new分配的是自由存储空间, 可以在main中访问
    // 如此设计的一个弊端是必须在调用函数内手动释放存储空间, 后面将通过构造函数与析构函数解决这个问题
    char *pstr = new char[repeat + 1];
    pstr[repeat] = '\0';
    while (--repeat >= 0)
    {
        pstr[repeat] = ch;
    }
    return pstr;
}
```


#### 7.6 函数和结构
```c++
// 函数与结构
// 与数组不同, 函数可以直接返回结构
// 并且结构名就是结构名, 要获取结构到的地址, 必须使用地址运算符&
// 在函数中, 结构变量的行为更接近于单值变量

// 按值传递结构有一个缺点, 就是当结构非常大时, 复制结构将增加内存需求并降低运行速率
// 由于C语言中不允许按值传递结构, 所以很多C程序员倾向于传递结构的地址
// 然而C++提供了另外一种解决方案: 按引用传递

// 当结构比较小时, 按值传递最为合理

// 传递结构的地址应注意的点
//     1. 调用函数时, 传递的是地址
//     2. 函数头和原型中是结构指针, 如果不想修改, 还应该加上const限定符
//     3. 访问结构体成员时, 应该使用间接成员运算符(->)
//     4. 为了充分利用指针效率, 应该在参数中传递指针, 而不是在返回值中返回一个指针

#include "iostream"
#include "cmath"

using namespace std;

// 表示直角坐标
struct rect
{
    double x;
    double y;
};

// 表示极坐标
struct polar
{
    double distance;
    double angle; // 弧度制
};

void show_polar(polar pos);
void show_polar_by_addr(const polar *pos);
polar rect_to_polar(rect pos);
void rect_to_polar_by_addr(const rect *rpos, polar *ppos);

int main()
{
    // 按值传递 - 直接传递结构
    rect rpos = {3, 4};
    polar ppos = rect_to_polar(rpos);
    show_polar(ppos);

    // 按值传递 - 传递结构的地址
    rpos = {30, 40};
    cout << endl;
    rect_to_polar_by_addr(&rpos, &ppos);
    show_polar_by_addr(&ppos);

    return 0;
}

void show_polar(polar pos)
{
    const double Rad2deg = 180 / 3.1415926;
    cout << "distance: " << pos.distance << ", angle(deg): " << pos.angle * Rad2deg << endl;
}

void show_polar_by_addr(const polar *pos)
{
    const double Rad2deg = 180 / 3.1415926;
    cout << "distance: " << pos->distance << ", angle(deg): " << pos->angle * Rad2deg << endl;
}

polar rect_to_polar(rect pos)
{
    polar result;
    result.distance = sqrt(pos.x * pos.x + pos.y * pos.y);
    result.angle = atan2(pos.y, pos.x);
    return result;
}

// 注意, 这里没有返回polar*, 而是修改已有的结构ppos
void rect_to_polar_by_addr(const rect *rpos, polar *ppos)
{
    ppos->distance = sqrt(rpos->x * rpos->x + rpos->y * rpos->y);
    ppos->angle = atan2(rpos->y, rpos->x);
}
```


#### 7.7 函数和string对象
```c++
// 虽然C风格字符串与string的作用几乎相同, 但是string对象更类似于结构
//     1. 可以将一个string对象赋值给另一个dvxd
//     2. 可以将string对象作为参数传递给函数

// 如果需要多个字符串, 可以声明一个string对象数组, 而不是二维的char数组

#include "iostream"
#include "cstring"

using namespace std;
void display(const string[], int);

int main()
{
    const int Size = 5;
    string neighbors[Size] = {
        "zhangsan",
        "lisi",
        "wangwu",
        "zhaoliu",
        "sunqi",
    };
    display(neighbors, Size);

    return 0;
}

void display(const string sa[], int size)
{
    for (int i = 0; i < size; ++i)
    {
        cout << i + 1 << ": " << sa[i] << endl;
    }
}
```


#### 7.8 函数与array对象
```c++
// 在C++中, 类对象是基于结构的, 因此结构编程方面的考虑因素也适用于类

#include "iostream"
#include "string"
#include "array"

using namespace std;

const int Seasons = 4;
const array<string, Seasons> Season_names = {"Spring", "Summer", "Fall", "Winter"};
typedef array<double, Seasons> expenses;

void display(expenses arr);
void fill(expenses *parr);

int main()
{
    expenses exps;
    fill(&exps);
    display(exps);

    return 0;
}

// 直接传递expenses对象, 效率低
void display(expenses arr)
{
    double total = 0.0;
    cout << "\n== EXPENSES ==\n";
    for (int i = 0; i < Seasons; ++i)
    {
        cout << Season_names[i] << ": $" << arr[i] << endl;
        total += arr[i];
    }
    cout << "total expenses: $" << total << endl;
}

// 传递expenses对象的地址, 提高了效率, 但是数据表示更加复杂了
void fill(expenses *parr)
{
    for (int i = 0; i < Seasons; ++i)
    {
        cout << "Enter " << Season_names[i] << " expense: ";
        cin >> (*parr)[i]; // 没有校验输入的有效性, 因为这里不是重点
    }
}
```


#### 7.9 递归
```c++
// 递归
// 与C言语不同的是, C++不允许main()调用自己

#include "iostream"

using namespace std;
const int Lens = 128;
const int Divs = 8;

void countdown(int n);
void subdivide(char str[], int low, int high, int level);

int main()
{
    countdown(4);

    // 模拟一个直尺
    char ruler[Lens];
    int i;
    for (i = 1; i < Lens - 2; ++i)
        ruler[i] = ' ';
    ruler[Lens - 1] = '\0';
    int max = Lens - 2;
    int min = 0;
    ruler[max] = ruler[min] = '|';
    cout << ruler << endl;
    for (i = 1; i < Divs; ++i)
    {
        subdivide(ruler, min, max, i);
        cout << ruler << endl;

        // reset
        for (int j = 1; j < Lens - 2; ++j)
            ruler[j] = ' ';
    }

    return 0;
}

// 包含单个递归调用的递归
void countdown(int n)
{
    cout << "Count down ... " << n << " at " << &n << endl;
    if (n > 0)
        countdown(n - 1);
    cout << n << ": Kaboom!\n";
}

// 包含多个递归调用的递归
// 这种递归的调用次数将呈几何级数增长, 当递归层次较浅的时候, 这是一种简单且精致的设计
void subdivide(char str[], int low, int high, int level)
{
    // 使用变量level控制递归层数
    if (level == 0 || low == high)
        return;

    int mid = (low + high) / 2;
    str[mid] = '|';
    subdivide(str, low, mid, level - 1);
    subdivide(str, mid, high, level - 1);
}
```


#### 7.10 函数指针
```c++
// 函数指针
// 与数据项类似, 函数也有地址, 是存储其机器语言代码内存的开始地址

// 获取函数的地址
// 函数名就表示对应函数的地址  ==>  注意区分传递的是函数的地址还是函数的返回值

// 声明函数指针
// 应该像函数原型那样指出函数的相关信息, 即返回类型和参数列表(特征标)
//     1. 如果函数原型为: double pam(int);
//     2. 那么对应的函数指针声明方式为: double (*pf)(int);

// 使用指针来调用函数
// 对于声明为`double (*pf)(int);`的函数指针pf, 调用方式有如下两种
//     1. 将(*pf)当成函数即可: (*pf)(5);  ==>  虽然格式不太好看, 但给出了强有力的提示, 当前正在使用函数指针
//     2. C++允许像使用函数名一样直接使用函数指针, 是一种简洁方式: pf(5);

// 使用函数指针的优势
//     1. 有助于之后的开发
//     2. 使在无法接触到某个函数源代码的情况下, 更改其中部分的行为

// 深入函数指针
// 如果有一个函数原型为: const double* f1(const double*, int);
// 那么声明一个对应函数指针的方式应该为: const double* (*pf)(const double*, int);
// 此时可以使用C++11自动类型推断功能: auto pf = f1;
// 如果有多个(例如, 5)该类型的指针需要声明, 为了方便, 可以声明一个函数指针数组, 方式如下
// const double* (*pa[5])(const double*, int);
//     1. 首先, pa是一个数组, 因此有`pa[5]`
//     2. 其次, pa的每一个元素都是一个指针, 因此有`*pa[5]`  ==>  因为[]的优先级比*高, 所以不需要括号
//     3. 最后, 剩余的部分用于确定每个指针元素指向的类型, 在这里是函数, 所以给出特征标和返回类型
//     4. 指的注意的是, 自动类型推断只能用于单值初始化, 不能用于初始化列表, 所以此处不能使用auto; 然而如果在已经声明了pa的情况下, 想要声明一个同类型的pb, 此时是可以使用auto的, 如: auto pb = pa;
//     5. 如何调用呢? 因为pa是一个指针, 同时也是一个包含5个元素的数组, 所以: pa[i]就表示第i个函数指针, 之前的调用方式就可以应用在其上了
//         1. pa[i](arr, 5);
//         2. 或者不嫌麻烦的话: (*pa[i])(arr, 5);
//     6. 又因为此处函数返回const double*, 所以为了取到这个值, 应该这样: double x = *pa[i](arr, 5);
// 再复杂一点
// 如果 auto pc = &pa;
// 那么pc真正的类型声明什么样子的呢?
//     1. 这次, 我们从另一个角度来讲, 因为显然pc是指向pa的, 所以*pc等价于pa
//     2. 所以在pa声明的基础上直接替换即可, 得到: const double* (*(*pc)[5])(const double*, int);
//     3. 如何调用? 显然, (*pc)[i]就是每一个函数指针, 照常使用即可

// 两种表示
//     1. *pa[3]  ==>  pa是一个包含3个元素的数组, 而每个元素都是一个指针
//     2. (*pa)[3]  ==>  (因为*与pa先结合)pa是一个指针, 指向的是包含3个元素的数组

// 数组和数组指针
// 假设pa是一个数组, 那么请注意区分&pa和pa
//     1. 从数值上来讲, &pa和pa是相等的
//     2. 从类型上讲, &pa和pa是不同的
//         1. pa是指向第一个元素的指针, &pa是指向整个数组的指针
//         2. 类型不同, 也意味着进行指针算数时, 移动的字节数是不相同的  ==>  ++pa将指向第2个元素, ++(&pa)将指向整个数组末尾
//     3. 从获取数组第i个元素来讲
//         1. pa直接索引即可, pa[i]
//         2. &pa需要多解除一次引用, (*&pa)[i]

// auto自动类型推断确保变量的类型与赋给它的初始值的类型一致
// 然而, 如果提供的初始值本身就不对(没有这种写法, 例如a为int, 不存在*a), 将导致编译错误

// 使用关于声明的两个技巧来简化代码
//     1. auto
//     2. typedef

#include "iostream"

using namespace std;

void estimate(int lines, double (*pf)(int));
double pam(int lines);
double betsy(int lines);
const double *f1(const double arr[], int n);
const double *f2(const double *arr, int n);
const double *f3(const double *arr, int n);

const int Size = 3;
const double arr[Size] = {1.1, 2.2, 3.3};

// 使用typedef将别名当做标识符声明
// 在之后的代码中都使用别名, 以简化代码
typedef const double *(*p_func[Size])(const double *, int);

int main()
{
    int lines = 65;
    cout << "here's betsy's estimate: ";
    estimate(lines, betsy);
    cout << "here's pam's estimate: ";
    estimate(lines, pam);

    // 深入探究函数指针
    p_func pa = {f1, f2, f3};
    auto pb = &pa; // 使用自动推断
    cout << endl;
    for (int i = 0; i < Size; ++i)
    {
        cout << "function call #" << i + 1 << endl;
        cout << "    addr:  " << (*pb)[i](arr, 0) << endl;
        cout << "    value: " << *(**(*pb + i))(arr, 0) << endl; // 故意写得复杂
        // value值的写法
        // 1. 最简式: *(*pb)[i](arr, 0)
        // 2. *pb是一个数组, 本身也是一个指针, 不使用下标索引: *(*(*pb + i))(arr, 0)
        // 3. 通过函数指针调用函数, 不使用简写形式: *(**(*pb + i))(arr, 0)
    }

    return 0;
}

void estimate(int lines, double (*pf)(int))
{
    cout << lines << " will take " << pf(lines) << " second(s).\n";
}

double pam(int lines)
{
    return 0.03 * lines + 0.0004 * lines * lines;
}

double betsy(int lines)
{
    return 0.05 * lines;
}

// 出于演示的目的, f1-f3的函数体都很简单
const double *f1(const double arr[], int n)
{
    return arr;
}

const double *f2(const double *arr, int n)
{
    return arr + 1;
}

const double *f3(const double *arr, int n)
{
    return arr + 2;
}
```


### 第八章: 函数探幽
#### 8.1 C++内联函数
```c++
// C++内联函数是为了提高程序运行速度所做的一项改进
// 常规函数与内联函数的区别不在于编写方式, 而在于C++编译器如何将它们组合到程序中
// 对于内联代码, 编译器使用相应的函数代码替换函数调用, 程序无需跳到另一个位置执行函数代码, 之后再跳回来
// 因此执行速度比常规函数稍快, 但代价是更多的内存
// 如果程序在10个不同的地方调用同一个内联函数, 那么程序将包含该内联代码的10个副本

// 何时使用内联函数?
// 相对于处理函数调用机制, 执行函数本身的时间较短, 并且该函数经常被调用

// 如何使用?
//     1. 在函数声明前加上关键字inline
//     2. 在函数定义前加上关键字inline
//     3. 调用内联函数和常规函数一样
// 通常的做法是省略函数原型, 之后将整个定义放在本应该提供原型的地方
// 并非没有原型, 而是整个函数定义充当了原型

// 值得注意的是, 请求将函数作为内联函数时, 编译器并不一定会满足, 可能的情况如下
//     1. 编译器可能认为函数过大
//     2. 函数调用了自己(内联函数不能递归)
//     3. 编译器没有启用或实现内联函数的特性

// 内联函数与宏
// C语言通过预处理器指令#define来提供宏
// 例如一个计算平方的宏为: #define SQUARE(X) X*X
// 这并不是通过传递来实现的, 而是通过文本替换实现的, 例如SQUARE(1 + 2)将被替换为1 + 2 * 1 + 2, 显然它并不能按照预期那样工作

#include "iostream"

inline double square(double x) { return x * x; }

int main()
{
    using namespace std;
    for (int i = 1; i < 10; ++i)
    {
        cout << "the square of " << i << " is: " << square(i) << endl;
    }

    return 0;
}
```


#### 8.2 引用变量
```c++
// 引用(reference)是已定义变量的别名
// 引用的主要作用是作为函数的形参, 让函数可以使用原始数据
// 如此, 除了指针之外, 引用也为处理大型数据提供了一种方便的途径

// 创建引用变量
// int a;
// int &b = a;  ==>  将b声明为a的引用, 注意此处的&不是地址运算符, 而是类型标识符int&的一部分
// 引用类似于const指针
//     1. 必须在声明引用的同时进行初始化
//     2. 一旦与某个变量关联, 将无法更改; 如果试图将另一个变量赋值给引用, 这仅仅是普通的赋值, 而不会修改引用的关系  ==>  换言之, 可以通过初始化来设置引用关系, 但是不能通过赋值来设置
//     3. 对比与const指针, 引用隐式的有一个解除引用操作

// 将引用用作函数参数(按引用传递)
// 用法演示: tp func(int &a)
// 按引用传递和按值传递在函数调用的时候看起来是一样的, 只能通过原型或者定义来区分
// 运算符&使得按地址传递在函数调用的时候, 可以清晰的识别出传递的是一个地址
// 引用是在函数调用的时候, 使用实参进行初始化的

// 引用的属性和特别之处
// 如果不想修改原始信息, 同时又想使用引用(数据规模较大), 则应该使用const引用, 如: double sqaure(const double &x);
// 如果引用参数是const, 则编译器将在下面两种情况生成临时变量, 而引用则作为该临时变量的别名, 并且这些临时变量仅存在于函数调用期间
//     1. 实参类型正确, 但不是左值
//     2. 实参类型不正确, 但可以转换为正确的类型
// 应该尽可能的使用const引用
//     1. 可以避免无意间修改原始数据
//     2. 能够处理const和非const实参, 否则将只能够接收非const数据
//     3. 能够正确生成并使用临时变量, 使得函数在处理参数种类方面更通用
// 左值: 是可被引用的数据对象, 例如: 变量, 数组元素, 结构成员, 引用, 解除引用的指针
// C++11新增了右值引用, 使用&&声明; 后面将详细讨论

// 将引用用于结构
// 为什么要返回引用?
//     1. 传统的按值返回机制, return后面的值被复制到一个临时位置, 而调用程序将使用它们
//     2. 对于函数调用x = accumulate(y);
//         1. 如果返回的是一个结构, 那么首先将把整个结构复制到一个临时位置, 之后再将这个拷贝复制给x
//         2. 如果返回的是一个引用, 那么将直接把结果复制给x, 效率更高
//     3. 值得注意的是, 返回引用的函数实际上是被引用变量的别名  ==>  所以, 该函数实际上是可以作为左值的
// 返回引用时需要注意的问题
//     1. 最重要的一点: 应该避免返回函数终止时, 不再存在的内存单元的引用; 如何避免呢?
//         1. 返回一个作为参数传递给函数的引用
//         2. 使用new分配新的存储空间
// 引用返回类型需要添加const限定吗?  ==>  看需求
//     1. 如果不希望返回值被修改或者说不希望函数整体作为左值, 那么就添加const限定
//     2. 为了减少犯错的可能性, 在没有明确是否需要const时, 通常加上const限定更好

// 将引用用于类对象
// 将类对象传递给函数时, C++通常的做法都是使用引用

// 对象, 继承和引用
// 1. 派生类继承了基类的方法
// 2. 基类引用可以指向派生类对象, 而无需强制类型转换

// 何时使用引用参数?
// 总览
//     1. 需要修改调用函数中的数据对象
//     2. 当数据对象较大时, 通过传递引用提高程序的运行速度
// 对于仅使用而作修改原始数据的函数
//     1. 如果数据对象很小(内置类型或小型结构)   ==>  按值传递
//     2. 如果数据对象是数组                    ==>  使用const指针, 因为C++的函数不能传递数组
//     3. 如果数据对象是较大的结构              ==>  使用const指针或const引用
//     4. 如果数据对象是类对象                  ==>  使用const引用, 因为类设计的语义常常要求使用引用
// 对于需要修改原始数据的函数
//     1. 如果数据对象是内置数据类型   ==>  使用指针
//     2. 如果数据对是是数组          ==>  只能使用指针
//     3. 如果数据对象是结构          ==>  使用指针或引用
//     4. 如果数据对象是类对象        ==>  使用引用
// 当然, 上面的这些仅仅是指导原则, 如果有充分的理由, 完全可以做出其它的选择, 例如: cin对基本类型使用引用, 以便可以使用 cin >> x;

#include "iostream"
#include "fstream"
#include "cstring"
#include "cstdlib"

struct free_throws
{
    std::string name;
    int made;
    int attempts;
    float percent;
};

void swap_by_ref(int &a, int &b);
void swap_by_pt(int *pa, int *pb);
void display(const free_throws &ft);
void set_percent(free_throws &ft);
free_throws &accumulate(free_throws &target, const free_throws &source);
free_throws &clone(free_throws &ft);
void file_it(std::ostream &out, double fo, const double fe[], int n);

int main()
{
    using namespace std;

    // 创建引用变量
    int x = 10;
    int *px = &x; // 指针
    int &rx = x;  // 引用, 须在声明引用的同时进行初始化
    // x, *px, rx是可以互换的
    cout << "x: " << x << "\n*px: " << *px << "\nrx: " << rx << endl;
    // &x, px, &rx是可以互换的
    cout << "&x: " << &x << "\npx: " << px << "\n&rx: " << &rx << endl;

    // 按引用传递
    int a = 10;
    int b = 20;
    cout << "\nfirstly, a = " << a << ", b = " << b << endl;
    swap_by_ref(a, b);
    cout << "now, a = " << a << ", b = " << b << endl;
    swap_by_pt(&a, &b);
    cout << "now, a = " << a << ", b = " << b << endl;

    // 右值引用
    double radius = 2.0;
    double &&area = 3.1415926 * radius * radius;
    cout << "\narea = " << area << endl;

    // 将引用用于结构
    free_throws one = {"Ifelsa Branch", 13, 14};
    free_throws two = {"Andor Knott", 10, 16};
    free_throws three = {"Minnie Max", 7, 9};
    free_throws dup;
    cout << endl;
    set_percent(one);
    display(one);
    accumulate(two, one);
    display(two);
    accumulate(accumulate(three, one), two);
    display(three);
    dup = accumulate(three, two);
    display(dup);
    free_throws &ft_copy = clone(one);
    display(ft_copy);
    delete &ft_copy;

    // 基类引用
    ofstream fout;
    const char filepath[] = "ep-data.txt";
    fout.open(filepath);
    if (!fout.is_open())
    {
        cout << "can't open file: " << filepath << endl;
        exit(EXIT_FAILURE);
    }
    double fo = 1800;
    const int Size = 5;
    double fe[Size] = {30, 19, 14, 8.8, 7.5};
    cout << endl;
    file_it(fout, fo, fe, Size);
    file_it(cout, fo, fe, Size);

    return 0;
}

// 交换两个变量的值, 通过引用实现
void swap_by_ref(int &a, int &b)
{
    int temp = a;
    a = b;
    b = temp;
}

// 交换两个变量的值, 通过指针实现
void swap_by_pt(int *pa, int *pb)
{
    int temp = *pa;
    *pa = *pb;
    *pb = temp;
}

void display(const free_throws &ft)
{
    using std::cout;
    using std::endl;
    cout << "name: " << ft.name << "\n  made: " << ft.made << "  attempts: " << ft.attempts << "  percent: " << ft.percent << endl;
}

void set_percent(free_throws &ft)
{
    if (ft.attempts != 0)
    {
        ft.percent = 100.0f * float(ft.made) / float(ft.attempts);
    }
    else
    {
        ft.percent = 0;
    }
}

// 返回引用
free_throws &accumulate(free_throws &target, const free_throws &source)
{
    target.attempts += source.attempts;
    target.made += source.made;
    set_percent(target);
    return target;
}

free_throws &clone(free_throws &ft)
{
    free_throws *pt = new free_throws;
    *pt = ft;
    return *pt;
}

// fo: 物镜焦距
// fe: 目镜焦距
// n: 数组fe的长度
// 对于该程序而言, 最重要的一点是: 参数out可以指向ostream对象, 也可以指向ofstream对象
void file_it(std::ostream &out, double fo, const double fe[], int n)
{
    using std::endl;
    using std::ios_base;

    ios_base::fmtflags initial = out.setf(ios_base::fixed);
    out.precision(0);
    out << "Focal length of objective: " << fo << " mm\n";
    out.setf(ios_base::showpoint);
    out.precision(1);
    out.width(12);
    out << "f.l. eyepiece";
    out.width(15);
    out << "magnification" << endl;
    for (int i = 0; i < n; ++i)
    {
        out.width(12);
        out << fe[i];
        out.width(15);
        out << int(fo / fe[i] + 0.5) << endl;
    }
    out.setf(initial); // 恢复初始格式化设置
}
```


#### 8.3 默认参数
```c++
// 如何设置默认值?  ==>  在函数原型中将默认值赋给参数即可, 而函数定义不变
// 注意事项:
//     1. 对于具有默认值的参数, 它右边的参数也必须提供默认值

#include "iostream"
#include "cstring"

char *left(const char *str, int n = 1);

int main()
{
    using namespace std;
    const int Size = 80;
    char sample[Size] = "hello world!";
    char *ps = left(sample, 5);
    cout << "ps: " << ps << endl;
    delete[] ps;
    ps = left(sample);
    cout << "ps: " << ps << endl;
    delete[] ps;

    return 0;
}

char *left(const char *str, int n)
{
    if (n < 0)
    {
        n = 0;
    }
    int len = std::strlen(str);
    n = (n < len) ? n : len;
    char *pt = new char[n + 1];
    int i;
    for (i = 0; i < n; ++i)
    {
        pt[i] = str[i];
    }
    while (i <= n)
    {
        pt[i++] = '\0';
    }
    return pt;
}
```


#### 8.4 函数重载
```c++
// 默认参数, 使程序员可以使用不同数目的参数调用同一个函数
// 函数重载, 亦即函数多态, 使程序员可以使用多个同名的函数

// 术语"多态"指的是有多种形式, 因此函数多态允许函数有多种形式
// 术语"函数重载"指的是可以有多个同名的函数, 因此对名称进行了重载
// 这两个术语指的是等价的, 通常习惯使用"函数重载"

// 就像一个单词在不同的语境有不同的含义
// C++根据上下文来确定要使用的重载函数版本

// C++函数重载的关键是参数列表(又称特征标, 或函数签名), 如果参数数目或参数类型不同(变量名无关紧要), 则特征标不同
//     ps: 强调, 关键是特征标, 跟变量名和返回类型没关系
// 使用被重载的函数时, 需要在函数调用时传入正确的参数类型; 因为C++会尝试使用标准类型转换强制进行匹配, 如果在多个重载函数的版本中, 存在多种可能得转换(即有歧义), 则C++将拒绝这种函数调用, 将其视为错误
// 为了避免函数匹配时出现歧义
//     1. 编译器会把类型引用和类型本身视为相同的特征标

// 重载引用参数
// 下面有3个版本的重载函数
//     1. void pick(int &x1);        ==> 匹配非const左值
//     2. void pick(const int &x2);  ==> 匹配非const左值, const左值, 右值  ==> 这也是之前提到过的推荐版本, 因为它的通用性更好
//     3. void pick(int &&x3);       ==> 匹配右值
// 注意到与x1或x3匹配的参数, 同时也匹配x2, 此时, 将使用最匹配的版本
// 如此, 将能够根据参数是非const左值, const左值, 右值来定制函数的行为

// 何时使用函数重载?
//     1. 几个函数基本上执行相同的任务, 但使用不同形式的数据, 方可使用函数重载
//     2. 如果可以通过默认参数实现同样的目的, 则优先使用默认参数; 如果需要使用不同类型的参数, 则默认参数就不管用了, 需要使用函数重载

// C++是如何跟踪重载函数的呢?
// 使用的技术是名称修饰(name decration), 又称为名称矫正(name mangling)
// 编译器根据函数的特征标对每个函数进行加密, 作为内部表示

#include "iostream"
#include "cstring"

char *left(const char *str, unsigned n);
unsigned long left(unsigned long num, unsigned int n);

int main()
{
    using namespace std;
    const char str[] = "hello world!";
    char *ps = left(str, 5);
    cout << "ps: " << ps << endl;
    delete[] ps;
    unsigned long num = left(114514, 3);
    cout << "num: " << num << endl;

    return 0;
}

// 返回字符串str的前n个字符
char *left(const char *str, unsigned n)
{
    int len = std::strlen(str);
    n = (n < len) ? n : len;
    char *pt = new char[n + 1];
    pt[n] = '\0';
    for (int i = 0; i < n; ++i)
        pt[i] = str[i];
    return pt;
}

// 返回整数的前n位
unsigned long left(unsigned long num, unsigned int n)
{
    unsigned digits = 1;
    unsigned long temp = num;
    if (n == 0 || num == 0)
        return 0;

    // 计算num的总位数
    while (temp /= 10)
        ++digits;

    // 截掉多余的数位
    if (digits > n)
    {
        digits -= n;
        while (digits--)
            num /= 10;
    }
    return num;
}
```


#### 8.5 函数模板
```c++
// 函数模板是通用的函数描述, 使用泛型来定义函数
// 通过将具体类型作为参数传递给模板, 使编译器生成该类型的函数
// 因为模板使用了泛型, 因此有时也被称为通用编程
// 因为类型是用参数表示的, 所以模板特性有时也被称为参数化类型(parameterized types)

// 语法: template <typename T> ...
// 后面跟正常函数定义, 类型使用T(只是一个标识符名称, 通常用T)
// 注意: 在C++98天假关键字typename之前, 使用的是关键字class, 在这种上下文中, 它们两个是等价的; 如果不考虑向后兼容, 则应该使用关键字typename
// 如何使用?
//     1. 提供模板函数原型
//     2. 定义模板函数
//     3. 像常规函数一样, 调用模板函数即可  ==>  编译器会检查所使用的参数类型, 并生成相应的函数

// 使用模板提高程序执行速度
// 最终的代码不包含任何模板, 而是包含了为程序生成的实际函数, 就像以手工方式定义的一样
// 使用模板的好处是: 使生成等多个函数定义更简洁, 更可靠

// 重载的模板
// 如果需要多个对不同类型使用同一种算法的函数, 可以使用模板
// 然而, 并非所有类型都使用相同的算法, 为满足这种需求, 可以像常规函数那样, 重载模板定义

// 模板的局限性
// 模板函数很可能无法处理某些类型
// 一些操作在特定的类型上是无效的, 但是在实际应用场景中是有意义的, 比如两个坐标(通过结构表示)相加, 有两种解决方法
//     1. 运算符重载
//     2. 为特定类型提供具体化的模板定义  ==>  显式具体化(explicit specialization)

// 显式具体化
// 当编译器找到与函数调用匹配的具体化定义时, 将使用该定义, 而不再寻找模板
//     1. 对于给定的函数名, 可以有非模板函数, 模板函数和显式具体化模板函数, 以及它们的重载版本
//     2. 显式具体化的原型和定义应该以`template<>`打头, 并通过名称来指出类型
//     3. 优先级: 非模板函数 > 具体化模板 > 常规模板

// 实例化与具体化
// 在代码中包含函数模板本身并不会生成函数定义, 它只是一种用于生成函数定义的方案
// 编译器如果使用模板为特定类型生成函数定义时, 得到的是模板实例(instantiation)
// 两种实例化方式
//     1. 隐式: 由函数调用触发  ==>  如: swap(i, j);
//     2. 显式: 直接命令编译器创建特定的实例
//         1. 方式一: 定义函数时用<>标识类型, 并在声明前加上关键字template  ==>  如: template void swap<int>(int, int);
//         2. 方式二: 函数调用时, 在函数名后面加<类型>  ==<  如: swap<int>(i, j);
// 两种显式具体化的声明
//     1. template<> void swap<int>(int &a, int &b);
//     2. template<> void swap(int &a, int &b);
// 显式实例化和显式具体化的区别
//     1. 显式具体化并不生成函数定义, 而显式实例化会
//     2. 显式具体化的关键字template后面有一对尖括号<>, 而显示实例化没有
// 在同一个文件中, 同时使用同一种类型的显示实例化和显式具体化会导致编译报错
// 隐式实例化, 显式实例化, 显式具体化统称为具体化, 它们的共同之处在于, 都是使用具体类型的函数定义, 而不是通用描述

// 重载解析(overloading resolution)
// step1: 创建候选函数列表, 其中包括与被调函数名称相同的函数和模板函数
// step2: 使用候选函数列表创建可行函数列表  ==>  参数数目正确, 并且参数类型可以隐式转换为正确类型的函数
// step3: 确定最佳可行函数, 如果有就使用, 否则该函数调用出错
// 从最佳到最差的顺序
//     1. 完全匹配, 但常规函数优先级高于模板函数
//     2. 需要提升转换
//     3. 需要标准转换
//     4. 需要执行用户定义的转换
// 详细知识参考高级教程

// 模板函数的发展
// 关键字decltype
//     1. 在模板中如果有类型为T1的变量x, 类型为T2的变量y, 那么如何确定x+y的类型?
//     2. decltype(a)声明了一种类型, 这种类型与a的类型相同
//     3. 所以前面的问题得到了解决: decltype(x+y) xy = x + y;
// 后置返回类型
//     1. 同decltype面临的问题一样, 如果需要返回x+y, 则应该如何确定类型
//     2. 因为此时还没有x和y, 所以无法使用decltype
//     3. 在这种情况下, 使用auto充当占位符, 并将真正的返回类型放在后面即可  ==>  如: auto add(x, y) -> decltype(x+y);

#include "iostream"

struct job
{
    char name[40];
    double salary;
    int floor;
};

template <typename T>
void swap(T &a, T &b);

template <typename T>
void swap(T *a, T *b, int size);

template <>
void swap<job>(job &a, job &b); // <job>是可选的, 因为参数类型已经表明这是一个job的具体化
// void swap(job &a, job &b);

template <typename T>
void show_arr(T *pa, int size);

void show_job(const job &j);

int main()
{
    using std::cout;
    using std::endl;

    // int
    int i = 10;
    int j = 20;
    cout << "before swap: i = " << i << ", j = " << j << endl;
    swap(i, j);
    cout << "after swap: i = " << i << ", j = " << j << endl;

    // double
    double x = 3.1415926;
    double y = 2.7182818;
    cout << "\nbefore swap: x = " << x << ", y = " << y << endl;
    swap(x, y);
    cout << "after swap: x = " << x << ", y = " << y << endl;

    // 模板重载
    const int Size = 6;
    int arr1[Size] = {1, 1, 4, 5, 1, 4};
    int arr2[Size] = {3, 1, 4, 1, 5, 9};
    cout << "\nbefore swap:\n";
    cout << "  arr1:\n";
    show_arr(arr1, Size);
    cout << "  arr2:\n";
    show_arr(arr2, Size);
    swap(arr1, arr2, Size);
    cout << "after swap:\n";
    cout << "  arr1:\n";
    show_arr(arr1, Size);
    cout << "  arr2:\n";
    show_arr(arr2, Size);

    // 显式具体化
    job zhangsan = {"zhangsan", 3000, 3};
    job lisi = {"lisi", 2500, 2};
    cout << "\nbefore swap:\n";
    show_job(zhangsan);
    show_job(lisi);
    swap(zhangsan, lisi);
    cout << "after swap:\n";
    show_job(zhangsan);
    show_job(lisi);

    return 0;
}

// 交换两个参数的值
template <typename T>
void swap(T &a, T &b)
{
    T temp = a;
    a = b;
    b = temp;
}

// 交换两个数组个元素的值
template <typename T>
void swap(T *a, T *b, int size)
{
    T temp;
    for (int i = 0; i < size; ++i)
    {
        temp = a[i];
        a[i] = b[i];
        b[i] = temp;
    }
}

// 显式具体化
template <>
void swap<job>(job &a, job &b)
{
    // 需求: 对于job, 只交换salary和floor两个成员
    double temp_salary = a.salary;
    int temp_floor = a.floor;
    a.salary = b.salary;
    b.salary = temp_salary;
    a.floor = b.floor;
    b.floor = temp_floor;
}

// 控制台显示数组的各个元素
template <typename T>
void show_arr(T *pa, int size)
{
    using std::cout;
    using std::endl;
    for (int i = 0; i < size; ++i)
        cout << "    [" << i << "]: " << pa[i] << endl;
}

void show_job(const job &j)
{
    using std::cout;
    using std::endl;
    cout << "  " << j.name << ": \n";
    cout << "    salary: " << j.salary << endl;
    cout << "    floor: " << j.floor << endl;
}
```


### 第九章: 内存模型和名称空间
#### 9.1 单独编译
##### main.cpp
```c++
// 头文件中常包含的内容
//     1. 函数原型
//     2. 使用#define或const定义的符号常量
//     3. 结构声明
//     4. 模板声明
//     5. 内联函数

// 包含头文件时, 使用双引号和尖括号的区别
//     1. 尖括号: C++编译器将在存储标准头文件的主机系统的文件系统中查找
//     2. 双引号: C++编译器将首先在当前工作目录或源代码目录中查找, 如果没有找到, 然后才在标准位置查找

// 在IDE中, 不要将头文件加入到项目列表(#include指令管理头文件), 也不要使用#include包含源代码文件(将导致多重声明)
// 在同一个文件中, 只能将同一个头文件包含一次

// 因为C++允许不同的编译器实现不同的名称修饰方式, 所以不同的编译器生成的二进制模块可能无法正确的链接

#include "coordinate.h"

int main()
{
    rect rpos = {3, 4};
    polar ppos = rect_to_polar(rpos);
    show_polar(ppos);

    return 0;
}
```


##### source/coordinate.cpp
```c++
#include <iostream>
#include <cmath>
#include "coordinate.h"

polar rect_to_polar(rect rpos)
{
    using std::atan2;
    using std::sqrt;
    polar ppos;
    ppos.distance = sqrt(rpos.x * rpos.x + rpos.y * rpos.y);
    ppos.angle = atan2(rpos.y, rpos.x);
    return ppos;
}

void show_polar(polar ppos)
{
    using std::cout;
    using std::endl;
    const double Rad_to_deg = 180.0 / 3.1415926;
    cout << "distance = " << ppos.distance << "\tangle(deg) = " << ppos.angle * Rad_to_deg << endl;
}
```


##### include/coordinate.h
```c++
// #ifndef + #define两条预处理器指令用于避免多次包含同一个头文件
// #ifndef COORDINATE_H_ 指出仅当COORDINATE_H_变量没有被声明时, 才处理后面的内容
#ifndef COORDINATE_H_
#define COORDINATE_H_

struct polar
{
    double distance;
    double angle; // 弧度制
};

struct rect
{
    double x;
    double y;
};

polar rect_to_polar(rect rpos);
void show_polar(polar ppos);

#endif
```


#### 9.2 存储持续性、作用域和链接性
##### main.cpp
```c++
// C++使用3种(C++11又新增1种)不同的方案存储数据  ==>  区别在于数据保留在内存中的时间
//     1. 自动存储持续性  ==>  在函数定义中声明的变量或函数参数是自动的; 在开始执行函数时被创建, 在结束执行函数时被释放
//     2. 静态存储持续性  ==>  在函数外或使用关键字static定义的变量是静态的; 在程序的整个运行过程中都存在
//     3. 动态存储持续性  ==>  使用new运算符分配的内存是动态的; 直到使用delete运算符释放或程序结束(由OS释放)为止, 有时也被称为自由存储或堆
//     4. 线程存储持续性  ==>  (C++11)使用thread_local声明的变量, 其声明周期和所属线程一样长

// 作用域和链接性
// 作用域(scope): 描述了名称如何在文件中共享
// 链接性(linkage): 描述了名称如何在不同文件之间共享  ==>  链接性为外部的可在文件间共享, 链接性为内部的只能在该文件中共享
// 自动变量没有链接性, 因此不能共享
// C++变量作用域的类型
//     1. 局部作用域: 只在定义它的代码块中可用  ==>  自动变量的作用域为局部
//     2. 全局作用域(文件作用域): 从定义位置到文件结尾之间都可用
//     3. 函数原型作用域: 在函数原型中使用的名称只在包含参数列表的括号内可见  ==>  这就是函数原型中变量名称是否使用, 以及是否与定义相同都不重要的原因
//     4. 类作用域: 在类中声明的成员的作用域为整个类
//     5. 名称空间作用域: 在名称空间中声明的作用域, 为整个名称空间  ==>  全局作用域是名称空间作用域的特例

// 自动存储持续性
// 在函数中声明函数参数和变量的存储持续性是自动的, 作用域是局部的,
// 执行到代码块时, 将为变量分配内存, 但其作用域的起点是声明的位置  ==>  意思是在代码块开始时统一分配内存, 然而直到变量的声明位置, 该变量都不可用
// 在C++11中auto用于自动类型推断, 但在这之前, auto的含义截然不同, 它用于显式的指出变量为自动存储
// 初始化: 可以使用任何在声明时, 其值为已知的表达式来初始化自动变量
// 自动变量和栈
//     1. 程序使用两个指针来跟踪栈, 一个指向栈底(开始位置), 另一个指向栈顶
//     2. 函数开始时, 自动变量被加入到栈, 并且栈顶指针更新到下一个可用内存单元
//     3. 函数结束时, 栈顶指针被重置为调用函数之前的值, 从而释放内存
// 寄存器变量: 关键字register最初由C语言引入, 它建议编译器使用CPU寄存器来存储自动变量, 旨在提高访问速度; 但是在C++11之后, 该关键字失去了作用, 仅作为保留字, 避免使用该关键字的现有代码非法

// 静态存储持续性
// C++为静态变量提供3种链接性
//     1. 外部链接性: 必须在代码块外面声明  ==>  简称外部变量, 也称全局变量
//     2. 内部链接性: 必须在代码块外部声明, 并使用static限定符  ==>  内部静态变量会隐藏同名的外部变量, 且不必担心与其它文件中同名的静态内部变量冲突
//     3. 无链接性: 必须在代码块内部声明, 并使用static限定符
// 由于静态变量存在于整个程序运行期间, 并且数目是不变的, 所以不需要特殊的装置(如栈)来管理, 编译器将为其分配固定的内存来存储所有的静态变量
// 静态初始化(编译阶段)
//     1. 零初始化: 未被初始化的静态变量, 编译器将所有的位都设置成0
//     2. 常量表达式初始化
// 动态初始化(运行阶段)
// 整个初始化过程
//     1. 首先进行零初始化
//     2. 如果提供了显式的初始化表达式; 则
//         1. 编译器尝试进行常量初始化, 必要时进行简单计算
//         2. 如果没有足够的信息(如表达式中有函数调用), 那么就进行动态初始化
// C++11增加了关键字constexpr, 提供了新的创建常量表达式的方式
// 定义声明和引用声明
//     1. 一方面, 在每个使用外部变量的文件中都必须声明该变量
//     2. 另一方面, C++单规则定义指出, 变量只能有一次定义
//     3. 为满足这种需求, C++提供了2种变量声明方式
//         1. 定义声明: 给变量分配存储空间
//         2. 引用声明: 引用已有变量, 而不分配存储空间  ==>  语法: 使用关键字extern且不进行初始化
//     4. 在多文件程序中, 可以在1个且只能是1个文件中定义1个外部变量, 使用该变量的其它文件必须使用关键字extern声明它
// C++使用作用域解析运算符"::", 放在变量名前面表示使用变量的全局版本
// 如果初始化了静态局部变量, 则程序只在启动时初始化一次, 之后再调用函数时, 不会像自动变量那样再次被初始化

// C++存储说明符
//     1. register(C++11中, 只是显式的指出变量是自动的)
//     2. static
//     3. extern
//     4. thread_local(C++11新增)
//     5. mutable: 用于指出即使某个结构(类)变量为const, 其成员也可以被修改
//     ps: 在同一个声明中, 不能使用多个说明符(thread_local除外)
// cv-限定符
//     1. const
//     2. volatile: 即是程序代码没有对内存进行任何修改, 其值也可能发生变化  ==>  如将指针指向某个硬件位置, 它包含了串口信息, 此时硬件可能修改其中的内容  ==>  该关键字主要是为了改善编译器优化

// const
// 在C++中, const全局变量的链接性为内部, 相当于默认使用了static说明符, 如: static const int data;
// const的内部链接性还意味着, 每个文件都有自己的一组常量, 而不是所有文件共享一组常量  ==>  这样, 就可以将常量定义放在头文件, 需要的源代码文件只要包含该头文件即可
// 如果出于某种原因, 希望常量的链接性为外部, 则可以使用extern关键字来覆盖这种行为, 如: extern const int data;

// 函数和链接性
// C++不允许在一个函数(或代码块)中定义另一个函数, 因此所有函数的存储持续性都为静态
// 在默认情况下, 函数的链接性为外部  ==>  实际上可以再函数原型中使用关键字extern来指出函数是在另一个文件中定义的, 不过这是可选的
// 要将函数的链接性设置为内部, 必须同时在函数的原型和定义中使用关键字static
// 单定义规则也适用于非内联函数
// C++在哪里搜索函数定义
//     1. 如果原型指出该函数是static, 则编译器只在该文件中查找, 否则
//     2. 编译器在所有程序文件中查找, 否则
//     3. 编译器在库文件中查找
// 如果定义了一个与库函数同名的函数, 则使用程序员定义的版本  ==>  然而, 通常情况下程序员不应该使用标准库函数的名称

// 语言链接性
// 连接程序要求不同的函数有不同的符号名, 而C和C++在内部可能使用不同的方式来表示这个符号名
// 所以, 如果C++程序要使用C库中预编译的函数, 应该如何做呢?  ==>  答案是在函数原型中指定, 如
//     1. extern "C" void spiff(int);
//     2. extern void spiff(int);
//     3. extern "C++" void spiff(int);  ==>  默认使用的就是C++语言链接性, 显式的指出来也可以

// 存储方案和动态分配
// 通常, 编译器使用3块独立的内存, 分别用于存储: 静态变量, 自动变量, 动态变量
// 虽然之前的5种存储方案(自动, 静态外部/内部/局部, 语言链接性)不适用于动态内存, 但是可以用来跟踪动态内存的自动/静态指针变量

// 使用new运算符的初始化
//     1. C++98
//         1. 内置标量类型: double *pi = new double(3.14);
//     2. C++11
//         1. 常规结构或数组
//             1. person *zhangsan = new person{"张三", 18, true};
//             2. int *arr = new int[4]{1, 2, 3, 4};
//         2. 单值变量: double *pi = new double{3.14};
// new运算符失败, 将引发异常std::bad_alloc
// 定位new运算符
//     1. 不跟踪哪些内存被使用, 也不查找哪些内存未使用, 而是将这一任务交给程序员
//     2. 因为delete只能用于指向常规new运算符分配的堆内存, 所以:
//         1. 如果定位new指定的位置是在堆内存, 则可以使用delete释放
//         2. 否则, 不能使用delete释放

#include <iostream>
#include <new>
using namespace std;

double warming = 0.3;
int tom = 3;
int dick = 30;
static int harry = 300;

void auto_var();
void update(double dt);
void local();
void remote_access();
void strcount(const char *str);

int main()
{
    auto_var();

    // 静态存储持续性 + 外部链接性
    cout << "\nglobal warming is " << warming << " degrees.\n";
    update(0.1);
    cout << "global warming is " << warming << " degrees.\n";
    local();
    cout << "global warming is " << warming << " degrees.\n";

    // 静态存储持续性 + 内部链接性
    cout << "\nmain() reports the following address:\n";
    cout << "&tom = " << &tom << endl;
    cout << "&dick = " << &dick << endl;
    cout << "&harry = " << &harry << endl;
    remote_access();

    // 静态存储持续性 + 无链接性
    char str1[] = "hello world!";
    char str2[] = "wutieshan jia you";
    cout << endl;
    strcount(str1);
    strcount(str2);

    // 定位new运算符
    const int BUF_SIZE = 512;
    const int N = 5;
    static char buffer[BUF_SIZE];
    double *pd1, *pd2;
    int i;
    pd1 = new double[N];
    pd2 = new (buffer) double[N]; // 定位new
    for (i = 0; i < N; i++)
        pd1[i] = pd2[i] = 1000 + 20.0 * i;
    cout << "\nmemory addr:\n";
    cout << "heap: " << pd1 << endl;
    cout << "static: " << (void *)buffer << endl;
    cout << "memory content:\n";
    for (i = 0; i < N; i++)
    {
        cout << pd1[i] << " at " << pd1 + i << ";\t";
        cout << pd2[i] << " at " << pd2 + i << endl;
    }
    delete[] pd1;
    // delete[] pd2; // 不能这么做, 因为buffer对应的是静态内存, 不再delete的管辖范围之内

    return 0;
}

void auto_var()
{
    int x = 1;
    cout << "(1)x = " << x << ", &x = " << &x << endl;
    {
        cout << "(2)x = " << x << ", &x = " << &x << endl;
        int x = 2;
        cout << "(3)x = " << x << ", &x = " << &x << endl; // 新定义的x隐藏了之前旧的x, 外部的x暂时不可见
    }
    cout << "(4)x = " << x << ", &x = " << &x << endl;
}

void strcount(const char *str)
{
    static int total = 0;
    int count = 0;
    cout << "\"" << str << "\" contains:";
    while (*str++)
        count++;
    total += count;
    cout << "characters: " << count << endl;
    cout << "total characters: " << total << endl;
}
```


##### support.cpp
```c++
#include <iostream>

extern double warming;
extern int tom;
static int dick = 10;
int harry = 200;

void update(double dt);
void local();
void remote_access();

void update(double dt)
{
    using std::cout;
    warming += dt;
    cout << "update warming to " << warming << " degrees.\n";
}

void local()
{
    using std::cout;
    double warming = 0.8; // 隐藏全局变量warming
    cout << "local warming = " << warming << " degrees.\n";
    cout << "global warming = " << ::warming << " degrees.\n"; // 访问全局变量
}

void remote_access()
{
    using std::cout;
    using std::endl;
    cout << "remote_access() reports the following address:\n";
    cout << "&tom = " << &tom << endl;
    cout << "&dick = " << &dick << endl;
    cout << "&harry = " << &harry << endl;
}

```


#### 9.3 名称空间
##### main.cpp
```c++
// 传统的C++名称空间
// 声明区域: 可以在其中进行声明的区域
// 潜在作用域: 从声明点开始, 到声明区域的结尾  ==>  变量并非在其潜在作用域内的任何位置都可见, 因为可能被另一个在嵌套声明区域内的同名变量隐藏
// 作用域: 变量对程序而言可见的范围
// C++关于全局/局部变量规则定义了一种名称空间层次: 在每个声明区域都可以声明名称, 并且独立于其它声明区域的名称

// 新的名称空间特性
// 通过关键字namespace创建命名的名称空间, 从而提供一个声明名称的区域, 并且不同的名称空间中的相同名称不会发生冲突
// 名称空间可以是全局的, 也可以位于另一个名称空间中, 但不能位于代码块中  ==>  因此默认情况下, 名称空间中声明的名称的链接性是外部的
// 除了用户定义的名称空间外, 还存在另一个全局名称空间, 它对应于文件级声明区域
// 名称空间是开放的, 即可以把名称加入到已有的名称空间中
// 可以通过作用域解析运算符"::"来限定名称

// using声明和using编译指令 - 简化对名称空间中名称的使用(不需要加限定)
// using声明将特定的名称添加到它所属的声明区域, 如: using std::cout;
// using编译指令使名称空间中所有的名称都可用, 如: using namespace std;
// using声明和using编译指令的比较
//     1. 使用using声明就像是声明了相应的名称一样, 在同一声明区域不能再次声明该名称
//     2. 使用编译指令, 将进行名称解析, 就像是在紧挨着该声明区域的外部创建了一个新的声明区域, 在其中使用using声明声明了名称空间中所有的名称; 此时我们在使用using编译指令的声明区域是可以再次声明同一各变量的, 这是将覆盖名称空间中的同名名称
//     3. 一般来说, 使用using声明更为安全
// 名称空间是可以传递的: 若存在名称空间A, B, C, 如果将A导入B, 之后又将B导入C, 那么此时A和B都被导入到了C
// 给名称空间创建别名
//     1. 用于简化很长的标识符  ==>  namespace mvft = my_very_favorite_things;
//     2. 用于简化嵌套名称空间的使用  ==>  namespace MEF = myth::elements::fire;
// 可以通过省略名称来创建未命名的名称空间, 这提供了链接性为内部的静态变量的替代品

// 名称空间相关的指导原则
//     1. 使用在已命名的名称空间中声明的变量, 而不是使用外部全局变量, 也不是静态全局变量
//     2. 如果开发了一个函数库或类库, 则将其放在一个名称空间中  ==>  事实上, C++提倡将标准函数库放在名称空间std中
//     3. 仅将using编译指令作为旧代码过渡到使用名称空间的权宜之计
//     4. 不要在头文件中使用using编译指令  ==>  导致: 掩盖了要使用n哪些名称空间, 同时包含头文件的顺序也可能影响程序的行为
//     5. 导入名称时, 首先使用作用域解析运算符或using声明方法
//     6. 对于using声明, 首先将其作用域设置为局部而不是全局

#include <iostream>
#include "namesp.h"

void other();
void another();

int main()
{
    other();
    another();

    return 0;
}

void other()
{
    using std::cout;
    using std::endl;
    using namespace debts;
    person dg = {"Doodles", "Glister"};
    show_person(dg);
    cout << endl;
    debt zippy[3];
    for (int i = 0; i < 3; i++)
    {
        get_debt(zippy[i]);
        show_debt(zippy[i]);
    }
    cout << "total debt: $" << sum_debts(zippy, 3) << endl;
}

void another()
{
    using pers::person;
    person collector = {"Milo", "Rightshift"};
    pers::show_person(collector);
    std::cout << std::endl;
}
```


##### namesp.h
```c++
#ifndef _NAMESP_H_
#define _NAMESP_H_
#include <string>

namespace pers
{
    struct person
    {
        std::string fname;
        std::string lname;
    };
    void get_person(person &);
    void show_person(const person &);
}

namespace debts
{
    using namespace pers; // 只是演示, 不要这样做
    struct debt
    {
        person name;
        double amount;
    };
    void get_debt(debt &);
    void show_debt(const debt &);
    double sum_debts(const debt *, int);
}

#endif
```


##### namesp.cpp
```c++
#include <iostream>
#include "namesp.h"

namespace pers
{
    using std::cin;
    using std::cout;
    void get_person(person &rp)
    {
        // 不做校验
        cout << "Enter the first name: ";
        cin >> rp.fname;
        cout << "Enter the last name: ";
        cin >> rp.lname;
    }
    void show_person(const person &rp)
    {
        cout << rp.fname << ", " << rp.lname;
    }
}

namespace debts
{
    using std::cin;
    using std::cout;
    void get_debt(debt &rd)
    {
        get_person(rd.name);
        cout << "Enter the amount of debt: ";
        cin >> rd.amount;
    }
    void show_debt(const debt &rd)
    {
        show_person(rd.name);
        cout << ": $" << rd.amount << std::endl;
    }
    double sum_debts(const debt *darr, int n)
    {
        double total = 0;
        for (int i = 0; i < n; i++)
            total += darr[i].amount;
        return total;
    }
}
```


### 第十章: 对象和类
#### 10.1 过程性编程和面向对象编程
```c++
// 最重要的OOP特性
//     1. 抽象
//     2. 封装和数据隐藏
//     3. 多态
//     4. 继承
//     5. 代码的可重用性

// 采用OOP方法, 首先从用户角度考虑对象, 即描述对象所需的数据以及用户与数据交互所需的操作
```


#### 10.2 抽象和类
##### main.cpp
```c++
// 在C++中, 用户定义类型指的是实现抽象接口的类设计

// 指定基本类型完成了3项工作
//     1. 决定数据对象的内存数量
//     2. 决定如何解释内存中的位
//     3. 决定可使用数据对象执行的操作或方法
// 对于内置类型来说, 相关的操作信息被写入到编译器; 而对于C++用户自定义类型, 相关的操作需要程序员自己定义, 这些工作换来了新定制数据对象的强大功能和灵活性

// 类是一种将抽象转换为用户定义类型的C++工具
// 一般来说, 类规范由两部分组成
//     1. 类声明: 以数据成员的方式描述数据部分; 以成员函数的方式描述公有接口  ==>  通常放在头文件
//     2. 类方法定义: 描述如何实现类成员函数  ==>  通常放在源代码文件
// 什么是接口?
//     1. 接口是一个共享框架, 供两个系统交互时使用
//     2. 对于类, 我们说公共接口; 类设计禁止公共用户直接访问类, 但可以使用类方法

#include <iostream>
#include "stock.h"

int main()
{
    Stock fluffy_the_cat;
    fluffy_the_cat.acquire("nanosmart", 20, 12.50);
    fluffy_the_cat.show();
    fluffy_the_cat.buy(15, 18.125);
    fluffy_the_cat.show();
    fluffy_the_cat.sell(4, 20.00);
    fluffy_the_cat.show();

    return 0;
}
```


##### stock.h
```c++
#ifndef _STOCK_H_
#define _STOCK_H_

#include <string>

class Stock
{
    // 关键字class标识类定义
    // 要存储的数据以类数据成员的形式出现
    // 要执行的操作以类函数成员的形式出现, 成员函数可以就地定义(自动成为内联函数), 也可以使用原型表示
    // 访问控制
    //     1. 使用类对象的程序都可以访问公有部分, 但只能通过公有成员函数来访问对象的私有成员
    //     2. 防止程序直接访问数据被称为数据隐藏
    //     3. 三种级别: private, protected, public
    // 类设计将公有接口(抽象组件)与实现细节分开, 这被称为封装
    //     1. 数据隐藏是一种封装
    //     2. 将实现细节隐藏在私有部分, 也是一种封装
    //     3. 将类函数定义和声明放在不同的文件, 也是一种封装
    // 数据隐藏不仅防止了直接访问数据, 还让开发者(用户)无需了解数据的表示
    // 公有还是私有?
    //     1. 无论成员函数还是成员数据, 都可以在公有部分或私有部分声明
    //     2. 但是由于OOP数据隐藏的特性, 通常数据项被放在私有部分, 组成类接口的成员函数放在公有部分
    //     3. 通常, 使用私有成员函数来处理不属于公有接口的视线细节
    // 值得注意的是, 不必再类声明中使用关键字private, 因为这是默认的, 但是为了强调数据隐藏, 也可以显式的指出
    // 实际上, C++对结构进行了扩展, 使之具有与类相同的特性, 它们之间唯一的区别是: 结构的默认访问类型为public, 而类的默认访问类型为private
    // 通常, C++程序员使用类来实现类描述, 使用结构来表示纯粹的数据对象
    // 定义位于类声明中的函数将自动成为内联函数; 根据改写规则, 也可以在类声明中写函数原型, 在类声明之外定义成员函数, 通过关键字inline使之成为内联函数
private:
    std::string campany; // 股票的发行公司
    long shares;         // 所持有的股票数量
    double share_value;  // 股票的价格
    double total_value;  // 股票总价格
    void set_total() { total_value = shares * share_value; }

public:
    void acquire(const std::string &name, long num, double price);
    void buy(long num, double price);
    void sell(long num, double price);
    void update(double price);
    void show();
}; // 类定义也是一条语句, 这个分号不要忘了

#endif
```


##### stock.cpp
```c++
#include <iostream>
#include "stock.h"

// 类成员函数的定义与常规函数定义基本一致, 主要有2点区别
//     1. 需要使用作用域解析运算符"::"来限定函数名
//     2. 成员函数具有类作用域, 可以访问类中的private组件
// 如何调用成员函数?
//     1. Stock st;
//     2. st.stock();
// 每一个新对象都有自己的存储空间, 用于存储内部变量和类成员
// 然而同一个类的所有对象共享一组类方法, 即每种方法只有一个副本
// 在OOP中, 调用成员函数被称为发送消息, 因此将同样的消息发给2个不同的对象, 将调用同一个方法, 不同的是使用的对象

void Stock::acquire(const std::string &name, long num, double price)
{
    campany = name;
    if (num < 0)
    {
        std::cout << "number of shares can't be negative; " << campany << " shares set to 0.\n";
        shares = 0L;
    }
    else
    {
        shares = num;
    }
    share_value = price;
    set_total();
}

void Stock::buy(long num, double price)
{
    if (num < 0)
    {
        std::cout << "number of shares purchased can't be negative. transaction is aborted.\n";
        return;
    }
    shares += num;
    share_value = price;
    set_total();
}

void Stock::sell(long num, double price)
{
    if (num < 0)
    {
        std::cout << "number of shares sold can't be negative. transaction is aborted.\n";
        return;
    }
    else if (num > shares)
    {
        std::cout << "you can't sell more you have. transaction is aborted.\n";
        return;
    }

    shares -= num;
    share_value = price;
    set_total();
}

void Stock::update(double price)
{
    share_value = price;
    set_total();
}

void Stock::show()
{
    using std::cout;
    using std::endl;
    using std::ios_base;
    ios_base::fmtflags initial = cout.setf(ios_base::fixed, ios_base::floatfield);
    std::streamsize precision = cout.precision(3);
    cout << "campany: " << campany << "  shares: " << shares << endl;
    cout << "share price: $" << share_value << "  total worth: $" << total_value << endl;
    cout.setf(initial);
    cout.precision(precision);
}
```


#### 10.3 类的构造函数和析构函数
##### main.cpp
```c++
#include <iostream>
#include "stock.h"

int main()
{
    using std::cout;
    Stock st1 = Stock("nanosmart", 12, 20.0);
    st1.show();
    Stock st2("boffo objects", 2, 2.0);
    st2.show();

    // 对象赋值
    // 在默认情况下, 将一个对象赋值给另一个二同类型的对象时, C++将源对象的每个数据成员的内容复制到目标对象相应的数据成员中
    // 如果既可以通过初始化, 也可以通过赋值来设置对象的值, 则应该采用初始化, 因为这种方式的效率更高
    st2 = st1;
    st2.show();
    st2 = Stock("hellokitty", 15, 6.28); // 会创建一个临时变量

    return 0;
}
```


##### stock.h
```c++
#ifndef _STOCK_H_
#define _STOCK_H_

#include <string>

class Stock
{
private:
    std::string campany_; // 股票的发行公司
    long shares_;         // 所持有的股票数量
    double price_;        // 股票的价格
    double total_;        // 股票总价格
    void set_total() { total_ = shares_ * price_; }

public:
    // Stock()是构造函数
    //     1. 构造函数的名称与类名相同
    //     2. 虽然没有返回值, 但是没有声明返回void  ==>  实际上构造函数没有声明类型
    // 成员函数的参数名不能与成员名相同
    //     1. 一种做法: 给数据成员名添加前缀"m_"
    //     2. 另一种做法: 给数据成员名添加后缀"_"
    // C++提供两种使用构造函数的方式
    //     1. 显式的调用构造函数: Stock st = Stock(...);
    //     2. 隐式的调用构造函数: Stock st(...);
    // 使用new动态分配内存: Stock *pst = new Stock(...);
    // 默认构造函数: 在程序未提供显式的初始值时, 用来创建对象的构造函数  ==>  即允许只声明而不显式初始化: Stock st;
    //     1. 如果没有提供任何构造函数, C++将自动提供默认的构造函数, 它是隐式的, 不会做任何工作
    //     2. 当为类定义了构造函数之后, C++就不再自动提供默认构造函数, 需要程序员自己提供, 否则类似`Stock st;`的声明是无效的
    //     3. 默认构造函数不接受任何参数
    // 定义默认构造函数的两种方式
    //     1. 给已有构造函数的所有参数提供默认值
    //     2. 通过函数重载定义另一个不接收任何参数的构造函数
    // 在设计类时, 通常应该提供对所有类数据成员做隐式初始化的默认构造函数
    // C++11列表初始化: 提供与某个构造函数参数列表匹配的内容即可
    // 如果构造函数只有一个参数, 则将对象初始化为一个与参数类型相同的值时, 构造函数将被调用
    Stock();
    Stock(const std::string &campany, long shares, double price);
    // ~Stock()是析构函数
    //     1. 析构函数的名称是在类名前加上~
    //     2. 析构函数的作用完成清理工作
    //     3. 析构函数也没有返回值和声明类型
    //     4. 析构函数没有参数
    // 如果没有显式的定义析构函数, 则编译器会自动生成一个生么也不做的隐式的析构函数
    // 通常不应该在代码中显式的调用析构函数, 而应该由编译器决定何时调用它
    // 如果构造函数使用了new, 则必须提供使用delete的析构函数
    ~Stock();
    void buy(long shares, double price);
    void sell(long shares, double price);
    void update(double price);
    // const成员函数
    // 因为成员函数所使用的对象是由方法调用隐式提供, 所以像常规的const函数一样声明在语法上有问题
    // 所以C++的解决方法是将const关键字放在成员函数的括号后面, 用于承诺不会修改对象
    void show() const;
};

#endif
```


##### stock.cpp
```c++
#include <iostream>
#include "stock.h"

Stock::Stock()
{
    std::cout << "default constructor called\n";
    campany_ = "no name";
    shares_ = 0L;
    price_ = 0.0;
    total_ = 0.0;
}

Stock::Stock(const std::string &campany, long shares, double price)
{
    campany_ = campany;
    if (shares < 0)
    {
        std::cout << "number of shares can't be negative; " << campany << " shares set to 0.\n";
        shares_ = 0L;
    }
    else
    {
        shares_ = shares;
    }
    price_ = price;
    set_total();
}

Stock::~Stock()
{
    std::cout << "deconstructor called\n";
}

void Stock::buy(long shares, double price)
{
    if (shares < 0)
    {
        std::cout << "number of shares purchased can't be negative. transaction is aborted.\n";
        return;
    }
    shares_ += shares;
    price_ = price;
    set_total();
}

void Stock::sell(long shares, double price)
{
    if (shares < 0)
    {
        std::cout << "number of shares sold can't be negative. transaction is aborted.\n";
        return;
    }
    else if (shares > shares_)
    {
        std::cout << "you can't sell more you have. transaction is aborted.\n";
        return;
    }

    shares_ -= shares;
    price_ = price;
    set_total();
}

void Stock::update(double price)
{
    price_ = price;
    set_total();
}

void Stock::show() const
{
    using std::cout;
    using std::endl;
    using std::ios_base;
    ios_base::fmtflags initial = cout.setf(ios_base::fixed, ios_base::floatfield);
    std::streamsize precision = cout.precision(3);
    cout << "campany: " << campany_ << "  shares: " << shares_ << endl;
    cout << "share price: $" << price_ << "  total worth: $" << total_ << endl;
    cout.setf(initial);
    cout.precision(precision);
}
```


#### 10.4 this指针
##### stock.h
```c++
#ifndef _STOCK_H_
#define _STOCK_H_

#include <string>

class Stock
{
private:
    std::string campany_; // 股票的发行公司
    long shares_;         // 所持有的股票数量
    double price_;        // 股票的价格
    double total_;        // 股票总价格
    void set_total() { total_ = shares_ * price_; }

public:
    Stock();
    Stock(const std::string &campany, long shares, double price);
    ~Stock();
    void buy(long shares, double price);
    void sell(long shares, double price);
    void update(double price);
    void show() const;
    const Stock &topvalue(const Stock &) const;
};

#endif
```


##### stock.cpp
```c++
#include <iostream>
#include "stock.h"

Stock::Stock()
{
    campany_ = "no name";
    shares_ = 0L;
    price_ = 0.0;
    total_ = 0.0;
}

Stock::Stock(const std::string &campany, long shares, double price)
{
    campany_ = campany;
    if (shares < 0)
    {
        std::cout << "number of shares can't be negative; " << campany << " shares set to 0.\n";
        shares_ = 0L;
    }
    else
    {
        shares_ = shares;
    }
    price_ = price;
    set_total();
}

Stock::~Stock()
{
    // be quiet
}

void Stock::buy(long shares, double price)
{
    if (shares < 0)
    {
        std::cout << "number of shares purchased can't be negative. transaction is aborted.\n";
        return;
    }
    shares_ += shares;
    price_ = price;
    set_total();
}

void Stock::sell(long shares, double price)
{
    if (shares < 0)
    {
        std::cout << "number of shares sold can't be negative. transaction is aborted.\n";
        return;
    }
    else if (shares > shares_)
    {
        std::cout << "you can't sell more you have. transaction is aborted.\n";
        return;
    }

    shares_ -= shares;
    price_ = price;
    set_total();
}

void Stock::update(double price)
{
    price_ = price;
    set_total();
}

void Stock::show() const
{
    using std::cout;
    using std::endl;
    using std::ios_base;
    ios_base::fmtflags initial = cout.setf(ios_base::fixed, ios_base::floatfield);
    std::streamsize precision = cout.precision(3);
    cout << "campany: " << campany_ << "  shares: " << shares_ << endl;
    cout << "share price: $" << price_ << "  total worth: $" << total_ << endl;
    cout.setf(initial);
    cout.precision(precision);
}

// 如果成员函数涉及多个对象, 则需要this指针
// this指针指向用来调用成员函数的对象
// this指针被作为隐藏参数传递给方法
const Stock &Stock::topvalue(const Stock &s) const
{
    if (s.total_ > total_)
        return s;
    else
        return *this;
}
```


#### 10.5 对象数组
##### main.cpp
```c++
#include <iostream>
#include "stock.h"

const int STKS = 4;

int main()
{
    Stock stocks[STKS] = {
        Stock("nanosmart", 12, 20.0),
        Stock("boffo objects", 200, 2.0),
        Stock("monolithic obelisks", 130, 3.25),
        Stock("fleep enterpises", 60, 6.5),
    };
    std::cout << "stock holdings:\n";
    int i;
    for (i = 0; i < STKS; i++)
        stocks[i].show();
    const Stock *top = &stocks[0];
    for (i = 1; i < STKS; i++)
        top = &top->topvalue(stocks[i]);
    std::cout << "\nmost valuable holding;\n";
    top->show();

    return 0;
}
```


##### stock.h和stock.cpp与10.4小节相同


#### 10.6 类作用域
1. 在类中定义的名称(数据成员或函数成员)的作用域都为整个类
2. 要访问类成员, 必须通过对象
3. 在定义成员函数时, 必须使用作用域解析运算符限定其名称, 将其置于类作用域
4. 只有在类声明或成员函数定义中, 才可以使用未修饰的成员名称; 在其它地方必须通过成员运算符(.), 间接成员运算符(->), 作用域解析运算符(::)
5. 在类作用域中创建所有对象共享的常量
   1. 在类中(私有部分)声明一个(未命名的)枚举  ==>  这种方式不会创建类数据成员
   2. 使用static关键字: static const int Months = 12;  ==>  不能省略static, 否则将只是一个普通的数据成员, 不会被共享
6. 作用域内枚举(C++11)  ==>  解决多个枚举的枚举量发生冲突问题
   1. enum class axx {...};
   ps:
   - 这样枚举axx的作用域就被限制在了类中, 此时必须提供枚举名称来限定
   - 关键字class可以用struct替代
   - 作用域内枚举保证了类型安全, 它不会执行隐式的转换
   - 在C++11中, 默认情况下, 作用域内枚举的底层类型为int; 也可以自己指定底层类型(但必须为整型): enum class:short pizza{...};
   - C++中也可以通过这种语法来指定常规枚举的底层类型, 但是如果没有指定, 底层类型将依赖于编译器的实现


#### 10.7 抽象数据类型
##### main.cpp
```c++
// 抽象数据类型(ADT), 以通用的方式描述类型, 而没有引入语言或实现细节
// 比如栈的描述
//     1. 创建空栈
//     2. 入栈操作
//     3. 出栈操作
//     4. 查看栈是否填满
//     5. 查看栈是否为空
// 可以将上述操作转换为一个类声明
//     1. 公有成员表示栈操作的接口
//     2. 私有数据成员负责存储栈数据

#include <iostream>
#include <cctype>
#include "stack.h"

int main()
{
    using namespace std;
    Stack st;
    char ch;
    unsigned long po;
    cout << "Enter A to add a purchase order,\n"
         << "  P to process a po,\n"
         << "  or Q to quit.\n";
    while (cin >> ch && toupper(ch) != 'Q')
    {
        while (cin.get() != '\n')
            continue;
        if (!isalpha(ch))
        {
            cout << "invalid input!\n";
            continue;
        }
        switch (toupper(ch))
        {
        case 'A':
            if (st.isfull())
                cout << "stack already full.\n";
            else
            {
                cout << "Enter a po number to add: ";
                cin >> po;
                st.push(po);
                cout << "po #" << po << " added.\n";
            }
            break;

        case 'P':
            if (st.isempty())
                cout << "stack is empty.\n";
            else
            {
                st.pop(po);
                cout << "po #" << po << " popped\n";
            }
            break;
        }

        cout << "Enter A to add a purchase order,\n"
             << "  P to process a po,\n"
             << "  or Q to quit.\n";
    }
    cout << "Bye!\n";

    return 0;
}
```


##### stack.h
```c++
#ifndef _STACK_H_
#define _STACK_H_

typedef unsigned long Item;

class Stack
{
private:
    enum
    {
        MAX = 10
    };
    Item items[MAX];
    int top; // index for top stack item

public:
    Stack();
    bool isempty() const;
    bool isfull() const;
    bool push(const Item &item);
    bool pop(Item &item);
};

#endif
```


##### stack.cpp
```c++
#include "stack.h"

Stack::Stack()
{
    top = 0;
}

bool Stack::isempty() const
{
    return top == 0;
}

bool Stack::isfull() const
{
    return top == MAX;
}

bool Stack::push(const Item &item)
{
    if (top < MAX)
    {
        items[top++] = item;
        return true;
    }
    else
        return false;
}

bool Stack::pop(Item &item)
{
    if (top > 0)
    {
        item = items[--top];
        return true;
    }
    else
        return false;
}
```


### 第十一章: 使用类
#### 11.1 运算符重载
1. C++根据操作数的数目和类型来决定采用哪种操作
2. 语法: operator op(arglist)  ==>  op必须是有效的C++运算符


#### 11.2 计算时间: 一个运算符重载示例
##### main.cpp
```c++
#include <iostream>
#include "mytime.h"

int main()
{
    using std::cout;
    using std::endl;
    Time coding(2, 40);
    Time fixing(5, 55);
    Time total = coding + fixing;
    cout << "total time: ";
    total.show();
    Time diff = fixing - coding;
    cout << "\ndiff time: ";
    diff.show();
    Time mult = coding * 3.5;
    cout << "\nmult time: ";
    mult.show();

    return 0;
}
```


##### mytime.h
```c++
#ifndef _TIME_H_
#define _TIME_H_

class Time
{
private:
    int hours_;
    int minutes_;

public:
    Time();
    Time(int h, int m);
    void add_hours(int h);
    void add_minutes(int m);
    void reset(int h = 0, int m = 0);
    // 可以将operator+整体当作一个方法名来调用
    // 然而更简洁的方式是使用 a + b形式
    // 此时a作为调用对象, b作为参数传递
    // 可以将两个以上的对象相加吗?
    //     1. a + b + c
    //     2. 因为运算符+是从左向右结合的, 所以上述表达式等效于: a.operator+(b + c)  ==>  a.operator+(b.operator+(c))
    //     3. 上述语句在此处的情景下是合法的
    // 重载的限制
    //     1. 重载后的运算符必须有一个操作数是用户定义的类型  ==>  防止了用户为标准类型重载运算符
    //     2. 不能潍坊运算符原来的句法规则
    //         1. 不能修改运算符操作数的数目
    //         2. 不能修改运算符的优先级
    //         3. 只能重载C++有效的运算符, 而不能创造新的运算符
    //         4. 有些运算符不能被重载: sizeof, ., .*, ::, ?:, typeid, const_cast, dynamic_cast, reinterpret_cast, static_cast
    //         5. 有些运算符只能通过成员函数进行重载: =, (), [], ->
    //         6. (约定)不要将运算符重载成不相关的功能
    Time operator+(const Time &t) const;
    Time operator-(const Time &t) const;
    Time operator*(double mult) const;
    void show() const;
};

#endif
```


##### mytime.cpp
```c++
#include <iostream>
#include "mytime.h"

Time::Time()
{
    hours_ = minutes_ = 0;
}

Time::Time(int h, int m)
{
    hours_ = h;
    minutes_ = m;
}

void Time::add_hours(int h)
{
    hours_ += h;
}

void Time::add_minutes(int m)
{
    minutes_ += m;
    hours_ += minutes_ / 60;
    minutes_ %= 60;
}

void Time::reset(int h, int m)
{
    hours_ = h;
    minutes_ = m;
}

Time Time::operator+(const Time &t) const
{
    Time ans;
    ans.minutes_ = t.minutes_ + minutes_;
    ans.hours_ = t.hours_ + hours_ + ans.minutes_ / 60;
    ans.minutes_ %= 60;
    return ans;
}

Time Time::operator-(const Time &t) const
{
    Time ans;
    int _total1 = minutes_ + 60 * hours_;
    int _total2 = t.minutes_ + 60 * t.hours_;
    ans.hours_ = (_total1 - _total2) / 60;
    ans.minutes_ = (_total1 - _total2) % 60;
    return ans;
}

Time Time::operator*(double mult) const
{
    Time ans;
    long _total = (hours_ * 60 + minutes_) * mult;
    ans.hours_ = _total / 60;
    ans.minutes_ = _total % 60;
    return ans;
}

void Time::show() const
{
    std::cout << hours_ << " hours, " << minutes_ << " minutes";
}
```


#### 11.3 友元
##### main.cpp
```c++
// 通常, 公有类方法提供唯一的(私有数据)访问途径
// 但是有时候这种限制太严格, 于是C++提供另一种形式的访问限制: 友元
// 3种友元
//     1. 友元函数
//     2. 友元类
//     3. 友元成员函数

// 通过使函数成为类的友元, 可以赋予该函数与类的成员函数相同的访问权限
// 为类重载二元运算符, 当两个操作数的类型不同时, 可以使用非成员函数来重载, 这时就需要友元了

// 创建友元函数
//     1. 将函数原型放在类声明中, 并在声明前加上关键字friend
//     2. 编写函数定义, 因为它不是成员函数, 所以不需要前缀限定  ==>  另外, 在定义中不需要使用关键字friend

#include <iostream>
#include "mytime.h"

int main()
{
    using namespace std;
    Time coding(2, 40);
    Time mult = 2.75 * coding;
    cout << "mult time: " << mult;

    return 0;
}
```


##### mytime.h
```c++
#ifndef _TIME_H_
#define _TIME_H_
#include <iostream>

class Time
{
private:
    int hours_;
    int minutes_;

public:
    Time();
    Time(int h, int m);
    void add_hours(int h);
    void add_minutes(int m);
    void reset(int h = 0, int m = 0);
    Time operator+(const Time &t) const;
    Time operator-(const Time &t) const;
    Time operator*(double mult) const;
    friend Time operator*(double mult, const Time &t);
    // 重载<<运算符, 使其能够与ostream对象协同工作
    // 返回std::ostream &的目的是为了支持链式操作
    friend std::ostream &operator<<(std::ostream &out, const Time &t);
    void show() const;
};

#endif
```


##### mytime.cpp
```c++
#include <iostream>
#include "mytime.h"

Time::Time()
{
    hours_ = minutes_ = 0;
}

Time::Time(int h, int m)
{
    hours_ = h;
    minutes_ = m;
}

void Time::add_hours(int h)
{
    hours_ += h;
}

void Time::add_minutes(int m)
{
    minutes_ += m;
    hours_ += minutes_ / 60;
    minutes_ %= 60;
}

void Time::reset(int h, int m)
{
    hours_ = h;
    minutes_ = m;
}

Time Time::operator+(const Time &t) const
{
    Time ans;
    ans.minutes_ = t.minutes_ + minutes_;
    ans.hours_ = t.hours_ + hours_ + ans.minutes_ / 60;
    ans.minutes_ %= 60;
    return ans;
}

Time Time::operator-(const Time &t) const
{
    Time ans;
    int _total1 = minutes_ + 60 * hours_;
    int _total2 = t.minutes_ + 60 * t.hours_;
    ans.hours_ = (_total1 - _total2) / 60;
    ans.minutes_ = (_total1 - _total2) % 60;
    return ans;
}

Time Time::operator*(double mult) const
{
    Time ans;
    long _total = (hours_ * 60 + minutes_) * mult;
    ans.hours_ = _total / 60;
    ans.minutes_ = _total % 60;
    return ans;
}

Time operator*(double mult, const Time &t)
{
    // 可以在这个友元函数内实现自己的逻辑
    // 也可以任务委托给成员函数, 此时其实没必要将这个函数声明为友元, 但是还是推荐这个做, 因为如果将来需要修改这个函数的逻辑时, 就不需要修改类声明了

    // Time ans;
    // long _total = (t.hours_ * 60 + t.minutes_) * mult;
    // ans.hours_ = _total / 60;
    // ans.minutes_ = _total % 60;
    // return ans;

    return t * mult;
}

std::ostream &operator<<(std::ostream &out, const Time &t)
{
    out << t.hours_ << " hours, " << t.minutes_ << " minutes";
    return out;
}

void Time::show() const
{
    std::cout << hours_ << " hours, " << minutes_ << " minutes";
}
```


#### 11.4 重载运算符: 作为成员函数还是非成员函数


#### 11.5 再谈重载: 一个矢量类
