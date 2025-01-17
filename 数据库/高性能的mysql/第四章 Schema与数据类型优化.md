## Schema与数据类型优化
### 选择优化的数据类型
1. 更小的通常更好

    一般情况下，应该尽量选择可以正确存储数据的最小数据类型。更小的数据类型通常更快，因为他们占用更少的磁盘，内存和cpu缓存，并且处理时需要cpu周期也更少。
    但是要确保没有低估需要存储的值得范围。

2. 简单就好

    简单的数据类型的操作通常需要更少的cpu周期。例如，整型比字符串操作代价更低，因为字符集和校对规则（排序规则）使字符集比整型复杂。

3. 尽量避免Null
    
    很多表都可以包含为 null(空值) 的列，即使应用程序并不需要保存 null 也是如此，这是因为 null 是列的默认属性。通常情况下，最好指定列为 not null，除非真的需要存储 null 值。
   
   
    **如果查询中包含可为 null 的值，对 mysql 来说更难优化，因为可为 null 的列使得索引、索引统计和值比较都变的复杂。**可为null的列会使用更多的存储空间，在 mysql 里面也需要特殊处理。当可为 null 的列被索引时，每个索引记录需要一个额外的字节，在 MyISAM 里面甚至还可能导致固定大小的索引变成可变大小的索引。

​    通常把可为 null的列改为 not null 带来的性能提升比较小，所以(调优时)没有必要首先在现有的 schema 中查找并修改掉这种情况。但是，**如果计划在列上建索引，就应该尽量避免设计成可为 null 的列。**
​	 当然也有例外，例如值得一提的是，**InnoDB 使用单独的位(bit)存储 null值，所以对于稀疏数据有更好的空间效率。**

4. 字符串类型
    另外，慷慨是不明智的。即使 VARCHAR(5) 和 VARCHAR(200)存储'hello'的空间开销是一样的(char和varchar最大的区别就在于char(n)不管实际value都会占用n个字符的空间，而varchar(n)只会占用实际字符应该占用的空间+1，并且实际空间+1<=n)，但是更长的列会消耗更多的内存，因为 MySQL 通常会分配固定大小的内存来保存内部值。尤其是使用内存临时表进行排序或操作时会特别糟糕。在利用磁盘临时表进行排序时也同样糟糕。所以最好的策略是只分配真正需要的空间。
   
**BLOB 和 TEXT 类型**

BLOB 和 TEXT 家族之间仅有的不同是 BLOB 类型存储的是二进制数据，没有排序规则或字符集，而 TEXT类型有字符集和排序规则。

5. 特殊数据类型

    一个例子是 IPv4 地址。人们经常使用 VARCHAR(15)列来存储 IP 地址。然而，它们实际上是32位无符号整数，不是字符串。用小数点将地址分成4段的表示方式只是为了让人们更容易阅读。MySQL 提供 INET_ATON()和 INET_NTOA()函数在这两种表示方法之间转换。
    
    ```sql
    INSERT my_table(ip) VALUES (INET_ATON('192.168.0.1')); /*ip = 3232235521*/
    ELECT INET_NTOA(ip) As IPAddress FROM my_table; /*IPAddress = 192.168.0.1*/
    ```

### 范式与反范式
1. 范式：
    * 1NF 每个属性都不可再分
    * 2NF 所有非主属性完全依赖主属性
    * 3NF 不存在传递依赖

2. 范式化的优点：
    * 范式化的数据更新操作通常比反范式化更快
    * 当数据较好的范式化时，就**只有很少或者没有重复数据**，所以只需要修改更少的数据
    * 范式化的表通常更小， 可以更好的放在内存里。所以执行操作会更快
    * 很少有多余的数据意味着检索列表数据时更少需要distinct或者group by语句.
3. 范式化的缺点：
    在复杂一些的查询语句在符合范式的schema上都可能需要至少一次关联，甚至多次关联。关联的代价是昂贵的，也可能使一些索引策略无效。

4. 反范式化的优点：
    * 可以很好地避免关联
    * 反范式就是在通过增加冗余数据或者数据分组来提高数据库**读性能**的过程。有时候反范式能掩盖关系型数据库软件的低效。
    * **使用反范式的表能使用更加有效的索引策略。**

### 混合使用范式化和反范式化
**从性能来说，范式化有更好的写性能，反范式化有更好的读性能。**

### 缓存表和汇总表

有时提升性能的方法是在同一张表中保存衍生的冗余数据。然而，有时也需要创建一张完全独立的汇总表或缓存表（特别是为满足检索的需求时）。如果能容许少量的脏数据，这是非常好的方法，但是有时确实没有选择的余地（例如，需要避免复杂、昂贵的实时更新操作）。

术语“缓存表”和“汇总表”没有标准的含义。我们用术语**“缓存表”来表示存储那些可以比较简单地从schema 其他表获取**（但是每次获取的速度比较慢）**数据的表**（例如，逻辑上冗余的数据）。**“汇总表”，则保存的是使用GROUP BY语句聚合数据的表**（例如，数据不是逻辑上冗余的）。也有人使用术语“累积表（Roll-Up Tables）”。

### 计数器表
# 第四章 Schema 与数据类型优化

## 4.1 选择优化的数据类型

MySQL 支持的数据类型非常多，选择正确的数据类型对于获得高性能至关重要。不管存储哪种类型的数据，下面几个简单的原则都有助于做出更好的选择。

**更小的通常更好**

​		一般情况下，应该尽量选择可以正确存储数据的最小数据类型。更小的数据类型通常更快，因为它们占用更少的磁盘，内存和 cpu 缓存，并且处理时需要 cpu 周期也更少。
​		但是要确保没有低估需要存储的值的范围。

**简单就好**

​		简单的数据类型的操作通常需要更少的 cpu 周期。例如，整型比字符串操作代价更低，因为字符集和校对规则(排序规则)使字符集比整型复杂。这里有1个例子，一个是应该使用 mysql 内建的类型而不是字符串来存储日期和时间，另外一个是应该使用整型来存储 IP 地址。



**尽量避免 NULL**

​		很多表都可以包含为 null(空值) 的列，即使应用程序并不需要保存 null 也是如此，这是因为 null 是列的默认属性。通常情况下，最好指定列为 not null，除非真的需要存储 null 值。

​		**如果查询中包含可为 null 的值，对 mysql 来说更难优化，因为可为 null 的列使得索引、索引统计和值比较都变的复杂。**可为null的列会使用更多的存储空间，在 mysql 里面也需要特殊处理。当可为 null 的列被索引时，每个索引记录需要一个额外的字节，在 MyISAM 里面甚至还可能导致固定大小的索引变成可变大小的索引。

​		通常把可为 null的列改为 not null 带来的性能提升比较小，所以(调优时)没有必要首先在现有的 schema 中查找并修改掉这种情况。但是，**如果计划在列上建索引，就应该尽量避免设计成可为 null 的列。**
​		当然也有例外，例如值得一提的是，**InnoDB 使用单独的位(bit)存储 null值，所以对于稀疏数据有更好的空间效率。**

### 4.1.3 字符串类型

另外，慷慨是不明智的。即使 VARCHAR(5) 和 VARCHAR(200)存储'hello'的空间开销是一样的(char和varchar最大的区别就在于char(n)不管实际value都会占用n个字符的空间，而varchar(n)只会占用实际字符应该占用的空间+1，并且实际空间+1<=n)，但是更长的列会消耗更多的内存，因为 MySQL 通常会分配固定大小的内存来保存内部值。尤其是使用内存临时表进行排序或操作时会特别糟糕。在利用磁盘临时表进行排序时也同样糟糕。所以最好的策略是只分配真正需要的空间。



**BLOB 和 TEXT 类型**

BLOB 和 TEXT 家族之间仅有的不同是 BLOB 类型存储的是二进制数据，没有排序规则或字符集，而 TEXT类型有字符集和排序规则。

### 4.1.7 特殊数据类型

一个例子是 IPv4 地址。人们经常使用 VARCHAR(15)列来存储 IP 地址。然而，它们实际上是32位无符号整数，不是字符串。用小数点将地址分成4段的表示方式只是为了让人们更容易阅读。MySQL 提供 INET_ATON()和 INET_NTOA()函数在这两种表示方法之间转换。

```mysql
INSERT my_table(ip) VALUES (INET_ATON('192.168.0.1')); /*ip = 3232235521*/
SELECT INET_NTOA(ip) As IPAddress FROM my_table; /*IPAddress = 192.168.0.1*/
```



## 4.3 范式和反范式

对于任何给定的数据库都有很多种表示方法，从完全的范式话到完全的反范式花，以及两者折中。在范式化的数据库中，每个事实数据只会出现一次，相反，在反范式花中，信息是冗余的。范式化就是消除数据的冗余，消除数据依赖。

下面以经典的“雇员、部门、部门经理”的例子开始：

| Employee | department  | leader |
| :------- | :---------- | :----- |
| Jones    | Accounting  | Jones  |
| Smith    | Engineering | Smith  |
| Brown    | Accounting  | Jones  |
| Green    | Engineering | Smith  |

对这样一个schema ，显然其中有些数据是重复的，修改数据时可能发生不一致。假如 Brown 接任了 Accounting 部门的领导，那么需要修改很多行来反映这个变化，这很麻烦而且很容易出错，并且如果Smith这一行的 leader 和 Green 这一行的 leader 不一样，那就不知道到底谁是对的了。这样设计的一张表还存在很多问题，比如部门不存在雇员就没法表示一个部门，针对这些问题我们要对这张表进行**范式化**。

将表拆分是范式化的手段，将信息冗余的列从原表中拆分出来做一个新表，然后通过关联表建立联系。

雇员表：

| Employee | department  |
| :------- | :---------- |
| Jones    | Accounting  |
| Smith    | Engineering |
| Brown    | Accounting  |
| Green    | Engineering |

部门表：

| department  | leader |
| :---------- | :----- |
| Accounting  | Jones  |
| Engineering | Smith  |

这样设计的两张表符合第二范式，在很多情况下做到这一步已经足够好了，然而，第二范式只是许多可能的范式中的一种，让我们来看下范式存在的优缺点。

### 4.3.1 范式化的优缺点

我竟然从来没想过为什么要分成不同的表，只是理所当然的“雇员表——部门表”！

在解决数据库性能问题时，经常会被建议对 schema 进行范式化建议，尤其是**写密集**的场景。这通常是个好建议，范式话能带来这些好处：

- 范式化的数据更新操作通常比反范式化要快
- 当数据较好地范式化时，就**只有很少或者没有重复数据**，所以只需要修改更少的数据
- 范式化的表通常更小，可以更好地放在内存里，所以执行操作会很快
- 很少有多余的数据意味着检索列表数据时更少需要distinct 或者 group by 语句，在前面的例子中，需要使用 distinct 或者 group by 才能获得一份唯一的部门列表，如果部门是一种单独的表则只需要简单查询这张表就可以了

当然范式化的设计并不是只带来好处，而稍微复杂一些的查询语句在符合范式的schema上都可能需要至少一次关联，甚至多次关联。关联的代价是很昂贵的，也可能使一些索引策略无效。例如范式化可能将列存在不同的表中，而这些列如果在同一表中本可以属于同一个索引。



### 4.3.2 反范式化的优缺点

反范式化的 schema 因为所有数据都在一张表中，可以很好地避免关联。

反范式就是在通过增加冗余数据或数据分组来提高数据库**读性能**的过程。有时候反范式能掩盖关系型数据库软件的低效(比如 nosql)。

如果不需要关联表，则对大部分查询最差的情况——即使表没有使用索引(是全表扫描)，当数据比内存还大的时候可能比关联表要快得多，因为这样避免了随机IO（全表扫描基本上是顺序IO）。**使用反范式的表能使用更加有效的索引策略。**



### 4.3.3 混合使用范式化和反范式化

范式化和反范式化因为各有优缺点，在实际应用中经常需要混用，可能使用部分范式化的schema、缓存表，以及其他技巧。

最常见的反范式化数据的方法是复制或者缓存，在不同的表中，存储相同的特定列。但是反范式化使得更新数据的代价变大了，需要考虑更新的频率以及更新的时常，并和执行select查询的频率进行比较。所以实际使用中，是否使用反范式化还是要根据具体需求确定，如果查询多于更新，可以反范式化多一些，如果需要经常更新数据，那么过多的反范式化列使得整体的性能反而降低了。

一般来说，在范式化达到一定的满意水平并且所需要的约束和规则都已经建立起来才进行反范式化。

**从性能来说，范式化有更好的写性能，反范式化有更好的读性能。**



## 4.4 缓存表和汇总表

有时提升性能的方法是在同一张表中保存衍生的冗余数据。然而，有时也需要创建一张完全独立的汇总表或缓存表（特别是为满足检索的需求时）。如果能容许少量的脏数据，这是非常好的方法，但是有时确实没有选择的余地（例如，需要避免复杂、昂贵的实时更新操作）。

术语“缓存表”和“汇总表”没有标准的含义。我们用术语**“缓存表”来表示存储那些可以比较简单地从schema 其他表获取**（但是每次获取的速度比较慢）**数据的表**（例如，逻辑上冗余的数据）。而术语**“汇总表”时，则保存的是使用GROUP BY语句聚合数据的表**（例如，数据不是逻辑上冗余的）。也有人使用术语“累积表（Roll-Up Tables）”称呼这些表。因为这些数据被“累积”了。

### 4.4.1 物化视图

许多数据库管理系统(例如 Oracle 或微软 SQL Server)都提供了一个被称为物化视图的功能。物化视图实际上是预先计算并且存储在磁盘上的表，可以通过各种各样的策略刷新和更新。MySQL 并不原生支持物化视图，但可以使用开源工具入 flexviews实现物化视图。

### 4.4.2 计数器表

计数器表在 web 应用中很常见，可以用这种表缓存一个用户的朋友数、文件下载次数等，创建一张独立的表存储计数器通常是个好主意，这样可使计数器表小且快。使用独立的表可以帮助避免查询缓存失效，并且可以使用本节展示的一些更高级的技巧。

应该让事情变得尽可能简单，假设有一个计数器表，只有一行数据，记录网站的点击次数：

`CREATE TABLE hit_counter (cnt int unsigned not null)`

网站的每次点击都会导致对计数器进行更新：

`UPDATE hit_counter SET cnt = cnt+1`

问题在于，对于任何想要更新这一行的事务来说，这条记录上都有一个全局的互斥锁（mutex）。这会使得这些事务只能串行执行。要获得更高的并发更新性能，也可以将计数器保存在多行中，每次随机选择一行进行更新。这样做需要对计数器表进行如下修改：

```mysql
CREATE TABLE hit_counter (
  slot tinyint unsigned not null promary key,
  cnt int unsigned not null
)
```

现在每次随机选择一行进行更新即可，若要总的统计结果，需要使用如`sum(cnt)` 这样的聚合查询。