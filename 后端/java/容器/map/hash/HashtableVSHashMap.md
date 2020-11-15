## 与HashMap之间的关系
1. 区别
   1. hashMap是非线程安全的，只能用于单线程环境下。hashtable中的方法是synchronize的，可以用于多线程。
   2. 继承关系区别，HashMap继承自Map接口，HashTable继承自Directory接口。
   3. Hashtable中，key和value中都不允许有空值.HashMap中可以使用null作为键。
   4. 哈希碰撞的处理方式不同。hashMap会在链表达到长度8时变为树，而hashtable一直都是链表。
2. 相同点
   1. 都是key-value格式
   2. 都是利用hash&length, 获取坐标，然后哈希碰撞时采用链表法来扩展

## Hashtable
**Entry**
节点的定义和HashMap没啥区别

**put**
```java
// 这里使用synchronized关键字，说明这个方法是线程安全的，当一个线程调用这个方法时，其他方法都进行阻塞
public synchronized V put(K key, V value) {
    // Make sure the value is not null
    // value也不能为空
    if (value == null) {
        throw new NullPointerException();
    }

    // Makes sure the key is not already in the hashtable.
    Entry<?,?> tab[] = table;
    int hash = key.hashCode();
    // 利用hash值和数组长度做与操作来获取坐标
    int index = (hash & 0x7FFFFFFF) % tab.length;

    @SuppressWarnings("unchecked")
    Entry<K,V> entry = (Entry<K,V>)tab[index];
    // 上面是用来获取到index上的节点
    for(; entry != null ; entry = entry.next) {
        // 遍历这个节点上的链表，找到hash值相同且key相同的节点
        if ((entry.hash == hash) && entry.key.equals(key)) {
            // 如果找到了就更新value
            V old = entry.value;
            entry.value = value;
            return old;
        }
    }
    // 如果没有找到，就新增一个节点，
    addEntry(hash, key, value, index);
    return null;
}
private void addEntry(int hash, K key, V value, int index) {
    Entry<?,?> tab[] = table;
    if (count >= threshold) {
        // Rehash the table if the threshold is exceeded
        // 到达阈值就进行扩容
        rehash();

        tab = table;
        hash = key.hashCode();
        // 如果扩容了重新计算index
        index = (hash & 0x7FFFFFFF) % tab.length;
    }

    // Creates the new entry.
    @SuppressWarnings("unchecked")
    Entry<K,V> e = (Entry<K,V>) tab[index];
    // 这里的new  Entry 最后一个参数e是当前index上的节点，这里就是把新插入的节点放在队首，也算是加入链表了。
    tab[index] = new Entry<>(hash, key, value, e);
    count++;
    modCount++;
}
```
这里不需要转为树形，所以操作会简单一些，不过看源码的话也差不多吧，多一种情况来处理而已。
其他操作不看了，大体上和hashMap差不多。