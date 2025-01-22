#include <iostream>

void test(int *t)
{
    std::cout << "t1" << std::endl;
}

void test(int t)
{
    std::cout << "t2" << std::endl;
}

auto main() -> int
{
    std::cout << (NULL == 0) << std::endl;
}