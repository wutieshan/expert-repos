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
// 两个线程同时需要锁住多个互斥, 某一时刻它们都分别锁住了其中一部分, 等待对方解锁, 形成死循环


// 防范死锁的方法
// 1. 确保始终按照相同的顺序加锁
```