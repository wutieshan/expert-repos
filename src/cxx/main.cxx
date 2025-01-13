#include <cmath>
#include <future>
#include <iostream>
#include <stdexcept>

double square_root(double x)
{
    if (x < 0) {
        throw std::invalid_argument("sqrt argument must be non-negative");
    }
    return std::sqrt(x);
}

auto main() -> int
{
    std::future<double> f = std::async(square_root, -1);
    std::cout << "Square root of 25: " << f.get() << std::endl;
}