# c++ 17


## reference


## No.1 [结构化绑定](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0217r3.html)
### 1.1 概述
```c++
/// 通过使用一个对象的元素或成员同时实例化多个实体
/// 换一种说法就是: 解构对象/解构声明, 即把对象的成员绑定到新的变量
/// 优点:
///     1. 可以直接访问成员变量;
///     2. 把值绑定到能体现语义的变量上, 可读性更强;


struct student {
    std::string name;
    int age;
};
student lisi {"lisi", 26};


// 下面任意一种方式都支持
auto [u, v] = lisi;
auto [u, v] {lisi};
auto [u, v] (lisi);
```


### 1.2 典型用法
```c++
// 1. 用于返回结构体或数组的函数
student get_student(){
    return student{"zhangsan", 18};
}
auto [name, age] = get_student();


// 2. 用于std::map<>
std::map<int, std::string> map;
// insert some vlaues into map here
// 如果要遍历一个map, 常规方法如下:
for (auto& elem: map) std::cout << elem.first << ": " << elem.second << std::endl;
// 使用结构化绑定, 如下:
for (auto& [k, v]: map) std::cout << k << ": " << v << std::endl;


// 3. 理论上讲, 结构化绑定适用于任何具有public数据成员的结构体, C-Style数组, 类元组对象
// - 对于所有非静态数组成员都是public的结构体或类, 可以把每一个成员绑定到一个新的变量上; 需要特别注意的是, 在具有层次结构的类中, 所有非静态数据成员必须在同一个类中定义, 其目的是保证数据成员的顺序固定
// - 对于原生数组, 可以把数组的每一个元素都绑定到一个新的变量上
// - 对于任何类型, 都可以通过tuple-like API来绑定新的名称, 对于类型type, 需要如下组件:
//      - std::tuple_size<type>::value 返回元素的数量
//      - std::tuple_element<idx, type>::type 但会第idx个元素的类型
//      - get<idx>() 这是全局或成员函数, 返回第idx个元素的值

// 标准库中的std::pair<>, std::tuple<>, std::array<>...提供了tuple-like API
// 然而, 我们也可以通过提供tuple-like API为任何类型提供结构化绑定的支持
// 假定有如下类Customer
class Customer
{
private:
    std::string first;
    std::string last;
    long val;

public:
    Customer(std::string f, std::string l, long v) : first(std::move(f)), last(std::move(l)), val(v) {};
    ~Customer() {};
    std::string getfirst() const { return first; }
    std::string &getfirst() { return first; }
    std::string getlast() const { return last; }
    std::string &getlast() { return last; }
    long getval() const { return val; }
    long &getval() { return val; }
};


// 我们为其添加tuple-like API
// 这里提供了3个版本的特化, 分别用来处理常量, 非常量, 移动对象
// 为了能够返回引用, 应该使用decltype(auto)作为返回类型
template <std::size_t Idx>
decltype(auto) get(const Customer &c)
{
    static_assert(Idx < 3);
    if constexpr (Idx == 0)
        return c.getfirst();
    else if constexpr (Idx == 1)
        return c.getlast();
    else if constexpr (Idx == 2)
        return c.getval();
}

template <std::size_t Idx>
decltype(auto) get(Customer &c)
{
    static_assert(Idx < 3);
    if constexpr (Idx == 0)
        return c.getfirst();
    else if constexpr (Idx == 1)
        return c.getlast();
    else if constexpr (Idx == 2)
        return c.getval();
}

template <std::size_t Idx>
decltype(auto) get(Customer &&c)
{
    static_assert(Idx < 3);
    if constexpr (Idx == 0)
        return c.getfirst();
    else if constexpr (Idx == 1)
        return c.getlast();
    else if constexpr (Idx == 2)
        return c.getval();
}


// 再定义特化的getter
template <std::size_t>
auto get(const Customer&);

template <>
auto get<0>(const Customer& c)
{
    return c.getfirst();
}

template <>
auto get<1>(const Customer& c)
{
    return c.getlast();
}

template <>
auto get<2>(const Customer& c)
{
    return c.getval();
}


// 现在, 终于可以在Customer类上使用结构化绑定了
Customer zhangsan("zhang", "san", 25);
auto [first, last, val] = zhangsan;
```


### 1.3 深入理解结构化绑定
```c++
// 发生结构化绑定时, 其实背后有一个匿名的对象, 新的变量名其实都是这个匿名对象成员的别名, 如下:
auto [x, y] = pos;

auto pos_tmp = pos;     // 假设pos对象的两个成员分别为i, j
alias x = pos_tmp.i;    // 注意: 这里不能理解为引用, 因为行为上存在差别, 如结构化绑定的生命周期结束时, 匿名变量自动销毁
alias y = pos_tmp.j;


// 可以对结构化绑定使用修饰符: const, &,..., 它们将直接作用在匿名对象上, 如下
const auto& [x, y] = pos;


// 如果结构化绑定是一个临时对象的引用, 那么该临时对象的生命周期会被延长到结构化绑定的生命周期, 典型的情况就是函数
const auto& [x, y] = get_pos();


// 移动语义
/// @1 原结构体移动赋值给匿名结构体, 原结构体不在持有值
auto [name, age] = std::move(lisi);
/// @2 匿名结构体是原结构体的右值引用, 原结构体仍然持有值
auto&& [name, age] = std::move(lisi);


// 任何时候, 结构化绑定中声明得到变量数目必须与数据成员的数据相等
// 如果不想使用某个数据成员, 可以使用`_`接收, 其本质上仍是一个变量, 所以同一作用域内不能重复使用
auto [name, _] = lisi;
```


## No.2 [带初始化的if和switch语句](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0305r1.html)
### 2.1 概述
```c++
// 现在if和switch语句允许在条件表达式里添加一条初始化语句
// - 在if语句条件表达式中初始化的变量在整个if语句有效
if(init_expr; condition) {...}


// - 在switch语句条件表达式中初始化的变量在整个switch语句有效
switch(init_expr; condition) {...}
```


### 2.2 典型用法
```c++
// 1. 锁的使用
if(std::lock_guard lg{collMutex}; !coll.empty()){...}


// 2. 向map中插入元素, 并检查是否成功
std::map<std::string, int> coll;
if(auto [pos, ok] = coll.insert({"New", 42}); !ok) {...}
```


## No.3 [内联变量](https://wg21.link/p0386r2)
### 3.1 概述
```c++
// 自c++17开始, 可以在头文件中使用inline定义全局对象


// 内联变量产生的动机
// 1. 不能在类中初始化非常量的静态成员, 如果简单的将定义放在类外面又因违反一次定义原则(ODR)而导致链接错误


// ==> 解决方法
// 1. 在一个class/struct中初始化数字或枚举类型的静态常量
class MyClass{
    static const bool trace = true;
    ...
};
// 2. 定义一个返回局部静态变量的内联函数
inline std::string& getMsg() {
    static std::string msg{"OK"};
    return msg;
}
// 3. 定义一个返回该值的static成员函数
class MyClass{
    static std::string& getMsg(){
        static std::string msg{"OK"};
        return msg;
    }
};
// 4. 使用变量模板(c++14)
template<typename T = std::string>
T msg{"OK"};
// 5. 为静态成员定义一个模板类, 然后继承它
template<typename = void>
class MyClassStatic{
    static std::string msg;
};
// 6. 使用内联变量
class MyClass{
    inline static std::strring msg{"OK"};
};
inline MyClass mycls;



// 自c++17开始, constexpr static成员隐含着inline
// 即下面两个定义等价
static constexpr int n = 5;
inline static constexpr int n = 5;


// 通过使用thread_local, 可以为每个线程创建一个内联变量
inline thread_local std::vector<std::string> cache;
```


## No.4 [聚合体扩展](https://wg21.link/p0017r1)
### 4.1 概述
```c++
struct Data{
    std::string name;
    double value;
};
// c++最初引入的初始化方法是用花括号括起来的一组值
Data data = {"pi", 3.14};

// 自c++11开始, 可以省略等号
Data data{"pi", 3.14};

// 自c++17开始, 聚合体可以拥有基类
struct MoreData{
    bool done;
};
MoreData mdata{{"pi", 3.14}, false};
// 甚至可以省略嵌套的花括号(如果给出了内层聚合体需要的所有值), 传递的实参被用来初始化那个成员取决于它们的顺序
MoreData mdata{"pi", 3.14, false};


// 扩展聚合体初始化的动机
// - 如果没有这个特性, 所有的派生类都不能使用聚合体初始化


// c++17中被认为是聚合体的对象
// - 数组
// - 满足下列条件的类类型
//      - 没有用户定义的和explicit的构造函数
//      - 没有使用using声明继承的构造函数
//      - 没有private和protected的非静态数据成员
//      - 没有virtual函数
//      - 没有virtaul, private, protected基类
```


### 4.2 典型应用
```c++
// 1. 对一个派生自C-Style结构体并添加了新成员的类进行初始化
struct Data{
    const char* name;
    double value;
};
struct CppData: Data{
    bool critical;
    void show() const {
        std::cout << "[" << name << ", " << value << "]\n";
    }
};

CppData data{"pi", 3.14, false};
data.show();


// 2. 也可以从非聚合体派生出聚合体
struct MyString : std::string
{
    void show() const
    {
        if (empty()) { std::cout << "<undefined>\n"; }
        else { std::cout << c_str() << std::endl; }
    }
};

MyString ms{};
ms.show();


// 3. 多重继承
// 内部嵌套的初值列表将按照继承时基类声明的顺序传递给基类
template <typename T>
struct D : std::string, std::complex<T>
{
    std::string data;
};

D<double> d{{"description"}, {2.72, 3.14}, "data"};
```


## No.5 [强制省略拷贝或传递未实质化的对象](https://wg21.link/p0135r1)
### 5.1 概述
```c++
// 从技术上讲, c++17引入了一个新的机制: 当以值传递或返回一个临时对象时, 必须省略对该临时对象的拷贝, 即可以没有拷贝/移动构造函数
// 从效果上讲, 实际上传递的是一个未实质化的对象(unmaterialized objects)


// 强制省略临时变量拷贝的动机
// 在c++17之前, 当以值传递或返回一个临时对象时, 可能会发生编译器优化, 省略拷贝/移动构造函数的调用
// 但是, 这种优化并不是强制性的, 所以实际上还是需要显式或隐式的拷贝/移动构造函数, 否则会发生编译错误


// 强制省略临时变量拷贝的作用
// 1. 减少拷贝会带来更好的性能
// 2. 尽管移动语义可以显著的降低拷贝的开销, 但是如果直接省略拷贝, 将会得到更大的性能提升
// 3. 尽管在此之前很多编译器就进行了这种优化, 但是该特性在标准上作出保证
// 4. 可以减少输出参数的使用, 转而直接返回一个值
// 5. 可以定义一个总是可以工作的工厂函数, 它返回一个不允许拷贝/移动的对象
template<typename T, typename... Args>
T create(Args&&... args){
    // ...
    return T{std::forward<Args>(args)...};
}
// 6. 对弈移动构造函数被显式删除的类, 也可以通过返回临时对象来初始化


// 强制省略临时变量拷贝的副作用: 值类型体系的修改
// 什么是值类型体系? c++中每一个表达式都有值类型, 这个类型描述了表达式可以用来做什么
// c++98的值类型体系: 从c语言继承而来的左值和右值, 根据赋值语句划分

// c++11的值类型体系:
//      Note that: 严格来讲, 下面这些术语(lvalue, prvalue,...)是描述表达式的, 而不是描述值的; 例如一个变量并不是左值, 只含有这个变量而表达式才是左值
//      - lvalue    左值
//      - prvalue   纯右值
//      - xvalue    到期值
//      - glvalue   广义左值, 包括lvalue, xvalue
//      - rvalue    右值, 包括prvalue, xvalue
// lvalue:
//  - 只含有单个变量, 函数或成员(除了右值以外的普通成员)的表达式
//  - 只含有字符串字面量的表达式
//  - 解引用运算符(*)的结果
//  - 一个返回左值引用(T&)的函数返回值
//  - 对函数的任何引用, 即使使用std::move()标记
// prvalue
//  - 除字符串字面量和用户自定义字面量以外的字面量组成的表达式
//  - 取地址运算符(&)的结果
//  - 内建的数学运算符的结果
//  - 一个返回值的函数返回值
//  - lambda表达式
// xvalue
//  - 一个返回右值引用(T&&)的函数返回值(典型的是std::move()的返回值)
//  - 把一个对象转换成右值引用操作的结果
//  - 右值的非静态成员的值
// summary:
//  - 所有用作表达式的变量名都是lvalue
//  - 所有用作表达式的字符串字面量都是lvalue
//  - 其它所有字面量(4.2, true, nullptr,...)都是prvalue
//  - 所有临时对象(例如以值返回的对象)都是prvalue
//  - std::move()的结果是xvalue

// c++17的值类型体系
// 从广义上来讲, 值得类型有两种:
//  - glvalue: 用于描述函数或对象位置的表达式(xvalue描述了一种特殊的位置, 它表示一个资源可被回收利用的对象)
//  - prvalue: 用于初始化的表达式
// c++17引入了一个新的术语, 临时对象实质化(materialization), 这是一种prvalue到xvalue的转换, 任何情况下prvalue出现在需要glvalue的地方都是有效的, 首先会用prvalue初始化一个临时对象X, 然后用X替换prvalue


// 因为prvalue不再是对象, 而是可以被用来初始化对象的表达式, 所以用prvalue初始化对象时不再需要prvalue是可移动的, 所以也不需要任何拷贝/移动构造函数
// 所有以值返回临时对象的过程都是在传递未实质化的返回值, 所以不需要任何拷贝/移动构造函数
```


## No.6 [lambda表达式扩展](https://wg21.link/p0170r1)
### 6.1 概述
```c++
/// @c++11引入了lambda表达式
/// @c++14引入了泛型lambda表达式
/// @c++17扩展了lambda表达式的应用场景


// 在常量表达式中使用
// 从c++17开始, lambda表达式会尽可能的隐式声明constexpr, 即任何只使用有效的编译期上下文的lambda都可以被用于编译期
// 使用编译期上下文中不允许的特性, 将会使lambda失去constexpr的能力, 但是我们仍然可以在运行时使用lambda
// Note that: 编译期上下文, 即只有字面量, 没有静态变量, 没有try/catch, 没有new/delete, 没有虚函数
auto squared = [](auto val) { return val * val; };
std::array<int, squared(5)> arr;
// 如果不确定特定的lambda表达式是否确实用于编译期, 只需要显式的加上constexpr修饰, 如果出现了编译期不允许的特性, 将会引发编译错误
// 注意, 此处有两个constexpr, 含义如下:
//  - 第1个: 表示该lambda表达式可用于编译期
//  - 第2个: 表示该lambda表达式在编译期被初始化
constexpr auto squared = [](auto val) constexpr {...};
// 从c++17开始, 如果lambda被显式或隐式的定义为constexpr, 那么生成的函数调用也将是constexpr


// 在需要当前对象的拷贝时使用
// 当在非静态成员函数中使用lambda函数时, 不能隐式的获取该对象成员的使用权
// 在c++11和c++14中, 可以通过值或引用捕获this
[this](){}
[=](){}
[&](){}
// 然而, 即便是按值的方式捕获this, 实质上获得的也是引用, 因为this本身是一个指针, 当lambda的生命周期比对象更长时将会引发问题
// c++14提供了一种解决方案
[thisCopy=*this](){}
// c++17再次基础上作了进一步的优化, 可以通过*this显式的捕获当前对象的拷贝
[*this](){}


// 以常量引用捕获
```


## No.7 [新属性和属性特性](https://wg21.link/p0068r0)
### 7.1 概述
```c++
// 从c++11开始就可以指明属性, c++17中又增加了新的属性


[[nodiscard]]
// 鼓励编译器在某个函数的返回值未被使用时给出警告
// 通常用于放置某些因为返回值未被使用而引发的不当行为:
//  - 内存泄露(申请资源, 但自身并不释放而是将资源返回)
//  - 未知或出乎意料的行为 -> std::async的返回值如果未被使用, 将变成同步行为
//  - 不必要的开销
// 如果因为某些原因, 确实不想使用被[[nodiscard]]标记函数的返回值, 可以将返回值转换为void来禁止警告
// 成员函数被覆盖或继承时, 基类中标记的属性不被继承
// 可以把属性标记在函数前的所有修饰符之前, 也可以把属性标记在函数名之后
[[nodiscard]] constexpr void foo();
constexpr void foo [[nodiscard]]();


[[maybe_unused]]
// 可以避免编译器在某个变量未被使用时发出警告


[[fallthrough]]
// 避免编译器在switch语句的某个标签中缺少break发出警告, 该标记放在本应该放break的位置, 并且需要加分号结尾


[[deprecated]]
// 废弃标记, 可以作用于命名空间, 枚举子(枚举类型的值)


// 用户自定义的属性一般放在某个命名空间中, 可以使用using声明简化
[[MySpeace::webservice, MySpace::restful, MySpace::doc("html")]] void foo();
[[using MySpace: webservice, restful, doc("html")]] void foo();
```


## No.8 [其它语言特性](https://wg21.link/n4230)
### 8.1 概述
```c++
// 1. 嵌套命名空间
namespace A::B::C {}
// 等价于
namespace A{
    namespace B{
        namespace C{}
    }
}


// 2. 有定义的表达式求值顺序


// 3. 更宽松的用整型初始化枚举值的规则


// 4. 修正auto类型的列表初始化


// 5. 十六进制浮点数字面量


// 6. utf8字符字面量


// 7. 异常声明作为类型的一部分
// 如下两个声明的的类型是不同的
void f_maythrow();
void f_noexcept() noexcept;
// 然而重载一个函数签名相同, 异常声明不同的函数是不允许的


// 8. 单参数static_assert
// c++17以前要求用作错误信息的参数变成可选的了


// 9. 预处理条件__has_include
// 用于检查某个头文件是否已经被包含过
```


## No.9 [类模板参数推导]()
### 9.1 概述
```c++
// 在c++17之前, 必须指明所有的类模板参数
std::complex<double> cplx{3.14, 2.8};
// 从c++17开始, 该限制被放宽
std::complex cplx{3.14, 2.8};


// 使用类模板参数推导(CTAD)的条件
// 只要编译器能够根据初始值推导出所有的模板参数, 那么就可以不指明参数
// 并且支持任何有效方式的初始化
std::complex cplx{1.1, 2.2};
std::complex cplx(1.1, 2.2);
std::complex cplx = 1.1;
srd::complex cplx = {1.1};
```


## No.10 编译期if语句
### 10.1 概述
```c++
// 在编译期计算条件表达式
// 决定使用if constexpr的then部分或者else部分的代码
// 这意味着不使用的代码甚至不会生成(能减小可执行程序的大小), 但仍然会进行语法检查
if constexpr(...){}
else if constexpr(...){}
else {}


// 使用场景
// 1. 理论上讲, 只要条件表达式是编译期表达式, 就可以使用编译期if
// 2. 也可以混合使用运行时if和编译期if
// 3. 完美返回泛型值
// 4. 使用编译期if进行类型分发, 以避免为每种类型重载  ==>  重载版本遵循最佳匹配, 而编译期if版本遵循最先匹配协议


// 注意事项
// 1. 只能在函数体内使用if constexpr, 所以不能用它来替换预处理器的条件编译
// 2. 可能会影响函数的返回值类型
auto foo(int x){
    if constexpr (sizeof(int) > 4) {return 42;}
    else {return 42u};
}
// 3. 下述两种写法不能等效转换, 这会影响类型推断
if constexpr (...) {return a;}
else {return b;}
// 
if constexpr (...) {return a;}
return b;
// 4. 编译期if在实例化时并不进行短路求值
// 这意味着如果后面条件的有效性依赖于前面的条件, 需要将条件嵌套而不是使用逻辑运算符链接


// 编译期if也可以带初始化
```


## No.11 折叠表达式
### 11.1 概述
```c++
// 折叠表达式出现的动机
// 1. 不必再用递归实例化模板的方式来处理厂形参包


// 1. 一元左折叠
// 一般情况下, 从左到右求值是比较符合直觉的, 故推荐使用左折叠
// (((arg1 op arg2) op arg3) ...) op argn
(... op args)
// 2. 一元右折叠
// arg1 op (... (argn-2 op (argn-1 op argn)))
(args op ...)
// 3. 二元左折叠
// 二元折叠表达式就是在一元的基础上增加一个初始值E
// 值得注意的是, 省略号两侧的操作符必须相同
// (((E op arg1) op arg2) ...) op argn
(E op ... op args)
// 4. 二元右折叠
// arg1 op (... (argn-1 op (argn op E)))
(args op ... op E)


// 折叠表达式处理空形参包的规则
// 1. 如果op为&&, 则值为true
// 2. 如果op为||, 则值为false
// 3. 如果op为,, 则值为void()
// 4. 如果op为其它, 则引发错误


// 可以对除了., ->, []之外的所有二元运算符使用折叠表达式
```


## No.12 处理字符串字面量模板参数
### 12.1 概述
```c++
template<const char* str>
struct Msg{};

static const char greet[] = "have a nice dinner!";
Msg<greet> msg{};
```


## No.13 占位符类型作为模板参数
### 13.1 概述
```c++
// 可以使用占位符auto, decltype(auto)作为非类型模板参数的类型
// 但是需要注意的是, 不能用该特性实例化本不能用于模板参数的类型, 如double
template<auto N>
struct X{};

X<42> x1;
X<'x'> x2;


// 同样的, 可以指明类型的版本作为部分特化
template<int N>
struct X<int> {};


// 也支持类模参数推导


// 使用场景
// 1. 字符和字符串模板参数
// 2. 定义元编程常量
// 3. 变量模板的参数


// decltype(auto)的推导规则
// 1. prvalue -> type
// 2. lvalue -> type&
// 3. xvalue -> type&&
```


## No.14 扩展的using声明
### 14.1 概述
```c++
// 支持逗号分隔的名称列表, 同样适用于参数包


// 使用场景
// 1. 构建lambda集合
// 2. 继承构造函数
```


## No.15 std::optional
### 15.1 概述
```c++
// std::optional对象的内存大小等于内部对象的大小加上一个bool类型的大小
// 
```