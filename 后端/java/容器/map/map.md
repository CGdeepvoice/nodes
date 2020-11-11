## map
map就是key-value的数据格式，并且key值不能重复，一个key对应一个value.

它定义了一个内部接口Entry，A map entry (key-value pair).  也就是说每个键值对就是一个Entry

**Entry**
interface Entry<K, V>, 他是有两个泛型的，key和value的类型可以不一样
他的主要方法：
1. getKey() 返回这个键值对的key
2. V getValue();
3. V setValue(V value);
4. comparingByValue, comparingByKey,通过值或者键来进行比较

```java
// 返回值类型是泛型， <K extends Comparable<? super K>, V> 这里用<>括起来是声明一个泛型K， K是继承了Comparable接口的子类型，Comparable里的参数又是K的父类型，类型V
// Comparator<Map.Entry<K, V>> 返回值是Comparator接口类型，参数是Entry
public static <K extends Comparable<? super K>, V> Comparator<Map.Entry<K, V>> comparingByKey() {
            return (Comparator<Map.Entry<K, V>> & Serializable)
                (c1, c2) -> c1.getKey().compareTo(c2.getKey());
        }
```

entry就像是tree上的node,是构成Map的部分

继续看**Map**
看下他内部定义的方法：
1. Set<K> keySet(); 这里就是全部的key的set集合，因为key不能重复，所以使用了set容器
2. Collection<V> values(); 值是可以重复的
3. Set<Map.Entry<K, V>> entrySet(); 键值对是不能重复的

应该就这三个变量了
主要的方法
1. boolean containsKey(Object key);
2. boolean containsValue(Object value);
3. V get(Object key);
4. V put(K key, V value);
5. V remove(Object key);
6. replace

```java
default V replace(K key, V value) {
    // 修改
    V curValue;
    if (((curValue = get(key)) != null) || containsKey(key)) {
        curValue = put(key, value);
    }
    return curValue;
}
```
7. 静态方法 entry
```java
static <K, V> Entry<K, V> entry(K k, V v) {
    // KeyValueHolder checks for nulls
    //KeyValueHolder 继承自Entry
    return new KeyValueHolder<>(k, v);
}
```

和其他一样，也有of方法用来创建不可变对象，放在不可变集合内部Map12,MapN

**AbstractMap**
每个都有抽象类，但是这个不同于List,set,因为没有继承自AbstractCollection，他和collection是平级的

实现的方法：
1. containsValue, 利用了entrySet的iterator迭代器来循环获取值，进行比较
2. containsKey 和上面一样
3. get remove putall,
4. 这里还实现了KeySet和values，利用了AbstractCollection和AbstractSet，实现了其内部的迭代器，返回了一个对象
5. equals 这个比较差不多，就是比较内部的键值对的每个值是否对方都包含，双方的size是否一样

这里还定义了两个内部类实现了Entry方法，SimpleEntry和SimpleImmutableEntry，前者是简单的实现了方法，后者是不可变的键值对，值是不能修改的。两者的键都是不能改的。 `private final V value;`

