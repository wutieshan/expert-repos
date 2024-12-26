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