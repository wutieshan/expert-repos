#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>

class demo
{
public:
    demo() {}

    void produce()
    {
        for (int i = 0; i < 20; i++) {
            std::unique_lock<std::mutex> lock(mutex_);
            cv_.wait(lock, [this]() { return queue_.size() < max_size; });
            queue_.push(i);
            std::cout << "produced: " << i << std::endl;
            cv_.notify_one();
        }
    }

    void consume()
    {
        while (true) {
            std::unique_lock<std::mutex> lock(mutex_);
            cv_.wait(lock, [this]() { return !queue_.empty(); });
            int value = queue_.front();
            queue_.pop();
            std::cout << "comsumed: " << value << std::endl;
            cv_.notify_one();
            if (value == 19) {
                break;
            }
        }
    }

private:
    std::queue<int> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;

    const int max_size = 10;
};