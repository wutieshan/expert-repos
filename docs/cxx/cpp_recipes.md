# C++ Recipes


## Reference
> - [everystep](https://mp.weixin.qq.com/s/M8SbAmQcVtE282UIldwzdA)


## 1 类型安全
### 1.1 告别union, 拥抱std::variant
```c++
#include <iostream>
#include <string>
#include <variant>

union userdata_v1
{
    int uid;
    std::string name;
    double balance;
};

typedef std::variant<int, std::string, double> userdata_v2;

void process_userdata(const userdata_v1 &data) {}

void process_userdata(const userdata_v2 &data)
{
    // 使用类型检查判断当前的数据类型
    if (std::holds_alternative<int>(data)) {
        std::cout << "uid: " << std::get<int>(data) << std::endl;
    }
    else if (std::holds_alternative<std::string>(data)) {
        std::cout << "name: " << std::get<std::string>(data) << std::endl;
    }
    else if (std::holds_alternative<double>(data)) {
        std::cout << "balance: " << std::get<double>(data) << std::endl;
    }
}

auto main() -> int
{
    userdata_v2 data(100);
    process_userdata(data);

    data = "tieshan";
    process_userdata(data);

    data = 3.14;
    process_userdata(data);

    return 0;
}
```


### 1.2 类型转换
```c++
#include <iostream>

class Shape
{
public:
    virtual void draw() = 0;
};

class Circle: public Shape
{
public:
    Circle(int radius): radius_(radius) {}

    void draw() override {};

    void set_radius(int radius) { radius_ = radius; }

private:
    double radius_;
};

void update_shape_v1(Shape *shape)
{
    Circle *circle = (Circle *)shape;  //C风格的类型转换, 存在隐患
    circle->set_radius(5.0);
}

void update_shape_v2(Shape &shape)
{
    // dynamic_cast在运行时会进行类型检查
    // 虽然有一定的性能开销, 但是为了程序的安全性和可靠性是完全值得的
    if (Circle *circle = dynamic_cast<Circle *>(&shape)) {
        circle->set_radius(5.0);
    }
    else {
        // 如果转换失败, 可以优雅的处理
        std::cout << "not a circle, skipped!" << std::endl;
    }
}
```


### 1.3 std::span, 解决数组参数传递时丢失长度信息问题
1. std::span是C++20引入的, 不仅可以处理普通数组, 还可以处理std::array, std::vector等容器
```c++
#include <iostream>
#include <span>

double calculate_average(double scores[], int size)
{
    // double[]数组变成了裸指针double*, 完全不知道自身的长度了
    // 需要通过额外的参数size来指出其长度, 并且不能保证传的size参数就一定正确
    double sum = 0.0;
    for (int i = 0; i < size; i++) { sum += scores[i]; }
    return sum / size;
}

double calculate_average(std::span<const double> scores)
{
    double sum = 0.0;
    for (const auto score: scores) { sum += score; }  // 可以使用range-based遍历
    return sum / scores.size();                       // size()方法自动推导长度
}

auto main() -> int
{
    double scores[] = {85.0, 92.0, 79.0, 88.0, 95.0};
    double avg      = 0.0;

    // 1
    int size = sizeof(scores) / sizeof(scores[0]);
    avg      = calculate_average(scores, size);
    std::cout << "avg_1: " << avg << std::endl;

    // 2
    avg = calculate_average(std::span<const double>(scores, 5));
    std::cout << "avg_2: " << avg << std::endl;

    return 0;
}
```


### 1.4 告别窄缩, 让类型转换更安全
```c++
#include <cstdlib>
#include <exception>
#include <iostream>
#include <limits>
#include <stdexcept>

void process_data_v1(int value)
{
    short small           = value;  // 大数转小数, 可能导致数据丢失
    unsigned int positive = value;  // 负数转无符号
    float fvalue          = value;  // 精度丢失
}

void process_data_v2(int value)
{
    // 1. 使用花括号初始化, 防止窄缩
    // short small{value};  // 编译器直接报错, 帮助定位问题

    // 2. 使用std::numeric_limits进行范围检查
    if (value > std::numeric_limits<short>::max() || value < std::numeric_limits<short>::min()) {
        throw std::out_of_range("value的值超出short范围");
    }
    else {
        short small = static_cast<short>(value);
    }

    // 3. 使用static_cast代替隐式转换, 让代码意图更明确
    if (value >= 0) {
        unsigned int positive = static_cast<unsigned int>(value);
    }

    // 4. 处理浮点数精度问题
    double dvalue = 123456789.0;
    float fvalue  = static_cast<float>(dvalue);
    if (static_cast<double>(fvalue) != dvalue) {
        throw std::runtime_error("浮点数精度丢失");
    }
}

auto main() -> int
{
    std::system("chcp 65001");  // 解决中文显示问题

    try {
        process_data_v2(-123456789);
    }
    catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
```


## 2 函数美化之路
### 2.1 一个函数只做一件事情
```c++
struct User
{
};

// 每个函数各司其职
User get_user();
void validate_user(const User &user);
void save_user(const User &user);
void notify_user_created(const User &user);

// 可以根据需要自由组合
void process_new_user()
{
    auto user = get_user();
    validate_user(user);
    save_user(user);
    notify_user_created(user);
}

// 还可以借助模板, 让函数变得更加通用
template<typename T> void validate(const T &entity);
template<typename T> void save(const T &entity);
template<typename T> void notify(const T &entity);
```


### 2.2 保持函数简短
```c++
#include <numeric>
#include <vector>

struct Item
{
    double price;
    int quantity;
};

struct Order
{
    std::vector<Item> items;

    bool has_discount;
    int vip_level;
};

// 一个臃肿的函数
double calculate_final_price_v1(const Order &order)
{
    double price = 0.0;

    // 计算商品总价
    for (auto &item: order.items) { price += item.price * item.quantity; }

    // 计算折扣
    if (order.has_discount) {
        if (order.vip_level > 2) {
            price *= 0.8;
        }
        else {
            price *= 0.9;
        }
    }

    // 计算税费
    price *= (1 + 0.05);

    return price;
}

// ============================================================
double calculate_items_total_price(const std::vector<Item> &items)
{
    return std::accumulate(items.begin(), items.end(), 0.0, [](double sum, const Item &item) {
        return sum += item.price * item.quantity;
    });
}

double apply_discount(double price, int vip_level)
{
    return vip_level > 2 ? price * 0.8 : price * 0.9;
}

double apply_tax(double price)
{
    return price * (1 + 0.05);
}

// 保持函数精简的黄金法则
// 1. 一个函数最好不要超过20行
// 2. 如果一个函数超过一屏幕(约50行), 就应该考虑拆分了
// 3. 复杂的逻辑要分而治之
double calculate_final_price_v2(const Order &order)
{
    double price = calculate_items_total_price(order.items);
    if (order.has_discount) {
        price = apply_discount(price, order.vip_level);
    }
    price = apply_tax(price);
    return price;
}
```


### 2.3 constexpr--让函数在编译时就算出结果
```c++
#include <stdexcept>

// 1. constexpr不保证一定在编译时计算; 它只是给编译器一个提示, 让它可以在编译时进行常量表达式的计算
// 2. 不要想着把所有函数都变成constexpr, 该运行时计算(依赖运行时的配置或业务逻辑)的还要运行时计算
constexpr int factorial(int n)
{
    constexpr int max = 17;
    if (n < 0 || n > max) {
        throw std::invalid_argument("n must be between 0 and 17");
    }

    int x = 1;
    for (int i = 2; i <= n; i++) { x *= i; }

    return x;
}
```


### 2.4 小而快的函数应该内联
```c++
// 1. 简单的getter/setter函数
// 2. 常用的数学函数
// 3. 小型工具函数


// 稳定的API接口慎用内联
// constexpr函数自带内联属性
// 类中定义的函数默认就是内联的
// 模板函数通常定义在头文件中, 所以自带内联属性
```


### 2.5 noexcept--指定函数不抛异常
```c++
// 将函数标记为noexcept意味着: 函数不会抛出异常, 如果确实抛出了异常, 那么程序将调用std::terminate()终止执行


// 应用场景
// 1. 数学计算函数, 它们的功能通常很单纯
// 2. 构造函数/析构函数/复制构造函数/移动构造函数, 以确保它们在资源转移的过程中不会抛出异常
// 3. 内存操作函数, 要么成功要么崩溃, 不存在中间状态


// 不要盲目的给所有函数都加上noexcept, 一下情况需谨慎
// 1. 标准库一类的通用代码
// 2. 需要处理内存分配失败的情况
// 3. 调用了可能抛出异常的其他函数
```


### 2.6 不要盲目使用智能指针
```c++
// 只能指针在内存管理上确实提供了很大的便利, 但有的时候, 我们仅使用裸指针就足够了


// 杀鸡用牛刀
// 1. 额外的性能开销
// 2. 意图不明
// 3. 限制太多
void show_info(std::shared_ptr<Person> &person);

// 简单明了
void show_info(const Person &person);


// shared_ptr的主要开销
// 1. 引用计数管理: 每个shared_ptr都需要维护一个引用计数
// 2. 内存结构: shared_ptr本身占2个指针的大小, 一个指向对象, 一个指向控制块
// 3. 原子操作: 每次拷贝/销毁都要原子的修改引用计数; 多线程环境下的同步问题
// 4. 间接访问: 需要通过指针间接访问对象; 影响现代cpu流水线优化


// 总结
// 1. 如果不需要管理对象的生命周期, 就别用智能指针, 用裸指针或引用就够了
// 2. 过度使用智能指针会使代码变得又慢又复杂
```


### 2.7 纯函数 vs 非纯函数
```c++
// 纯函数
// 1. 传什么参数就用什么参数
// 2. 相同的输入总是得到相同的输出
// 3. 代码整洁有序, 易于理解和优化


// 非纯函数
// 1. 会悄悄的修改全局变量
// 2. 每次调用的结果都不一样, 令人迷惑
// 3. 容易产生意想不到的副作用
```


### 2.8 未使用的参数要悄悄的不命名
```c++
// C++17引入了标记[[maybe_unused]], 提示编译器不产生未使用的警告


template<typename T>
T* find(const std::set<T>& set, const T& v, [[maybe_unused]] std::string hint);
```


### 2.9 可重用的操作需要一个好名字
```c++
// 1. 如果有一个超长的lambda表达式需要被重复使用, 最好的做法是将其变成一个普通函数, 并给一个清晰的名称
```


## 3 参数传递
### 3.1 输入参数: 值 vs 引用
```c++
// 按值传递的特点
// 1. 简单直接, 没有指针解引用的开销


// 按引用传递的特点
// 1. 避免拷贝大型对象的开销


// 应用场景
// 1. 如果参数占用空间较小(int, double, 指针...), 按值传递
// 2. 如果参数占用空间较大(对象, 容器...), 按引用传递
// 3. 也有例外情况: 需要移动语义, 需要修改原始对象, ...
```


### 3.2 对于需要修改的参数, 使用非const引用
```c++
// 值得注意的是, 有些类型看似人畜无害, 实际上它们可能悄悄的修改原对象


#include <iostream>
#include <memory>
#include <vector>

class Widget
{
public:
    Widget(): data_() {}

    void add(int x) { data_.push_back(x); }

    void show_info() const
    {
        for (auto x: data_) { std::cout << x << " "; }
        std::cout << std::endl;
    }

private:
    std::vector<int> data_;
};

void process(std::shared_ptr<Widget> w)
{
    // 看似是一个按值传递, 实际上可以改变原始数据
    w->add(10);
    w->add(20);
    w->add(25);
}

void update_iterator(std::vector<int>::iterator it)
{
    // 迭代器虽然是按值传递的, 但它可以修改原始数据
    *it = 100;
}

auto main() -> int
{
    Widget w;
    std::shared_ptr<Widget> w1 = std::make_shared<Widget>(w);
    process(w1);
    w1->show_info();

    std::vector<int> v = {1, 2, 3, 4, 5};
    update_iterator(v.begin());
    for (auto vv: v) { std::cout << vv << " "; }
    std::cout << std::endl;

    return 0;
}
```


### 3.3 对于不需要修改的参数, 使用const引用
```c++
```


### 3.4 移动语义--让数据传递更高效
```c++
// 看到T&&参数, 记得使用std::move把它移走
// 被移动后的对象会变成一个空壳, 不要再使用它的值
// 移动是为了性能, 同时你也得对它负责


#include <iostream>
#include <string>
#include <utility>

std::string make_greeting(std::string &&name)
{
    return "hello, " + std::move(name) + "!";
}

auto main() -> int
{
    std::string name     = "tieshan";
    std::string greeting = make_greeting(std::move(name));
    std::cout << greeting << std::endl;
    return 0;
}
```


### 3.5 返回值 vs 输出参数
```c++
// 返回值
// 1. 简单直观
// 2. 编译器会做返回值优化(会删除不必要的拷贝), 不必过于担心性能, 正常情况下用直观的返回值就好


// 输出参数
// 1. 需要在循环中反复使用同一个容器
// 2. 复制或移动操作代价过大, 最好提前准备好结果容器
```


### 3.6 返回多个值时, 使用结构体封装
```c++
// 在c++中, 一个函数只能返回一个参数
// 如果需要返回多个参数, 可以使用输出参数, 但是可读性较差
// 更好的方式是, 使用结构体封装


#include <cmath>
#include <iostream>
#include <vector>

struct Stats
{
    double mean;     // 平均值
    double std_dev;  // 标准差
};

Stats calculate_stats(const std::vector<int> &data)
{
    Stats stats;

    for (auto x: data) { stats.mean += x; }
    stats.mean /= data.size();

    for (auto x: data) { stats.std_dev += (x - stats.mean) * (x - stats.mean); }
    stats.std_dev = std::sqrt(stats.std_dev / data.size());

    return stats;
}

auto main() -> int
{
    // C++17的结构化绑定可以让使用更方便
    std::vector<int> data {1, 2, 3, 4, 5, 6};
    auto [mean, std_dev] = calculate_stats(data);
    std::cout << "mean=" << mean << ", std_dev=" << std_dev << std::endl;
    return 0;
}
```


### 3.7 输入输出参数
```c++
// 某些情况下, 使用输入/输出参数是合理的
// 比如文件等IO操作
```


### 3.8 为复杂的返回数据定义专门的类型
```c++
#include <format>
#include <iostream>
#include <string>

struct Location
{
    double longitude;  // 经度
    double latitude;   // 纬度
    double altitude;   // 海拔

    std::string to_string() const { return std::format("({:.2f}, {:.2f}, {:.2f}m)", longitude, latitude, altitude); }
};

Location get_current_location()
{
    return {123.456, 78.901, 100.5};
}

auto main() -> int
{
    Location loc = get_current_location();
    std::cout << "current location: " << loc.to_string() << std::endl;
    return 0;
}
```


### 3.9 谨慎使用piar/tuple
```c++
#include <string>
#include <tuple>

// 糟糕的写法, 使用时不清楚各个值的具体含义
std::tuple<int, int, int> get_coordinate();

// 改成结构体就清晰多了, 否则还要回去翻文档才能知道各个值的含义
struct Coordinate
{
    int x;
    int y;
    int z;
};

struct QueryResult
{
    int status_code;
    std::string error_msg;
    bool has_data;
};
```


### 3.10 使用std::optional表示可能失败的操作
```c++
#include <iostream>
#include <optional>
#include <string>

std::optional<std::string> get_details(bool success)
{

    return success ? std::optional<std::string> {"details"} : std::nullopt;
}

auto main() -> int
{
    std::cout << get_details(true).value() << std::endl;
    std::cout << get_details(false).value_or("default") << std::endl;
    return 0;
}
```


### 3.11 指针 vs 引用
```c++
// 指针的特点
// 1. 可以为空nullptr
// 2. 潇洒随意


// 引用的特点
// 1. 必须与一个对象绑定
// 2. 安全可靠


// 如果即想要指针的潇洒, 又想要引用的可靠
// 可以使用gsl::not_null
// https://github.com/microsoft/GSL/blob/main/include/gsl/pointers
class Customer {};
void process(gsl::not_null<Customer*> customer);
```


## 4 智能指针
### 4.1 std::unique_ptr--有效的避免内存泄漏和悬空指针
```c++
// std::unique_ptr解决的问题
// 1. 通过析构函数自动释放内存
// 2. 避免悬空指针
// 3. 独占所有权, 移动语义更清晰


#include <iostream>
#include <memory>

struct Investment
{
};

Investment *make_investment_v1()
{
    Investment *investment = new Investment();

    // 这里要是抛个异常, investment指向的这块内存就无法访问了

    // 返回指针, 就是把这块内存的控制权移交给调用者, 需要调用者自己负责delete
    return investment;
}

void invest_v1()
{
    auto investment = make_investment_v1();

    if (true) {
        delete investment;
        return;
    }

    delete investment;
}

auto make_investment_v2()
{
    // 自定义deleter, 增加额外的处理逻辑
    auto deleter = [](Investment *p) {
        std::cout << "delete investment" << std::endl;
        delete p;
    };

    std::unique_ptr<Investment, decltype(deleter)> investment(new Investment(), deleter);
    return investment;
}

void invest_v2()
{
    auto investment = make_investment_v2();

    // 完全不用管内存的释放问题, std::unique_ptr会处理好的
    if (true) {
        return;
    }
}

auto main() -> int
{
    invest_v2();
    return 0;
}
```


### 4.2 std::shared_ptr--资源共享
```c++
// std::shared_ptr解决的问题
// 1. 自动管理引用计数, 避免内存泄漏
// 2. 线程安全, 允许多个线程同时访问同一资源


#include <memory>

class Image
{
};

class Widget
{
public:
    Widget(Image *image): image_(image) {}

    ~Widget()
    {
        // 究竟该不该释放image_?
        // 如果释放, 切好又有其它地方会用到这块内存, 可能导致程序崩溃
        // 如果不释放, 又可能导致内存泄漏
        delete image_;
    }

private:
    // 像一个定时炸弹
    Image *image_;
};

class Widget_V1
{
public:
    Widget_V1(std::shared_ptr<Image> image): image_(image) {}

    ~Widget_V1()
    {
        // 根本无需在析构函数中处理image_, 而是将这项工作交给智能指针
    }

private:
    std::shared_ptr<Image> image_;
};
```


### 4.3 std::unique_ptr vs std::shared_ptr
```c++
// std::unique_ptr
// 1. 


// std::shared_ptr
// 1. 资源共享场景
// 2. 缓存系统
// 3. 比std::unique_ptr更多的性能开销
// 4. 自动计数
// 5. 线程安全
// 6. 自定义清理方式
```


### 4.4 std::weak_ptr--解决循环引用问题
```c++
// 循环引用场景
// 有两个类相互引用对方, 如果对用std::shared_ptr, 那么引用计数永远不会等于0, 导致资源不被释放
// std::weak_ptr就像一个旁观者, 它可以看到对象是否还活着, 但是不会影响其生命周期


// std::weak_ptr的特点
// 1. 观察但不占有
// 2. 安全检查机制
// 3. 使用前需要lock获取一个临时的std::shared_ptr


#include <iostream>
#include <memory>
#include <string>

class Person_V1
{
public:
    Person_V1(const std::string &name): name_(name) {}

    void make_friend(std::shared_ptr<Person_V1> _friend) { friend_ = _friend; }

private:
    std::string name_;
    std::shared_ptr<Person_V1> friend_;
};

class Person_V2
{
public:
    Person_V2(const std::string &name): name_(name) {}

    void make_friend(std::shared_ptr<Person_V2> _friend) { friend_ = _friend; }

    void meet_friend()
    {
        // 需要时, 可以尝试将weak_ptr提升为shared_ptr
        // 通过lock方法来获取一个临时的shared_ptr, 如果对象已经被释放, 则返回nullptr
        if (auto ptr = friend_.lock()) {
            std::cout << "meet " << ptr->name_ << " successfully!" << std::endl;
        }
        else {
            std::cout << ptr->name_ << " has gone." << std::endl;
        }
    }

private:
    std::string name_;
    std::weak_ptr<Person_V2> friend_;  //使用weak_ptr存储, 不增加引用计数
};

void create_friendship()
{
    auto lucy = std::make_shared<Person_V1>("lucy");
    auto lily = std::make_shared<Person_V1>("lily");
    lucy->make_friend(lily);  // lily的引用计数变成2
    lily->make_friend(lucy);  // lucy的引用计数变成2
    // 函数结束时, 两个对象都还有一个引用, 所以不会被删除

    // 将shared_ptr改为weak_ptr, 情况就不一样了
    auto zhangsan = std::make_shared<Person_V2>("zhangsan");
    auto lisi     = std::make_shared<Person_V2>("lisi");
    zhangsan->make_friend(lisi);  // lisi的引用计数依旧是1
    lisi->make_friend(zhangsan);  // zhangsan的引用计依旧是1
    zhangsan->meet_friend();
    lisi->meet_friend();
}

auto main() -> int
{
    create_friendship();
    return 0;
}
```


### 4.5 std::unique_ptr vs std::shared_ptr vs std::weak_ptr
```c++
// std::unique_ptr就像是一个独行侠, 优先选择使用
// std::shared_ptr就像是一个社交达人, 适合需要共享的场景
// std::weak_ptr就像是一个观察者, 适合解决循环引用的问题
```


## 5 auto
### 5.1 auto(c++11), 让生活更美好
```c++
// 1. 可以自动处理所有的类型声明
// 2. 可以避免书写冗长的类型名


// ps:
// 在c++11之前, auto是用来声明自动变量的, 属实有点鸡肋
// 在c++11, auto通过类型推导成功逆袭


// 简单类型声明, auto的作用似乎不大
#include <map>
#include <string>
#include <vector>
auto x1 = 1;
auto x2 = 1.0;
auto x3 = "tieshan";
auto x4 = true;
auto x5 = nullptr;

// 复杂类型声明, auto直接化身救世主
std::vector<int> v {1, 2, 3};
auto it = v.begin();

std::map<std::string, int> map {{"zhangsan", 1}, {"lisi", 2}, {"wangwu", 3}};
auto pair = *map.begin();
```


### 5.2 auto(c++14), 返回类型推导大法
```c++
#include <iostream>
#include <string>

// 从前的函数这样写
auto multiply_v1(int x, double y) -> decltype(x * y)
{
    return x * y;
}

// 现在可以这样写
auto multiply_v2(int x, double y)
{
    return x * y;
}

// lambda表达式更是如虎添翼
// int|float|double|string..., 都可以来
auto magic_calculate = [](auto x, auto y) { return x + y; };

auto main() -> int
{
    std::cout << magic_calculate(2, 3.14) << std::endl;
    std::cout << magic_calculate(std::string("wu"), std::string("tieshan")) << std::endl;
    return 0;
}
```


### 5.3 auto(c++17), 结构化绑定
```c++
#include <iostream>
#include <map>
#include <string>
#include <utility>

auto main() -> int
{
    std::map<std::string, int> scores {{"zhangsan", 90}, {"lisi", 80}, {"wangwu", 70}, {"zhaoliu", 60}};
    for (const auto &[name, score]: scores) { std::cout << name << ": " << score << std::endl; }

    auto [x, y] = std::make_pair("tieshan", 26);
    std::cout << x << ": " << y << std::endl;

    return 0;
}
```


### 5.4 auto(c++20) 概念约束
```c++
#include <concepts>
#include <iostream>

// 约束让auto有了智能过滤的功能
// 此处process函数只接受整数类型
void process(std::integral auto x)
{
    std::cout << "received integer: " << x << std::endl;
}

template<std::floating_point auto V> struct Constants
{
    static constexpr auto value = V;
};

auto main() -> int
{
    process(10);
    process(20L);

    Constants<3.14> c;
    std::cout << "value of c: " << c.value << std::endl;

    return 0;
}
```


### 5.5 auto--更简洁的迭代器
```c++
#include <iostream>
#include <string>
#include <vector>

auto main() -> int
{
    std::vector<std::string> words = {"have", "a", "nice", "day", "auto"};

    // 传统写法, 像论文一样严肃
    for (std::vector<std::string>::iterator it = words.begin(); it != words.end(); it++) { std::cout << *it << " "; }
    std::cout << std::endl;

    // 使用auto, 像写散文一样
    for (auto it = words.begin(); it != words.end(); it++) { std::cout << *it << " "; }
    std::cout << std::endl;

    // 使用auto + ranged-based-for, 像写诗一样
    for (auto word: words) { std::cout << word << " "; }
    std::cout << std::endl;

    return 0;
}
```


### 5.6 auto--模板返回值的救星
```c++
#include <iostream>

template<typename T, typename U> auto add(T t, U u)
{
    return t + u;
}

auto main() -> int
{
    auto sum = add(1, 2);
    std::cout << "sum = " << sum << std::endl;
    return 0;
}
```


### 5.7 auto--作为参数
```c++
#include <iostream>
#include <string>

auto add(auto x, auto y)
{
    return x + y;
}

auto main() -> int
{
    std::cout << add(1, 2) << std::endl;
    std::cout << add(3.14, 2.71) << std::endl;
    std::cout << add(std::string("wu"), std::string("tieshan")) << std::endl;
    return 0;
}
```


### 5.8 auto--能力越大, 责任越大
```c++
// 切勿滥用
// 1. 导致代码可读性下降
// 2. 类型安全被削弱
// 3. 可能发生隐式类型转换, 导致bug
// 4. 增加维护难度
auto x = do_something();
auto y = process();


// 可能推导出意外的类型
auto str = "tieshan";  // 希望是std::string, 但实际上是const char*
auto v = {1};  // 希望是std::vector<int>, 但实际上是std::initializer_list<int>
auto value = get_reference();  // 可能丢失引用语义
```


## 6 c++防崩溃秘诀
### 6.1 编译期魔法--constexpr
```c++
// constexpr
// 1. 在编译期计算各种数值
// 2. 优化程序性能
// 3. 在编译期捕获异常
// 4. 能在编译期完成的计算, 尽量用constexpr, 毕竟谁不想要一个超快的程序


#include <array>

constexpr int square(int x)
{
    return x * x;
}

auto main() -> int
{
    // 在编译期直接算出结果: 100
    constexpr int x = square(10);

    // 在编译期就直到数组的大小
    std::array<int, square(3)> y = {1, 2, 3, 4};

    return 0;
}
```


### 6.2 编译期魔法--static_assert
```c++
#include <cstddef>
#include <type_traits>

template<typename T> class Vector
{
public:
    Vector()
    {
        // 运行时才发现问题, 太晚了
        // if (sizeof(T) > 256) {
        //     throw std::runtime_error("type T too large");
        // }

        // 更好的做法是在编译期检查
        static_assert(sizeof(T) <= 256, "type T only supports up to 256 bytes");
        static_assert(std::is_default_constructible_v<T>, "type T must be default constructible");
    }

private:
    T *data_;
    std::size_t size_;
};
```


### 6.3 编译期魔法--模板推导
```c++
#include <string>
#include <utility>
#include <vector>

auto main() -> int
{
    // 普通做法
    std::pair<std::string, std::vector<int>> p1 = std::make_pair(std::string("tieshan"), std::vector<int> {1, 2, 3});

    // 更好的做法
    using std::string_literals::operator""s;
    auto p2 = std::make_pair("tieshan"s, std::vector {1, 2, 3});

    return 0;
}
```


### 6.4 运行时检查--警惕使用裸指针
```c++
#include <algorithm>
#include <optional>
#include <vector>

struct Student
{
    int id;
};

std::optional<Student> find_student(Student *students, int size, int id)
{
    // 定时炸弹: 稍不注意就可能引起数组越界
    // 后期维护的时候, 无法直观的看出students表示的一个数组
    for (int i = 0; i < size; i++) {
        if (students[i].id == id) {
            return students[i];
        }
    }
    return std::nullopt;
}

std::optional<Student> find_student(const std::vector<Student> &students, int id)
{
    // 优势
    // 1. 

    // 第一种方式: 遍历整个数组
    // for (auto &student: students) {
    //     if (student.id == id) {
    //         return student;
    //     }
    // }
    // return std::nullopt;

    // 第二种方式: 使用find_if算法
    auto it = std::find_if(students.begin(), students.end(), [&id](const Student &student) {
        return student.id == id;
    });

    if (it == students.end()) {
        return std::nullopt;
    }
    return *it;
}
```


### 6.5 运行时检查--std::span, 数组的防护罩
```c++
// std::span的特点
// 1. 零开销抽象, 性能较好
// 2. 自带范围检查
// 3. 支持动态和静态大小
// 4. 可以兼容多种容器


#include <numeric>
#include <span>

double calculate_average(std::span<const double> scores)
{
    // 空数组
    if (scores.empty()) {
        return 0.0;
    }

    double sum = std::accumulate(scores.begin(), scores.end(), 0.0);
    return sum / scores.size();
}
```


### 6.6  自己实现安全的字符串类
```c++
#include <cstddef>
#include <stdexcept>
#include <string>

// 封装std::string, 额外添加
// 1. 空指针处理
// 2. 边界检查
class SafeString
{
public:
    SafeString(const char *data): data_(data ? data : "") {}

    SafeString(const std::string &data): data_(data) {}

    char at(size_t pos) const
    {
        if (pos >= data_.size()) {
            throw std::out_of_range("SafeString::at: pos out of range");
        }
        return data_[pos];
    }

    SafeString substr(size_t pos, size_t npos) const
    {
        if (pos >= data_.size()) {
            throw std::out_of_range("SafeString::substr: pos out of range");
        }
        return SafeString(data_.substr(pos, npos));
    }

private:
    std::string data_;
};
```


## 7. enum class--类作用域枚举
### 7.1 使用enum class的理由
```c++
// 1. 作用域控制: 不会产生名称冲突
// 2. 类型安全: 解决隐式类型转换问题
// 3. 自定义底层类型: enum class Flags std::unit8_t {};


// 颜色
enum class Color { RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET };
// 星期
enum class Weekday { SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY };
// 游戏角色状态
enum class PlayerState { IDLE, RUNNING, JUMPING, SWIMMING, WALKING, SLEEPING };

// HTTP状态码
enum class StatusCode : unsigned int {
    OK = 200,

    BADREQUEST   = 400,
    UNAUTHORIZED = 401,
    FORBIDDEN    = 403,
    NOTFOUND     = 404,

    SERVERERROR    = 500,
    NOTIMPLEMENTED = 501,
    BADGATEWAY     = 502,
};
```


### 7.2 枚举+switch
```c++
#include <iostream>
enum class Season { Spring, Summer, Autumn, Winter };

// 配合switch-case使用
void describe_season(Season season)
{
    switch (season) {
    case Season::Spring: std::cout << "spring" << std::endl; break;
    case Season::Summer: std::cout << "summer" << std::endl; break;
    case Season::Autumn: std::cout << "autumn" << std::endl; break;
    case Season::Winter: std::cout << "winter" << std::endl; break;
    default            : std::cout << "unknown season" << std::endl;
    }
}
```


### 7.3 枚举 -> 整数
```c++
#include <cstddef>
#include <iostream>
#include <type_traits>

enum class Gender { Male, Female };

enum class Numbers { One, Two, THree, Four, Five, Six, Seven, Eight, Nine, Ten };

// 安全的类型转换
void show_gender(Gender gender)
{
    // 枚举 -> 整数
    auto value = static_cast<std::underlying_type_t<Gender>>(gender);
    std::cout << "gender value: " << value << std::endl;

    // 计数
    constexpr auto count = static_cast<std::size_t>(Numbers::Eight);
    std::cout << "Numbers::Eight means " << count << std::endl;
}
```


### 7.4 位运算符重载
```c++
enum class Permissions : unsigned int {
    None    = 0,
    Read    = 1 << 0,
    Write   = 1 << 1,
    Execute = 1 << 2,

    All = Read | Write | Execute,  //可以自由组合
};

// 重载位或操作
constexpr Permissions operator|(Permissions a, Permissions b)
{
    return static_cast<Permissions>(static_cast<unsigned int>(a) | static_cast<unsigned int>(b));
}
```


### 7.5 枚举值命名
```c++
// 1. 推荐用单数, 即推荐用Status, 而不是Statuses
// 2. 使用描述性强的单词或组合, 即推荐用NotFound, 而不是Code404
```


### 7.6 自由的掌控内存大小
```c++
#include <cstdint>

enum class Small : int8_t {};
enum class Medium : int16_t {};
enum class Large : int32_t {};
```


### 7.7 让枚举更具表现力
```c++
enum class LogLevel { Debug, Info, Warning, Error, Fatal };

// 通过一个转换器, 将枚举值转换为字符串
constexpr const char *to_string(LogLevel level)
{
    switch (level) {
    case LogLevel::Debug  : return "DEBUG";
    case LogLevel::Info   : return "INFO";
    case LogLevel::Warning: return "WARNING";
    case LogLevel::Error  : return "ERROR";
    case LogLevel::Fatal  : return "FATAL";
    default               : return "UNKNOWN";
    }
}
```


## 8 类型转换的正确姿势
### 8.1 传统的类型转换-格式
```c++
int num  = 42;
float x1 = (float)num;  //C风格
float x2 = float(num);  //C++风格
```


### 8.2 传统的类型转换-没有约束
```c++
#include <iostream>

class Animal
{
public:
    void make_sound() { std::cout << "Animal sound" << std::endl; }
};

class Car
{
public:
    void drive() { std::cout << "Car drive" << std::endl; }
};

void magic_transform()
{
    Animal *cat = new Animal;
    cat->make_sound();

    // 传统的类型转换: 把Animal类转换为Car类
    Car *car = (Car *)cat;

    // 到这里发现问题了, 虽然转换成功了, 但是cat指针实际上还是指向Animal类的对象, 而不是Car类的对象
    // 可能存在潜在的隐患
    car->drive();
}
```


### 8.3 传统的类型转换-令人迷惑
```c++
// 如下代码x2究竟想干啥, 我们不得而知
// 是想修改写x1的值吗?
#include <iostream>
const char *x1 = "tieshan";
char *x2       = (char *)x1;

auto main() -> int
{
    x2[0] = 'H';
    std::cout << x1 << std::endl;
    std::cout << x2 << std::endl;
    return 0;
}
```


### 8.4 传统的类型转换-难以排查问题
```c++
void process(void *data)
{
    // 各种各样的转换, 简直是bug的温床
    // 传进来的参数data, 我们只知道他是一个指针
    // 具体能转换成哪些类型, 我们不得而知
    // 另外, 这段代码在编译期是检查不出来问题的, 增加了排查问题的难度
    int *nums      = (int *)data;
    double *prices = (double *)data;
    char *text     = (char *)data;
}

class Box
{
public:
    // 我们不知道T的具体类型
    // 也没法分析潜在的问题, 只能等到程序崩溃
    template<typename T> T *peek() { return (T *)data_; }

private:
    void *data_;
};
```


### 8.5 传统的类型转换-无法识别转换是否安全
```c++
class Base
{
};

class Derived: public Base
{
};

class Unrelated
{
};

Base *base           = new Base();
Derived *derived     = (Derived *)base;    // 可能失败
Unrelated *unrelated = (Unrelated *)base;  //肯定失败
```

### 8.6 static_cast
```c++
// 啥时候找static_cast?
// 1. 数值类型之间的转换
// 2. 继承关系明确的类型之间转换
// 3. 枚举和数值类型之间的转换


// 啥时候别用static_cast?
// 1. 不确定的指针转换 -> dynamic_cast
// 2. 完全不相关的类型 -> reinterpret_cast
// 3. 改变常量性质 -> const_cast


#include <iostream>
#include <memory>

class Animal
{
public:
    virtual void sound() {}
};

class Dog: public Animal
{
public:
    void bark() { std::cout << "bark!" << std::endl; }
};

class Cat: public Animal
{
public:
    void meow() { std::cout << "meow!" << std::endl; }
};

// static_cast的弱点1: 不会做任何运行时检查, 继承关系的类之间可以随意转换, 错误的转换可能带来未定义的行为或程序崩溃
void weak_1()
{
    Animal *p_animal = new Cat();
    Dog *p_dog       = static_cast<Dog *>(p_animal);
    p_dog->bark();  // 在我自己的环境上这里是可以的
}

auto main() -> int
{
    // 数值类型转换
    int x1    = 10;
    double x2 = static_cast<double>(x1);

    // 对象转换
    // static_cast可以把子类转换为父类, 也能把父类转换为子类(有一定风险), 但是不允许两个毫不相干的类之间进行转换
    Animal *p_animal = new Dog();
    Dog *p_dog = static_cast<Dog *>(p_animal);  // 向下转型, 需要考虑清楚, 建议使用dynamic_cast

    // 数值与枚举的转换
    enum class Color { RED, GREEN, BLUE };
    int y1   = static_cast<int>(Color::BLUE);
    Color y2 = static_cast<Color>(1);

    // 配合智能指针使用
    auto p1_dog    = std::make_shared<Dog>();
    auto p1_animal = static_cast<std::shared_ptr<Animal>>(p1_dog);

    weak_1();

    return 0;
}
```


### 8.7 dynamic_cast
```c++
// dynamic_cast的性能开销
// 1. 追踪vptr找到虚函数表
// 2. 查找类型信息
// 3. 遍历继承链


#include <format>
#include <iostream>

class Animal
{
public:
    // 编译期发现这里有一个虚函数, 会自动增加一个指向虚函数表的指针
    // void* __vptr;
    // 这个指针会记录: 类型信息, 完整的继承族谱关系
    virtual ~Animal()         = default;
    virtual void make_sound() = 0;
};

class Dog: public Animal
{
public:
    void make_sound() override { bark(); }

    void bark() { std::cout << "dog bark." << std::endl; }
};

class Cat: public Animal
{
public:
    void make_sound() override { meow(); }

    void meow() { std::cout << "cat meow." << std::endl; }
};

void safe_check(Animal *p_animal)
{
    // dynamic_cat在运行时检查和执行安全的向下转型, 如果无法转换, 则返回nullptr, 而不会导致程序崩溃
    // dynamic_cast的大致检查过程:
    //   1. 获取p_animal对象的vptr
    //   2. 通过vptr找到p_animal对象的实际类型
    //   3. 沿着继承链从下往上查找, 直至找到目标类型, 或者返回nullptr  ==>  引出一个问题, 如果继承链太长, 可能会导致dynaic_cast效率低下
    // dynamic_cast的工作需要借助于vptr, 所以如果一个对象根本没有vptr(没有虚函数, 没有多态性), 则无法使用dynamic_cast
    if (auto p_dog = dynamic_cast<Dog *>(p_animal)) {
        p_dog->bark();
    }
    else if (auto p_cat = dynamic_cast<Cat *>(p_animal)) {
        p_cat->meow();
    }
    else {
        std::cout << "it's neither a dog nor a cat." << std::endl;
    }

    // 像上面一样一个个的检查, 效率低, 而且当类型较多时, 代码量也会增加
    // 可以利用虚函数的能力(多态), 让程序自己决定应该调用哪一个方法?
    p_animal->make_sound();
}

auto main() -> int
{
    Animal *p_animal = new Cat();
    safe_check(p_animal);

    // RTTI(Run Time Type Information)三大利器
    // 1. typeid
    // 2. dynamic_cast
    // 3. type_info
    const std::type_info &info = typeid(*p_animal);
    std::cout << std::format("name={0}, hashcode={1}", info.name(), info.hash_code()) << std::endl;

    return 0;
}
```


### 8.8 static_cast vs dynamic_cast
```c++
// 性能
// dynamic_cast = static_cast + 运行时类型检查 + RTTI查找 + 安全保障


// 使用场景
// 1. 向上转换: 推荐static_cast
// 2. 向下转换: 推荐dynamic_cast, 但是如果能够确保类型一定正确, 也可以使用static_cast(程序员自己承担风险)
```


### 8.9 const_cast
```c++
#include <iostream>

class LegacyAPI
{
public:
    virtual bool need_non_const() = 0;
};

// 使用const_cast的情况: 我们确定函数不会修改参数, 由于某种原因形参没有加const修饰符, 导致无法接收const参数
void no_const_api(char *str) {}

// 滥用const_cast的后果1: 暗中修改了常量数据, 导致未定义的行为
// 导致未定义行为的原因: 编译器可能对const变量做了一系列的优化操作
void abuse_const_cast_1()
{
    const int x = 1;
    int *px     = const_cast<int *>(&x);
    *px         = 2;

    std::cout << "x = " << x << " | *px = " << *px << std::endl;
}

// 滥用const_cast的后果2: 导致程序崩溃
void abuse_const_cast_2()
{
    const char *greeting = "have a nive day!";
    char *p              = const_cast<char *>(greeting);
    *p                   = 'H';  // Access volation
}

// const_cast的推荐用法: 不到万不得已的时候, 不要轻易使用
void recommend(LegacyAPI *api, const char *data)
{
    if (api->need_non_const()) {
        char *data_v = const_cast<char *>(data);
        // do something with data_v in api
    }
    else {
        // do something with const data in api
    }
}

// const_cast功能如何实现的: 重写类型信息 + 不改变任何实际数据
// 这是一个编译期的魔法, 只能骗过编译器, 无法改变内存中数据实际的保护属性, 如果尝试修改只读内存, 后果非常严重
void realization()
{
    int v1        = 1;
    const int *v2 = &v1;                    // [const=true, type=int*]
    int *v3       = const_cast<int *>(v2);  // [const=false, type=int*]
}

auto main() -> int
{
    const char *name = "tieshan";
    // no_const_api(name);  // 编译器报错
    no_const_api(const_cast<char *>(name));

    abuse_const_cast_1();
    abuse_const_cast_2();

    return 0;
}
```


### 8.10 reinterpret_cast
```c++
#include <cstdint>
#include <iostream>

class Spaceship
{
};

class Dragon
{
};

struct Packet
{
    uint32_t data;
};

// reinterpret_cast的本质
void reality()
{
    // 1. 假设又一段内存: [01000001][01000010][01000011][01000100]
    const char *bytes = "ABCD";
    std::cout << "bytes: " << bytes << std::endl;

    // 2. reinterpret_cast不会修改任何位模式, 而是重新解释这一段内存
    // 需要注意的是, reinterpret_cast可能导致如下后果:
    // 2.1 错误的数据解释
    // 2.2 未定义的行为
    // 2.3 程序崩溃
    const int *num = reinterpret_cast<const int *>(bytes);
    std::cout << "num: " << *num << std::endl;
}

// reinterpret_cast应用之一: 不同类型对象之间的转换
void apply_01()
{
    Spaceship *spaceship = new Spaceship();
    Dragon *dragon       = reinterpret_cast<Dragon *>(spaceship);
}

// reinterpret_cast应用之二: 指针和整数之间的转换
void apply_02()
{
    int *px1      = new int(42);
    uintptr_t px2 = reinterpret_cast<uintptr_t>(px1);  // uintptr_t用于在整数和指针之间安全的转换
    int *px3      = reinterpret_cast<int *>(px2);
    delete px1;
}

// reinterpret_cast应用之三: 字节炼金术
void apply_03(char *buffer)
{
    Packet *packet = reinterpret_cast<Packet *>(buffer);
    std::cout << "packet->data: " << packet->data << std::endl;
}

// reinterpret_cast可能引发的问题
void problems()
{
    // 1. 类型大小不一致
    int8_t x1   = 42;
    int64_t *x2 = reinterpret_cast<int64_t *>(&x1);
    // *x2         = 1024;  // 程序崩溃

    // 2. 内存对齐
    char buffer[7];
    double *x3 = reinterpret_cast<double *>(buffer);
    // *x3        = 3.14;  // double通常需要8字节对齐, 程序崩溃
}

auto main() -> int
{
    reality();
    problems();
}
```


## 9 const vs define
### 9.1 const
```c++

#include <iostream>

// const的安全防护机制, 保护数据不被修改
void safe_const()
{
    const int MAX_PLAYERS = 100;
    const double PI       = 3.1415926;
}

// const与指针搭配
void const_and_ptr()
{
    // 1. 指向常量的指针
    // 不能修改原始数据, 但是可以修改指针指向的地址
    int height = 180;
    int weight = 58;

    const int *p1 = &height;
    std::cout << "height: " << *p1 << std::endl;
    p1 = &weight;
    std::cout << "weight: " << *p1 << std::endl;

    // 2. 常量指针
    // 不能修改指针指向的地址, 但是可以修改指针指向的数据
    int age       = 26;
    int *const p2 = &age;
    std::cout << "age=" << age << ", *p2=" << *p2 << std::endl;
    *p2 = 27;
    std::cout << "age=" << age << ", *p2=" << *p2 << std::endl;

    // 3. 指向常量的常量指针
    // 既不能修改指针指向的地址, 也不能修改指针指向的数据
    int money           = 10000;
    const int *const p3 = &money;
}

// const与引用搭配
void const_and_ref()
{
    // 1. 使用const引用的原因:
    // 引用原始数据, 性能较好
    // 保护原始数据不被修改
    // 可以接收临时数据
    int height    = 180;
    const int &r1 = height;
}
```


### 9.2 define
```c++
#include <iostream>

// 1. 无视类型检查, 单纯的做文本替换
#define MAX_VALUE    100
#define NAME         "tieshan"
#define DOUBLE_IT(x) (x * 2)

// 2. 可以随意的定义和取消定义
#define SECRET_CODE  12345

void do_something()
{
    std::cout << "secret code: " << SECRET_CODE << std::endl;
#undef SECRET_CODE
}

// 3. 极致性能, 不消耗内存(预处理阶段的文本替换)
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int x1 = MAX(1 + 2, 2);

// 4. 实际结果可能和预想的不同
// #define MULTIPLY(a, b) ((a) * (b))
#define MULTIPLY(a, b) (a * b)
int x2 = MULTIPLY(3 + 4, 2);  // 你希望得到14, 实际上得到11(运算优先级导致的)

#define DEBUG 1
// 5. 通过条件编译, 隐藏代码
#ifdef DEBUG
#define LOG(msg) std::cout << msg << std::endl
#else
#define LOG(msg)
#endif

auto main() -> int
{
    LOG("tieshan");

    // define的缺点
    // 1. 没有类型安全
    // 2. 没有作用域概念
    // 3. 发生再预处理阶段, 调试不方便
    return 0;
}
```


### 9.3 const vs define
```c++
// 1. 能用const, 就不用define
// 2. 使用define的场景:
//   2.1 条件编译
//   2.2 宏定义
//   2.3 头文件保护
```


## 10 引用
### 10.1 指针的缺点
```c++
// 1. 代码中到处都是星号和箭头
// 2. 需要经常取地址(&)和间接访问(*), 令人迷惑
// 3. 需要检查空指针
// 4. 为了保证运算优先级, 还得添加必要的括号
// 5. 指针算数和运算符重载混在一起, 简直就是灾难
```


### 10.2 引用
```c++
class Matrix
{
private:
    const int rows_ = 100;
    const int cols_ = 100;
    double data_[100][100];

public:
    // 尝试用指针重载减法运算, 糟糕的想法
    // 编译器会将(px1 - px2)理解韦指针算数, 而不是矩阵减法
    Matrix *operator-(const Matrix *const other)
    {
        for (int i = 0; i < this->rows_; i++) {
            for (int j = 0; j < this->cols_; j++) { this->data_[i][j] -= other->data_[i][j]; }
        }
        return this;
    }

    // 通过引用重载减法运算
    Matrix &operator-(const Matrix &other)
    {
        for (int i = 0; i < this->rows_; i++) {
            for (int j = 0; j < this->cols_; j++) { this->data_[i][j] -= other.data_[i][j]; }
        }

        return *this;
    }

    // const引用
    // 1. 可以绑定临时对象
    // 2. 编译器会自动创建临时对象进行类型转换
    // 3. 并且临时变量的声明周期延长至生命周期结束
    void print(const int &x) const
    {
        // ...
    }

    static void swap(int &x, int &y)
    {
        int tmp = x;
        x       = y;
        y       = tmp;
    }
};
```


## 11 构造函数
### 11.1 构造函数的各种形式
```c++
#include <string>

class Superhero
{
public:
    // 1. 默认构造函数
    // 如果没有任何显式定义的构造函数, 编译器也会自动生成一个默认构造函数
    Superhero() {}

    // 2. 带参数的构造函数
    Superhero(int p, const std::string &sp): power_(p), superpower_(sp) {}

    // 3. 拷贝构造函数
    // 如果不显式的定义构造函数, 编译器会自动创建, 但是对于管理动态内存的类, 最好手动写一个深拷贝的构造函数, 否则可能造成灾难性的后果
    // 下面一些场景中, 会自动调拷贝构造函数:
    //   3.1 对象作为参数传递
    //   3.2 函数放回对象
    //   3.3 用一个对象初始化另一个对象
    Superhero(const Superhero &other): power_(other.power_), superpower_(other.superpower_) {}

    // 4. 移动构造函数
    // 移动构造函数必须标记noexcept, STL容器才能放心的使用它
    Superhero(Superhero &&other) noexcept:
        power_(other.power_),
        superpower_(std::move(other.superpower_))
    {
    }

    // 5. 委托构造函数
    // 在构造函数中调用其它构造函数
    // 值得注意的是, 委托构造函数不能形成循环依赖
    Superhero(int p): Superhero(p, "tieshan") {}

private:
    int power_;
    std::string superpower_;
};
```


### 11.2 特殊的构造函数


## 12 const
### 12.1 修饰成员函数
```c++
class CakeCounter
{
public:
    CakeCounter(): cakes_eaten_(0) {}

    void eat_cake() { cakes_eaten_++; }

    // 保证绝对不会修改对象内部数据
    int get_cakes_eaten() const { return cakes_eaten_; }

private:
    int cakes_eaten_;
};
```


### 12.2 const -> mutable
```c++
#include <iostream>
#include <string>

class Logger
{
public:
    Logger(): count_(0) {}

    void log(const std::string &msg) const
    {
        std::cout << "Log msg: " << msg << std::endl;
        count_++;
    }

    int get_count() const { return count_; }

private:
    // 当成员函数被声明为const之后, 就是向编译器承诺不会修改任何数据
    // 但是有些时候需要我们在不违背承诺的前提下, 悄悄的修改一些内部状态
    // 此时, mutable就像一张VIP通行证, 允许我们在保持对象表面不变的情况下, 在内部做一些必要的更新
    // mutable的实际应用场景:
    //   1. 缓存机制: 偷偷存储计算结果
    //   2. 懒加载: 第一次访问时偷偷初始化
    //   3. 性能计数器: 统计函数的调用次数
    //   4. 线程同步: 修改互斥锁状态
    mutable int count_;
};
```


### 12.3 mutable的其它用法
```c++
#include <cmath>
#include <cstddef>
#include <iostream>
#include <vector>

// lambda表达式中的mutable
// 应用场景:
//   1. 计数器
//   2. 状态机
//   3. 缓存
//   4. 迭代器设计
void mutable_in_lambda()
{
    int count      = 1;
    auto increment = [count]() mutable {
        std::cout << "increment count addr: " << &count << std::endl;
        count++;
    };
    auto decrement = [&count]() {
        std::cout << "decrement count addr: " << &count << std::endl;
        count--;
    };

    std::cout << "origin count addr: " << &count << std::endl;

    // mutable可以在lambda表达式中修改按值捕获的变量, 但这其实是一种魔法(声明了一个同名变量), 是不会影响原始数据的
    increment();
    std::cout << "increment: count = " << count << std::endl;

    // 通过引用捕获, 是能够真实访问到原始数据的, 所以修改也会响应原始数据
    decrement();
    std::cout << "decrement: count = " << count << std::endl;
}

// 缓存优化案例
class MathHelper
{
public:
    double calculate(double input) const
    {
        // 缓存检测
        if (input == cached_input_ && is_cache_valid_) {
            return cached_result_;
        }

        double result = 0;
        for (int i = 0; i < 10000; i++) { result += std::sin(input * i); }

        cached_input_   = input;
        cached_result_  = result;
        is_cache_valid_ = true;

        return result;
    }

private:
    mutable double cached_input_  = 0.0;
    mutable double cached_result_ = 0.0;
    mutable bool is_cache_valid_  = false;
};
```


## 13 std::string_view


## 14 this指针
### 14.1 this指针的特点
```c++
// 1. 作为隐含参数传递给成员函数
// 2. 通常通过寄存器传递
// 3. 无法对this取址
// 4. 不会成为空指针
// 5. 静态成员函数没有this指针
// 6. 构造函数中, this指向正在构造的对象
// 7. this指针并不是存储在对象内部的
// 8. this指针的传递方式依赖于: 编译器实现, cpu架构
```


## 15 c++对象模型
### 15.1 c语言的烦恼
```c++
struct warrior
{
    int health;  //生命值
    int attack;  //攻击力
};

void warrior_attack(struct warrior *w, struct warrior *target)
{
    target->health -= w->attack;
}

void warrior_heal(struct warrior *w, int amount)
{
    w->health += amount;
}

int main()
{
    struct warrior hero  = {10, 10};
    struct warrior enemy = {50, 5};

    // 1. 函数太多太乱, 分不清哪个函数是给谁用的
    // 2. 数据完全暴露在外面, 谁都可以修改, 不安全
    // 3. 代码中到处都是指针, 令人眼花缭乱
    warrior_attack(&hero, &enemy);
    warrior_heal(&hero, 5);

    return 0;
}
```


### 15.2 指针时代
```c++
// 将函数和数据放在一起, 并加上访问控制
// 1. 内存占用非常多
// 2. 漫天的指针
// 3. 数据访问跳来跳去
// 4. cpu缓存命中率极低
class Student_1
{
private:
    int *p_age_;
    char **p_name_;
    float *p_score_;

public:
    void (*p_study)();
    void (*p_play)();
};

// 改进版
// 数据和成员函数分两种方式存储
// 1. 可以在运行时动态的选择需要调用的方法
class Student_2
{
private:
    int score_;

public:
    void study() { score_ += 5; }

    void play() { score_ -= 10; }
};

void (Student_2::*p_action)() = &Student_2::study;
Student_2 zhangsan;
(zhangsan.*p_action)();
p_action = &Student_2::play;
(zhangsan.*p_action)();
```


### 15.3 表格模型
```c++
// 优点:
// 1. 管理整齐
// 2. 查找方便
// 3. 容易扩展


// 缺点
// 1. 访问数据需要跳3级
// 2. 访问速度极差
// 3. 内存占用极大


#include <string>
#include <vector>

class ObjectLibrary
{
    // 数据目录
    struct DataCatalog
    {
        std::vector<int *> numbers;
        std::vector<std::string *> texts;
    } *data;

    // 函数目录
    struct FunctionCatalog
    {
        std::vector<Method *> methods;
        std::vector<Handler *> handlers;
    } *func;
};
```


### 15.4 最终方案
```c++
// 对象实例的内存布局
// 1. vptr + 成员数据(静态成员在全局数据区)


#include <string>

class Tool
{
    std::string name;
    static int total_tools;

    virtual void use() {}
};
```


## 16 左右值引用
### 16.1 左值引用
```c++
// 可以理解为给对象起了一个别名
```


### 16.2 右值引用
```c++
#include <string>
#include <utility>

template<typename T> void move_resource(T *&oldptr, T *&newptr)
{
    newptr = oldptr;
    oldptr = nullptr;
}

class Cat
{
};

class Home
{
public:
    Home(Home &&other)
    {
        // 指针成员的移动
        move_resource(other.cat_, cat_);

        // 对象成员的移动
        addr_ = std::move(other.addr_);
    }

private:
    Cat *cat_;
    std::string addr_;
};
```


### 16.3 引用折叠
```c++
#include <string>
#include <utility>

class Gift
{
public:
    Gift(const std::string &name): name_(name) {}

private:
    std::string name_;
};

template<typename T> void wrapper(T &&gift)
{
    // 1. 如果传入的是左值, T会被推导为Gift&, T&&展开之后就是 Gift& &&
    // 2. 如果传入的是右值, T会被推导为Gift, T&&展开之后就是 Gift&&

    // 于是C++11引入了引用折叠规则
    // 1. T& &      -> T&
    // 2. T& &&     -> T&
    // 3. T&& &     -> T&
    // 4. T&& &&    -> T&&
    // 总结下来就是: 只要有左值引用, 最后都会变成左值引用

    // 引用折叠的作用: 完美转发, 即保持gift原本的包装方式转发给别人
    std::forward<T>(gift);
}
```


## 17 深入static
### 17.1 修饰普通变量
```c++
#include <iostream>

void count_visitors()
{
    // 适用于:
    // 1. 统计函数被调用的次数
    // 2. 缓存计算结果
    // 3. 实现单例模式
    // 4. 维护函数内部状态
    static int visitors = 0;
    std::cout << "visitor order: " << ++visitors << std::endl;
}

auto main() -> int
{
    count_visitors();
    count_visitors();
}
```


### 17.2 修饰普通函数
```c++
// 作用:
// 1. 将函数的作用域限制为内部链接性, 方便隐藏实现细节, 并且可以防止不同编译单元中的函数名称冲突问题
// 2. 注意头文件中的函数不要使用static修饰, 否则会导致每个包含该头文件的源文件都有一个独立副本, 这回导致代码膨胀和不必要的复杂性
// 3. c++11之后, 推荐使用匿名空间来实现内部链接性, 它具有更好的语义和兼容性
```


### 17.3 修饰成员变量/函数
```c++
class Bank
{
public:
    // 静态成员函数的特点
    // 1. 不需要创建对象就能调用
    // 2. 只能访问static成员, 保证了数据的独立性
    // 3. 适合作为工具函数
    // 4. 可以作为命名空间使用
    static void set_interest_rate(double rate) { interest_rate_ = rate; }

    double get_interest() const { return balance_ * interest_rate_; }

private:
    // 静态成员变量适用于
    // 1. 跟踪类的总实例数
    // 2. 实现共享配置
    // 3. 管理公共资源
    // 4. 实现计数器或ID生成器
    static double interest_rate_;
    double balance_;
};

// 在源文件中初始化静态成员变量
double Bank::interest_rate_ = 0.05;
```


### 17.4 static-单例模式
```c++
// 精髓
// 1. 构造函数私有化
// 2. 私有静态成员变量保存唯一实例
// 3. 提供一个全局访问点


#include <iostream>

class Singleton
{
public:
    static Singleton *get_instance()
    {
        if (instance_ == nullptr) {
            instance_ = new Singleton();
        }
        return instance_;
    }

private:
    static Singleton *instance_;

    Singleton() { std::cout << "private constructor called" << std::endl; }
};

Singleton *Singleton::instance_ = nullptr;

auto main() -> int
{
    auto s1 = Singleton::get_instance();
    auto s2 = Singleton::get_instance();

    return 0;
}
```


### 17.5 计数器和ID生成器
```c++
class Visitor
{
public:
    Visitor() { visitors_++; }

private:
    static int visitors_;
};
```


### 17.6 static的初始化时机
```c++
// 1. 普通静态成员变量只能在类外初始化, 放在源文件中, 避免重复定义
// 2. const或constexpr修饰的静态成员可以在类中初始化, 因为它们是编译时常量
// 3. 局部静态变量(函数中)可以在声明时直接初始化
```


### 17.7 线程安全
```c++
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

class ThreadsafeCounter
{
public:
    static void increment()
    {
        std::lock_guard<std::mutex> lock(mutex_);
        count_++;
    }

    static void increment_without_lock() { count_++; }

    static void reset() { count_ = 0; }

    static int get() { return count_; }

private:
    static int count_;
    static std::mutex mutex_;
};

int ThreadsafeCounter::count_ = 0;
std::mutex ThreadsafeCounter::mutex_;

void multithread_increment(bool has_lock)
{
    const int num_threads    = 10;
    const int max_iterations = 10000;
    std::vector<std::thread> threads;
    void (*increment)()
        = has_lock ? ThreadsafeCounter::increment : ThreadsafeCounter::increment_without_lock;

    ThreadsafeCounter::reset();
    for (size_t i = 0; i < num_threads; i++) {
        auto fn = [increment]() {
            for (size_t j = 0; j < max_iterations; j++) { increment(); }
        };
        std::thread t(fn);
        threads.push_back(std::move(t));
    }

    for (auto &t: threads) { t.join(); }
    std::cout << "increment final count: " << ThreadsafeCounter::get() << std::endl;
}

auto main() -> int
{
    multithread_increment(true);
    multithread_increment(false);
}
```


### 17.8 注意
```c++
// 静态变量会一直占用内存直到程序结束
// 过渡使用可能会导致巨大的内存开销
// 所以, 使用之前请谨慎评估是否必要
```


## 18 c++20模块
### 18.1 传统头文件的痛点
```c++
// 1. 编译速度慢: 如果同一个头文件被包含多次, 那么会重复进行预处理, 语法分析, 词法分析
// 2. 不规范的宏定义会污染命名空间
// 3. 依赖关系复杂
```


### 18.2 模块的特点
```c++
// 1. 模块预编译一次, 生成接口文件
// 2. 编译单元之间共享接口文件
```


### 18.3 模块初探
> - [clang++官方文档](https://clang.llvm.org/docs/Modules.html#introduction)


## 19 std::format
### 19.1 使用方法
```c++
// std::format是C++20引入的新标准, 借鉴了python中的f-string, 用法类似
// std::format能在编译时进行检查


#include <chrono>
#include <format>
#include <iostream>
#include <locale>
#include <string>

auto main() -> int
{
    std::string msg;

    // 1. std::format的第一种打开方式
    // template<typename... Args> std::string format(std::format_string<Args...> fmt, Args&&... args);
    msg = std::format("he is {} years old today.", 28);
    std::cout << msg << std::endl;

    // 2. std::format的第二种打开方式
    // template<typename... Args> std::string format(const std::locale& loc, std::format_string<Args...> fmt, Args&&... args);
    msg = std::format(std::locale(), "it's {} now!", std::chrono::system_clock::now());
    std::cout << msg << std::endl;

    // 此外, 1和2还有各自的宽字符版本
}
```


### 19.2 格式化语法
```c++
// 1. 整数:     {:d}
// 2. 浮点数:   {:.2f}
// 3. 左对齐:   {:<10}
// 4. 右对齐:   {:>10}
// 5. 居中:     {:^10}
// 6. 填充字符:  {:0>10}


// 更多参考: https://docs.python.org/zh-cn/3/library/string.html#formatstrings
```


### 19.3 动态格式字符串
```c++
#include <format>
#include <string>
#include <string_view>

// C++20
std::string dynamic_format_cpp20(std::string_view fmt, const std::string &name)
{
    return std::vformat(fmt, std::make_format_args(name));
}

// c++26
std::string dynamic_format_cpp26(std::string_view fmt, const std::string &name)
{
    return std::format(std::runtime_format(fmt), name);
}
```


## 20 数据解包
### 20.1 绑定方式
```c++
#include <string>
#include <tuple>

struct Person
{
    std::string name;
    int age;
};

Person get_person()
{
    return {"tieshan", 18};
}

auto main() -> int
{
    // 1. 数组绑定
    int scores[3]                                  = {98, 95, 89};
    [[maybe_unused]] auto [chinese, math, english] = scores;

    // 2. tuple绑定
    auto student     = std::make_tuple<std::string, int>("tieshan", 18);
    auto [name, age] = student;

    // 3. 结构体绑定
    const auto [name1, age1] = get_person();
}
```


### 20.2 结构化绑定 + if判断
```c++
#include <format>
#include <iostream>
#include <map>
#include <string>

auto main() -> int
{
    std::map<std::string, int> scores;
    if (const auto [it, success] = scores.insert({"tieshan", 98}); success) {
        std::cout << std::format("{}'s score is {}.\n", it->first, it->second);
    }
}
```


### 20.3 绑定临时变量
```c++
#include <utility>

auto main() -> int
{
    // 临时变量不能绑定到非const引用上
    // auto &[x, y] = std::make_pair(1, 2);

    // 1. const引用
    [[maybe_unused]] const auto &[x1, y1] = std::make_pair(1, 2);

    // 2. 转发引用
    [[maybe_unused]] auto &&[x2, y2] = std::make_pair(1, 2);

    // 3. 具名变量
    auto pair                       = std::make_pair(1, 2);
    [[maybe_unused]] auto &[x3, y3] = pair;
}
```


## 21 std::optional
### 21.1 与传统方法对比
```c++
#include <format>
#include <iostream>
#include <optional>
#include <string>
#include <utility>

struct User
{
    std::string name;
    int age;

    void say_hi() const
    {
        std::cout << std::format("hi, my name is {} and I am {} years old.\n", name, age);
    }
};

// 方法1: 指针
// 找到了就返回指针, 找不到就返回nullptr
// 问题: 指针该由谁来维护?
User *find_user_01(const std::string &name);

// 方法2: pair
// 返回一个值和一个标志位
// 问题: 就算没有找到, 也要构造User, 浪费内存空间
std::pair<User, bool> find_user_02(const std::string &name);

// 方法3: std::optional
std::optional<User> find_user_03(const std::string &name)
{
    if (name == "tieshan") {
        return User {"tieshan", 25};
    }
    return std::nullopt;
}

auto main() -> int
{
    // 第一种使用方式: 直接判断
    if (auto user = find_user_03("tieshan")) {
        user->say_hi();
    }

    // 第二种使用方式: 给默认值
    auto user1 = find_user_03("zhangsan").value_or(User {"lisi", 18});
    user1.say_hi();
}
```


### 21.2 应用场景
```c++
#include <algorithm>
#include <cctype>
#include <iostream>
#include <optional>
#include <string>

struct User
{
    std::string name;
    int age;
};

// 1. 解析端口号
std::optional<int> parse_port(const std::string &desc)
{
    if (!std::all_of(desc.begin(), desc.end(), ::isdigit)) {
        return std::nullopt;
    }

    int port = std::stoi(desc);
    if (port > 0 && port < 65536) {
        return port;
    }
    return std::nullopt;
}

// 2. 链式调用
std::optional<User> find_user(const std::string &name);
std::optional<std::string> get_user_email(const User &user);
std::optional<bool> send_email(const std::string &email);

void notify_user(const std::string &name)
{
    [[maybe_unused]] auto result
        = find_user(name).and_then(get_user_email).and_then(send_email).value_or(false);
    if (result) {
        std::cout << "email has sent successfully.\n";
    }
    else {
        std::cout << "email failed to send.\n";
    }
}
```


### 21.3 高级特性
```c++
#include <optional>
#include <stdexcept>

auto main() -> int
{
    // 1. 构造
    std::optional<int> op1;
    std::optional<int> op2(std::nullopt);
    std::optional<int> op3(42);
    std::optional<int> op4 = 42;
    std::optional<int> op5(op3);
    std::optional<int> op6 = std::make_optional(42);

    // 2. 获取std::optional的值
    // 2.1 value()
    try {
        int x1 = op6.value();
    }
    catch (const std::bad_optional_access &) {
        throw std::runtime_error("optional is empty");
    }
    // 2.2 operator*
    if (op6) {
        int x2 = *op6;
    }
    // 2.3 value_or()
    int x3 = op6.value_or(0);
}
```


### 21.4 c++23新特性
```c++
#include <iostream>
#include <optional>
#include <string>

std::optional<int> safe_divide(int a, int b)
{
    if (b == 0) {
        return std::nullopt;
    }
    return a / b;
}

std::optional<std::string> tostring(int num)
{
    return std::to_string(num);
}

auto main() -> int
{
    // 1. transform: 结果加工
    auto result1 = safe_divide(10, 2).transform([](int x) { return x * 2; });
    std::cout << "result1: " << result1.value_or(-1) << std::endl;

    // 2. and_then: 链式调用
    auto result2 = safe_divide(10, 2).and_then([](int x) { return ::tostring(x); });
    std::cout << "result2: " << result2.value_or("") << std::endl;

    // 3. or_else: 异常处理
    auto result3 = safe_divide(10, 0).or_else([]() { return std::optional<int>(0); });
    std::cout << "result3: " << result3.value_or(-1) << std::endl;
}
```


### 21.5 性能
```c++
// 特点
// 1. 内存使用仅比原始对象多1个字节
// 2. 数据存储空间自动对齐
// 3. 没有动态内存分配, 所有数据都在栈上
template<typename T> class optional
{
    bool has_value_;
    alignas(T) char data_[sizeof(T)];
};
```


## 22 聚合初始化
### 22.1 基本语法
```c++
#include <string>

struct Person
{
    std::string name;
    int age;
};

auto main() -> int
{
    // 1. 基础写法
    Person p1 = {"tieshan", 25};

    // 2. c++11, 可以省略等号
    Person p2 {"tieshan", 25};

    // 3. c++20, 给每个值贴上标签
    Person p3 = {.name = "tieshan", .age = 25};
}
```


### 22.2 使用聚合初始化的前提
```c++
// 1. 数据是public
// 2. 没有构造函数
// 3. 没有虚函数
std::array<std::array<int, 2>, 3> grid = {{{1, 2}, {3, 4}, {5, 6}}};
```


## 23 告别裸数组
### 23.1 std::array的结构
```c++
template<typename T, std::size_t N> class array
{
};
```