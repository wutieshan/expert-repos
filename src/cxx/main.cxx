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