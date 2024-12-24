# C++ Design Pattern


## Reference
> - [C++常用设计模式](https://refactoringguru.cn/design-patterns)


## 1. Introduction


## 2. 创建型模式
### 2.1 工厂方法
1. 意图: 在父类中提供一个创建对象的方法, 允许子类决定实例化对象的类型
2. 方案: 使用特殊的工厂方法代替对象构造函数的直接调用
#### 2.1.1 模板
```c++
class Product {
    // 对接口进行声明
    // 对于由工厂方法创建的对象, 这些接口是通用的
};
class ProductA: public Product {};
class ProductB: public Product {};

class Factory {
public:
    // 工厂方法可以有一个默认的行为; 也可以是抽象的
    Product* create_product();
};
class FactoryA: public Factory {};
class FactoryB: public Factory {};
```


#### 2.1.2 示例
```c++
#include <iostream>
#include <stdexcept>

class Button
{
public:
    virtual void render()  = 0;
    virtual void onclick() = 0;
};

class WindowsButton: public Button
{
public:
    void render() override
    {
        std::cout << "rendering Windows button" << std::endl;
    }

    void onclick() override
    {
        std::cout << "clicking Windows button" << std::endl;
    }
};

class HtmlButton: public Button
{
public:
    void render() override
    {
        std::cout << "rendering HTML button" << std::endl;
    }

    void onclick() override
    {
        std::cout << "clicking HTML button" << std::endl;
    }
};

class Dialog
{
public:
    void render()
    {
        Button *button = create_button();
        button->onclick();
        button->render();
    };

    virtual Button *create_button() = 0;
};

class WindowsDialog: public Dialog
{
public:
    Button *create_button() override { return new WindowsButton(); }
};

class WebDialog: public Dialog
{
public:
    Button *create_button() override { return new HtmlButton(); }
};

class Application
{
public:
    // Application(): _dialog(nullptr) {};

    void run(std::string os)
    {
        if (os == "windows") {
            _dialog = new WindowsDialog();
        }
        else if (os == "web") {
            _dialog = new WebDialog();
        }
        else {
            throw std::runtime_error("Unsupported OS");
        }

        _dialog->render();
    }

private:
    Dialog *_dialog;
};

auto main() -> int
{
    Application *app = new Application();
    app->run("windows");
    app->run("web");
}
```


### 2.2 抽象工厂
1. 意图: 创建一系列相关对象, 而无需指定它们具体的类
2. 方案: 首先, 为系列中的每个产品明确声明接口, 确保所有产品变体都继承这些接口; 接着声明包含系列中所有产品创建方法的抽象工厂
#### 2.2.1 模板
```c++
// 产品A及其变体
class ProductA {};
class ProductA1: public ProductA {};
class ProductA2: public ProductA {};

// 产品B及其变体
class ProductB {};
class ProductB1: public ProductB {};
class ProductB2: public ProductB {};

class AbstractFactory {
public:
    // 抽象工厂声明创建每种产品的方法
    // 对于每一种变体产品的创建方法, 在具体的工厂方法中实现
    ProductA* create_product_a();
    ProductB* create_product_b();
};
class Factory1: public AbstractFactory {};
class Factory2: public AbstractFactory {};
```


#### 2.2.2 示例
```c++
#include <iostream>
#include <stdexcept>
#include <string>

class Button
{
public:
    virtual void info() = 0;
};

class WinButton: public Button
{
public:
    void info() override
    {
        std::cout << "this is a windows button" << std::endl;
    }
};

class MacButton: public Button
{
public:
    void info() override { std::cout << "this is a mac button" << std::endl; }
};

class Checkbox
{
public:
    virtual void info() = 0;
};

class WinCheckbox: public Checkbox
{
    void info() override
    {
        std::cout << "this is a windows checkbox" << std::endl;
    }
};

class MacCheckbox: public Checkbox
{
public:
    void info() override { std::cout << "this is a mac checkbox" << std::endl; }
};

class GuiFactory
{
public:
    virtual Button *create_button()     = 0;
    virtual Checkbox *create_checkbox() = 0;
};

class WinGuiFactory: public GuiFactory
{
public:
    Button *create_button() override { return new WinButton(); }

    Checkbox *create_checkbox() override { return new WinCheckbox(); }
};

class MacGuiFactory: public GuiFactory
{
public:
    Button *create_button() override { return new MacButton(); }

    Checkbox *create_checkbox() override { return new MacCheckbox(); }
};

class Application
{
public:
    void create_gui(std::string platform)
    {
        if (platform == "windows") {
            _factory = new WinGuiFactory();
        }
        else if (platform == "macos") {
            _factory = new MacGuiFactory();
        }
        else {
            throw std::runtime_error("Unsupported platform");
        }

        _button   = _factory->create_button();
        _checkbox = _factory->create_checkbox();

        _button->info();
        _checkbox->info();
    }

private:
    GuiFactory *_factory;
    Button *_button;
    Checkbox *_checkbox;
};

auto main() -> int
{
    Application *app = new Application();
    app->create_gui("windows");
    app->create_gui("macos");
}
```


### 2.3 生成器模式
1. 意图: 分步创建复杂对象, 允许使用相同的创建代码生成不同类型和形式的对象
2. 方案: 将对象构造代码抽象出来, 单独放在一个名为生成器的独立对象中
#### 2.3.1 模板
```c++
class Product
{
};

class ProductA: public Product
{
};

class ProductB: public Product
{
};

class Builder
{
public:
    // 所有类型生成器中通用的接口声明
    virtual void reset();
    virtual void build_part_1();
    virtual void build_part_2();
    virtual void build_part_3();
};

class BuilderA: public Builder
{
public:
    void reset() override;
    void build_part_1() override;
    void build_part_2() override;
    void build_part_3() override;
    ProductA *get_product() const;

private:
    ProductA *_product;
};

class BuilderB: public Builder
{
public:
    void reset() override;
    void build_part_1() override;
    void build_part_2() override;
    void build_part_3() override;
    ProductB *get_product() const;

private:
    ProductB *_product;
};

// 主管类, 定义调用构造步骤的顺序, 并负责与客户端交互
class Director
{
public:
    Director(Builder *builder);
    void change_builder(Builder *builder);
    Product *make();

private:
    Builder *_builder;
};
```


#### 2.3.2 示例
```c++
#include <iostream>
#include <string>

class Car
{
public:
    Car()
    {
        _seats         = 0;
        _engine        = "";
        _trip_computer = false;
        _gps           = false;
    }

    void set_seats(int seats) { _seats = seats; }

    void set_engine(std::string engine) { _engine = engine; }

    void set_trip_computer() { _trip_computer = true; }

    void set_gps() { _gps = true; }

    void info()
    {
        std::cout << std::boolalpha << "seats: " << _seats
                  << " | engine: " << _engine
                  << " | trip computer: " << _trip_computer
                  << " | gps: " << _gps << std::endl;
    }

private:
    int _seats;
    std::string _engine;
    bool _trip_computer;
    bool _gps;
};

class CarManual
{
public:
    CarManual() { _desc = ""; }

    void add_desc(std::string desc) { _desc += desc; }

    void reset_desc() { _desc.clear(); }

    void info() { std::cout << _desc << std::endl; }

private:
    std::string _desc;
};

class Builder
{
public:
    virtual void reset()                        = 0;
    virtual void set_seats(int seats)           = 0;
    virtual void set_engine(std::string engine) = 0;
    virtual void set_trip_computer()            = 0;
    virtual void set_gps()                      = 0;
};

// 汽车生成器
class CarBuilder: public Builder
{
public:
    CarBuilder()
    {
        _car = nullptr;
        this->reset();
    }

    ~CarBuilder()
    {
        delete _car;
        _car = nullptr;
    }

    void reset() override
    {
        if (_car != nullptr) {
            delete _car;
        }
        _car = new Car();
    }

    void set_seats(int seats) override { _car->set_seats(seats); }

    void set_engine(std::string engine) override { _car->set_engine(engine); }

    void set_trip_computer() override { _car->set_trip_computer(); }

    void set_gps() override { _car->set_gps(); }

    Car *get_product() { return _car; }

private:
    Car *_car;
};

// 汽车配套使用手册生成器
class CarManualBuilder: public Builder
{
public:
    CarManualBuilder()
    {
        _manual = nullptr;
        this->reset();
    }

    ~CarManualBuilder()
    {
        delete _manual;
        _manual = nullptr;
    }

    void reset() override
    {
        if (_manual != nullptr) {
            delete _manual;
        }
        _manual = new CarManual();
    }

    void set_seats(int seats) override
    {
        _manual->add_desc("number of seats: " + std::to_string(seats) + "\n");
    }

    void set_engine(std::string engine) override
    {
        _manual->add_desc("engine: " + engine + "\n");
    }

    void set_trip_computer() override
    {
        _manual->add_desc("trip computer: yes\n");
    }

    void set_gps() override { _manual->add_desc("gps: yes\n"); }

    CarManual *get_product() { return _manual; }

private:
    CarManual *_manual;
};

class Director
{
public:
    static void construct_sports_car(Builder *builder)
    {
        builder->reset();
        builder->set_seats(2);
        builder->set_engine("V8");
        builder->set_trip_computer();
        builder->set_gps();
    }

    static void consttruct_suv(Builder *builder)
    {
        builder->reset();
        builder->set_seats(4);
        builder->set_engine("V6");
        builder->set_trip_computer();
    }
};

// 客户端代码
class Application
{
public:
    static void run()
    {
        CarBuilder *car_builder          = new CarBuilder();
        CarManualBuilder *manual_builder = new CarManualBuilder();

        // sports car
        // 相同的创建代码生成了不同的对象
        Director::construct_sports_car(car_builder);
        Director::construct_sports_car(manual_builder);
        car_builder->get_product()->info();
        manual_builder->get_product()->info();

        // suv
        Director::consttruct_suv(car_builder);
        Director::consttruct_suv(manual_builder);
        car_builder->get_product()->info();
        manual_builder->get_product()->info();
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


### 2.4 原型模式
1. 意图: 复制已有对象, 同时让代码不依赖于对象实际类型
2. 方案: 将复制过程委派给被复制的实际对象, 为所有支持复制的对象声明一个接口, 从而将对象与其所属的类解耦; (支持克隆的对象即为原型)
#### 2.4.1 模板


#### 2.4.2 示例
```c++
#include <array>
#include <iostream>
#include <string>

class Shape
{
public:
    Shape(float x, float y, const std::string color): x(x), y(y), color(color)
    {
    }

    Shape(const Shape &src)
    {
        this->x     = src.x;
        this->y     = src.y;
        this->color = src.color;
    }

    virtual ~Shape() {}

    virtual Shape *clone() const = 0;

    virtual void info() const { std::cout << "x: " << x << " | y: " << y; }

private:
    float x;
    float y;
    std::string color;
};

class Rectangle: public Shape
{
public:
    Rectangle(
        float width, float height, float x, float y, const std::string color):
        width(width),
        height(height),
        Shape(x, y, color)
    {
    }

    Rectangle(const Rectangle &src): Shape(src)
    {
        this->width  = src.width;
        this->height = src.height;
    }

    // TODO: 返回指针可能会出现潜在的问题; 但此处只是为了说明原型模式, 故不作深究
    Shape *clone() const override { return new Rectangle(*this); }

    void info() const override
    {
        Shape::info();
        std::cout << " | width: " << width << " | height: " << height
                  << (void *)this << std::endl;
    }

private:
    float width;
    float height;
};

class Circle: public Shape
{
public:
    Circle(float radius, float x, float y, const std::string color):
        radius(radius),
        Shape(x, y, color)
    {
    }

    Circle(const Circle &src): Shape(src) { this->radius = src.radius; }

    Shape *clone() const override { return new Circle(*this); }

    void info() const override
    {
        Shape::info();
        std::cout << " | radius: " << radius << (void *)this << std::endl;
    }

private:
    float radius;
};

class Application
{
public:
    static void run()
    {
        std::array<Shape *, 10> shapes;
        Rectangle *rect = new Rectangle(10, 20, 100, 200, "red");
        Circle *circle  = new Circle(5, 300, 400, "blue");

        for (int i = 0; i < shapes.size(); i++) {
            if (i % 2 == 0) {
                shapes[i] = rect->clone();
            }
            else {
                shapes[i] = circle->clone();
            }
        }

        for (auto shape: shapes) {
            shape->info();
            delete shape;
        }

        delete rect;
        delete circle;
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


### 2.5 单例模式
1. 意图: 保证一个类只有一个实例, 并提供一个访问该实例的全局节点
2. 方案:
    2.1 将默认构造函数设为私有, 防止其他对象使用单例类的new运算符
    2.2 新建一个静态方法作为构造函数, 调用私有的构造函数来创建对象, 并将保存在一个静态成员变量中, 此后所有对该函数的调用都返回该缓存对象
#### 2.5.1 模板
```c++
class Singleton
{
public:
    static Singleton *get_instance()
    {
        if (instance == nullptr) {
            instance = new Singleton();
        }

        return instance;
    }

private:
    Singleton() {}

    static Singleton *instance;
};

// 初始化静态成员
Singleton *Singleton::instance = nullptr;
```


#### 2.5.2 示例
```c++
#include <iostream>

class Database
{
public:
    static Database *getInstance()
    {
        if (instance == nullptr) {
            instance = new Database();
        }
        return instance;
    }

private:
    static Database *instance;

    Database() {}
};

// 初始化静态变量
Database *Database::instance = nullptr;

class Application
{
public:
    static void run()
    {
        Database *db1 = Database::getInstance();
        Database *db2 = Database::getInstance();
        if (db1 == db2) {
            std::cout << "db1 and db2 are the same instance" << std::endl;
        }
        else {
            std::cout << "db1 and db2 are different instances" << std::endl;
        }
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


## 3. 结构型模式
### 3.1 适配器模式
1. 意图: 使接口不兼容的对象能够相互合作
2. 方案: 创建一个适配器(一个特殊的对象), 通过封装对象, 将复杂的转换过程隐藏
#### 3.1.1 模板


#### 3.1.2 示例
```c++
#include <cmath>
#include <iostream>

// 通过一个经典的问题(方钉是否能放进圆孔内)来演示适配器模式

class SquarePeg
{
public:
    SquarePeg(float _width): width(_width) {}

    float get_width() const { return width; }

private:
    float width;
};

// 构造一个圆钉类
class RoundPeg
{
public:
    virtual float get_radius() const = 0;
};

class RoundHole
{
public:
    RoundHole(float _radius): radius(_radius) {}

    float get_radius() const { return radius; }

    bool fits(const RoundPeg &peg) const
    {
        return this->get_radius() >= peg.get_radius();
    }

private:
    float radius;
};

class SquarePegAdapter: public RoundPeg
{
public:
    SquarePegAdapter(const SquarePeg &_peg): peg(_peg) {}

    // 通过get_radius方法将SquarePeg适配成RoundPeg
    float get_radius() const override
    {
        return peg.get_width() * std::sqrt(2) / 2.0;
    }

private:
    SquarePeg peg;
};

class Application
{
public:
    static void run()
    {
        RoundHole round_hole(2.0);

        SquarePeg small_peg(2.0);
        SquarePeg large_peg(3.0);

        bool fits_small = round_hole.fits(SquarePegAdapter(small_peg));
        bool fits_large = round_hole.fits(SquarePegAdapter(large_peg));
        std::cout << "round hole can" << (fits_small ? " " : " not ")
                  << "fit small peg." << std::endl;
        std::cout << "round hole can" << (fits_large ? " " : " not ")
                  << "fit large peg." << std::endl;
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


### 3.2 桥接模式
1. 意图: 将一个大类拆分成抽象和实现两个独立的层次结构
2. 方案: 将继承改为组合, 抽取其中一个维度使之成为独立的类层次, 这样就可以在初始类中引入这个新的层次对象, 从而使一个类不必拥有所有的状态和行为
#### 3.2.1 模板


#### 3.2.2 示例
```c++
#include <iostream>

// Device类是实现部分的公共接口
class Device
{
public:
    virtual bool is_enabled() const = 0;
    virtual void enable()           = 0;
    virtual void disable()          = 0;

    virtual int get_volume() const      = 0;
    virtual void set_volume(int volume) = 0;

    virtual int get_channel() const       = 0;
    virtual void set_channel(int channel) = 0;

    virtual void info() const = 0;
};

class TV: public Device
{
public:
    TV(bool is_enabled, int volume, int channel):
        is_enabled_(is_enabled),
        volume_(volume),
        channel_(channel)
    {
    }

    bool is_enabled() const override { return is_enabled_; }

    void enable() override { is_enabled_ = true; }

    void disable() override { is_enabled_ = false; }

    int get_volume() const override { return volume_; }

    void set_volume(int volume) override { volume_ = volume; }

    int get_channel() const override { return channel_; }

    void set_channel(int channel) override { channel_ = channel; }

    void info() const override
    {
        std::cout << "TV: " << (is_enabled_ ? "enabled" : "disabled")
                  << ", volume: " << volume_ << ", channel: " << channel_
                  << std::endl;
    }

private:
    bool is_enabled_;
    int volume_;
    int channel_;
};

class Radio: public Device
{
};

// Remote类作为抽象部分, 同客户端代码交互
class Remote
{
public:
    Remote(Device &device): device(device) {}

    void toggle_power()
    {
        if (this->device.is_enabled()) {
            this->device.disable();
        }
        else {
            this->device.enable();
        }
    }

    void volume_up() { this->device.set_volume(this->device.get_volume() + 1); }

    void volume_down()
    {
        this->device.set_volume(this->device.get_volume() - 1);
    }

    void channel_up()
    {
        this->device.set_channel(this->device.get_channel() + 1);
    }

    void channel_down()
    {
        this->device.set_channel(this->device.get_channel() - 1);
    }

    void show_info() const { this->device.info(); }

protected:
    Device &device;
};

// 扩展Remote类, 增加新的功能
class AdvancedRemote: public Remote
{
public:
    void mute() { this->device.set_volume(0); }
};

class Application
{
public:
    static void run()
    {
        TV tv(false, 50, 1);
        Remote remote(tv);

        remote.show_info();
        remote.toggle_power();
        remote.channel_up();
        remote.volume_up();
        remote.show_info();
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


### 3.3 组合模式
1. 意图: 将对象组合成树形结构, 并且可以如同使用独立对象一样使用它们
2. 方案: 使用一个通用的接口来在对象之间交互
#### 3.3.1 模板
```c++
#include <vector>

// 组件接口描述了树中简单项目和复合项目共同的操作
class Component
{
public:
    Component()          = default;
    virtual ~Component() = default;

    virtual void execute() = 0;
};

// 叶子节点是树的基本结构, 不包含子项目, 会完成大部分的实际工作
class Leaf: public Component
{
public:
    Leaf()  = default;
    ~Leaf() = default;

    void execute() override;
};

// 组合(又称容器), 包含叶子节点及其他组合等子项目
// 组合收到请求之后, 会把具体工作委派给其子项目, 然后对中间结果做一些必要的处理, 最后返回给客户端
class Composite: public Component
{
public:
    typedef std::vector<Component *> Children;

    Composite()  = default;
    ~Composite() = default;

    void add(Component *child);
    void remove(Component *child);
    Children get_children() const;

    void execute() override;

private:
    Children children_;
};
```


#### 3.3.2 示例
```c++
#include <algorithm>
#include <iostream>
#include <vector>

class Graphic
{
public:
    virtual void draw()               = 0;
    virtual void move(int dx, int dy) = 0;
};

class Dot: public Graphic
{
public:
    Dot(int x, int y): x_(x), y_(y) {}

    ~Dot() = default;

    void draw() override
    {
        std::cout << "drawing a dot at (" << x_ << ", " << y_ << ")"
                  << std::endl;
    }

    void move(int dx, int dy) override
    {
        x_ += dx;
        y_ += dy;
        std::cout << "moving a dot to (" << x_ << ", " << y_ << ")"
                  << std::endl;
    }

protected:
    int x_;
    int y_;
};

class Circle: public Dot
{
public:
    Circle(int x, int y, int radius): Dot(x, y), radius_(radius) {}

    ~Circle() = default;

    void draw() override
    {
        std::cout << "drawing a circle at (" << x_ << ", " << y_
                  << ") with radius " << radius_ << std::endl;
    }

    void move(int dx, int dy) override
    {
        x_ += dx;
        y_ += dy;
        std::cout << "moving a circle to (" << x_ << ", " << y_
                  << ") with radius " << radius_ << std::endl;
    }

protected:
    int radius_;
};

class CompoundGraphic: public Graphic
{
public:
    typedef std::vector<Graphic *> Graphics;

    CompoundGraphic() { this->graphics_ = Graphics(); }

    ~CompoundGraphic() = default;

    void add(Graphic *graphic) { graphics_.push_back(graphic); }

    void remove(Graphic *graphic)
    {
        graphics_.erase(std::find(graphics_.begin(), graphics_.end(), graphic));
    }

    void draw() override
    {
        std::cout << "drawing a compound graphic" << std::endl;
        for (auto graphic: graphics_) { graphic->draw(); }
    }

    void move(int dx, int dy) override
    {
        std::cout << "moving a compound graphic" << std::endl;
        for (auto graphic: graphics_) { graphic->move(dx, dy); }
    }

private:
    Graphics graphics_;
};

class Application
{
public:
    void run()
    {
        // load graphics
        graphics_ = CompoundGraphic();
        graphics_.add(new Dot(1, 2));
        graphics_.add(new Circle(5, 3, 10));

        // draw
        graphics_.draw();
        std::cout << std::endl;

        // move
        graphics_.move(10, 20);
        std::cout << std::endl;
    }

private:
    CompoundGraphic graphics_;
};

auto main() -> int
{
    Application app;
    app.run();
    return 0;
}
```


### 3.4 装饰模式
1. 意图: 将对象放入包含行为的特殊封装对象, 为原对象绑定新的行为
2. 方案: 通过组合实现
#### 3.4.1 模板
```c++
// 声明封装器和被封装对象的公共接口
class Component
{
public:
    virtual void execute() = 0;
};

// 被封装对象所属的类, 定义了基础行为, 但是封装器可以改变这些行为
class ConcreteComponent: public Component
{
public:
    void execute() override;
};

// 基础装饰类
// 拥有一个指向被封装对象的引用成员变量
// 装饰器会将所有具体的操作委托给它
class Decorator: public Component
{
public:
    Decorator(Component *component);
    void execute() override;

protected:
    Component *component_;
};

// 具体装饰器类
// 定义了动态的添加到被装饰对象的额外行为
// 会重写装饰基类的方法, 并在调用父类方法之前或之后添加额外的行为
class ConcreteDecorator: public Decorator
{
public:
    ConcreteDecorator(Component *component);
    void execute() override;
};
```


#### 3.4.2 示例
```c++
#include <iostream>
#include <string>

class DataSource
{
public:
    DataSource()          = default;
    virtual ~DataSource() = default;

    virtual void write_data(int size) = 0;
    virtual void read_data(int size)  = 0;
};

class FileDataSource: public DataSource
{
public:
    FileDataSource(): filename_("data.txt") {}

    void write_data(int size) override { std::cout << "write data to file" << std::endl; }

    void read_data(int size) override { std::cout << "read data from file" << std::endl; }

private:
    std::string filename_;
};

class NetworkDataSource: public DataSource
{
public:
    NetworkDataSource(): hostname_("127.0.0.1"), port_(80) {}

    void write_data(int size) override { std::cout << "write data to network" << std::endl; }

    void read_data(int size) override { std::cout << "read data from network" << std::endl; }

private:
    std::string hostname_;
    int port_;
};

// 装饰基类
class DataSourceDecorator: public DataSource
{
public:
    DataSourceDecorator(DataSource *datasource): datasource_(datasource) {}

    void write_data(int size) override { datasource_->write_data(size); }

    void read_data(int size) override { datasource_->read_data(size); }

private:
    DataSource *datasource_;
};

// 具体装饰类: 加密
class DataSourceEncryptionDecorator: public DataSourceDecorator
{
public:
    DataSourceEncryptionDecorator(DataSource *datasource): DataSourceDecorator(datasource) {}

    void write_data(int size) override
    {
        // 数据加密
        std::cout << "encrypt data" << std::endl;

        DataSourceDecorator::write_data(size);
    }

    void read_data(int size) override
    {
        DataSourceDecorator::read_data(size);

        // 数据解密
        std::cout << "decrypt data" << std::endl;
    }
};

// 具体装饰类: 压缩
class DataSourceCompressionDecorator: public DataSourceDecorator
{
public:
    DataSourceCompressionDecorator(DataSource *datasource): DataSourceDecorator(datasource) {}

    void write_data(int size) override
    {
        // 数据压缩
        std::cout << "compress data" << std::endl;

        DataSourceDecorator::write_data(size);
    }

    void read_data(int size) override
    {
        DataSourceDecorator::read_data(size);

        // 数据解压
        std::cout << "decompress data" << std::endl;
    }
};

class Application
{
public:
    static void run()
    {
        DataSource *datasource = new FileDataSource();

        datasource = new DataSourceCompressionDecorator(datasource);
        datasource = new DataSourceEncryptionDecorator(datasource);

        datasource->write_data(1024);
        std::cout << std::endl;
        datasource->read_data(1024);

        delete datasource;
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


### 3.5 外观模式
1. 意图: 为程序库, 框架, 或其它复杂类提供一个简单的接口
2. 方案: 创建一个外观类, 整合类库, 框架, 或其他它复杂类常用的接口, 从而避免业务代码与三方库的紧密耦合
#### 3.5.1 模板
#### 3.5.2 示例


### 3.6 享元模式
1. 意图: 通过共享多个对象所共有的相同状态, 减少内存占用
2. 方案: 通过一个仅存储内在状态的对象(享元), 来共享多个对象所共有的相同状态
#### 3.6.1 模板
#### 3.6.2 示例
```c++
#include <iostream>
#include <map>
#include <string>

// 享元类包含原始对象中部分能在多个对象中共享的状态
class TreeCommon
{
public:
    TreeCommon(const std::string name, const std::string color, const std::string texture):
        name_(name),
        color_(color),
        texture_(texture)
    {
    }

    void draw(int x, int y)
    {
        std::cout << "drawing tree at (" << x << ", " << y << ") with name: " << name_ << std::endl;
    }

private:
    std::string name_;
    std::string color_;
    std::string texture_;
};

// 享元工厂会对已有享元的缓存池进行管理
class TreeCommonFactory
{
public:
    static TreeCommon *get_treecommon(const std::string name, const std::string color, const std::string texture)
    {
        static std::map<TreeCommonParams, TreeCommon *> trees;

        TreeCommonParams params(name, color, texture);
        if (trees.find(params) == trees.end()) {
            std::cout << "create new tree with name: " << name << std::endl;
            trees[params] = new TreeCommon(name, color, texture);
        }
        return trees[params];
    }

private:
    typedef std::tuple<std::string, std::string, std::string> TreeCommonParams;
};

// Context
// 情景类包含原始对象中各不相同的外在状态
// 情景对象与享元组合在一起就表示原始对象的全部状态
class Tree
{
public:
    Tree(int x, int y, std::string name, std::string color, std::string texture):
        x_(x),
        y_(y),
        common_(TreeCommonFactory::get_treecommon(name, color, texture))
    {
    }

    void draw() { common_->draw(x_, y_); }

private:
    int x_;
    int y_;
    TreeCommon *common_;
};

class Forest
{
};

class Application
{
public:
    static void run()
    {
        Tree t1(10, 20, "Oak", "Brown", "Smooth");
        Tree t2(30, 40, "Oak", "Brown", "Smooth");
        Tree t3(50, 60, "Maple", "Green", "Fir");

        t1.draw();
        t2.draw();
        t3.draw();
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


### 3.7 代理模式
1. 意图: 提供对象的替代品或占位符, 代理控制着对于原对象的访问, 并且可以在将请求提交给对象前后做一些处理
2. 方案: 新建一个与原对象接口相同的代理类, 将对原对象的请求委托给代理
#### 3.7.1 模板
```c++
class Service
{
public:
    virtual void execute() = 0;
};

class ServiceImpl: public Service
{
public:
    void execute() override;
};

class ServiceProxy: public Service
{
public:
    ServiceProxy(Service *service): service_(service) {}

    void execute() override;

    // 一些额外的业务逻辑
    bool check_access() const;
    void log() const;
    void delay_init();

private:
    Service *service_;
};
```


#### 3.7.2 示例
```c++
#include <array>
#include <format>
#include <iostream>
#include <map>
#include <string>

// 接口类
class ThirdPartyTV
{
public:
    virtual void list_videos() const           = 0;
    virtual void get_video_info(int id) const  = 0;
    virtual std::string download_video(int id) = 0;
};

class ThirdPartyTVImpl: public ThirdPartyTV
{
public:
    void list_videos() const override { std::cout << "listing videos: ..." << std::endl; }

    void get_video_info(int id) const override { std::cout << "info of video(" << id << "): ..." << std::endl; }

    std::string download_video(int id) override { return std::format("download details of video({})", id); }
};

class CachedTVImpl: public ThirdPartyTV
{
public:
    CachedTVImpl(ThirdPartyTV *tv): tv_(tv), count_(), caches_() {}

    void list_videos() const override { tv_->list_videos(); }

    void get_video_info(int id) const override { tv_->list_videos(); }

    // 假设原始的ThirdPartyTVImpl类提供的download_video方法效率非常低
    // 如果用户反复下载同一个视频, 通过代理提供缓存
    std::string download_video(int id) override
    {
        if (count_.find(id) == count_.end()) {
            count_[id] = 1;
        }
        else {
            count_[id]++;
        }

        if (count_[id] >= cache_threshod_) {
            if (caches_.find(id) == caches_.end()) {
                caches_[id] = tv_->download_video(id);
            }

            std::cout << "from cache for video(" << id << ") " << std::endl;
            return caches_[id];
        }
        else {
            return tv_->download_video(id);
        }
    }

private:
    ThirdPartyTV *tv_;

    // 视频缓存相关信息
    const int cache_threshod_ = 3;
    std::map<int, int> count_;
    std::map<int, std::string> caches_;
};

class Application
{
public:
    static void run()
    {
        int ids[] = {
            1,
            2,
            3,
            4,
            5,
            4,
            4,
            2,
            2,
            2,
            1,
            1,
        };

        CachedTVImpl tv(new ThirdPartyTVImpl());
        tv.list_videos();
        tv.get_video_info(1);

        for (int id: ids) { tv.download_video(id); }
    }
};

auto main() -> int
{
    Application::run();
    return 0;
}
```


## 4. 行为模式
### 4.1 责任链模式
1. 意图: 将请求沿着处理者链传递
2. 方案: 
#### 4.1.1 模板
#### 4.1.2 示例
```c++
```