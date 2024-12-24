# mysql


## 参考
> - [官方文档](https://dev.mysql.com/doc/refman/8.4/en/)
> - [中文文档](https://mysql.net.cn/)
> - [下载](https://dev.mysql.com/downloads/)


## 安装
### zip安装
### zip安装
```shell
# 演示版本: 8.4.2


# 1. 下载并加压


# 2. 配置环境变量: 将bin目录添加到PATH环境变量中


# 3. 安装msvc运行库
# https://learn.microsoft.com/zh-cn/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version


# 4. 执行配置程序, 根据提示操作即可完成安装
mysql_configurator


# 5. 连接
mysql -u root -p
```


## 概念
1. 数据库
2. 表
3. 数据类型
4. 主键


## sql语言的组成
1. DDL: 数据定义语句; drop, create, alter,...
2. DML: 数据操作语句; insert, delete, update,...
3. DQL: 数据查询语句; select
4. DCL: 数据控制语句; grant, revoke, commit, rollback,...


## 数据库访问接口
1. odbc
2. jdbc
3. ado
4. pdo


## 数据库的基本操作
```sql
-- 显示当前目录下的所有数据库
show databases;

-- 创建数据库
create database <db_name>;

-- 查看建库语句
show create database <db_name>;

-- 删除数据库
drop database <db_name>;
```


## 数据库表的基本操作
```sql
-- 操作表之前, 应该切换到相应的数据库, 否则就要使用前置限定
use <db_name>;

-- 创建数据表
create table <tb_name> (
  `field_name` type [constraint] [default_value] [comment],
  ...,
  [constraint]
);

-- 显示当前数据库中的所有表
show tables;


-- 指定主键  =>  不允许为空
-- 1. 在定义字段的同时指定: "PRIMARY KEY"
-- 2. 在定义完所有字段后指定: "[constraint <主键名>] PRIMARY KEY (<filed_name>,...)"  =>  该方式可以指定复合主键

-- 指定外键  =>  允许为空, 但如果非空, 就必须是某个表的主键
-- 在定义完所有字段后指定: [constraint 外键名] FOREIGN KEY (<filed_name>,...) REFERENCES <tb_name> (<filed_name>,...)

-- 指定非空约束
-- 在定义字段的同时指定: NOT NULL

-- 指定唯一/独立约束  =>  允许为空, 但只能有一个为空
-- 1. 在定义字段的同时指定: UNIQUE
-- 2. 在定义完所有字段后指定: [constraint <约束名>] UNIQUE (<field_name>)

-- 指定默认约束
-- 在定义字段的同时指定: DEFAULT <value>

-- 指定自增
-- 在定义字段的同时指定: AUTO_INCREMENT
-- (默认)初始值为1, 自动增加1
-- 一张表只能有一个, 并且该字段必须是主键的一部分
-- 可以作用于任何证书类型


-- 查看表的基本结构
describe <tb_name>;
desc <tb_name>;

-- 查看建表语句
show create table <tb_name>;


-- 修改表的结构
-- 1. 修改表名
alter table <tb_name> rename [to] <new_tb_name>;

-- 2. 修改字段的数据类型
-- 不同数据类型的存储方式不一样, 所以当表中有数据时不要轻易修改数据类型
alter table <tb_name> modify <field_name> <data_type>;

-- 3. 修改字段名
-- 必须指定数据类型, 如果不需要改变, 设为原来一样即可
alter table <tb_name> change <field_name> <new_field_name> <data_type>;

-- 4. 添加字段
alter table <tb_name> add <field_name> <data_type> [constraint] [first | after <some_exist_field_name>];

-- 5. 删除字段
alter table <tb_name> drop <field_name>;

-- 6. 修改字段的排列位置
alter table <tb_name> modify <field_name_1> <data_type> first | after <field_name_2>;

-- 7. 更改表的存储引擎
-- 可以使用`show engines;`查看系统支持的引擎: MyISAM | InnoDB | MEMORY | BDB | FEDERATED...
alter table <tb_name> engine=<new_engine_name>;

-- 8. 删除表的外键约束
alter table <tb_name> drop foreign key <constraint_name>;


-- 删除数据表
-- 1. 删除没有被关联的表
drop table [if exists] <tb_name1>, <tb_name2>...;

-- 2. 删除被其它表关联的表
-- 2.1 想保留子表: 先解除子表的外键约束, 再删除父表即可
-- 2.2 不想保留子表
drop table <tb_name>,... casecade;
```


## 数据类型
1. 数值类型: tinyint, smallint, mediumint, int, bigint; float, double, decimal
2. 日期/时间类型: year, date, time, datetime, timestamp
3. 字符串类型: char, varchar, bit, binary, varbinary, blob(tiny, ., medium, long), text(tiny, ., medium, long), enum, set


## 运算符
1. 算数运算符: `=, -, *, /, %`
2. 比较运算符: `>, <, =, >=, <=, <=>, !=(<>)`, in, not in, between...and, is null, isnull, is not null, greatest, least, like, regexp
3. 逻辑运算符: not(!), and(&&), or(||), xor
4. 位运算符: &, |, ~, ^, <<, >>

mysql中的比较比区分大小写, 如果确实有需要, 可以加上binary关键字, 例如: `binary 'a' = 'A'`


## 函数
1. 数学函数
   1. abs(x)
   2. pi()
   3. sqrt(x)
   4. mod(x, y)
   5. ceil(x) | ceiling(x)
   6. floor(x)
   7. round(x) | round(x, y)
   8. truncate(x, y)
   9. rand(seed)
   10. sign(x)
   11. pow(x, y) | power(x, y)
   12. exp(x)  <!-- e的x次方 -->
   13. log(x) | log10(x)
   14. radians(x)  <!-- 角度值转换为弧度值 -->
   15. degrees(x)  <!-- 弧度值转换为角度值 -->
   16. sin(x)
   17. asin(x)
   18. cos(x)
   19. acos(x)
   20. tan(x)
   21. atan(x)
   22. cot(x)
2. 字符串函数
    1.  char_length(s)  <!-- 字符串中的字符个数 -->
    2.  length(s)  <!-- 字符串的字节长度 -->
    3.  concat(s1, s2, ...)  <!-- 拼接字符串 -->
    4.  concat_ws(sep, s1, s2, ...)  <!-- 第一个参数是分隔符 -->
    5.  insert(s1, pos, len, s2)  <!-- s1从pos位置开始的len个字符被s2替换, 并返回s1 -->
    6.  lower(s) | lcase(s)
    7.  upper(s) | ucase(s)
    8.  left(s, n)  <!-- 返回字符串s左边的n个字符 -->
    9.  right(s, n)
    10. lpad(s1, len, s2)  <!-- 字符串s1左边用s2填充至长度len, 如果s1原来的长度大于len, 则截断 -->
    11. rpad(s1, len, s2)
    12. ltrim(s)  <!-- 删除字符串s左侧的空格 -->
    13. rtrim(s)
    14. trim(s)
    15. trim(s1 from s)  <!-- 删除字符串s两侧的所有字符s1 -->
    16. repeat(s, n)  <!-- 返回重复n次s的字符串 -->
    17. space(n)  <!-- 返回由n个空格组成的字符串 -->
    18. replace(s, s1, s2)  <!-- 使用字符串s2替换s中的s1 -->
    19. strcmp(s1, s2)  <!-- 若s1<s2则返回-1, 若s1=s2则返回0, 若s1>s2则返回1 -->
    20. substring(s, pos, len) | mid(s, pos, len)  <!-- 返回字符串s从pos位置开始的len个字符组成的子串 -->
    21. locate(s1, s) | position(s1 in s) | instr(s, s1)  <!-- 返回s1在s中的起始位置 -->
    22. reverse(s)  <!-- 反转字符串s -->
    23. elt(k, s1, s2, s3, ..., sn)  <!-- 返回sk -->
    24. field(s, s1, s2, s3, ..., sn)  <!-- 返回字符串s在列表s1, s2, s3, ... 中自一次出现的位置 -->
    25. filed_in_set(s, s1)  <!-- 返回字符串s在字符串列表s1中首次出现的位置; 其中s1是多个由逗号分开的字符串组成 -->
    26. make_set(x, s1, s2, s3,...)  <!-- 按照x二进制位的1/0取字符串形成set -->
3. 日期和时间
   1. curdate() | current_date()  <!-- date -->
   2. current_timestamp() | localtime() | now() | sysdate()  <!-- datetime -->
   3. unix_timestamp(date=now())  <!-- 返回unix时间戳 -->
   4. utc_date()
   5. utc_time()
   6. month(date)
   7. monthname(date)
   8. dayname(date)
   9.  weekday(date)  <!-- 工作日索引: 0表示周一 -->
   10. week(date) | weekofyear(date)
   11. dayofyear(date) | dayofmonth(date) | dayofweek(date)
   12. year(date)
   13. quarter(date)  <!-- 第几季度 -->
   14. hour(time) | minite(time) | second(time)
   15. extract(type from date)  <!-- 从日期中截取指定值 -->
   16. time_to_sec(time) | sec_to_time(secs)
   17. date_add() | adddate()
   18. date_sub() | subdate()
   19. addtime()
   20. subtime()
   21. datediff()
   22. date_format(date, fmt)
   23. time_format(time, fmt)
   24. get_format(value, type)  <!-- 获取日期/时间的表示格式 -->
4. 条件判断函数
   1. if(expr, x1, x2)  <!-- 如果expr为true则返回x1, 否则返回x2 -->
   2. ifnull(x1, x2)  <!-- 如果x1不为null则返回x1, 否则返回x2 -->
   3. case expr when x1 then y1 [when x2 then y2]... else yk end  <!-- switch...case结构 -->
5. 系统信息函数
   1. version()
   2. connection_id()  <!-- 查看当前用户的连接数 -->
   3. show [full] processlist  <!-- 查看当前用户的连接信息 -->
   4. user() | current_user() | system_user() | session_user()
   5. charset(s)  <!-- 返回字符串s的字符集 -->
   6. collation(s)  <!-- 返回字符串s的字符排序方式 -->
   7. last_insert_id()  <!-- 返回最后一个auto_increment值 -->
6. 加密函数
   1. md5(s)
   2. sha(s)
   3. sha2(s, length)  <!-- 其中length的取值是特定的 -->
7. 其它函数
   1. format(x, n)  <!-- 将数字x格式化, 保留小数点后n位 -->
   2. conv(n, from_base, to_base)  <!-- 进制转换 -->
   3. inet_aton(s) | inet_nota(int)  <!-- 网址字符串与整数互相转换 -->
   4. get_lock(s, timeout) | release_lock(s) | is_free_lock(s) | is_used_lock(s)
   5. benchmark(count, expr)  <!-- 重复执行expr表达式count次 -->
   6. convert(... using ...)  <!-- 字符集转换 -->
   7. cast(x, as type)  <!-- 转换数据类型: type的取值有binary, char(n), datetime, decimal, signed, unsigned -->


## 查询语句
```sql
-- 查询语句基本结构
select * from ... where ... group by ... having ... order by ... limit ...


-- 单表查询
-- 1. 查询所有字段
select * from <tb_name>;

-- 2. 查询指定字段
select <field_name>,... from <tb_name>;

-- 3. 查定指定记录
-- 3.1 比较运算符
-- 3.2 in运算符: where x [not] in (a, b, c,...)
-- 3.3 between...and: where x between 2.1 and 3.2   =>  包含两边的边界值
-- 3.4 like: %匹配任意(包含0)长度的字符; _匹配任意一个字符
-- 3.5 is null: where x is [not] null
-- 3.6 多条件查询: and or

-- 4. 去除重复的字段
select distinct <field_name> from ...

-- 5. 对结果排序
-- 5.1 单列排序
select ... from ... order by <field_name>
-- 5.2 多列排序
select ... from ... order by <field_name1>, <field_name2>,...
-- 5.3 指定排序方向
select ... from ... order by <field_name> [asc | desc]

-- 6. 分组查询
-- group by通常和集合函数一起使用: max(), min(), count(), sum(), avg() 
-- group by配合集合函数使用时, 先分组, 然后再对每组记录进行统计
select ... from ... group by <field_name>
-- 6.1 显示每个组的个数
select id, count(*) as total from ... group by id
-- 6.2 显示每个组某一字段的全部结果
select id, group_concat(<field_ name>) as xxx from ... group by id
-- 6.3 对接过进行过滤
-- where与having的区别: having是在数据分组之后进行过滤来选择分组; where是在分组之前过滤来选择记录
select ... from ... group by ... having expr
-- 6.4 汇总: 在结果的最后添加一行统计记录的数量
select ... from ... group by ... with rollup
-- 6.5 多字段分组: 先根据第1个字段分组, 然后在第1个字段相同的记录中根据第2个字段分组
select ... from ... group by <field_name1>, <field_name2>...
-- 6.6 与order by一起使用: 需要注意的是order by不能和with rollup一起使用
select ... from ... group by ... order by ...

-- 7. 限制查询的数量
-- offset: 从第几条记录开始, 默认为0, 表示从第1条记录开始
-- lines: 表示要显示的总行数
select ... from ... limit [<offset>,] <lines>
select ... from ... limit <offset> offset <lines>
```


## 集合函数
1. count
   1. count(*): 计算表中总的行数, 不管是否有数值还是为空
   2. count(<field_name>): 计算指定列下总的行数, 忽略空值的行
2. sum: 计算指定列的总和, 并且忽略null值
3. avg: 计算指定列的平均数
4. max: 计算。指定列的最大值; 适用于数值类型和字符串类型
5. min


## 连接查询
```sql
-- 内连接: 返回查询结果中仅符合连接条件的行
-- 下面两个查询语句得到的结果是一样的; 区别是使用inner join语法更加规范, 并且不容易忘记连接条件, 同时使用where子句在某些情况下会影响性能
SELECT f.s_id, f.f_name, f.f_price, s.s_name FROM fruits f, suppliers s  WHERE f.s_id = s.s_id;
SELECT f.s_id, f.f_name, f.f_price, s.s_name FROM fruits f INNER JOIN suppliers s ON f.s_id = s.s_id;

-- 如果在一个连接查询中涉及到的两张表都是同一张表, 这种情况下被称为自连接查询
SELECT f1.f_id, f1.f_name FROM fruits f1 INNER JOIN fruits f2 ON f1.s_id = f2.s_id AND f2.f_id = 'a1';


-- 外连接: 返回查询结果中不仅包含符合连接条件的行, 还包含左表/右表/两张表
-- 查询所有(包括没有订单的)客户
SELECT c.c_id, o.o_num FROM customers c LEFT JOIN orders o ON c.c_id = o.c_id;
-- 查询所有(包括没有客户的)订单
SELECT c.c_id, o.o_num FROM customers c RIGHT JOIN orders o ON c.c_id = o.c_id;
```


## 子查询
```sql
-- 子查询指的是一个查询语句嵌套在另一个查询语句内部的查询
-- 子查询的结果作为外层查询的过滤条件, 常用的操作符有: any(some), all, in, exists
-- 子查询可以添加到select, update, delete语句中

-- any(some), all
SELECT num1 FROM tbl1 WHERE num1 > ANY(SELECT num2 FROM tbl2);

-- exists: 系统对exists子查询进行判断, 如果至少返回一行结果则返回true, 否则返回false
-- 如果exists结果为true则外层查询将继续, 否则外层查询终止
SELECT * FROM fruits WHERE EXISTS(SELECT * FROM suppliers WHERE s_id = 107) AND f_price > 10.20;

-- in: 内层查询语句仅仅返回一个数据列, 提供给外层查询语句进行比较
```


## 合并查询结果
```sql
-- union | union all: 合并时, 两张表对应的列数和数据类型必须相同
-- union会删除重复的记录, 返回的所有行都是唯一的; 反之, union all则不删除重复的数据, 也不对结果进行自动排序
-- union all因为不会删除重复记录, 所以使用的资源较少, 应该尽可能的使用它以提高查询效率
```


## 别名
```sql
-- 为表取别名
-- 表的名字很长或者一些特殊的查询
-- 自连接查询必须使用别名, 否则将不知道究竟使用的是哪一张表
<tb_name> [as] <tb_alias>


-- 为字段取别名
-- 显示输出结果时, 替换掉不够直观的表达式或者很长的名称
<field_name> [as] <field_alias>


-- 总结
-- 表别名在执行查询的时候使用, 而列别名在返回结果中显示
```


## 使用正则表达式查询
```sql
select ... from ... where <field_name> regexp <pattern>


-- 常用的特殊字符
1. ^
2. $
3. .
4. *
5. +
6. []
7. [^]
8. {n,} --至少n次
9. {m}  --至多m次
10. {n,m}
```


## 插入数据
```sql
-- 为表的所有字段插入数据
-- 两种方式: 显式的指定所有字段名; 不指定字段名
insert into <tb_name> (<column_list>) values (<value_list>),...

-- 为表的部分字段插入数据, 未指定的字段使用默认值

-- 同时插入多条数据

-- 将查询结果插入到表中
insert into <tb_name> (<column_list>) select <column_list> from ...
```


## 更新数据
```sql
update <tb_name> set <field_name1>=<value1>,... where ...
```


## 删除数据
```sql
delete from <tb_name> where ...

-- 删除表中所有记录
-- 直接删除整张表并创建一张新表, 速度比delete更快
truncate table <tb_name>;


-- 建议在更新或删除数据之前, 使用select确认一下, 以免造成难以挽回的结果
```


## 为表增加计算列
```sql
-- 计算列: 即通过其它列计算得到
-- create table和alter table都支持增加计算列
<field_name> <data_type> [generated always] as <expr> <constraint>


-- 演示
DROP TABLE IF EXISTS tbl1;
CREATE TABLE tbl1 (
	id INT(9) NOT NULL auto_increment,
	a INT(9) DEFAULT NULL,
	b INT(9) DEFAULT NULL,
	c INT(9) generated always as (a + b) virtual,
	PRIMARY KEY (id)
);
```


## 索引
```sql
-- 索引用于快速找出在某一列中有特定值的行
-- 索引是对数据库表中一列或多列的值进行排序的结构, 使用索引可以提高数据库中特定数据的查找速度
-- 所有mysql数据类型都可以被索引
-- 索引是在存储引擎中实现的, 因此每种引擎的索引不一定完全相同, 并且各种引擎对不同数据类型的支持程度也不一样
-- mysql中索引的类型有两种: btree, hash


-- 索引的有点
1. 通过创建唯一索引, 可以保证每一行数据的唯一性
2. 加快数据的查询速度
   加快表与表之间的连接
   加快分组和排序的速度


-- 索引的缺点
1. 对表中的数据进行增删改操作的时候, 索引也需要动态的维护, 间接的影响了insert|update|delete语句的性能, 需要额外的消耗空间和时间


-- 索引的分类
1. 普通索引: 允许空值和重复
2. 唯一索引: 允许空值, 但索引列的值必须唯一
3. 主键索引: 特殊的唯一索引, 不允许空值
4. 单列索引 & 组合索引: 组合索引有一个名为"最左前缀"的规则, 如果不符合则不会使用组合索引
   例如组合索引(a, b, c), 可以搜索(a, b, c) | (a, b) | (a)
5. 全文索引: 在定义索引的列上支持全文查找, 允许重复和空值, 可以在CHAR, VARCHAR, TEXT类型的列上创建
   只有myisam引擎支持全文索引
   全文索引适用于大型数据集
6. 空间索引: 对空间数据类型(geometry, point, linestring, ploygon)的字段创建的
   mysql使用关键字spatial进行扩展, 使得能够用类似创建常规索引的语法创建空间索引
   创建空间索引的列必须声明为not null
   只有myisam引擎支持空间索引


-- 索引的设计原则
1. 并非越多越好
2. 数据规模小的表最好不使用索引
3. 避免对进场更新的表过多的索引, 并且索引中的字段尽量少
4. 在条件表达式中经常用到的不同值较多的列建立索引
5. 当唯一性是数据本身的特征时, 建立唯一索引
6. 在频繁进行排序和分组的列建立索引, 如果排序的列有多个可以建立组合索引
7. 最好使用段索引; 如对于一个char(255)的数据, 如果前面20个字符内多数值已经是唯一的, 则指定索引长度为20


-- 查看指定表中创建的索引
show index from <tb_name>;


-- 创建索引
-- 1. create table
/* 
1. 索引类型
   unique: 唯一索引
   fulltext: 全文索引
   spatial: 空间索引
2. index和key的作用相同, 用来指定创建索引
3. index_name指定索引名称, 默认为field_name
4. 只有字符串类型的字段才能指定索引长度length
5. asc和desc指定索引存储的顺序
 */
create table <tb_name> (
   ...
   [unique|fulltext|spatial] [index|key] [<index_name>] (<field_name>(<length>)...) [asc|desc],
);
-- 2. alter table
alter table <tb_name> add [unique|fulltext|spatial] [index|key] [<index_name>] (<field_name>(<length>)...) [asc|desc];
-- 3. create index
-- 在mysql中, create index被映射到alter table语句上
create [unique|fulltext|spatial] index <index_name> on <tb_name> (<field_name>(<length>)...) [asc|desc];


-- 删除索引
-- 在删除表的列时, 如果该列是索引得到组成部分, 则该列也会从索引中删除
-- 1. alter table
alter table <tb_name> drop index <index_name>
-- 2. drop index
-- 在mysql中, drop index被映射到alter table语句
drop index <index_name> on <tb_name>;
```


## 存储过程和函数
```sql
-- 创建存储过程
/* 
1. 参数指定形式: [in | out | inout] <param_name> <data_type>
2. characteristics指定存储过程的特性, 取值有
   LANGUAGE SQL: 指明body部分是由sql语句组成
   [not] deterministic: 指明结果是否确定(相同输入是否能得到相同输出)
   {contains sql | no sql | reads sql data | modifies sql data}: 指明使用sql的限制
   sql security {definer | invoker}: 指明谁有权限执行
   comment '...': 注释信息
 */
create procedure p_name(<params>...)
[characteristics...]
begin
...
end;


-- 创建存储函数
/* 
1. returns语句指定函数返回数据的类型
2. 函数必须包含一个return语句
 */
create function <f_name>(<params>...)
returns <data_type>
[characteristics...]
begin
...
end;


-- 变量的使用
-- 1. 定义变量
declare <var_name>,... <data_type> [default <value>];
-- 2. 赋值
set <var_name> = expr [, <var_name> = expr];
select <field_list> into <var_list> from ...;


-- 定义条件和处理程序
-- 定义程序执行过程中可能遇到的问题以及处理方式
-- 1. 定义条件
/* 
1. condition_type的表示方式: sqlstate_value(长度为5的字符串)和mysql_error_code
   例如: 在ERROR 1142 (42000)中, sqlstate_value=42000, mysql_error_code=1142
 */
declare <condition_name> condition for [<condition_type>]
-- 2. 定义处理程序

```