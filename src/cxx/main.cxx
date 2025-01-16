#include <atomic>

// 使用std::atomic_flag实现自旋锁
class spinlock
{
public:
    spinlock(): flag_(ATOMIC_FLAG_INIT) {}

    void lock()
    {
        // 自旋等待, 一旦读取值变成false, 则表明线程已将标志设置为成立
        // 可以发现, 这种实现是在lock()函数内忙等
        while (flag_.test_and_set(std::memory_order_acquire)) {}
    }

    void unlock() { flag_.clear(std::memory_order_release); }

private:
    std::atomic_flag flag_;
};