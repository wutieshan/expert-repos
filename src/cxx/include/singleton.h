#pragma once
#include <iostream>


template <typename T>
class Singleton
{
private:
    static T* inst_;

private:
    Singleton() { std::cout << "Singleton() be called." << std::endl; }
    ~Singleton() {};
    Singleton(const T&)    = delete;
    T& operator=(const T&) = delete;

public:
    static T* get_inst()
    {
        if (inst_ == nullptr) { inst_ = new T(); }
        return inst_;
    }
};


template <typename T>
T* Singleton<T>::inst_ = nullptr;
