# multi-thread


## reference
- [C++并发编程实战](https://weread.qq.com/web/reader/65a3287072898be365ae09ekc81322c012c81e728d9d180)


## 1 并发简介


## 2 线程管控


## 3 在线程间共享数据
### 3.1 线程间共享数据的问题
```c++
// 归根结底, 多线程共享数据的问题由数据改动引起


// 针对某一特定数据的"不变量", 如双向链表,
// 假设现在要删除其中一个节点, 则该节点相邻两侧节点的指针需要更新, 指向彼此,
// 如果其中一个节点先更新, 那么这个"不变量"关系就被破坏, 直到另一个节点也更新完成, "不变量"关系又重新建立


// 条件竞争: 在多线程环境下, 执行结果取决于线程执行的相对次序
// 一些情况下, 这是可以接受的, 如向队列添加数据项以待处理, 先添加哪个数据通常不重要
// 另一些情况下, 条件竞争导致"不变量"被破坏, 这会导致程序未定义的行为


//  采用并发计数的程序通常会涉及许多复杂的逻辑, 其目的正是避开恶性条件竞争, 通常有以下几种方法:
// 1. 包装数据结构, 确保"不变量"被破坏时, 中间状态只对执行改动的线程可见, 在其它线程的看来, 改动要么尚未开始, 要么已经完成
// 2. 修改数据结构的设计以及"不变量", 由一连串不可拆分的操作完成数据变更, 而每个操作都维持数据结构的"不变量"关系  ==>  无锁编程
// 3. 把修改数据结构当作事务处理, 完成之后统一提交  ==>  事务性编程, 软件事务内存(STM)
```


### 3.2 用互斥保护共享数据
```c++
// 基本思想
// 访问数据结构之前, 先锁住与数据相关的互斥(mutual exclusion, mutex, 一种同步原语), 访问结束后, 再解锁互斥
```


#### 3.2.1 c++中使用互斥
```c++
// 通过构造std::mutex实例来创建互斥
// 调用成员函数lock()和unlock()来对互斥加锁和解锁
// 这种方式需要记住, 每条代码路径(包括异常)都要调用unlock()


// c++标准库提供了std::lock_guard, 是针对互斥的RAII封装, 在构造时枷锁, 析构时解锁, 从而保证互斥总是被正确解锁
// 一般的, 会将数据和对应的互斥封装到一个类中


// 如果成员函数返回指针或引用, 指向受保护的数据, 此时互斥的保护形同虚设
// 所以, 使用互斥保护共享数据时, 需要谨慎设计接口, 防止留后门


#include <algorithm>
#include <list>
#include <mutex>

class Lst
{
public:
    Lst() {}

    void add_to_lst(int num)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        data_.push_back(num);
    }

    bool contains(int num)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = std::find(data_.begin(), data_.end(), num);
        return it != data_.end();
    }

private:
    std::list<int> data_;
    std::mutex mutex_;
};
```

#### 3.2.2 组织&编排代码以保护共享数据
```c++
// 不能向锁所在作用域之外传递共享数据的指针或引用


// 1. 谨慎设计接口, 不向调用者提供指向共享数据的指针或引用
// 2. 警惕在临界区调用其它能够访问共享数据的函数
```


#### 3.2.3 发现固有接口的条件竞争
```c++
// 使用栈举例
// 即使在栈容器的成员函数内部使用互斥保护数据
// 在接口间也可能存在条件竞争, 如: 在empty()和top()之间, 另一个线程可能调用pop()导致栈为空, 从而top()操作异常
if (!stack.empty()) {
    const int v = stack.top();
}


// 解决方案
// 1. 更改接口的实现方式: 如top在空栈上调用时抛异常
// 2. 传入引用: 通过一个外部变量接收栈容器弹出的元素
// 3. 提供不抛异常的拷贝构造函数或移动构造函数
// 4. 返回指针, 指向弹出的元素


// 总结
// 锁的粒度大小是一个值得注意的问题
// 太小, 需要被保护的数据没有完全覆盖, 可能出现条件竞争
// 太大, 极端的例子, 所有线程都受同一个全局锁限定, 这会消除并发带来的任何性能优势


#include <exception>
#include <memory>
#include <mutex>
#include <stack>
#include <utility>

struct empty_stack: std::exception
{
    const char *what() const noexcept override;
};

template<typename T> class threadsafe_stack
{
public:
    threadsafe_stack() {};

    threadsafe_stack(const threadsafe_stack &other)
    {
        std::lock_guard<std::mutex> lock(other.mutex_);
        data_ = other.data_;
    }

    threadsafe_stack &operator=(const threadsafe_stack &) = delete;

    void push(T value)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        data_.push(std::move(value));
    }

    std::shared_ptr<T> pop()
    {
        std::lock_guard<std::mutex> lock(mutex_);
        if (data_.empty()) {
            throw empty_stack();
        }

        const std::shared_ptr<T> result = std::make_shared(data_.top());
        data_.pop();
        return result;
    }

    void pop(T &value)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        if (data_.empty()) {
            throw empty_stack();
        }

        value = data_.pop();
        data_.pop();
    }

    bool empty() const
    {
        std::lock_guard<std::mutex> lock(mutex_);
        return data_.empty();
    }

private:
    std::stack<T> data_;
    mutable std::mutex mutex_;
};
```


#### 3.2.4 死锁
```c++
// 问题产生原因
// 为了完成某项操作而需要对多个互斥加锁, 在某一时刻, 两个线程都持有了一部分锁, 而又相互等待对方持有的锁被释放, 由此形成循环等待


// 防范死锁的方法
// 1. 始终按照相同的顺序加锁
// 2. 使用std::lock()同时锁ovudoge互斥, 而没有死锁的风险
#include <mutex>

class some_big_object
{
};

void swap(some_big_object &, some_big_object &);

class X
{
public:
    X(const some_big_object &obj): obj_(obj) {}

    friend void swap_v1(X &x1, X &x2)
    {
        if (&x1 == &x2) {
            return;
        }
        std::lock(x1.mtx_, x2.mtx_);                                    // 在此处同时锁住两个互斥, std::lock()的语义是all-or-nothing
        std::lock_guard<std::mutex> lock_x1(x1.mtx_, std::adopt_lock);  // 使用std::adopt_lock表明互斥已经被锁住, 仅做所有权的转移, 以构造lock_guard对象
        std::lock_guard<std::mutex> lock_x2(x2.mtx_, std::adopt_lock);
        swap(x1.obj_, x2.obj_);
    }

    friend void swap_v2(X &x1, X &x2)
    {
        if (&x1 == &x2) {
            return;
        }

        // c++17提供的RAII模板std::scoped_lock针对swap_v1的简化
        // std::soped_lock与std::lock_guard等价, 唯一区别是std::scoped_lock接收可变参数
        std::scoped_lock lock(x1.mtx_, x2.mtx_);
        swap(x1.obj_, x2.obj_);
    }

private:
    some_big_object obj_;
    std::mutex mtx_;
};
```


####  3.2.5 防范死锁的补充准则
```c++
// 虽然死锁最常见的诱因是锁操作, 但即便没有锁, 也可能发生死锁  ->  任何同步机制导致的循环等待都会导致死锁出现
// 考虑一种情况: 线程A和B相互join(), 构成循环等待, 也会引起死锁
// 防范死锁的基本准则: 只有另一线程有可能在等待当前线程, 那么当前线程不能反过来等待它
// 具体如下:
// 1. 避免嵌套锁
// 2. 一旦持有锁, 就须避免调用由用户提供的API  ->  规则1的延伸
// 3. 根据固定顺序获取锁
// 4. 按层级加锁: 一旦在某个层级的互斥上持有锁, 那么只能由相对低层级的互斥获取锁, 从而限制代码行为
// 5. 将准则推广到锁操作之外


#include <climits>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <vector>

class hierarchical_mutex
{
public:
    explicit hierarchical_mutex(unsigned long value): value_(value), previous_value_(0) {}

    void lock()
    {
        check_for_hierarchy_violation();
        mtx_.lock();
        update_hierarchy_value();
    }

    void unlock()
    {
        if (this_thread_value_ != value_) {
            throw std::logic_error("mutex hierarchy violation");
        }
        this_thread_value_ = previous_value_;
        mtx_.unlock();
    }

    bool try_lock()
    {
        check_for_hierarchy_violation();
        if (!mtx_.try_lock()) {
            return false;
        }
        update_hierarchy_value();
        return true;
    }

private:
    std::mutex mtx_;
    const unsigned long value_;
    unsigned long previous_value_;
    static thread_local unsigned long this_thread_value_;

    void check_for_hierarchy_violation() const
    {
        if (this_thread_value_ <= value_) {
            throw std::logic_error("mutex hierarchy violation");
        }
    }

    void update_hierarchy_value()
    {
        previous_value_    = this_thread_value_;
        this_thread_value_ = value_;
    }
};

thread_local unsigned long hierarchical_mutex::this_thread_value_ = ULONG_MAX;

hierarchical_mutex high_level_mutex(200);
hierarchical_mutex low_level_mutex(100);

int do_low_level_stuff()
{
    std::cout << "low level stuff done" << std::endl;
    return 0;
};

int low_level_func()
{
    std::lock_guard lock(low_level_mutex);
    return do_low_level_stuff();
}

void do_high_level_stuff(int value)
{
    std::cout << "input argument: " << value << std::endl;
}

void high_level_func()
{
    std::lock_guard lock(high_level_mutex);
    do_high_level_stuff(low_level_func());
}

auto main() -> int
{
    std::vector<std::thread> threads;
    threads.emplace_back(std::thread(high_level_func));
    threads.emplace_back(std::thread([]() {
        high_level_func();
        low_level_func();
    }));
    threads.emplace_back([]() {
        low_level_func();
        high_level_func();
    });
    for (auto &t: threads) { t.join(); }
}
```


#### 3.2.6 std::unique_lock
```c++
// 相较于std::lock_guard, std::unique_lock提供了更多的灵活性
// 可以自主选择在构造时是否给互斥加锁
// 1. std::adopt_lock  ->  转义归属权
// 2. std::defer_lock  ->  延迟加锁


// 但是需要为这份灵活性付出代价, 即储存和更新互斥信息
```


#### 3.2.7 在不同作用域之间转移互斥归属权
```c++
// std::unique_lock不占有与之关联的互斥
// 因此, 可以在不同作用域之间转移互斥的归属权
// 1. 如果数据的来源是左值, 则必须显式的调用std::move()转移其归属权, 以免归属权以外转移到别处
// 2. 如果数据的来源是右值, 则会自动进行


// 应用1: 在函数中锁定互斥, 将归属权转义给调用者, 允许其在同一个锁的保护下执行其它操作
```


#### 按适合的粒度加锁
```c++
// 仅在访问共享数据期间锁住互斥
// 持有锁期间尽量避免耗时的操作


#include <chrono>
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

static int count = 0;
static std::mutex mutex;

void get_and_process_data()
{
    std::unique_lock<std::mutex> lock(mutex);
    count++;

    // 耗时操作, 暂时解锁
    lock.unlock();
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    lock.lock();
    count--;
}

auto main() -> int
{
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; i++) { threads.push_back(std::thread(get_and_process_data)); }
    for (auto &t: threads) { t.join(); }
    std::cout << "now, count = " << count << std::endl;
}
```


### 3.3 保护共享数据的其它工具
#### 3.3.1 在初始化过程中保护共享数据
```c++
// 延迟初始化场景


#include <mutex>

struct data_packet
{
};

struct connection_info
{
};

struct connection_handle
{
    void send(const data_packet &);
    data_packet receive();
};

class DB
{
public:
    static DB &create(const connection_info &info)
    {
        // case1: 对于只需要用到唯一一个全局实例的情况

        // c++11规定初始化只会在某一线程上单独发生
        // 在初始化完成之前, 其它线程不会越过静态数据的声明而继续执行
        static DB instance(info);
        return instance;
    }

    void send(const data_packet &data)
    {
        // case2: 对于需要函数调用的情况

        // 令人诟病的双重检验锁定模式
        // 可能导致恶性条件竞争, 即一个线程在读取指针, 另一个线程获取到锁, 进入保护范围进行写操作, 由此产生读写不同步问题

        // std::call_once确保指针初始化被某一个线程安全且唯一的完成
        // 必要的同步数据由std::once_flag存储
        // 同时, 相比于显式的使用互斥, 开销更低
        std::call_once(flag_, &DB::connect, this);
        handle_.send(data);
    }

    data_packet receive()
    {
        std::call_once(flag_, &DB::connect, this);
        return handle_.receive();
    }

private:
    connection_info info_;
    connection_handle handle_;
    std::once_flag flag_;

    DB(const connection_info &info): info_(info) {}

    void connect()
    {
        // init handle_ there
    }
};
```


#### 3.3.2 保护甚少更新的数据结构
```c++
// 读写锁
// std::shared_timed_mutex相较于std::shared_mutex更灵活, 但需要付出相应的性能代价
// 特点:
// 1. 如果共享锁已被某些线程持有, 此时其它线程试图获取排他锁, 就会发生阻塞, 直到全部共享锁被释放
// 2. 如果任一线程持有排他锁, 此时, 其它线程试图获取共享锁和排他锁也会被阻塞


#include <map>
#include <mutex>
#include <shared_mutex>
#include <string>

class dns_entry
{
};

class dns_cache
{
public:
    dns_entry find_entry(const std::string &domain) const
    {
        // 读: 允许多个线程同时持有
        std::shared_lock lock(mutex_);
        auto it = entries_.find(domain);
        return it == entries_.end() ? dns_entry() : it->second;
    }

    void update_entry(const std::string &domain, const dns_entry &entry)
    {
        // 写: 同时只能由一个线程持有
        std::lock_guard lock(mutex_);
        entries_[domain] = entry;
    }

private:
    std::map<std::string, dns_entry> entries_;
    mutable std::shared_mutex mutex_;
};
```


#### 3.3.3 递归加锁
```c++
// std::recursive_mutex
// 特点:
// 1. 对于某互斥, 同一线程可以多次加锁
// 2. 必须释放全部锁之后, 才可以让另一个线程获取锁


// 
```