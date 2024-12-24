# Python C API


## demo
### 1. main.cxx
```c++
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>


auto main() -> int {
    // 初始化python解释器
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('c:/tieshan/project/learn-cxx')");

    // 导入模块
    PyObject* pModule = PyImport_ImportModule("example");
    if (pModule == nullptr) {
        std::cerr << "Failed to import module example" << std::endl;
        return 1;
    }

    // 获取python函数
    PyObject* pFunc = PyObject_GetAttrString(pModule, "hello");
    if (pFunc == nullptr || !PyCallable_Check(pFunc)) {
        std::cerr << "Failed to get function hello" << std::endl;
        Py_DECREF(pModule);
        return 1;
    }

    PyObject* pArgs = PyTuple_Pack(0);
    PyObject* pResult = PyObject_CallObject(pFunc, nullptr);
}
```


### 2. example.py
```python
def hello():
    print("have a nice day!")
```


### 编译
```shell
g++ -o main main.cxx -I"/path/to/python/include" -L"/path/to/python/libs" -lpython3.x
```